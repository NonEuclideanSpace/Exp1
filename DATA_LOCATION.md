# 2026-11-19 · FLUX 当日实验数据专区

归档日期为 **2026 年 11 月 19 日**，时区为 **香港（UTC+8）**。本目录收录当天启动的 FLUX 实验；同批任务运行期间的新结果继续更新到该日期目录。

AutoDL 数据盘总目录为 `/root/autodl-tmp/flux-experiments/2026-11-19/`。具备这台机器文件读取权限的 Claude 请先打开 `CLAUDE.md`，然后打开同目录下的 `live.json`。网页版 Claude 可直接读取 [GitHub 进度快照](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/data/machine-live.json) 和 [精选原始对照](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/review/evidence.md)。

| 相对位置 | 数据 |
|---|---|
| `01-initial-40/` | 30 个简单样本和 10 个 LongBench 样本，含完整提示词、原图和逐步记录 |
| `02-simple-30/` | 第二批简单样本，10 条提示词 × 3 个种子 |
| `03-bowl-interventions/` | 动作归属、H22、注意力与前馈干预、分步移植、逐块删减 |
| `03-bowl-interventions/routing-values-fp32/` | 相同种子与七块下，将图像注意力路由、图像值、文本贡献分开移植的原始输出 |
| `04-cross-scene-150/` | 10 个场景家族 × 3 个条件 × 5 个种子，含原图、词空间分布、逐头读数和残差 |
| `05-multiturn-360/` | 同一家族在简单和复杂条件下的编辑链。各编辑目录含输入来源、原图和内部追踪 |
| `06-similarity-distance/` | Claude 提出的相似度 × 距离实验，原方案为 `protocol.md`，图在 `images/`，逐图读数在 `judgments/`，分层内部追踪在 `passive/` |
| `07-hypothesis-tests/` | 十条猜想的补充试验，包括高噪声跨区响应、定向图像 V 干预、草图身份和连续编辑对照 |
| `source/` | 碗底干预和测量用的源代码 |
| `live.json` | 机器实时进度、最近更新时刻以及各类记录数量 |
| `CLAUDE.md` | 读取顺序、干预条件、原始字段和判读口径 |

网页版 Claude 可以通过 GitHub 的原图和结构化测量审阅。普通网页无法打开 AutoDL 的绝对路径，完整内部张量需要具有该实例文件权限的 Claude 读取。
