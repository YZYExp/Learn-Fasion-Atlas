# Homepage and GitHub Pages

The website is published from `web/dist/`. Links are relative so the reader,
images and PDF work under the repository's GitHub Pages subpath.

The `Deploy GitHub Pages` workflow runs on pushes to `main`, pull requests,
and manual dispatch. It rebuilds online content from the book's Markdown,
regenerates undistorted thumbnail panels, checks resources, and uploads a
Pages artifact. Pull requests validate without deployment.

## One-time repository setup

In **Settings → Pages → Build and deployment**, select **GitHub Actions**.
This requires repository administration permission. Do not change repository
visibility to enable Pages. Private repositories need a plan that supports Pages.

## Local checks

From the repository root:

```sh
python -m pip install -r web/requirements.txt
python web/build_content.py
python web/build_thumbnails.py
node --check web/dist/app.js
node --check web/dist/reader.js
python web/check_site.py
```

The full PDF is copied from `output/pdf/fashion-atlas-expanded.pdf`; rebuild
that file separately when updating the downloadable book.

The gallery is generated from `web/atlas.json`; reading groups come from `book.json`. The image cache records source hashes, so content-only updates reuse verified WebP assets. Validation checks that every photographic plate has a gallery entry and every reading entry belongs to a group.

## 男装扩充与静态资源版本

图鉴使用 `audience` 区分 `mens`、`womens`、`mixed` 三种衣装展示方向，可与 `tag` 类目和搜索组合；不用于推断人物身份或限制穿着者。图板按实际可见内容归类，AI 示意的结构限制见正文图注。

构建时为脚本、样式、阅读数据和PDF下载计算内容指纹，避免新首页与旧脚本混用；同一输入重复构建保持相同版本。章节组从 book.json 派生，附录组序号紧接最后一部。
