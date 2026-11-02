---
作者:
  - "转转技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzIwMjk1ODMzMw==&amp;mid=2247505739&amp;idx=1&amp;sn=510985afa778783d1c9b1fcb38ea1498&amp;chksm=9723d6b941abde36d14bc0d8e41a8e53535ba0624a3fa79038137e4591272e079206fc3689b4&amp;mpshare=1&amp;scene=1&amp;srcid=0829YRnnwC3vMJxqjW0ptpV0&amp;sharer_shareinfo=bdd477f245e8017e3b7481110ff0f3e9&amp;sharer_shareinfo_first=4c1f3317ccc5fec3286ba1fdf9e6436b#rd
发布时间: ""
收藏时间: "2025-08-30"
关联日记: "[[2025-08-30]]"
tags:
  - 文章
---
- 1. 问题背景
- 2. 有什么场景可能会出现这样的问题？
- 2.1 主从同步延迟？2.2 事务没有生效？2.3 快照读？
- 3. Update执行流程
- 3.1 源码分析3.2 启发
- 4. 场景复现
- 4.1 表结构 和 数据4.2 步骤
- 5. 总结


注: 本文使用的MySQL版本 5.7.44， 事务隔离级别为 REPEATABLE-READ。

## 1. 问题背景

在一个平常的夜晚，收到业务反馈某个检测单流程卡住，不能继续往下走。接到反馈后，连忙上线排查。发现问题点在一个诡异的现象 —— 数据库更新消失: **在事务中，先更新一行记录，后读取该行，读取到竟为更新前的旧值！**

接口对应的业务逻辑大致有以下几步:

1. 用户选择一批初始状态为10的检测单ID发起流转；
2. 后端服务获取检测单对应的异常信息，**将没有异常的检测单的状态修改为 20。如果有异常的，则不修改状态**；
3. 最后根据检测单状态和其他信息执行不同的业务逻辑。


以上步骤均在一个事务内执行。

假设第一步获取到的检测单id列表为[1001,1002]，第二、第三步简化流程如下:

```
# T0 select获取检测单的异常记录
select id, exception_type, qc_order_id 
from qc_order_exception
where qc_order_id in (1001, 1002)


# T1 执行如下SQL，ID为1001, 1002更新检测单记录的状态。  注: 更新前 status = 10
update qc_order
set status = 20
where id in (1001, 1002);        


# T2 执行如下SQL，通过ID获取检测单信息。 注: T1更新为satus=20的记录，可能读取出来的 status = 10
select id, status, 
from qc_order 
where id in (1001, 1002)


# T3 根据检测单状态，执行不同的业务逻辑。 
if (qcOrder.getStatus() == 20) { // 检测单无异常
 log.info("逻辑1");         // 正常情况:1001、1002都执行这里逻辑。打印日志: "逻辑1"
} else {                  
 log.info("逻辑2");        // 偶发异常现象：1002走上面逻辑 1001走了这里的逻辑。 打印日志: "逻辑2"。但分明T1时刻ID = 1001这条记录的status应该已经被更新为了20
}
```

接到业务反馈后，我们在 打印日志: "逻辑2" 的分支中，加了监控告警，触发告警后，检测单没有后续的操作。这时去查看数据库中检测单的状态，没有异常的检测单的状态均为 status = 20（检测单最后状态是对的，但是在处理业务逻辑时，可能读取出旧值 status=10）。

我们观测日志发现，status被更新为20（即没有异常）的一批检测单，大部分情况，该批检测单内所有检测单执行打印日志: "逻辑1"；小部分情况，比如上面举例的[1001,1002]，这批检测单中，ID=1001的检测单执行：打印日志: "逻辑2"。——出现了奇怪的“更新消失”现象！

遇到这种偶发性"更新消失"的场景，此时我们表情如下：

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/d984c5af-ff51-4e74-8093-ecaf8b4b1bee.jpeg)

## 2. 有什么场景可能会出现这样的问题？

### 2.1 主从同步延迟？

- 如果 T2时刻，获取数据库记录时是通过数据库从节点读取，可能因为主从同步延迟的原因，导致读取到数据库旧值
- 为什么不是这个原因？
- T2时刻，通过断点com.alibaba.druid.pool.DruidPooledConnection（项目使用Druid连接池）的方法，确认T1和T2时刻执行SQL是用同一个数据源。所以不可能是主从同步延迟的原因。


### 2.2 事务没有生效？

- 如果事务没有生效时，存在 A 事务修改记录的status = 20，事务B又修改status = 10。如果没有事务，事务A可以看到事务B的修改。
- 为什么不可能是这个原因？
- 业务逻辑方法上有使用声明式事务@Transctional，断点后，确认线程栈中包含org.springframework.transaction.interceptor.TransactionInterceptor.invoke，可以判定所有操作均在同一个事务中执行。在测试环境复现场景时，在事务未提交时，记录修改，在其他事务不可见。


### 2.3 快照读？

##### ReadView

事务级别为 REPEATABLE-READ 时，则事务第一次执行 SELECT 时会生成一个 ReadView ，后续所有读操作复用该 ReadView。ReadView 的内容为:

- m_ids: 在创建 Read View 时，当前数据库中「活跃事务」的事务 id 列表，注意是一个列表，“活跃事务"指的是启动了但还没提交的事务。
- min_trx_id: 在创建 Read View 时，当前数据库中「活跃事务」中事务 id 最小的事务，也就是 m_ids 的最小值。
- max_trx_id: 这个并不是 m ids 的最大值，而是创建 Read View 时当前数据库中应该给下一个事务的id 值，也就是全局事务中最大的事务 id 值 +1。
- creator_trx_id: 创建该 Read View 的事务的事务 id


##### 快照读流程

当需要读取某行记录流程大致如下:

1. InnoDB 会先会定位到该行的最新版本（即当前数据页中的最新记录）。
2. 遍历 Undo Log 版本链找到一个当前 ReadView 可见的版本记录: 从最新版本开始，沿着行记录的DB_ROLL_PTR指针（指向旧版本数据的指针）遍历 Undo Log 中的历史版本链，通过行记录的 DB_TRX_ID（最后修改该行记录的事务ID）判断是否满足可见条件，条件如下:
3. 如果版本 DB_TRX_ID == creator_trx_id： 该版本是本事务修改的，可见。如果版本 DB_TRX_ID< min_trx_id： 该版本在 Read View 创建时已提交，可见。如果版本 DB_TRX_ID >= max_trx_id： 该版本在 Read View 创建后启动，不可见。遍历记录的版本链，继续查找更旧版本。如果版本 DB_TRX_ID 在 m_ids 列表中： 该版本对应的事务在 Read View 创建时仍活跃（未提交），不可见，继续查找更旧版本。
4. 如果找到满足可见的版本，返回该版本数据。如果不满足，则不返回数据。


如果在事务中执行了 Update 语句，则更新的行记录的 DB_TRX_ID 应该更新为当前事务ID 。根据快照读的流程，在更新后通过 Select 读取的这条行记录时，当前事务ID == DB_TRX_ID，这条行记录应该被读取出来，不应通过 DB_ROLL_PTR 读取历史版本数据。

但事故中，更新后偶发性地读取到历史版本的数据，是什么原因造成的呢？

苦思冥想后没有头绪，最终决定 Show code —— 尝试从 MySQL 源码中找到答案。

## 3. Update执行流程

### 3.1 源码分析

#### 阅读MySQL源码的Update SQL执行逻辑，从 mysql_update() 函数中看出端倪，整理后更新的简化流程如下:

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/24ed2ef5-d9d5-4936-a3e0-4b9eeba8f392.png)

⚠️ MySQL 在更新记录前，会通过 compare_records() 函数判断行记录更新前后是否发生了变化，如果行记录没有发生变化，则跳过更新。

#### compare_records() 怎么比对行记录更新前后是否有变化的？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/d2ea45eb-9829-4bb4-967a-49a3c67c061f.png)

- 如果存储引擎支持部分列读取，则只比较需要更新的列的值是否相等，如果列可为NULL，需要额外比较NULL值是否相等。
- 对于只支持完整读取的存储引擎：
- 判断是否是固定长度的列？如果是，则直接通过 memcmp 字节比较是否相同。否则执行第2步。判断更新前后的数据，所有可为NULL的列的NULL值是否相同？如果不相同，直接返回数据不相同。否则执行第3步。遍历所有需要更新的列，比较更新前后值是否相同。


### 3.2 启发

#### 从流程图中可以看出:

- **如果行记录更新前后没有变化， 就不会调用存储引擎执行实际更新行记录逻辑**， Update 语句可以正常执行没有报错。
- 批更新记录时，MySQL是逐行对比后，再调用存储引擎执行更新。


#### 那又为什么没有数据变化呢？

- **我们检查了业务逻辑代码，发现更新检测单状态时，并没有对记录加锁，那很大可能是存在并发执行的其他流程修改了检测单状态，且两个流程修改的检测单状态相同，导致数据执行前后没有变化。**


我们在测试环境构造下面场景来复现。

## 4. 场景复现

### 4.1 表结构 和 数据

```
create table qc_order_exception
(
    id             int      notnull primary key auto_increment comment'id',
    qc_order_id    int      notnullcomment'检测单id',
    exception_type tinyintcomment'异常类型',
    create_time    datetime notnulldefaultcurrent_timestampcomment'创建时间',
    update_time    datetime notnulldefaultcurrent_timestamponupdatecurrent_timestampcomment'更新时间'
) engine = innodbcomment'检测单异常记录';


createtable qc_order
(
    id          int      notnull primary key auto_increment comment'id',
    status      int      notnullcomment'状态',
    create_time datetime notnulldefaultcurrent_timestampcomment'创建时间',
    update_time datetime notnulldefaultcurrent_timestamponupdatecurrent_timestampcomment'更新时间'
) engine = innodbcomment'检测单表';


insertinto qc_order(id, status)
values (1001, 10),
       (1002, 10);
```

### 4.2 步骤

#### 记录初始状态:

```
select id, status, create_time, update_time
from qc_order;
```

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/6822a23c-99da-48ca-ab30-84770ed0697f.png)

#### T0时刻（事务A）: 开启事务 && 创建ReadView

```
begin;


select id, exception_type, qc_order_id
from qc_order_exception
where qc_order_id in (1001, 1002);
 -- 返回数据为空。

select trx_id, trx_state, trx_state, trx_mysql_thread_id, trx_query from information_schema.INNODB_TRX;
```

执行结果:


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/598652e7-cf40-4ff7-995a-6c40f66c515a.png)

- 事务A的线程ID: 7，trx_id: 421164174274160。这是临时的事务ID。


#### T1时刻（事务B）: 开启事务 && 更新数据 id=1001 && 获取事务信息 && 提交

```
begin;

update qc_order
set status = 20
where id = 1001;

select trx_id, trx_state, trx_state, trx_mysql_thread_id, trx_query from information_schema.INNODB_TRX;

commit;
```

执行结果:


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/665815e6-4788-4bc3-b9d9-a7aed275d384.png)

事务B中:

- Update 返回： 匹配行数: 1， 更新行行数: 1 。 表示更新成功了。
- select ... from information_schema 返回的线程ID: 8，**trx_id：4364**。


#### T2时刻（事务A）: 更新数据 id in (1001,1002)，设置 status = 20

```
update qc_order
set status = 20
where id in (1001, 1002);

select trx_id, trx_state, trx_state, trx_mysql_thread_id, trx_query from information_schema.INNODB_TRX;
```

执行结果:


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/4c932c4b-593e-4609-8fa0-95c0f01e1acc.png)

- Update返回： 匹配行数: 2， 更新行行数: 1 。表示找到2条数据，但只更新一条，有的数据实际没有执行更新。
- 事务A的 trx_id 发生变更，**trx_id: 4366**。因为这里执行了DML操作，需要分配实际的 trx_id。


#### T3时刻（事务A）: 查询数据 id=1001

```
select id, status, create_time, update_time
from qc_order
where id in (1001, 1002);
```

执行结果:


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/68b24638ad843515e39f3fed/6afb427d-1c34-49cd-9dec-3223badf6fd1.png)

返回的 id=1001 数据， status = 10。

⚠️注意:

- 事务A的trx_id：4366
- 事务B的trx_id：4364


#### 使用 undrop-for-innodb 工具分析ibd文件，观测qc_order表记录的 DB_TRX_ID 。验证是否事务A没有更新记录id=1001

undrop-for-innodb 是一款专为 InnoDB 存储引擎设计的开源数据恢复工具，支持从文件级别恢复误删除、损坏或丢失的数据。也可以用来从ibd文件中解析出表的数据，其兼容 MySQL 5.7 版本。

执行如下步骤:

```
# 1. 关闭 MySQL，复制 qc_order的ibd文件到 ./data 目录。需要确保MySQL参数， innodb_file_per_table=on
[root@localhost undrop-for-innodb]# ls -lh ./data/
total 96K
-rw-r-----. 1 root root 96K Aug 17 21:49 qc_order.ibd

# 2. 使用 stream_parser 进行拆页
[root@localhost undrop-for-innodb]# ./undrop-for-innodb/stream_parser -f ./data/qc_order.ibd 
Opening file: ./data/qc_order.ibd
File information:

ID of device containing file:        64768
inode number:                     70389401
protection:                         100640 (regular file)
number of hard links:                    1
user ID of owner:                        0
group ID of owner:                       0
device ID (if special file):             0
blocksize for filesystem I/O:         4096
number of blocks allocated:            192
time of last access:            1755438550 Sun Aug 17 21:49:10 2025
time of last modification:      1755438550 Sun Aug 17 21:49:10 2025
time of last status change:     1755438825 Sun Aug 17 21:53:45 2025
total size, in bytes:                98304 (96.000 kiB)

Size to process:                     98304 (96.000 kiB)
All workers finished in 0 sec

# 会生成目录：pages-qc_order.ibd/，其中 FIL_PAGE_INDEX/ 里是索引页

# 3. 确定叶子页文件名
[root@localhost undrop-for-innodb]# ls -lh ./pages-qc_order.ibd/FIL_PAGE_INDEX/
total 16K
-rw-r--r--. 1 root root 16K Aug 17 21:57 0000000000000049.page

# 4. 准备qc_order的DDL。
# undrop-for-innodb 的 c_parser 在解析 CREATE TABLE 时有个限制 —— 它的 SQL parser 只接受 简化版的 DDL，不能有多余的引号或不支持的选项。

[root@localhost undrop-for-innodb]# cat ./qc_order.sql 
CREATE TABLE qc_order (
  id INT NOT NULL,
  status INT NOT NULL,
  create_time DATETIME NOT NULL,
  update_time DATETIME NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=Dynamic;

# 5. 用 c_parser 解析叶子页。数据输出到 dump.tsv
[root@localhost undrop-for-innodb]# ./undrop-for-innodb/c_parser -6f ./pages-qc_order.ibd/FIL_PAGE_INDEX/0000000000000049.page -t ./qc_order.sql > ./dump.tsv 
SET FOREIGN_KEY_CHECKS=0;
LOAD DATA LOCAL INFILE '/root/undrop-for-innodb/dumps/default/qc_order' REPLACE INTO TABLE `qc_order` CHARACTER SET UTF8 FIELDS TERMINATED BY '\t' OPTIONALLY ENCLOSED BY '"' LINES STARTING BY 'qc_order\t' (`id`, `status`, `create_time`, `update_time`);
-- STATUS {"records_expected": 2, "records_dumped": 2, "records_lost": false} STATUS END

# 6. 查看 dump.tsv 内容
[root@localhost undrop-for-innodb]# cat dump.tsv 
-- Page id: 3, Format: COMPACT, Records list: Valid, Expected records: (2 2)
00000000110C	2A0000013C0323	qc_order	1001	20	"2025-08-17 17:04:35.0"	"2025-08-17 17:06:57.0"
00000000110E	2B0000013D0403	qc_order	1002	20	"2025-08-17 17:04:35.0"	"2025-08-17 17:07:42.0"
-- Page id: 3, Found records: 2, Lost records: NO, Leaf page: YES

# 第一列为记录的 DB_TRX_ID，以十六进制输出，也就是我们需要找的数据了。转换为 10进制:
00000000110C ->  4364    (id=1001)
00000000110E ->  4366    (id=1002)
```

DB_TRX_ID = 4364，就对应事务B的 trx_id。DB_TRX_ID = 4366，就对应事务A的 trx_id。可以表明事务B 更新了id=1001，事务A更新了 id=1002。

## 5. 总结

1. 事务中执行 Update 后为什么有时候不能读到更新后的数据，只能读到历史数据？


- 如果在事务A创建了 ReadView 后，Update语句执行前，存在其他流程并发的执行相同行记录的更新并提交了事务，且两个事务更新后的数据一致。当事务A执行 Update 语句时，MySQL会因行记录更新前后数据没有发生变化，跳过这条记录的更新。
- 因为 MySQL 跳过了行记录的更新，则行记录的 DB_TRX_ID 不会更新为当前事务 A 的事务ID。Update 更新后，通过Select 读取更新记录，根据快照读流程，这条记录的最新版本的数据对当前事务A 是不可见的，那只能通过记录的历史版本链，读取出创建ReadView开始前的数据返回。


1. 怎么避免 这种 "更新消失" 场景？


- 在事务开始前，使用 select ... for update 将待更新的记录加锁。避免事务期间，其他事务更新。


- 对于先更新后读取的场景，可以将更新的内容填充到后读取的记录中。
- 采用乐观锁机制，记录增加 version 字段，每次更新的时候：version = version + 1。


参考:

- https://dev.mysql.com/doc/refman/5.7/en/innodb-consistent-read.html
- https://github.com/twindb/undrop-for-innodb


> 关于作者曾明，转转履约中台研发工程师，主要负责质检业务。

想了解更多转转公司的业务实践，欢迎点击关注下方公众号：

