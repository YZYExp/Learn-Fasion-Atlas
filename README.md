# 衣着有名：从风格识别到单品描述

给兴趣读者的一本中文图解入门书。既认识服饰风格，也学会把“蕾丝的、偏内衣的、运动的那种裙子”逐步说成具体单品、领袖、材料、长度与装饰，用于人物衣着描述、检索、生图和设计讨论。

## 阅读

从 [全书合并稿](book.md) 连续阅读，或按下面的分章目录阅读。只想先学会描述人物穿着，可先看 [单品细节分册](garment-details.md)，从第 13—22 章进入；不需要先掌握风格名。图片全部附在工程内，解压后请保留目录关系。主稿为 Markdown，不需要联网才能看自有配图；真实作品与资料链接需联网访问。

| 顺序 | 章节 | 读完能做什么 |
|---|---|---|
| 0 | [导读](chapters/00-reading.md) | 分开年代、社群与审美标签 |
| 1 | [先看衣服，再猜风格](chapters/01-observe.md) | 按廓形、比例、材料、结构与配饰观察 |
| 2 | [经典、学院与城市](chapters/02-classic.md) | 区别极简、Ivy、Preppy 与学院审美 |
| 3 | [浪漫、田园与轻甜](chapters/03-romantic.md) | 区别 Boho、森系、田园、Coquette 与芭蕾灵感 |
| 4 | [朋克、哥特与街头](chapters/04-street.md) | 根据衣装关系理解音乐与街头风格 |
| 5 | [工装、户外与机能](chapters/05-functional.md) | 说清功能灵感来自哪里 |
| 6 | [复古不是一个年代](chapters/06-retro.md) | 用腰线、体积与单品区分年代路径 |
| 7 | [洛丽塔、王子系与蒸汽朋克](chapters/07-lolita.md) | 避免把社群衣着和历史幻想混称 |
| 8 | [传统、改良与新表达](chapters/08-tradition.md) | 标明复原、改良与视觉借用 |
| 9 | [极繁、解构与雕塑](chapters/09-avant.md) | 把抽象设计感拆成具体方法 |
| 10 | [鞋、包、首饰与面料](chapters/10-accessories.md) | 用细节词完善表达 |
| 11 | [检索、生图、设计与讨论](chapters/11-express.md) | 组合提示词、brief 与验收要求 |
| 12 | [日系街头与未来幻想](chapters/12-street-future.md) | 区别 Decora、视觉系、Gyaru、City boy 与未来想象 |
| 13 | [连衣裙叫什么](chapters/13-dresses.md) | 分清吊带裙、衬裙式、衬衫裙、裹身裙、贴体裙与网球裙装 |
| 14 | [同样是半裙](chapters/14-skirts.md) | 用轮廓、褶、裁片与分层说清裙体 |
| 15 | [上衣与内层](chapters/15-tops-underwear.md) | 分清吊带背心、坦克背心、挂脖、Bustier、Corset、衬裙与连体衣 |
| 16 | [领口与袖子](chapters/16-necklines-sleeves.md) | 用局部形状说出一件衣服的区别 |
| 17 | [材料与表面](chapters/17-fabrics.md) | 区分蕾丝镶边、蕾丝拼接、带衬蕾丝、刺绣与网纱 |
| 18 | [裤子与外搭](chapters/18-trousers-outerwear.md) | 分开裤型、袋型、衣型与长度 |
| 19 | [抽褶、褶裥与波浪边](chapters/19-details.md) | 不再把不同处理都叫“褶皱” |
| 20 | [人物衣着描述工坊](chapters/20-description-workshop.md) | 用八槽方法、十句范例和三次改写练表达 |
| 21 | [汉服形制与证据](chapters/21-hanfu.md) | 褙子、三件套、马面裙及资料核查 |
| 22 | [Cosplay与角色服装](chapters/22-cosplay.md) | 结构分组、仙侠幻想与角色参考 |
| A | [双语索引](appendices/01-glossary.md) | 查 81 条术语与正文位置 |
| B | [12 组易混辨析](appendices/02-comparisons.md) | 快速找到可见区别与讨论说法 |
| C | [单品细节词表](appendices/03-garment-words.md) | 从模糊说法查具体名称与部位词 |

## 图片与资料

36 张实际生成的 AI 教学图板，共 210 个对照格，另有 1 张原创几何廓形图。第二部分新增 10 张图板、60 格，改用全身、局部、面料近景与平铺来观察单品细节。对照格包括服装、配饰、结构与设计方法，不能等同于 210 种互斥风格。各章明确说明图中选择及已知偏差。

图像生成采用内置 image_gen。第一部分完整提示词见 [images.json](references/images.json)，单品细节部分见 [detail-plan.json](references/detail-plan.json)，均对应实际图片；袖型图保留了定向修图提示。几何图生成脚本单独保留。历史与社群资料及真实案例就近引用，集中入口见 [sources.md](references/sources.md)。本书的观察方法、比较表和提示词示例为原创教学组织。

## 构建与检查

Python 3.10 或更新版本即可检查书稿并合并全书，无第三方依赖：

```bash
python3 scripts/build.py
python3 scripts/build.py --check
```

需要重新绘制 H/A/X 几何图时，额外安装 Pillow，再运行：

```bash
python3 -m pip install Pillow
python3 scripts/draw_silhouettes.py
```

如果自行安装 Pandoc，可在根目录运行以下命令生成自含图片的 HTML；本交付没有执行该命令，也不附 HTML 成品：

```bash
mkdir -p build
pandoc book.md --from=gfm --standalone --embed-resources --resource-path=. --toc --metadata lang=zh-CN -o build/book.html
```

本项目由 [YZYExp/Learn-Fasion-Atlas](https://github.com/YZYExp/Learn-Fasion-Atlas) 管理。第一个提交仅含空 README.md；后续分别提交完整源稿与阅读版 PDF。旧写作阶段与图像修订记录见 [CHANGELOG.md](CHANGELOG.md)，协作约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。

[下载完整PDF](output/pdf/fashion-atlas-expanded.pdf) · [汉服章节PDF](output/pdf/chapters/21-hanfu.pdf)（可从 output/pdf/chapters 查看全部章节）。

重新导出 PDF：

```bash
python3 -m pip install -r requirements.txt
export FASHION_ATLAS_FONT=/absolute/path/to/NotoSansSC-Regular.ttf
python3 scripts/export_pdf.py
python3 scripts/split_pdf.py
```

字体需为支持中文的 Noto Sans SC 常规字重 TTF；脚本也会检查项目 fonts/、用户字体目录和常见系统目录。PDF 文件已随仓库提交，可直接阅读。阅读版内嵌图片采用 JPEG 82 质量优化体积，原始 PNG 保存在 assets/images/；如需更高图片质量，可在导出前设置 FASHION_ATLAS_JPEG_QUALITY=94。中间渲染、缓存、HTML 和历史归档包不进入版本控制。

仓库内的分章稿为编辑源；更改后重跑构建，即可同步全书。范围、覆盖表与图片校验说明见 [PROJECT.md](PROJECT.md)。

## 一类多款增补

新增10张图板、60套造型：吊带裙、蕾丝裙、运动裙装、胸衣式上衣、衬衫、针织、A字半裙、短外套、洛丽塔裙装与都市剪裁。全身美型成年模特以亚洲面孔为主，兼顾不同背景、肤色与体型；地区倾向体现在衣物与搭配语境，不将长相和风格绑定。完整提示词见 [variation-plan.json](references/variation-plan.json)。

## 汉服与角色服装增补

- [第21章：汉服形制与证据](chapters/21-hanfu.md)
- [第22章：Cosplay与角色服装](chapters/22-cosplay.md)

新增5张图板（含2张三联结构观察图），汉服依据具体博物馆资料核查，历史衣装、当代搭配与幻想角色服装分清标注。图像记录见 [hanfu-cosplay-images.json](references/hanfu-cosplay-images.json)，逐项核查见 [structure-audit.md](references/structure-audit.md)。完整PDF及分章PDF由 scripts/export_pdf.py 与 scripts/split_pdf.py 生成。

## 在线首页

[衣着有名 · Fashion Atlas](https://yzy-fashion-atlas.giving-macaw-4424.chatgpt.site)（当前仅所有者可访问）。提供分类图鉴、完整在线章节、衣着描述练习与 PDF 下载。首页源码位于 `web/`。
