---
作者:
  - "滴滴技术"
原文链接: https://mp.weixin.qq.com/s?__biz=MzU1ODEzNjI2NA==&amp;mid=2247574547&amp;idx=1&amp;sn=84cf51d6eb24def39b62a6c8b38796a2&amp;chksm=fdc5d31c9850a5413403e5dd9ac961a5eab4c4a2f984b4b00d0a1ec912f59e1f938b1ed819f3&amp;mpshare=1&amp;scene=1&amp;srcid=0814LU0KJuu9xhEnu0CHHtzu&amp;sharer_shareinfo=7d535b8ceef7befb325315732f7fbbbd&amp;sharer_shareinfo_first=7d535b8ceef7befb325315732f7fbbbd#rd
发布时间: ""
收藏时间: "2025-08-14"
关联日记: "[[2025-08-14]]"
tags:
  - 文章
---
![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/064919a7-8bcf-4c7e-b154-68857802604b.gif)

**导读**

本文围绕RocketMQ和基于其实现的DDMQ的顺序消费机制展开深度探讨，从源码解读二者顺序消费的实现原理和差异，包括发送端的顺序发送，Broker及消费端的顺序拉取，消费端的顺序消费等。

适合有一定消息队列基础，正在或计划使用RocketMQ及相关衍生产品进行开发，对消息顺序性有严格要求，期望深入理解底层原理以优化系统性能和稳定性的后端开发工程师、架构师阅读。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/5e9b7514-5688-4082-ad76-d20e68e9101f.gif)

**RocketMQ**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/c8f4f971-08d1-4cd3-b0f8-08909353e084.gif)

**RocketMQ模型**

先简单了解一下RocketMQ的模型，有个概念。

**部署模型**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/f2954d95-022b-45db-b0bf-5113ef2cb828.png)

NameServer：担任路由消息的提供者，使得生产者或消费者能够通过NameServer查找各Topic及其queue相应的Broker IP列表。

Broker：消息中转角色，负责接收从生产者发来的消息并存储，同时为消费者拉取请求做准备。

**队列模型**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/9d66d6a4-31bd-4690-9f44-35aa072a15c6.png)

Topic：一类消息的集合，每个topic包含若干条消息，但每条消息只能属于一个topic。

Tag：相同topic下可以有不同的tag，即再分类。

注：上图中TopicA和TopicB的Queue0不是同一个队列。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/f35f9b08-edc6-4878-b2da-91792b1fbfc9.png)

集群消费下，同一Topic下的队列会均匀分配给同一消费者组中的每位消费者。

Rebalance机制，即负载均衡机制：将队列均匀分配给消费者，包括队列数或消费者数有变化时也是通过该机制重新分配。

这里Rebalance策略有几种，由于不是本次分享重点就不展开了，感兴趣的可以看org.apache.rocketmq.client.consumer.rebalance目录下的实现。

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/c1a2b1df-9172-435e-84a5-653d43ede92c.gif)

**一张图了解RocketMQ如何顺序消费 **

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/1c50fb1f-109f-4706-b917-8c950adbfaa1.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/fd0005fa-7852-4921-b091-68e526fda685.gif)

**源码解读 **

```
<dependency>
    <groupId>org.apache.rocketmq</groupId>
    <artifactId>rocketmq-client</artifactId>
    <version>5.3.1</version>
</dependency>
```

**顺序发送消息**

做法：按序投递至同一队列中。

调用方法：org.apache.rocketmq.client.producer.DefaultMQProducer#send(org.apache.rocketmq.common.message.Message, org.apache.rocketmq.client.producer.MessageQueueSelector, java.lang.Object)

```
// 顺序发送使用示例
public static void main(String[] args) throws Exception {
    // 创建生产者实例并设置生产者组名
    DefaultMQProducer producer = new DefaultMQProducer("producer_group_name");
    // 设置Name Server地址
    producer.setNamesrvAddr("127.0.0.1:9876");
    producer.start();
    // 发送消息
    Message message = new Message("test_topic", "test_tag", "Hello, Rocketmq!".getBytes());
    SendResult sendResult = producer.send(message, new SelectMessageQueueByHash(), "test_arg");
    System.out.println(sendResult);
    //...
    producer.shutdown();
}
```

这个send方法有三个参数

- Message msg：包含Topic、Tag、消息内容。


- MessageQueueSelector selector：消息队列选择器（一个interface，有一个select方法，返回是消息队列），可自行实现也可以用SDK中提供的几个。


- Object arg：上面selector的select方法的参数。


```
// org.apache.rocketmq.client.producer.DefaultMQProducer#send(org.apache.rocketmq.common.message.Message, org.apache.rocketmq.client.producer.MessageQueueSelector, java.lang.Object)
// 消息发送调用入口
@Override
public SendResult send(Message msg, MessageQueueSelector selector, Object arg)
    throws MQClientException, RemotingException, MQBrokerException, InterruptedException {
    msg.setTopic(withNamespace(msg.getTopic()));
    // 选取发送的队列
    MessageQueue mq = this.defaultMQProducerImpl.invokeMessageQueueSelector(msg, selector, arg, this.getSendMsgTimeout());
    mq = queueWithNamespace(mq);
    // 执行消息发送
    if (this.getAutoBatch() && !(msg instanceof MessageBatch)) {
        return sendByAccumulator(msg, mq, null);
    } else {
        return sendDirect(msg, mq, null);
    }
}

// org.apache.rocketmq.client.impl.producer.DefaultMQProducerImpl#invokeMessageQueueSelector
// 选择器：选择发送的消息队列
public MessageQueue invokeMessageQueueSelector(Message msg, MessageQueueSelector selector, Object arg,
                                                final long timeout) throws MQClientException, RemotingTooMuchRequestException {
    long beginStartTime = System.currentTimeMillis();
    this.makeSureStateOK();
    Validators.checkMessage(msg, this.defaultMQProducer);
    
    // 获取Topic对象
    TopicPublishInfo topicPublishInfo = this.tryToFindTopicPublishInfo(msg.getTopic());
    if (topicPublishInfo != null && topicPublishInfo.ok()) {
        MessageQueue mq = null;
        try {
            // 获取Topic的所有队列
            List<MessageQueue> messageQueueList =
                    mQClientFactory.getMQAdminImpl().parsePublishMessageQueues(topicPublishInfo.getMessageQueueList());
            Message userMessage = MessageAccessor.cloneMessage(msg);
            String userTopic = NamespaceUtil.withoutNamespace(userMessage.getTopic(), mQClientFactory.getClientConfig().getNamespace());
            userMessage.setTopic(userTopic);
            
            // 选取发送的队列
            mq = mQClientFactory.getClientConfig().queueWithNamespace(selector.select(messageQueueList, userMessage, arg));
        } catch (Throwable e) {
            throw new MQClientException("select message queue threw exception.", e);
        }
        
        long costTime = System.currentTimeMillis() - beginStartTime;
        if (timeout < costTime) {
            throw new RemotingTooMuchRequestException("sendSelectImpl call timeout");
        }
        if (mq != null) {
            // 返回队列
            return mq;
        } else {
            throw new MQClientException("select message queue return null.", null);
        }
    }
    validateNameServerSetting();
    throw new MQClientException("No route info for this topic, " + msg.getTopic(), null);
}
```

SDK中提供的几种MessageQueueSelector实现

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/82f3638c-c4fc-46b0-ac82-b45fc30c98d2.png)

```
// org.apache.rocketmq.client.producer.selector.SelectMessageQueueByHash
// hash取余 选择消息队列
public class SelectMessageQueueByHash implements MessageQueueSelector {
    
    @Override
    public MessageQueue select(List<MessageQueue> mqs, Message msg, Object arg) {
        int value = arg.hashCode() % mqs.size();
        if (value < 0) {
            value = Math.abs(value);
        }
        return mqs.get(value);
    }
}
```

```
// org.apache.rocketmq.client.producer.selector.SelectMessageQueueByRandom
// 随机 选择消息队列
public class SelectMessageQueueByRandom implements MessageQueueSelector {
    private Random random = new Random(System.currentTimeMillis());
    
    @Override
    public MessageQueue select(List<MessageQueue> mqs, Message msg, Object arg) {
        int value = random.nextInt(mqs.size());
        return mqs.get(value);
    }
}
```

所以，消息顺序发送的重点就是这个selector，要确保消息都发送到了同一个队列中。

在消息队列数量不变的情况下，是可以使用hash取余的这种方法的，同时还需保证消息发送时传入的arg不变。一般默认也是用的这种方法。

**另外，若有并发问题或多实例同时投递问题还需要通过加锁等方式自行控制消息按序发送**。

**顺序消费消息**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/2ccd3ca8-ae2a-4613-b8e9-0d3ae65f54cb.png)

- 集群消费下，保证消费者集群只有一位在拉取及消费消息。
- 消费者消费时只有一个线程在消费；


```
// 客户端顺序消费使用示例
public static void main(String[] args) throws Exception {
    // 创建消费者实例并设置消费者组名和消费模式
    DefaultMQPushConsumer consumer = new DefaultMQPushConsumer("consumer_group_name");
    consumer.setNamesrvAddr("127.0.0.1:9876");
    consumer.setMessageModel(MessageModel.CLUSTERING);
    consumer.subscribe("test_topic", "test_tag");
    // 设置顺序消费消息监听器
    consumer.registerMessageListener(new MessageListenerOrderly() {
        @Override
        public ConsumeOrderlyStatus consumeMessage(List<MessageExt> msgs, ConsumeOrderlyContext context) {
            for (MessageExt msg : msgs) {
                try {
                    System.out.println(new String(msg.getBody()));
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
            return ConsumeOrderlyStatus.SUCCESS;
        }
    
    });
    consumer.start();
}
```

- 客户端-拉取消息


拉取消息前，请求Broker端上锁，定时20秒执行一次续锁：

```
// org.apache.rocketmq.client.impl.consumer.ConsumeMessageOrderlyService#start
// 拉取消息-客户端请求Broker端上锁
@Override
public void start() {
    // 集群消费模式下，通过定时器，每20s请求一次Broker上锁
    if (MessageModel.CLUSTERING.equals(ConsumeMessageOrderlyService.this.defaultMQPushConsumerImpl.messageModel())) {
        this.scheduledExecutorService.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
                try {
                    ConsumeMessageOrderlyService.this.lockMQPeriodically();
                } catch (Throwable e) {
                    log.error("scheduleAtFixedRate lockMQPeriodically exception", e);
                }
            }
        // REBALANCE_LOCK_INTERVAL 默认值为20000，可配置
        }, 1000, ProcessQueue.REBALANCE_LOCK_INTERVAL, TimeUnit.MILLISECONDS);
    }
}

// org.apache.rocketmq.client.impl.consumer.ConsumeMessageOrderlyService#lockMQPeriodically
public synchronized void lockMQPeriodically() {
    if (!this.stopped) {
        this.defaultMQPushConsumerImpl.getRebalanceImpl().lockAll();
    }
}

// org.apache.rocketmq.client.impl.consumer.RebalanceImpl#lockAll
public void lockAll() {
    HashMap<String, Set<MessageQueue>> brokerMqs = this.buildProcessQueueTableByBrokerName();
    
    Iterator<Entry<String, Set<MessageQueue>>> it = brokerMqs.entrySet().iterator();
    while (it.hasNext()) {
        Entry<String, Set<MessageQueue>> entry = it.next();
        final String brokerName = entry.getKey();
        final Set<MessageQueue> mqs = entry.getValue();
        
        if (mqs.isEmpty()) {
            continue;
        }
        
        // 获取Broker
        FindBrokerResult findBrokerResult = this.mQClientFactory.findBrokerAddressInSubscribe(brokerName, MixAll.MASTER_ID, true);
        if (findBrokerResult != null) {
            // 通过 消费者组 + clientId 对 messageQueue 进行Broker端上锁
            LockBatchRequestBody requestBody = new LockBatchRequestBody();
            requestBody.setConsumerGroup(this.consumerGroup);
            requestBody.setClientId(this.mQClientFactory.getClientId());
            requestBody.setMqSet(mqs);
            
            try {
                // 尝试上锁。这里的1s不是锁的过期时间，是请求超时时间；锁过期时间是维护在Broker端
                Set<MessageQueue> lockOKMQSet =
                    this.mQClientFactory.getMQClientAPIImpl().lockBatchMQ(findBrokerResult.getBrokerAddr(), requestBody, 1000);
                
                for (MessageQueue mq : mqs) {
                    ProcessQueue processQueue = this.processQueueTable.get(mq);
                    if (processQueue != null) {
                        if (lockOKMQSet.contains(mq)) {
                            if (!processQueue.isLocked()) {
                                log.info("the message queue locked OK, Group: {} {}", this.consumerGroup, mq);
                            }
                            // 上锁成功
                            processQueue.setLocked(true);
                            processQueue.setLastLockTimestamp(System.currentTimeMillis());
                        } else {
                            // 上锁失败
                            processQueue.setLocked(false);
                            log.warn("the message queue locked Failed, Group: {} {}", this.consumerGroup, mq);
                        }
                    }
                }
            } catch (Exception e) {
                log.error("lockBatchMQ exception, " + mqs, e);
            }
        }
    }
}
```

拉取消息，校验Broker端是否上锁成功。

拉取成功后触发消费回调。

```
// org.apache.rocketmq.client.impl.consumer.DefaultMQPushConsumerImpl#pullMessage
// 拉取消息-客户端请求Broker上锁后
public void pullMessage(final PullRequest pullRequest) {
    final ProcessQueue processQueue = pullRequest.getProcessQueue();

    // ... 省略
    
    if (!this.consumeOrderly) {
        // ... 省略
    } else {
        // 用前面上锁时设置的processQueue.locked判断Broker端是否上锁成功
        if (processQueue.isLocked()) {
            if (!pullRequest.isPreviouslyLocked()) {
                long offset = -1L;
                try {
                    offset = this.rebalanceImpl.computePullFromWhereWithException(pullRequest.getMessageQueue());
                    if (offset < 0) {
                        throw new MQClientException(ResponseCode.SYSTEM_ERROR, "Unexpected offset " + offset);
                    }
                } catch (Exception e) {
                    this.executePullRequestLater(pullRequest, pullTimeDelayMillsWhenException);
                    log.error("Failed to compute pull offset, pullResult: {}", pullRequest, e);
                    return;
                }
                boolean brokerBusy = offset < pullRequest.getNextOffset();
                log.info("the first time to pull message, so fix offset from broker. pullRequest: {} NewOffset: {} brokerBusy: {}",
                    pullRequest, offset, brokerBusy);
                if (brokerBusy) {
                    log.info("[NOTIFYME]the first time to pull message, but pull request offset larger than broker consume offset. pullRequest: {} NewOffset: {}",
                        pullRequest, offset);
                }
                
                // 设置上锁成功 和 消息消费进度
                pullRequest.setPreviouslyLocked(true);
                pullRequest.setNextOffset(offset);
            }
        } else {
            // 没上锁成功则后续再重试
            this.executePullRequestLater(pullRequest, pullTimeDelayMillsWhenException);
            log.info("pull message later because not locked in broker, {}", pullRequest);
            return;
        }
    }
    
    // ... 省略
    
    // 初始化拉取消息成功时的回调  
    PullCallback pullCallback = new PullCallback() {
        @Override
        public void onSuccess(PullResult pullResult) {
            if (pullResult != null) {
                pullResult = DefaultMQPushConsumerImpl.this.pullAPIWrapper.processPullResult(pullRequest.getMessageQueue(), pullResult,
                    subscriptionData);
                
                switch (pullResult.getPullStatus()) {
                    case FOUND:
                        // ... 省略
                        
                        // 触发消息消费
                        DefaultMQPushConsumerImpl.this.consumeMessageService.submitConsumeRequest(
                            pullResult.getMsgFoundList(),
                            processQueue,
                            pullRequest.getMessageQueue(),
                            dispatchToConsume);
        
        // ... 省略
    }
    
    // ... 省略
    
    // 触发消息拉取及消费
    try {
        this.pullAPIWrapper.pullKernelImpl(
            pullRequest.getMessageQueue(),
            subExpression,
            subscriptionData.getExpressionType(),
            subscriptionData.getSubVersion(),
            // 拉取offset
            pullRequest.getNextOffset(),
            this.defaultMQPushConsumer.getPullBatchSize(),
            this.defaultMQPushConsumer.getPullBatchSizeInBytes(),
            sysFlag,
            commitOffsetValue,
            BROKER_SUSPEND_MAX_TIME_MILLIS,
            CONSUMER_TIMEOUT_MILLIS_WHEN_SUSPEND,
            CommunicationMode.ASYNC,
            // 消费回调
            pullCallback
        );
    } catch (Exception e) {
        log.error("pullKernelImpl exception", e);
        this.executePullRequestLater(pullRequest, pullTimeDelayMillsWhenException);
    }
}
```

- Broker端-处理客户端加锁请求


Broker端锁过期时间为默认60s，且如果有副本节点，会升级为分布式锁。

这段代码不在客户端SDK中，需要查看Broker端源码 https://github.com/apache/rocketmq/tree/develop/broker/src/main/java/org/apache/rocketmq/broker。

```
// org.apache.rocketmq.broker.processor.AdminBrokerProcessor#lockBatchMQ
// 拉取消息-Broker端上锁
private RemotingCommand lockBatchMQ(ChannelHandlerContext ctx,
    RemotingCommand request) throws RemotingCommandException {
    final RemotingCommand response = RemotingCommand.createResponseCommand(null);
    LockBatchRequestBody requestBody = LockBatchRequestBody.decode(request.getBody(), LockBatchRequestBody.class);
    
    Set<MessageQueue> lockOKMQSet = new HashSet<>();
    // 锁住本地队列
    Set<MessageQueue> selfLockOKMQSet = this.brokerController.getRebalanceLockManager().tryLockBatch(
        requestBody.getConsumerGroup(),
        requestBody.getMqSet(),
        requestBody.getClientId());
    
    if (requestBody.isOnlyThisBroker() || !brokerController.getBrokerConfig().isLockInStrictMode()) {
        lockOKMQSet = selfLockOKMQSet;
    } else {
    // 若不仅仅是锁当前Broker的，则继续分布式锁逻辑
        requestBody.setOnlyThisBroker(true);
        int replicaSize = this.brokerController.getMessageStoreConfig().getTotalReplicas();
        
        // 计算法人数量
        int quorum = replicaSize / 2 + 1;
        
        // 如果无其他副本节点，则无需分布式锁
        if (quorum <= 1) {
            lockOKMQSet = selfLockOKMQSet;
        } else {
            // 计算本地各已上锁队列的锁数量
            final ConcurrentMap<MessageQueue, Integer> mqLockMap = new ConcurrentHashMap<>();
            for (MessageQueue mq : selfLockOKMQSet) {
                if (!mqLockMap.containsKey(mq)) {
                    mqLockMap.put(mq, 0);
                }
                mqLockMap.put(mq, mqLockMap.get(mq) + 1);
            }
            
            BrokerMemberGroup memberGroup = this.brokerController.getBrokerMemberGroup();
            
            if (memberGroup != null) {
                // 遍历除当前节点外的其他节点，向他们发起加锁请求，让它们也加上本地锁
                Map<Long, String> addrMap = new HashMap<>(memberGroup.getBrokerAddrs());
                addrMap.remove(this.brokerController.getBrokerConfig().getBrokerId());
                final CountDownLatch countDownLatch = new CountDownLatch(addrMap.size());
                requestBody.setMqSet(selfLockOKMQSet);
                requestBody.setOnlyThisBroker(true);
                for (Long brokerId : addrMap.keySet()) {
                    try {
                        this.brokerController.getBrokerOuterAPI().lockBatchMQAsync(addrMap.get(brokerId),
                            requestBody, 1000, new LockCallback() {
                                @Override
                                public void onSuccess(Set<MessageQueue> lockOKMQSet) {
                                    for (MessageQueue mq : lockOKMQSet) {
                                        if (!mqLockMap.containsKey(mq)) {
                                            mqLockMap.put(mq, 0);
                                        }
                                        // 加锁成功计数
                                        mqLockMap.put(mq, mqLockMap.get(mq) + 1);
                                    }
                                    countDownLatch.countDown();
                                }
                                
                                @Override
                                public void onException(Throwable e) {
                                    LOGGER.warn("lockBatchMQAsync on {} failed, {}", addrMap.get(brokerId), e);
                                    countDownLatch.countDown();
                                }
                            });
                    } catch (Exception e) {
                        LOGGER.warn("lockBatchMQAsync on {} failed, {}", addrMap.get(brokerId), e);
                        countDownLatch.countDown();
                    }
                }
                try {
                    countDownLatch.await(2000, TimeUnit.MILLISECONDS);
                } catch (InterruptedException e) {
                    LOGGER.warn("lockBatchMQ exception on {}, {}", this.brokerController.getBrokerConfig().getBrokerName(), e);
                }
            }
            
            // 加锁数大于等于法人数（过半）才算加锁成功
            for (MessageQueue mq : mqLockMap.keySet()) {
                if (mqLockMap.get(mq) >= quorum) {
                    lockOKMQSet.add(mq);
                }
            }
        }
    }
    
    LockBatchResponseBody responseBody = new LockBatchResponseBody();
    responseBody.setLockOKMQSet(lockOKMQSet);
    
    response.setBody(responseBody.encode());
    response.setCode(ResponseCode.SUCCESS);
    response.setRemark(null);
    return response;
}


// org.apache.rocketmq.broker.client.rebalance.RebalanceLockManager
public class RebalanceLockManager {
    // Broker端锁默认过期时间 60s
    private final static long REBALANCE_LOCK_MAX_LIVE_TIME = Long.parseLong(System.getProperty(
        "rocketmq.broker.rebalance.lockMaxLiveTime", "60000"));
    private final Lock lock = new ReentrantLock();
    // 一个消费者组 一组队列锁
    private final ConcurrentMap<String/* group */, ConcurrentHashMap<MessageQueue, LockEntry>> mqLockTable =
        new ConcurrentHashMap<>(1024);
    
    // ... 省略
    
    static class LockEntry {
        private String clientId;
        private volatile long lastUpdateTimestamp = System.currentTimeMillis();
        
        // 是否上锁
        public boolean isLocked(final String clientId) {
            boolean eq = this.clientId.equals(clientId);
            return eq && !this.isExpired();
        }
        
        // 是否过期
        public boolean isExpired() {
            boolean expired =
                (System.currentTimeMillis() - this.lastUpdateTimestamp) > REBALANCE_LOCK_MAX_LIVE_TIME;
            
            return expired;
        }
    }
}
```

- 客户端-消费消息


消费消息时需要对messageQueue和processQueue都上本地锁，且前提是已获得了Broker端的锁。

- messageQueue表示拉取回来的消息元数据信息。
- processQueue可以看作是MessageQueue的消费快照，本地操作主要是修改它的数据，messageQueue和processQueue是一一对应的。


```
// org.apache.rocketmq.client.impl.consumer.ConsumeMessageOrderlyService.ConsumeRequest#run
// 消费消息-消费前上本地锁
@Override
public void run() {
    if (this.processQueue.isDropped()) {
        log.warn("run, the message queue not be able to consume, because it's dropped. {}", this.messageQueue);
        return;
    }
    
    // messageQueue上线程锁
    final Object objLock = messageQueueLock.fetchLockObject(this.messageQueue);
    synchronized (objLock) {
        // 广播模式 或 Broker端上锁成功 才会继续执行
        if (MessageModel.BROADCASTING.equals(ConsumeMessageOrderlyService.this.defaultMQPushConsumerImpl.messageModel())
            || this.processQueue.isLocked() && !this.processQueue.isLockExpired()) {
            final long beginTime = System.currentTimeMillis();
            for (boolean continueConsume = true; continueConsume; ) {
                if (this.processQueue.isDropped()) {
                    log.warn("the message queue not be able to consume, because it's dropped. {}", this.messageQueue);
                    break;
                }
                
                // 集群消费 Broker端未上锁
                if (MessageModel.CLUSTERING.equals(ConsumeMessageOrderlyService.this.defaultMQPushConsumerImpl.messageModel())
                    && !this.processQueue.isLocked()) {
                    log.warn("the message queue not locked, so consume later, {}", this.messageQueue);
                    ConsumeMessageOrderlyService.this.tryLockLaterAndReconsume(this.messageQueue, this.processQueue, 10);
                    break;
                }
                
                // 集群消费 Broker端锁过期
                if (MessageModel.CLUSTERING.equals(ConsumeMessageOrderlyService.this.defaultMQPushConsumerImpl.messageModel())
                    && this.processQueue.isLockExpired()) {
                    log.warn("the message queue lock expired, so consume later, {}", this.messageQueue);
                    ConsumeMessageOrderlyService.this.tryLockLaterAndReconsume(this.messageQueue, this.processQueue, 10);
                    break;
                }
                
                // 超时重试
                long interval = System.currentTimeMillis() - beginTime;
                if (interval > MAX_TIME_CONSUME_CONTINUOUSLY) {
                    ConsumeMessageOrderlyService.this.submitConsumeRequestLater(processQueue, messageQueue, 10);
                    break;
                }
                
                final int consumeBatchSize =
                    ConsumeMessageOrderlyService.this.defaultMQPushConsumer.getConsumeMessageBatchMaxSize();
                
                List<MessageExt> msgs = this.processQueue.takeMessages(consumeBatchSize);
                defaultMQPushConsumerImpl.resetRetryAndNamespace(msgs, defaultMQPushConsumer.getConsumerGroup());
                if (!msgs.isEmpty()) {
                    final ConsumeOrderlyContext context = new ConsumeOrderlyContext(this.messageQueue);
                    
                    ConsumeOrderlyStatus status = null;
                    
                    // 消费前hook调用 ... 省略
                    
                    // 正式消费
                    long beginTimestamp = System.currentTimeMillis();
                    ConsumeReturnType returnType = ConsumeReturnType.SUCCESS;
                    boolean hasException = false;
                    try {
                        // processQueue上线程锁
                        this.processQueue.getConsumeLock().readLock().lock();
                        if (this.processQueue.isDropped()) {
                            log.warn("consumeMessage, the message queue not be able to consume, because it's dropped. {}",
                                this.messageQueue);
                            break;
                        }
                        // 触发业务消费
                        status = messageListener.consumeMessage(Collections.unmodifiableList(msgs), context);
                    } catch (Throwable e) {
                        log.warn("consumeMessage exception: {} Group: {} Msgs: {} MQ: {}",
                            UtilAll.exceptionSimpleDesc(e),
                            ConsumeMessageOrderlyService.this.consumerGroup,
                            msgs,
                            messageQueue, e);
                        hasException = true;
                    } finally {
                        // 释放processQueue线程锁
                        this.processQueue.getConsumeLock().readLock().unlock();
                    }
                    
                    
                    // 处理消费结果 ... 省略
                    
                    // 消费结束后的hook ... 省略
                    
                    ConsumeMessageOrderlyService.this.getConsumerStatsManager()
                        .incConsumeRT(ConsumeMessageOrderlyService.this.consumerGroup, messageQueue.getTopic(), consumeRT);
                    
                    continueConsume = ConsumeMessageOrderlyService.this.processConsumeResult(msgs, status, context, this);
                } else {
                    continueConsume = false;
                }
            }
        } else {
            // messageQueue线程锁 上锁失败，稍后重试
            if (this.processQueue.isDropped()) {
                log.warn("the message queue not be able to consume, because it's dropped. {}", this.messageQueue);
                return;
            }
            
            ConsumeMessageOrderlyService.this.tryLockLaterAndReconsume(this.messageQueue, this.processQueue, 100);
        }
    }
}
```

这里为什么对messageQueue和processQueue都要加锁？

- 对messageQueue加本地锁是保证同一时间只有一个线程在消费该队列。
- 对processQueue加本地锁是避免在rebalance时，将还在消费中的该队列给移除掉以分配给其他消费者。


将二者分别用两把锁锁住，也是为了让消费后的处理（如处理消费结果、触发消费结束的hook等），不阻塞Rebalance。

```
// org.apache.rocketmq.client.impl.consumer.RebalancePushImpl#tryRemoveOrderMessageQueue
// rebalance移除队列
private boolean tryRemoveOrderMessageQueue(final MessageQueue mq, final ProcessQueue pq) {
    try {
        boolean forceUnlock = pq.isDropped() && System.currentTimeMillis() > pq.getLastLockTimestamp() + UNLOCK_DELAY_TIME_MILLS;
        // 移除队列前需先获取processQueue本地锁
        if (forceUnlock || pq.getConsumeLock().writeLock().tryLock(500, TimeUnit.MILLISECONDS)) {
            try {
                RebalancePushImpl.this.defaultMQPushConsumerImpl.getOffsetStore().persist(mq);
                RebalancePushImpl.this.defaultMQPushConsumerImpl.getOffsetStore().removeOffset(mq);
                
                pq.setLocked(false);
                RebalancePushImpl.this.unlock(mq, true);
                return true;
            } finally {
                if (!forceUnlock) {
                    pq.getConsumeLock().writeLock().unlock();
                }
            }
        } else {
            pq.incTryUnlockTimes();
        }
    } catch (Exception e) {
        pq.incTryUnlockTimes();
    }
    
    return false;
}
```

**思考一个问题**

讲DDMQ中的顺序消费前先看一个问题：

以打车流程（叫车 -> 接车 -> 支付）为例，同一个人的流程需要保序，不同人的流程应互不影响。

例如甲乙两个人同时打车，甲的接车需在甲的叫车之后，而乙的接车不应因甲的接车阻塞而阻塞。

这种情况下，如果使用RocketMQ原生的顺序消费该怎么解？

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/304009d1-d430-42ba-8e9a-c9d635a88658.gif)

**DDMQ中的顺序消费**

https://github.com/didi/DDMQ

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/73e8a092-55e6-4f66-a42a-69790e58ee8d.gif)

**一张图了解DDMQ如何顺序消费**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/b729aa4d-167d-48bb-9d3e-a3768f32c984.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/df4fafed-abc9-4204-b3b8-7408d718b0cd.gif)

**时序图**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/c391cf1a-0e19-4667-a6f1-b44ae8e5b4f2.png)

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/a6682de2-6955-47d0-9402-88a69d7d8e0e.gif)

**源码解读 **

**客户端-拉取与消费**

每sleep一段时间（默认5s），就会触发一次向代理端的PULL请求，若拉取到了消息则触发业务消费，业务消费结束后，将消费结果记录在本地。

这个在PULL请求在拉取代理端的同时，会将本地此前已消费的记录放在参数中同步至代理端，然后再将本地记录清除。

```
// com.xiaojukeji.carrera.consumer.thrift.client.BaseCarreraConsumerPool#startConsume
// DDMQ启动消费入口-客户端
private void startConsume(BaseMessageProcessor processor, int concurrency, Map<String, Integer> extraConcurrency, List<Node> servers) {
    // 线程池总数，concurrency是业务设置的线程数，servers.size()以及下面的serverCnt是代理节点数
    int totalThreads = concurrency > 0 ? Math.max(concurrency, servers.size()) : 0;
    for (Integer topicConcurrency : extraConcurrency.values()) {
        totalThreads += topicConcurrency > 0 ? Math.max(topicConcurrency, servers.size()) : 0;
    }
    if (totalThreads == 0) {
        throw new RuntimeException("concurrency is too small, at least one for each server.");
    }
    // 线程池
    executorService = Executors.newFixedThreadPool(totalThreads, new ThreadFactoryBuilder().setNameFormat("MessageProcess-%d").build());
    
    Collections.shuffle(servers);
    
    int serverCnt = servers.size();
    if (concurrency > 0) {
        if (concurrency < serverCnt) {
            LOGGER.warn("concurrency({})<server number({}), use {} as concurrency", concurrency, serverCnt, serverCnt);
            concurrency = serverCnt;
        }
        // 为每个代理节点启动消费，如果指定的线程数大于代理节点数，则会有多个线程同时消费同一代理节点
        for (int i = 0; i < serverCnt; i++) {
            int threadNumber = concurrency / serverCnt;
            threadNumber += i < concurrency % serverCnt ? 1 : 0;
            if (threadNumber == 0) {
                LOGGER.warn("no thread for server:{}", servers.get(i));
            } else {
                createConsumer(processor, threadNumber, servers.get(i), null);
            }
        }
    }
    
    // ... 省略
}


// com.xiaojukeji.carrera.consumer.thrift.client.BaseCarreraConsumerPool#createConsumer(com.xiaojukeji.carrera.consumer.thrift.client.BaseMessageProcessor, int, com.xiaojukeji.carrera.consumer.thrift.client.node.Node, java.lang.String)
// 创建消费者
private void createConsumer(final BaseMessageProcessor processor, int consumerNumber,
                            Node server, String topic) {
    for (int i = 0; i < consumerNumber; i++) {
        CarreraConfig newConfig = config.clone();
        newConfig.setServers(server.toStrStyle());
        final BaseCarreraConsumer consumer = createConsumer(newConfig, topic);
        
        consumer.setType(getConsumeType());
        if (!consumerMap.containsKey(server)) {
            consumerMap.put(server, new ConcurrentLinkedQueue<BaseCarreraConsumer>());
        }
        consumerMap.get(server).add(consumer);
        executorService.execute(new Runnable() {
            @Override
            public void run() {
                try {
                    // 启动消费
                    consumer.startConsume(processor);
                } catch (InterruptedException e) {
                    if (consumer.isStopped()) {
                        LOGGER.info("consumer finished!");
                    } else {
                        LOGGER.error("consumer is interrupted!", e);
                    }
                }
            }
        });
    }
}


// com.xiaojukeji.carrera.consumer.thrift.client.BaseCarreraConsumer#startConsume
// 启动消费
public void startConsume(BaseMessageProcessor processor) throws InterruptedException {
//        init();
    isRunning = true;
    LOGGER.info("start consume group:{},server:{},topic:{}", config.getGroupId(), config.getServers(), topic);
    try {
        while (isRunning) {
            // 每隔一段时间拉取一次消息，有新的消息则触发消费，没有则sleep一段时间
            // 但这里的拉取和消费都没有上本地锁
            RES response = pullMessage();
            if (response == null) { //no new message
                doRetrySleep();
            } else {
                processResponse(response, processor);
            }
        }
    } finally {
        close();
    }
    LOGGER.info("consume group[{}] finished!", config.getGroupId());
}

// ----------------------- 拉取消息
// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#doPullMessage
protected PullResponse doPullMessage() throws TException {
    // 这里会将之前已成功消费但还未submit的消息拼接成一个链表放到请求入参中
    ConsumeResult curResult = buildConsumeResult();
    try {
        request.setResult(curResult);
        // 向代理端发起PULL请求
        PullResponse response = client.pull(request);
        // 然后将本地已消费成功但还未submit的记录清空
        clearResult(curResult);
        
        LOGGER.debug("Client Request for {}:{}, Response:{}", host, request, response);
        if (response == null || response.getMessages() == null || response.getMessages().size() == 0) {
            LOGGER.debug("retry in {}ms, response={}", config.getRetryInterval(), response);
            return null;
        } else {
            return response;
        }
    } catch (PullException e) {
        LOGGER.error("pull exception, code={}, message={}", e.code, e.message);
    }
    
    return null;
}

// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#buildConsumeResult
// 将之前已成功消费但还未submit的消息拼接成一个链表
private ConsumeResult buildConsumeResult() {
    ConsumeResult ret = null;
    if (resultMap == null) {
        return ret;
    }
    
    for (ConsumeResult r : resultMap.values()) {
        if (r.getFailOffsetsSize() > 0 || r.getSuccessOffsetsSize() > 0) {
            r.nextResult = ret;
            ret = r;
        }
    }
    return ret;
}

// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#clearResult
// 记录清空
private void clearResult(ConsumeResult result) {
    for (ConsumeResult r = result; r != null; r = r.nextResult) {
        r.getFailOffsets().clear();
        r.getSuccessOffsets().clear();
    }
}

// ----------------------- 



// ----------------------- 消费消息
// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#doProcessMessage(com.xiaojukeji.carrera.consumer.thrift.PullResponse, com.xiaojukeji.carrera.consumer.thrift.client.MessageProcessor)
protected void doProcessMessage(PullResponse response, MessageProcessor processor) {
    Context context = response.getContext();
    // 遍历从代理端拉取到的消息
    for (Message msg : response.getMessages()) {
        MessageProcessor.Result pResult = MessageProcessor.Result.FAIL;
        try {
            // 触发业务消费
            pResult = processor.process(msg, context);
            LOGGER.debug("ProcessResult:{},msg.key={},group={},topic={},qid={}，offset={}", pResult,
                    msg.getKey(), context.getGroupId(), context.getTopic(), context.getQid(), msg.getOffset());
        } catch (Throwable e) {
            LOGGER.error("exception when processing message, msg=" + msg + ",context=" + context, e);
        }
        // 记录消费结果
        switch (pResult) {
            case SUCCESS:
                ack(context, msg.getOffset());
                break;
            case FAIL:
                fail(context, msg.getOffset());
                break;
        }
    }
}

// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#ack
// 记录成功消费结果，仅仅只是写在本地，并没有直接响应代理端
public synchronized void ack(Context context, long offset) {
    getResult(context).getSuccessOffsets().add(offset);
}

// com.xiaojukeji.carrera.consumer.thrift.client.SimpleCarreraConsumer#fail
// 记录失败消费结果，仅仅只是写在本地，并没有直接响应代理端
public synchronized void fail(Context context, long offset) {
    getResult(context).getFailOffsets().add(offset);
}
// ----------------------- 
```

**代理端-消费**

消费代理端与Broker是使用了RocketMQ原生的顺序消费，代理端通过队列和线程锁的方式保证客户端的顺序消费。

```
// com.xiaojukeji.carrera.cproxy.consumer.AbstractCarreraRocketMqConsumer#setup
// DDMQ顺序消费-代理端消费Broker消息（非业务消费）
private void setup(DefaultMQPushConsumer rmqConsumer, RocketMQBaseConfig config, GroupConfig groupConfig) {
    // ... 省略
    
    // 此处也是用了RocketMQ的顺序消费 MessageListenerOrderly
    rmqConsumer.setMessageListener((MessageListenerOrderly) (msgs, context) -> {
        if (autoCommit) {
            context.setAutoCommit(false);
        }
        // 消费消息，这里的消费指的是代理端的消费，而非客户端的消费
        return consumeRocketMQMessages(msgs, context.getMessageQueue());
    });
    
    // ... 省略
}

// com.xiaojukeji.carrera.cproxy.consumer.CarreraConsumer#process
public void process(CommonMessage message, ConsumeContext context, ResultCallBack resultCallBack) {
    if (upstreamTopicMap.containsKey(message.getTopic())) {
        // 创建一个UpstreamJob实例，既是消息也是任务
        UpstreamJob job = new UpstreamJob(this, upstreamTopicMap.get(message.getTopic()), message, context, resultCallBack);
        workingJobs.add(job);
        job.registerJobFinishedCallback(this::onJobFinish);
        // 执行消费
        job.execute();
    } else {
        resultCallBack.setResult(true);
    }
}


// com.xiaojukeji.carrera.cproxy.consumer.UpstreamJob#execute
public void execute() {
    // ... 省略
    
    // 会遍历所配置的Action
    if (actionIndex == CollectionUtils.size(getActions())) {
        onFinished(true);
        return;
    }
    String actionName = getActions().get(actionIndex++);
    state = actionName;
    if (LOGGER.isTraceEnabled()) {
        LOGGER.trace("job executing... {} actionIndex={}, act={}, thread={}", info(), actionIndex - 1, actionName, Thread.currentThread());
    }
    
    Action action = actionMap.get(actionName);
    if (action == null) {
        LOGGER.error("wrong act: {}", actionName);
        onFinished(false);
        return;
    }
    
    if (isTerminated) {
        LOGGER.info("job is terminated! job={}", info());
        terminate();
        return;
    }
    
    Action.Status status;
    try {
        // 执行消费
        status = action.act(this);
    } catch (Throwable e) {
        LOGGER.error("unexpected err, job=" + info(), e);
        onFinished(false);
        return;
    }
    switch (status) {
        case FAIL:
            LOGGER.error("execute error,job={}", info());
            onFinished(false);
            break;
        case FINISH:
            // 完成或失败时会触发回调
            onFinished(true);
            break;
        case ASYNCHRONIZED:
            // 异步直接结束
            break;
        case CONTINUE:
            // 若未结束会递归继续遍历后面的Action
            execute();
    }
}

// ---------------------------- OrderAction 

// com.xiaojukeji.carrera.cproxy.actions.OrderAction#act
public Action.Status act(UpstreamJob job) {
    String orderKey = job.getUpstreamTopic().getOrderKey();
    
    if (StringUtils.isNotBlank(orderKey)) {
        Object orderValue = null;
        // DDMQ顺序消费的三种保序依据：QID、MsgKey、JsonPath
        if (ORDER_BY_QID.equals(orderKey)) {
            orderValue = job.getTopic() + job.getQid();
        } else if (ORDER_BY_KEY.equals(orderKey)) {
            orderValue = job.getMsgKey();
        } else if (job.getData() instanceof JSONObject) {
            try {
                orderValue = JsonUtils.getValueByPath((JSONObject) job.getData(), orderKey);
            } catch (Exception e) {
                LogUtils.logErrorInfo("Order_error",String.format("Get orderKey Exception! orderKey=%s, job=%s", orderKey, job.info()), e);
            }
        }
        return async(job, orderValue);
    } else {
        return async(job, null);
    }
}

// com.xiaojukeji.carrera.cproxy.actions.OrderAction#async
private Action.Status async(UpstreamJob job, Object orderValue) {
    // 设置保序依据
    if (orderValue != null) {
        job.setOrderId(orderValue.hashCode());
    }
    try {
        // 提交消息
        executor.submit(job);
        return Status.ASYNCHRONIZED;
    } catch (InterruptedException ignored) {
        Thread.currentThread().interrupt();
        return Status.FAIL;
    }
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobExecutorPool#submit
public void submit(UpstreamJob job) throws InterruptedException {
    // 注册消息完成时的回调
    job.registerJobFinishedCallback(this::onJobFinished);
    // 提交消息
    queue.submit(job);
    if (!useBackgroundThread) {
        queue.processNextMessage();
    }
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBlockingQueue#submit
public void submit(UpstreamJob job) throws InterruptedException {
    job.setState("Async.InMainQueue");
    jobSize.incrementAndGet();
    // 消息放入UpstreamJobBlockingQueue的mainQueue中
    mainQueue.add(job);
    // readyJobs是一个Semaphore，用于触发对mainQueue的处理
    readyJobs.release();
}

// ----------------------------
```

**代理端-处理消息**

```
// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobExecutorPool.WorkerThread#run
// DDMQ顺序消费-代理端处理消息
public void run() {
    LOGGER.info("Thread {} started.", getName());
    while (running) {
        // 线程不断拉取UpstreamJobBlockingQueue中的消息
        UpstreamJob job;
        try {
            // 这个queue是UpstreamJobBlockingQueue
            job = queue.poll();
        } catch (InterruptedException e) {
            LOGGER.info("worker thread {} is interrupted", getName());
            break;
        }
        assert job != null;
        activeThreadNumber.incrementAndGet();
        job.setWorkerId(workerId);
        try {
            // 消息处理，也就是上面的com.xiaojukeji.carrera.cproxy.consumer.UpstreamJob#execute
            // 也就是继续遍历Action
            job.execute();
        } catch (Exception e) {
            LogUtils.logErrorInfo("worker_running_error", "worker running error", e);
        }
        activeThreadNumber.decrementAndGet();
    }
    LOGGER.info("Thread {} finished. job after shutdown, group={}, queue.info={}",
            getName(), group, queue.info());
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBlockingQueue#poll
// 处理从Broker拉取到的消息
public UpstreamJob poll() throws InterruptedException {
    while (true) {
        // 等待唤醒
        readyJobs.acquire();
        // 处理消息
        UpstreamJob job = fetchJob();
        if (job != null) {
            return job;
        }
    }
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBlockingQueue#fetchJob
// 对mainQueue的处理
private UpstreamJob fetchJob() {
    // 优先取reActivationQueue中的消息，这个reActivationQueue是在消费结束后的回调中会放入当前顺序消息的下一个消息
    UpstreamJob job = reActivationQueue.poll();
    if (job != null) {
        putInWorkingQueue(job);
        return job;
    }
    ReentrantLock orderLock;
    Integer orderId;
    // mainQueue上锁
    mainQueueLock.lock();
    try {
        // 消费mainQueue中的消息
        job = mainQueue.poll();
        // 取出消息中的保序依据
        orderId = job.getOrderId();
        if (orderId == null) {
            // 若没有保序依据则为普通消费，直接返回，返回后会触发执行（com.xiaojukeji.carrera.cproxy.consumer.UpstreamJob#execute）
            if (LOGGER.isTraceEnabled()) {
                LOGGER.trace("job is out of mainQueue: job={}, no orderId", job.info());
            }
            // 这个workingQueue是仅用于日志的，可忽略不看
            putInWorkingQueue(job);
            return job;
        }
        // 若有保序依据则先上顺序锁
        orderLock = getLocks(orderId);
        orderLock.lock();
    } finally {
        // 释放mainQueue锁
        // 这里因为已经上了顺序锁了，所以可以释放掉mainQueue了
        // 目的是不阻塞后续其他线程对mainQueue的处理，这也就是前面甲乙二人打车例子实现的关键
        mainQueueLock.unlock();
    }
    
    try {
        // 根据保序依据取出排队链表(dependentJob有一个next字段来构成链表以代表顺序)，这里返回的是tail
        UpstreamJob dependentJob = jobOrderMap.putIfAbsent(orderId, job);
        if (dependentJob == null) {
            // 没有数据代表该消息此前的顺序消息没有或已被消费，直接返回
            if (LOGGER.isTraceEnabled()) {
                LOGGER.trace("job is out of mainQueue: job={}, no dependent job, orderId={}", job.info(), orderId);
            }
            putInWorkingQueue(job);
            return job;
        }
        
        // 非常重要的一步，对消息按序拼接，当前消息设为新的tail
        assert dependentJob.getNext() == null;
        dependentJob.setNextIfNull(job);
        
        if (LOGGER.isDebugEnabled()) {
            LOGGER.debug("job is out of mainQueue: job={}, enter jobOrderMap, orderId={}, dependent job={}", job.info(), orderId, dependentJob.info());
        }
        jobOrderMap.put(orderId, job);
    } finally {
        // 释放顺序锁
        orderLock.unlock();
    }
    
    return null;
}
```

**代理端-处理客户端拉取请求**

```
// com.xiaojukeji.carrera.cproxy.actions.PullServerBufferAction#act
// DDMQ客户端拉取消息-代理端
// 这里是上面execute会遍历到的一个Action
public Status act(UpstreamJob job) {
    job.setState("PullSvr.InBuffer");
    // 放入PullBuffer中
    buffer.offer(job);
    return Status.ASYNCHRONIZED;
}

// com.xiaojukeji.carrera.cproxy.actions.PullServerBufferAction#PullServerBufferAction
public PullServerBufferAction(ConsumerGroupConfig config) {
    this.config = config;
    // PullBuffer初始化
    buffer = ConsumerServiceImpl.getInstance().register(config);
}

// com.xiaojukeji.carrera.cproxy.server.ConsumerServiceImpl#register
public PullBuffer register(ConsumerGroupConfig config) {
    // PullBuffer会放入一个bufferMap中，key为消费者组
    PullBuffer buffer = bufferMap.computeIfAbsent(config.getGroup(), groupId -> {
        PullBuffer newBuffer = new PullBuffer(groupId, pullScheduler);
        pullScheduler.scheduleAtFixedRate(newBuffer::recoverTimeoutMessage, 2000, 100, TimeUnit.MILLISECONDS);
        pullScheduler.scheduleAtFixedRate(newBuffer::cleanWaitQueue, 2000, 5000, TimeUnit.MILLISECONDS);
        return newBuffer;
    });
    buffer.addClusterConfig(config);
    return buffer;
}

// com.xiaojukeji.carrera.cproxy.server.ConsumerServiceImpl#pull
// 该方法是最上面客户端代码中请求代理端拉取消息时，代理端的逻辑
public void pull(PullRequest request, AsyncMethodCallback resultHandler) {
    MetricUtils.incPullStatCount(request.getGroupId(), request.getTopic(), null, "request");
    
    String group = request.getGroupId();
    consumerManager.tryCreateConsumer(group);
    
    // 若客户端的请求参数中result非null，则代表客户端向代理端同步消费进度
    if (request.getResult() != null) {
        doSubmit(request.getResult());
    }
    
    Context context = new Context();
    context.setGroupId(request.getGroupId());
    context.setTopic(request.getTopic());
    
    // 根据消费者组从bufferMap中拉取消息返回，其中如果是广播消费，这里的groupId还会拼上具体客户端实例
    PullBuffer buffer = bufferMap.get(request.getGroupId());
    
    if (buffer == null) {
        responsePull(request, resultHandler, context, Collections.emptyList());
        return;
    }
   
    List<Message> messages = buffer.pull(context, request.maxBatchSize);
    
    if (CollectionUtils.isEmpty(messages)) {
        // ... 省略
    } else {
        // 返回message给客户端
        responsePull(request, resultHandler, context, messages);
    }
}

// com.xiaojukeji.carrera.cproxy.server.ConsumerServiceImpl#doSubmit
// 遍历处理客户端消费进度
private boolean doSubmit(ConsumeResult consumeResult) {
    LOGGER.debug("submit={},client={}", consumeResult, getClientAddress());
    // 遍历链表，这个链表是客户端拼接带来的
    for (ConsumeResult r = consumeResult; r != null; r = r.nextResult) {
        PullBuffer buffer = bufferMap.get(consumeResult.getContext().getGroupId());
        if (buffer == null) continue;
        // 处理消费结果
        buffer.processResult(r);
    }
    return true;
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBuffer#processResult
// 处理客户端消费结果
public synchronized List<Long> processResult(ConsumeResult result) {
    List<Long> nonExistsOffset = null;
    // 消费成功的
    if (CollectionUtils.isNotEmpty(result.getSuccessOffsets())) {
        for (Long offset : result.getSuccessOffsets()) {
            UpstreamJob job = workingJobs.remove(offset);
            if (job != null) {
                MetricUtils.qpsAndFilterMetric(job, MetricUtils.ConsumeResult.SUCCESS);
                MetricUtils.pullAckLatencyMetric(job, TimeUtils.getElapseTime(job.getPullTimestamp()));
                // 触发消息完结回调
                job.onFinished(true);  //success
            } else {
                if (nonExistsOffset == null) {
                    nonExistsOffset = new ArrayList<>();
                }
                nonExistsOffset.add(offset);
            }
        }
    }
    // 消费失败的
    if (CollectionUtils.isNotEmpty(result.getFailOffsets())) {
        for (Long offset : result.getFailOffsets()) {
            UpstreamJob job = workingJobs.remove(offset);
            if (job != null) {
                MetricUtils.pullAckLatencyMetric(job, TimeUtils.getElapseTime(job.getPullTimestamp()));
                int delay = job.nextRetryDelay();
                if (delay >= 0) {
                    scheduler.schedule(() -> this.offer(job), delay, TimeUnit.MILLISECONDS);
                } else {
                    // 这里dropJob也会触发消费完结的回调
                    dropJob(job);
                }
            } else {
                if (nonExistsOffset == null) {
                    nonExistsOffset = new ArrayList<>();
                }
                nonExistsOffset.add(offset);
            }
        }
    }
    return nonExistsOffset == null ? Collections.emptyList() : nonExistsOffset;
}

// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBuffer#dropJob
private void dropJob(UpstreamJob job) {
    MetricUtils.qpsAndFilterMetric(job, MetricUtils.ConsumeResult.FAILURE);
    LOGGER.warn("drop Job:{},errRetry={},retryIdx={}", job, job.getErrorRetryCnt(), job.getRetryIdx());
    DROP_LOGGER.info("beyondErrorRetry,job={},errRetry={},retryIdx={}",
        job, job.getErrorRetryCnt(), job.getRetryIdx());
    // 触发消息完结回调
    job.onFinished(true); //do not sendBack to rmq.
}
```

**代理端-消息完结回调**

客户端消费完结后， 触发代理端的回调，将顺序消息链表中的下一个消息放入queue中。

```
// com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBlockingQueue#onJobFinished
// DDMQ顺序消费-消费完结回调
public void onJobFinished(UpstreamJob job) {
    if (job == null) {
        LogUtils.logErrorInfo("JobFinished_error","onJobFinished error: job is null");
        return;
    }
    try {
        if (!removeWorkingQueue(job)) {
            LogUtils.logErrorInfo("remove_job_from_workingJobs","remove job from workingJobs failed, job={}", job.info());
        }
        Integer orderId = job.getOrderId();
        if (orderId != null) {
            // 根据保序依据上顺序锁
            ReentrantLock orderLock = getLocks(orderId);
            orderLock.lock();
            try {
                UpstreamJob nextJob = job.getNext();
                if (nextJob == null) {
                    // ... 省略
                } else {
                    if (LOGGER.isTraceEnabled()) {
                        LOGGER.trace("onJobFinished: job={}, orderId={}, size={}, has next:{}",
                                job.info(), orderId, getSize(), nextJob.info());
                    }
                    // 将链表中的下一个消息放入reActivationQueue
                    nextJob.setState("Async.InReActivationQueue");
                    reActivationQueue.offer(nextJob);
                    // 唤醒消息处理 (com.xiaojukeji.carrera.cproxy.actions.util.UpstreamJobBlockingQueue#fetchJob)
                    readyJobs.release();
                }
            } finally {
                orderLock.unlock();
            }
        } else {
            if (LOGGER.isTraceEnabled()) {
                LOGGER.trace("onJobFinished: job={}, size={}, no orderId.", job.info(), getSize());
            }
        }
    } finally {
        // 记录消费进度
        jobSize.decrementAndGet();
    }
}
```

**流程图梳理**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/ec29ed9b-00c4-4b39-8382-28cea9616354.png)

**思考一个问题**

为什么RocketMQ需要使用Broker端分布式锁加客户端本地线程锁来实现顺序消费，而DDMQ只需要代理端本地线程锁即可呢？

- 不需要Broker端分布式锁：因为代理端是单节点，不像RocketMQ中的Broker有主备及读写分离，所以代理端使用线程锁即可。
- 不需要客户端线程锁：因为客户端能够拉取到的消息，一定是无顺序关系的，所以也不需要加锁了。


![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/50d1f7dd-bb70-4476-a2e1-6104aa53e6a1.gif)

**RocketMQ与DDMQ顺序消费对比**

![图片](https://s.xinzhi-cdn.zone/user/66acedb068b6430eeafbea3d/689de96a47da9757c9a79436/43645dc4-9590-47ce-bb58-296e360e134b.png)

