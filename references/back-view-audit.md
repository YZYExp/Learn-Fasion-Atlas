# 背视补充与审查索引的独立审校

范围：图67—70、第13／25／34／35章本轮增补，以及独立图片审查索引。审校日期：2026-10-23。此记录不作为书籍正文。

## 实际图片检查

四张源PNG均已逐张查看，而非只读提示词。

| 图 | 实际结构与分格 | 结论与边界 |
|---|---|---|
|67|两行两列；上行平行肩带裙正／背，下行交叉肩带裙正／背|正面轮廓与背片、接点可相互衔接；背交叉带未画成凭空悬浮。前后姿态、布面褶线和边缘高度有轻微漂移，只能作为近似配对示意，不是制版转面证据。|
|68|三行两列；U背、工字背、交叉背带依次正／背配对|工字背有中央衣料连接，明显区别于第三行X形交叉带；头发未遮住上背，覆盖与腰线大致连续。不能据此证明支撑、运动或防晒性能。|
|69|三行背面；无开衩、后中单开衩、后两侧双开衩|无开衩格下摆连续；单开衩格后中有真实可见边缘与开口；双开衩格两侧有开口、中央片连续。不是只给装饰线换标签。不能从图推开衩厘米数或具体内部做法。|
|70|三行两列正／背；衬衫、哈灵顿式夹克、风衣|后育克下中央褶、夹克弧形后育克、风衣横向覆片与腰带均可见。中央褶较窄，不把单条阴影当精确箱褶折叠方向证据；覆片下方未展示，不以图保证通风、防水。|

## 独立审查索引

已静态解析 `review/image-index.html`：

- 70张源PNG对应70个唯一图片卡片，文件名集合与assets/images完全相等。
- 70个内嵌WebP预览全部完整解码，未发现外部src或href依赖。
- 源PNG与网页WebP／缩略图归并在同一个卡片，不重复计图。
- 单文件当前约10MB；预览为有损WebP，页面明确提醒精确像素审查应回到原PNG与SHA-256。
- 索引脚本从book.json实际正文图片引用抽取章节、行号和图注，从现有制作记录摘录审图说明，不自动编造旧图的审校结论。

正文及最终构建排除检查将在整合完成后追加；浏览器交互由主代理负责验收。

## 文字、图注与原始出处

已通读第13／25／34／35章本轮差异，图注与实际分格顺序相符。第13章明确新正背对照并非旧图的精确转面；第25章给出选择背视的条件与同款核对方法；第34章把图中可见内容保守称为“中央褶”，不凭生成图断言箱褶折叠方向；第35章区分后中缝与开衩，没有从站姿图承诺活动量、合身或内部工艺。

以下原始页面已独立打开核查，相关事实有就近引用支持：

| 新增事实 | 核查的原始出处 | 审校结果 |
|---|---|---|
|吊带裙可有可调交叉背带|[Reformation Amani Dress](https://www.thereformation.com/products/amani-dress/1310787.html)|商品描述支持；不把具体商品版型套到所有吊带裙。|
|racerback与crisscross应分辨|[Nike Swoosh](https://www.nike.com/sg/t/swoosh-womens-medium-support-sports-bra-NDQZsv/899371-010)、[Nike One Strappy Back](https://www.nike.ae/en/one-strappy-back-womens-medium-support-lightly-lined-printed-sports-bra/NKFZ2914-010.html)|分别明确命名工字背与交叉带；配图68相应结构可见。|
|衬衫后育克与中央褶是不同观察项|[Ralph Lauren Oxford](https://www.ralphlauren.com.sg/stitch-your-own-mens-oxford-CYO0053AP.html)|实物页面明确split back yoke及box pleat；正文不把图70的窄褶当精确折法证明。|
|G9的umbrella back yoke|[Baracuta官方说明](https://support.baracuta.com/en-US/what-is-the-g9-327300)|支持术语与背部位置，正文未据图承诺性能。|
|风衣背部覆片与腰带|[Burberry Kensington](https://tr.burberry.com/mid-length-kensington-heritage-trench-coat-p81172291)|页面列storm shield at back与belt；图70能看见覆片及腰带。|
|无／单／双开衩的区别|[Indochino Vents](https://support.indochino.com/hc/en-us/articles/360044131754-What-are-Vents)|支持开衩定义与数量／位置；图69有真实开口边缘。|

图70定向修订后已重新实看。此次所审PNG的SHA-256为`7f33801a3e913d44d8f748ccc7733f9fa5f05054173050b890fdf2754b7a3461`。

## 索引排除检查与交接

已检索book.json、book.md、garment-details.md、全部chapters／appendices，以及当时public dist中的HTML／JSON／JS：未发现`review/image-index.html`或索引标题进入读者内容，public dist中未发现review目录或image-index文件。索引脚本需在最终章节整合后重跑，以刷新章节用途及图注；此项已提醒制作代理。

未解决的内容／图形阻塞：无。以下为整合后验收待办，未列为通过：

- 最终重新生成的全书PDF中再次确认没有索引标题／路径；本次看到的198页旧PDF不作为本轮新版验收证据。
- 主代理执行独立HTML的浏览器交互检查及最终发布内容检查。

本报告只覆盖上述明确列出的源图、文字、来源与静态索引检查，不代表全书旧图全部重新审校。

## 主线程交付检查

- 全书204页、男装分册36页及40份分章PDF已生成。重点渲染检查第51、57、115、153、157页，图像比例、图注和引用无溢出。
- 扫描全书PDF文字，未发现image-index.html或审查索引标题。
- 独立HTML浏览器测试通过：70张源图计数、搜索筛选、放大对话框与图片加载正常，无横向溢出。
- 网页检查通过46个阅读入口；主发布目录无review目录和image-index.html。
