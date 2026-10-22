# 衣着有名 · Home Page

中文服饰图鉴的首页与在线读本。静态HTML/CSS/JavaScript，无外部运行时依赖。

- `dist/index.html`：图鉴首页、分类搜索、图组查看与描述练习。
- `dist/read.html`：22章正文、导读、附录和资料的在线阅读。
- `dist/content.json`：由分章Markdown构建的阅读内容。
- `dist/assets/`：由书稿配图压缩的WebP，不改变教学图的内容。
- `dist/fashion-atlas.pdf`：完整PDF下载。

源书仓库：https://github.com/YZYExp/Learn-Fasion-Atlas

内容更新时，将FASHION_ATLAS_SOURCE设为源书目录，运行`python3 build_content.py`。
