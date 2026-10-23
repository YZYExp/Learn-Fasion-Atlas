'use strict';
let atlas=[];
let filter='all',audience='all',query='';
const audienceWords={mens:'男装 男性',womens:'女装 女性',mixed:'中性 混合'};const gallery=document.getElementById('gallery');
function renderGallery(){
 const list=atlas.filter(x=>(filter==='all'||x.tag===filter)&&(audience==='all'||x.audience===audience)&&(`${x.title}${x.sub}${x.description}${audienceWords[x.audience]||''}`).toLowerCase().includes(query));
 gallery.replaceChildren();
 document.getElementById('gallery-count').textContent=`显示 ${list.length} / ${atlas.length} 组完整图板`;
 for(const item of list){
  const card=document.createElement('article');card.className='atlas-item'+(item.triptych?' triptych':'');
  card.innerHTML=`<button class="atlas-board" aria-label="放大查看${item.title}完整图组"><img src="assets/${item.id}.webp" alt="${item.title}：${item.count}，完整对照图组" width="${item.width}" height="${item.height}" loading="lazy" decoding="async"><span class="zoom-label">放大查看 ↗</span></button><span class="atlas-category">${item.label}</span><h3>${item.title}<small>${item.count}</small></h3><p>${item.sub}</p><a class="atlas-chapter" href="read.html?chapter=${item.chapter}">阅读对应章节 →</a>`;
  card.querySelector('.atlas-board').addEventListener('click',()=>openAtlas(item));gallery.append(card);
 }
 document.getElementById('no-results').classList.toggle('hidden',list.length>0);
}
function openAtlas(item){const d=document.getElementById('atlas-dialog');document.getElementById('dialog-kicker').textContent=item.label;document.getElementById('dialog-title').textContent=item.title;document.getElementById('dialog-description').textContent=item.description;const im=document.getElementById('dialog-image');im.src=`assets/${item.id}.webp`;im.alt=`${item.title}完整教学图组，${item.count}`;document.getElementById('dialog-chapter').href=`read.html?chapter=${item.chapter}`;d.showModal();d.scrollTop=0;document.body.style.overflow='hidden';}
function closeAtlas(){document.getElementById('atlas-dialog').close();document.body.style.overflow='';}
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;document.querySelectorAll('[data-filter]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b));});renderGallery();}));
document.querySelectorAll('[data-audience]').forEach(b=>b.addEventListener('click',()=>{audience=b.dataset.audience;document.querySelectorAll('[data-audience]').forEach(x=>{x.classList.toggle('active',x===b);x.setAttribute('aria-pressed',String(x===b));});renderGallery();}));
document.getElementById('atlas-search').addEventListener('input',e=>{query=e.target.value.trim().toLowerCase();renderGallery();});
document.querySelector('.close-dialog').addEventListener('click',closeAtlas);document.getElementById('atlas-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget)closeAtlas();});document.getElementById('atlas-dialog').addEventListener('close',()=>{document.body.style.overflow='';});
fetch('atlas.json?v=30ae7ce42a8c').then(r=>{if(!r.ok)throw new Error('atlas');return r.json();}).then(data=>{atlas=data;renderGallery();}).catch(()=>{const p=document.getElementById('no-results');p.textContent='图鉴暂时未载入，请刷新页面，或从章节目录阅读。';p.classList.remove('hidden');});
Promise.all([fetch('content.json?v=e494ac4f5cd6').then(r=>{if(!r.ok)throw new Error('content');return r.json();}),fetch('book-meta.json?v=519e02d2e6e9').then(r=>{if(!r.ok)throw new Error('meta');return r.json();})]).then(([chapters,meta])=>{
 const root=document.getElementById('chapter-groups');
 for(const group of meta.groups){
  const details=document.createElement('details');details.open=true;details.className='chapter-group';
  const summary=document.createElement('summary');summary.innerHTML=`<span class="group-number">${group.n}</span><h3></h3><span aria-hidden="true">−</span>`;summary.querySelector('h3').textContent=group.title;details.append(summary);details.addEventListener('toggle',()=>summary.lastElementChild.textContent=details.open?'−':'+');
  for(const c of chapters.filter(c=>group.ids.includes(c.id))){
   const a=document.createElement('a');a.className='chapter-row';a.href=`read.html?chapter=${c.id}`;const title=c.title.split('｜').slice(1).join('｜')||c.title;const number=c.kind==='appendix'?'↗':c.number===0?'序':String(c.number).padStart(2,'0');a.innerHTML=`<em>${number}</em><b></b><span aria-hidden="true">↗</span>`;a.querySelector('b').textContent=title;details.append(a);
  }
  root.append(details);
 }
}).catch(()=>{document.getElementById('chapter-groups').innerHTML='<p>章节暂时未载入，请刷新页面，或先下载完整 PDF 阅读。</p>';});

const presets={mensuit:{fields:[['外套',['藏蓝单排扣平驳领西装外套','深灰双排扣戗驳领西装外套']],['内搭',['白色翻领衬衫，配深蓝领带','米白圆领薄针织上衣']],['裤装',['中高腰灰色直筒长裤','同面料配套长裤']],['鞋履',['棕色德比鞋，裤脚轻触鞋面','黑色乐福鞋，裤脚停在鞋口附近']]],text:v=>`成年男性穿${v[0]}，肩线自然，衣身留有活动余量；内搭${v[1]}，下穿${v[2]}，配${v[3]}。`},menwork:{fields:[['外套',['橄榄色贴袋工装外套','靛蓝牛仔夹克']],['内搭',['米白圆领T恤','浅蓝扣领衬衫']],['裤装',['卡其色直筒奇诺裤','深蓝宽松直筒牛仔裤']],['鞋履',['棕色系带短靴','米白低帮运动鞋']]],text:v=>`成年男性穿${v[0]}敞开前襟，内搭${v[1]}；下穿${v[2]}，裤脚保持开放，配${v[3]}。双肩放松，一脚略向前，自然站立。`},slip:{fields:[['颜色',['墨蓝色','黑色','香槟色']],['领口',['浅V领','垂领']],['长度',['及踝','小腿中部']],['搭配',['外搭短款针织开衫','内搭白色T恤','配简洁低跟鞋']]],text:v=>`人物穿${v[0]}缎面细肩带吊带裙，${v[1]}带窄蕾丝饰边，裙长${v[2]}，裙身自然垂落；${v[3]}。`},sport:{fields:[['颜色',['白色','藏蓝色','鼠尾草绿']],['领口',['Polo领','半拉链领口']],['裙体',['膝上百褶裙摆','膝上A字裙摆']],['搭配',['搭配白色运动鞋','搭配短袜与运动鞋','外搭轻薄运动夹克']]],text:v=>`人物穿${v[0]}无袖运动连衣裙，上身采用${v[1]}，下部为${v[2]}；${v[3]}。`},mamian:{fields:[['裙色',['藏蓝色','深绿色','酒红色']],['上衣',['奶油色现代短夹克','白色棉质衬衫','黑色细针织上衣']],['装饰',['下部有横向纹样裙襕','采用低调素色面料']],['鞋履',['配低跟鞋','配平底鞋']]],text:v=>`人物穿${v[0]}马面裙，正面为平整裙门、两侧有密褶，${v[2]}；上配${v[1]}，${v[3]}。这是一套现代搭配。`}};
function buildFields(){const key=document.getElementById('preset').value;const p=presets[key];const root=document.getElementById('builder-fields');root.replaceChildren();for(const [label,values] of p.fields){const l=document.createElement('label');l.append(label);const select=document.createElement('select');for(const v of values){const o=document.createElement('option');o.value=v;o.textContent=v;select.append(o);}select.addEventListener('change',updateBrief);l.append(select);root.append(l);}updateBrief();}
function updateBrief(){const key=document.getElementById('preset').value;const vals=[...document.querySelectorAll('#builder-fields select')].map(s=>s.value);document.getElementById('brief-text').textContent=presets[key].text(vals);document.getElementById('copy-status').textContent='';}
document.getElementById('preset').addEventListener('change',buildFields);document.getElementById('copy-brief').addEventListener('click',async()=>{const text=document.getElementById('brief-text').textContent;try{await navigator.clipboard.writeText(text);document.getElementById('copy-status').textContent='已复制';}catch{const selection=window.getSelection();selection.removeAllRanges();const range=document.createRange();range.selectNodeContents(document.getElementById('brief-text'));selection.addRange(range);document.getElementById('copy-status').textContent='已选中文字，可手动复制';}});buildFields();
