# 修订约定

1. 编辑chapters/和appendices/中的分章源稿，再运行python3 scripts/build.py同步合并稿。
2. 配图放入assets/images/，在references/的对应JSON记录提示词、用途和来源文件名。图像须进入正文。
3. 形制与历史陈述优先核查具体博物馆或学术来源；引用放在使用位置，结构无法判断时保留边界。
4. 检查模特四肢、手脚、重心与衣物衔接，同时保持自然姿态和单品结构清晰。
5. 修改PDF相关内容后重新导出、拆分并渲染受影响页面检查；一并提交相应PDF。
6. 以实际变化组织commit，提交前运行python3 scripts/build.py --check。不提交缓存、临时图、HTML和重复归档包。

首次提交只包含空README.md。此后提交不改写远端既有历史；书稿、配图及阅读版变化应能通过Git追踪。
