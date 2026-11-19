# 2026-11-19 · Claude 当日实验读取说明

归档日期为 **2026 年 11 月 19 日**，时区为 **香港（UTC+8）**。本目录收录当天启动的 FLUX 实验；同批任务运行期间的新结果继续更新到该日期目录。

根目录为 `/root/autodl-tmp/flux-experiments/2026-11-19/`。先读 `DATA_LOCATION.md` 和 `live.json`，再按问题读取下表。

| 审阅问题 | 先读原记录 | 再看对照 |
|---|---|---|
| 同一个 rabbit 的两次提及落在哪里 | `02-simple-30/results/N04/tokens.json` 的 `template`、`groups`，以及 `03-bowl-interventions/head_mass.csv.gz` | N04、第一个去噪步、第 5 块 H22、词组 2 和 3。按每个种子分别计算 `mass_left / (mass_left + mass_right)` |
| 单独修 H22 是否改变伸爪者 | `03-bowl-interventions/orig__s{seed}.png` | 相同种子的 `route_L5H22__s{seed}.png`、`zero_L5H22__s{seed}.png` |
| 哪几块联合改变成图 | `03-bowl-interventions/refinement.json` 和 `guide-prompts.json` 中的 G1 | 同一种子的 `replicate`、`replicate_control`、`without_att_L{块号}`、`time_selected_steps12` 原图 |
| 作用来自路由还是值向量 | `source/bowl_factor_fp32.py` 和 `03-bowl-interventions/routing-values-fp32/results.json` | 每个种子均有 `base`、`copy`、`whole`、`R`、`V`、`T`、`RV`、`RT`、`VT`、`RVT` 原图。step1 是第一步，step12 是连续前两步 |
| 简单错误是否在复杂背景复现 | `04-cross-scene-150/prompts40.json`、`cross-score.json` | 按家族和随机种子配对，在 `results/C{家族}A/seed-{种子}/`、`results/C{家族}L/seed-{种子}/` 直接看原图和四步估计图 |
| 多轮是否沿用旧动作 | `05-multiturn-360/design.json` 和各编辑的 `complete.json` | 同一家族同一种子查看 `swap`、`swap_then_marble`、`undo`、`marble`、`marble_then_swap`、`combined`。每个条件保留 `trace.npz` 与 `trajectory.json` |
| Claude 新实验 | `06-similarity-distance/protocol.md`、`scripts/design.py`、`generation/` | `images/` 为原图，`judgments/` 为检测框、颜色判读和原回答，`summary.json` 为分子和分母，`passive/` 为逐层逐头记录。文件随阶段产生 |

代码和 CSV 的 `block_index`、`head_index`、`step_index` 从 0 开始；网页显示的全局块号和去噪步从 1 开始，H22 保持从 0 起算。读分开的 R/V/T 干预时使用 `routing-values-fp32/`。此前 `routing-values/` 是低精度重构诊断，用于追踪数值误差。选七块使用种子 2，种子 0、1 用于复测。

碗内粉色像素得分是颜色代理量。动作归属应看前腿是否与实体连续、是否伸至碗内以及另一实体的接触点。视觉模型自动评分、AI 直接看原图、独立人工盲审是三种不同来源。提示词优先引用存档原文，读数优先引用 CSV 或 JSON 的字段，干预结论注明种子、分母、对照和时间窗口。

## 重新设计的角色和接触实验

新实验位于 07-hypothesis-tests/error-panel/。先读 protocol.md 与 live.json。正式实验的原始提示词和参考图坐标在 mannequin-grid/full-contact/design.json，逐图判读在 mannequin-grid/full-contact/visual-readout.json，逐图自动盲评分在 mannequin-grid/full-contact/judgments/，四个去噪步的 32 块和 32 头紧凑记录在 mannequin-grid/full-contact/trace/样本编号/。碗的正反向新种子干预位于 causal-N04/，木人偶的参考图注意力干预位于 mannequin-grid/patch/。读数区分自动盲评分、AI 直接视觉判读和独立人工标注。
