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

Markdown 为主稿，按章分文件；Git 管理，远端为 https://github.com/YZYExp/Learn-Fasion-Atlas.git。不生成 HTML 成品；README 提供用户自行构建命令。所有章节为完整正文，图像为实际文件；持续由构建脚本检查相对链接与文件完整性。

## 完稿状态

早期扩充版完成导读、20章正文、原81条索引及新增84条细节索引、12组风格辨析及10组模糊描述改写，原27项加新增20项资料入口。原书与新分册均有合并稿，全部插图已入正文。用户授权并行后，单品章节、附录、审读与生图独立推进，主线程统稿。最终本地链接、图像记录、归档完整性与Git状态通过检查后交付。

## 一类多款增补

新增10张六格图板（23–32），共60套造型；现有31张生成图板、186格及1张几何图。按相关主题插入第2、7、13、14、15、18章。亚洲读者视角、多元成年模特与区域搭配语境同时落实。提示词与生成记录见 references/variation-plan.json。

## 汉服与Cosplay增补

新增21、22章及5张图板：南宋褙子、明初三件套、马面裙现代搭配、Cosplay结构分组、仙侠幻想。汉服选具体馆藏文字与结构为依据，保留不能从生成图判断的项目；不标成精确复原。总22章正文、36张生成图板及1张几何图。

## 当前交付状态

22章正文、导读、3份附录、37张实际配图（36张生成图板及1张几何图），全书122页PDF、23份独立章节PDF。已包含马面裙人物自然站姿修订。仓库采用空README初始提交，源稿与PDF分次提交；阶段记录见CHANGELOG.md。
