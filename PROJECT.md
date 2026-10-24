# 项目范围与完成记录

主题：《衣着有名：从风格识别到单品描述》。读者：非专业兴趣读者。目标：看图认识风格，并进一步说清人物身上的单品、领袖、材料、装饰与层次，用于检索、生图、设计与讨论。

## 分类覆盖

| 领域 | 正文 | 核心类别／方法 | 配图 |
|---|---|---|---|
| 入门 | 导读、1 | 名称层级；廓形、比例、材料、结构、配饰 | 08-avant |
| 经典城市 | 2 | Minimal、Smart casual、Ivy、Preppy、Dark/Light academia；Old money、法式、Clean fit 辨析 | 01-classic |
| 浪漫田园 | 3 | Romantic、Boho、Cottagecore、Mori kei、Coquette、Balletcore | 02-romantic |
| 音乐街头 | 4 | Punk、Goth、Grunge、Hip-hop、Skate、Biker | 03-subculture |
| 功能灵感 | 5 | Workwear、Military、Safari、Gorpcore、Techwear、Athleisure | 04-functional |
| 年代复古 | 6 | 1920s、1950s、Mod、Hippie、Disco、Y2K；Rococo、Regency、Bustle；Western、Nautical、Tweed chic | 05-retro、10-history |
| 社群与幻想 | 7 | Sweet/Classic/Gothic Lolita、Ouji、Victorian-inspired、Steampunk | 06-lolita |
| 传统与现代 | 8 | 汉服灵感、旗袍灵感、新中式、Kimono、Hanbok、Sari | 07-tradition |
| 设计方法 | 9 | Maximal、Deconstruction、Sculptural、Androgynous | 08-avant |
| 服饰品 | 10 | 鞋包、帽子、首饰、领袖门襟、材料词分层 | 09-accessories |
| 实践 | 11 | 6 条生图示例、brief、诊断与验收 | 前文章内对照 |
| 街头与未来延伸 | 12 | Decora、Visual kei、Gyaru、City boy、Cyberpunk、Space Age | 11-street-future |
| 查阅 | 附录 | 双语词表、易混比较 | 跳转正文 |
| 连衣裙与半裙 | 13—14 | Slip dress、蕾丝边、Shirt/Wrap/Bodycon/Tennis；A-line/Pencil/Pleated/Circle/Mermaid/Tiered | 13-dresses、14-skirts |
| 上衣与内层 | 15 | Camisole、Tank、Bustier top、Halter、Off-shoulder、Wrap；Bra/Bralette/Bustier/Corset/Slip/Bodysuit | 15-tops、16-underwear |
| 领口与袖型 | 16 | 六领口、六袖型；领口/领子/肩带、袖体/连接多维区分 | 17-necklines、18-sleeves-v2 |
| 织物表面与层次 | 17 | 缎面、蕾丝镶边/拼接/满幅加衬、刺绣、网纱罩层、罗纹 | 19-fabrics |
| 裤装与外搭 | 18 | 六裤型/袋型、六外搭；长度与单品分层 | 20-trousers、21-outerwear |
| 细节组织 | 19 | Ruching/Shirring/Ruffle/Flounce/Knife pleats/Drape | 22-details |
| 人物描述 | 20、附录C | 八槽描述、十句范例、三次改写；84条细节词与10组模糊说法改写 | 跳转单品近景与全身 |

## 插图制作与校验

首轮使用内置 image_gen 实际生成 21 张最终图板：前11张提示词在 references/images.json，后10张在 references/detail-plan.json；共126格，包含服装、配饰、设计方法与局部结构对照。另由 scripts/draw_silhouettes.py 绘制 H/A/X 几何示意。各图按教学对象采用全身、半身、裁片近景或衣物平铺，保持浅背景与英文短标签；图片已逐张查看。生成图共用教学排版语言，不把不同模特当严格同人实验。

已知视觉偏差并已就近注释：王子系裤长较长；Boho 腰带呈仿蛇纹表面；历史与传统衣装只作灵感示意，不把生成襟口、扣合、支撑作为复原证据。后续用于实物制作需以结构图与可靠参考另行核查。

新增图文核对：内层图Corset明确为underbust，并补全胸式辨析；网球裙明确为膝上短款与拉链式门襟；领口图High neck带短竖领，图注与无领例句分开；材料图明确浅蓝衬里与彩色刺绣；裤装图不声称统一裤长。Dolman格原弧形接缝会干扰袖型教学，已定向修图并采用18-sleeves-v2，保留修图提示；Ruffle/Flounce连接边与Shirring外观已核对。

## 工程约定

Markdown 为主稿，按章分文件；Git 管理，远端为 https://github.com/YZYExp/Learn-Fasion-Atlas.git。已按用户要求提供 GitHub Pages 主页与逐章阅读；网页与 PDF 共用分章 Markdown，网页 CI 不运行 PDF 排版。README 保留自行构建命令。所有章节为完整正文，图像为实际文件；持续由构建脚本检查相对链接与文件完整性。

## 完稿状态

早期扩充版完成导读、20章正文、原81条索引及新增84条细节索引、12组风格辨析及10组模糊描述改写，原27项加新增20项资料入口。原书与新分册均有合并稿，全部插图已入正文。用户授权并行后，单品章节、附录、审读与生图独立推进，主线程统稿。最终本地链接、图像记录、归档完整性与Git状态通过检查后交付。

## 一类多款增补

新增10张六格图板（23–32），共60套造型；现有31张生成图板、186格及1张几何图。按相关主题插入第2、7、13、14、15、18章。亚洲读者视角、多元成年模特与区域搭配语境同时落实。提示词与生成记录见 references/variation-plan.json。

## 汉服与Cosplay增补

新增21、22章及5张图板：南宋褙子、明初三件套、马面裙现代搭配、Cosplay结构分组、仙侠幻想。汉服选具体馆藏文字与结构为依据，保留不能从生成图判断的项目；不标成精确复原。总22章正文、36张生成图板及1张几何图。

## 汉服轮次交付状态（历史）

22章正文、导读、3份附录、37张实际配图（36张生成图板及1张几何图），全书122页PDF、23份独立章节PDF。已包含马面裙人物自然站姿修订。仓库采用空README初始提交，源稿与PDF分次提交；阶段记录见CHANGELOG.md。

## 辨识进阶扩展（本轮）

新增第23—28章，8张图板（38—45）。共28章正文、导读、3篇附录与45张实际配图。扩展分工见references/expansion-plan.md；统一章节清单为book.json。网页复用分章稿与原图，默认展开完整图板，新增鞋袜包袋筛选。历史数量记录保留以说明各轮变化；当前数量以清单和PDF元数据为准。

## 分类与描述扩充完成

新增29—31章、附录D与5张图板（46—50），现为31章正文、导读、4篇附录与50张实际配图。图鉴覆盖全部49张摄影教学图板，几何轮廓图保留在方法章节；不将未生成内容或提示词计为完成。全书审校修正导读范围、领口/领子层次和静态纹理推断弹性。网页阅读分组从book.json派生，图鉴从web/atlas.json派生；网页构建只处理变更图源，不运行整书排版。

## 男装系统扩充交付（历史阶段）

当前为39章正文、导读、5篇附录、66张实际配图（65组摄影图板与1张几何轮廓图），全书PDF198页。新增32—39章从上装、裤装、外套、西装晚礼服走到版型、鞋饰、风格与场景；图51—66全部实际生成、入正文、图鉴与PDF。新增男装检索附录E及男性服饰PDF分册。

网页新增男装／女装／中性或混合示例方向筛选，与原有单品／风格分类和搜索组合；男装方向16组，女装32组，混合／共通17组。分类说明衣装展示内容，不推断人物身份或限制穿着者。封面和首页同时展示男装与女装。

16张图由三组并行制作，8章由两组并行撰写，独立审校核对所有实际图、primary sources、术语与图文映射。修订详情和限制见references/menswear-audit.md及menswear-images-*.json。原始PNG保留，PDF在比例不变的前提下缩至适合屏幕阅读的嵌入尺寸。

## 选择性背视补充与当前交付

2026-10-23：保留39章正文、导读和5篇附录，配图增至70张（69组摄影图板、1张几何图）。新增67—70四组图：吊带裙前后配对、运动上装背部连接、西装后摆开衩、衬衫和外套背面细节；分别进入第13、34、35章，第25章补充描述方法。只补需要背面解释的对象，不推断旧正面图的隐藏结构。全书PDF204页，男装分册36页。

独立审查文件review/image-index.html收录全部70张源图，嵌入离线预览并记录章节、图注、源文件SHA256、派生图和审图备注，可搜索与放大。它进入Git管理，但不进入书稿、PDF或公开阅读站点；构建检查防止误入。生成命令为python scripts/build_image_index.py。四组实际图、结构术语、来源与PDF重点页已审查；详见references/back-view-audit.md。

## 背部开口与闭合补充（当前）

2026-10-23继续：新增71/72两张图板至第25章，先查重再并行生图与核源；挂脖/无肩带/后领开孔用同款正背图，拉链/纽扣/系带用整衣与近景。图72两次修订后纽扣与孔眼数量一致；制作记录与实际章节映射已校正。该轮完成时为39章正文、72张源图、208页全书与36页男装分册，40份分章PDF。审查索引72图全覆盖，含修图提示词，独立于正文和网页发布。

## 2026-10-24 多维分类修订完成

19张扩展卡入书，采用16张上传原图和3张内置image_gen定向编辑图；原72图保留，总91张。17个相关章节扩充教学解释；19张新增图逐张审查并记录限制。面料成分与组织不可由模拟图鉴定；现代汉服组件卡撤销无证历史定名；细节卡纠正分割缝、侧缝袋与包边。

审校记录：review/classification-audit-2026-10-24.md；入书映射：references/expanded-card-manifest-2026-10-24.json；来源和重绘提示词：references/expanded-card-review.json。最终使用版位于assets/images/，审图索引仍不进入在线目录。
