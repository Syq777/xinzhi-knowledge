from pathlib import Path
import json,re,hashlib,shutil,html
root=Path(__file__).resolve().parent.parent; out=root/'dist'; source=root/'reader'
if out.exists(): shutil.rmtree(out)
(out/'articles').mkdir(parents=True)
for n in ('index.html','style.css','app.js'):shutil.copy2(source/n,out/n)
shutil.copy2(source/'node_modules/marked/marked.min.js',out/'marked.min.js')
shutil.copy2(source/'node_modules/dompurify/dist/purify.min.js',out/'purify.min.js')
records=[]
for folder in ('文章','Sandbox专题'):
 for p in sorted((root/'新枝'/folder).rglob('*.md')):
  if not p.is_file() or not p.name.startswith('🔗'): continue
  text=p.read_text(encoding='utf-8',errors='replace'); match=re.match(r'^---\s*\n(.*?)\n---\s*\n?',text,re.S); header=match.group(1) if match else ''; body=text[match.end():] if match else text
  def field(k):
   m=re.search(r'^'+re.escape(k)+r':\s*(.*)$',header,re.M);return html.unescape(m.group(1).strip().strip('"\'')) if m else ''
  rel=p.relative_to(root/'新枝'/folder); group=rel.parts[0] if len(rel.parts)>1 and not rel.parts[0].startswith('🔗') else '新收录'
  group=re.sub(r'^\d+_','',group).replace('_',' · ')
  if folder=='Sandbox专题': group='Sandbox 专题 · '+group
  title=re.sub(r'^🔗\s*·\s*','',p.stem); title=re.sub(r'\s+\d+$','',title)
  uid=hashlib.sha256(str(p.relative_to(root)).encode()).hexdigest()[:16]
  record={'id':uid,'title':title,'group':group,'source':field('原文链接'),'date':field('收藏时间'),'path':str(p.relative_to(root))}
  records.append(record);(out/'articles'/f'{uid}.json').write_text(json.dumps({'body':body},ensure_ascii=False),encoding='utf-8')
(out/'index.json').write_text(json.dumps(records,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
print(f'已生成 {len(records)} 份文章文件')
