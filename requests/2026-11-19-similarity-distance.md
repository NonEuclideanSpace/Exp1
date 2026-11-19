# 实验需求：相似度 × 距离

- 发起：2026-11-19
- 状态：待执行
- 模型：FLUX.2-klein-9b-kv，只用原模型，不加任何注意力修改、掩码或潜变量混合

## 1. 要验证的结论

**相似实体出错，是因为两个相似的实体在生成中会互相读取、彼此趋同。趋同的程度由两者有多像决定；离得近只会让趋同进一步变成融合，也就是少画一个人。这件事与先画谁、后画谁无关：同时画会趋同，先后画会照抄。**

拆成三点，每一点都由这个实验直接回答：

1. 串特征（两人衣服颜色对调或变成一样）多不多，由相似度决定，不由距离决定。
2. 少一个人只发生在既相似又靠近的时候。
3. 改成先画一个、再加一个，相似的那组不会变好，而是后画的照抄先画的。

作为对照，一男一女和一人一狗这两组，在两种画法、所有距离下都应该基本不出这两种错。

结论成立，说明问题出在这一对实体之间的互相影响，不在顺序，也不在单个实体。下一步就去量这种互相读取发生在哪些块、哪些头。结论不成立时，按第 6 节看是哪一点不成立。

## 2. 与仓库里已有数据的关系

- P01–P04 是陶瓷猫和陶瓷兔、颜色交叉互换，12/12 通过。不同类别的两个实体在没有接触时不串色，与第 4 条对照预测一致。这次补上的是同类实体和距离两个变量。
- N04 里，第 5 块 H22 把动作句中的 rabbit 定位到猫一侧（77.6%–80.9%）。这属于关系层面的错绑，对应第 9 节的可选实验。

## 3. 生成设置

- 分辨率：512×512，与本仓库已有实验一致，方便以后复用逐头重放和移植的工具。
- 步数：4 步，bfloat16。
- 文本编码：`text_encoder_out_layers=(9, 18, 27)`，`max_sequence_length=max(512, 实际长度)`。
- 随机数：`torch.Generator("cpu").manual_seed(seed)`，种子 0–7。
- 先后画的第二步：把第一步的结果作为参考图，传给同一管线的 `image=[...]`。

## 4. 自变量

### 相似度三档

A 固定在左边，B 在右边。

| | 描述 |
|---|---|
| A | `a woman in her thirties with shoulder-length black hair, wearing a {cL} jacket and dark jeans` |
| B，高 | `a woman in her thirties with shoulder-length black hair, wearing a {cR} jacket and dark jeans` |
| B，中 | `a man in his thirties with short black hair, wearing a {cR} jacket and dark jeans` |
| B，低 | `a large golden retriever wearing a {cR} dog jacket` |

### 距离四档（DIST）

| 档 | 句子 |
|---|---|
| 远 | `The two are far apart, at opposite edges of the frame.` |
| 近 | `The two stand about one meter apart.` |
| 贴 | `The two stand side by side, touching each other.` |
| 叠 | `The one on the right stands slightly behind the one on the left and is partly hidden by her.` |

### 颜色四种分配（cL, cR）

(red, blue)、(blue, red)、(green, yellow)、(yellow, green)

### 两种画法

**同时画：**

```
A full-body photograph taken on a quiet city sidewalk in daylight. On the left, {A}, standing and facing the camera. On the right, {B}, standing and facing the camera. {DIST}
```

**先后画，第一步：**

```
A full-body photograph taken on a quiet city sidewalk in daylight. On the left, {A}, standing and facing the camera. The right half of the frame shows only the empty sidewalk.
```

**先后画，第二步**（参考图为第一步结果）：

```
Add {B} on the right, standing and facing the camera. {DIST} Keep the woman on the left and the background unchanged.
```

### 数量

| 部分 | 计算 | 次数 |
|---|---|---|
| 同时画 | 3 档 × 4 档 × 4 种配色 × 8 个种子 | 384 |
| 先后画第一步 | 只取决于 cL 和种子，各档共用：4 × 8 | 32 |
| 先后画第二步 | 3 × 4 × 4 × 8 | 384 |
| 合计 | | 800 次生成 |

## 5. 评测

### 检测

- 用 GroundingDINO（grounding-dino-base），文本 `a person. a dog.`，box_threshold 0.35，text_threshold 0.25。
- 同类之间做 NMS（阈值 0.5），只保留高度超过画面 15% 的框。
- 机器上没有 GroundingDINO 时，用现成的人和狗检测器代替。无论用哪个，所有条件都用同一个。

### 人数是否正确

- 高、中两档：人 = 2，狗 = 0。
- 低档：人 = 1，狗 = 1。

### 颜色

只对人数正确的图做。

1. 按框中心的横坐标分出左右。
2. 裁剪：人取框高 25%–60% 的躯干段；狗取框高 30%–80%。
3. 用本地 Qwen3-VL-8B（温度 0）提问：

```
What color is the jacket in this image? Answer with exactly one word from: red, blue, green, yellow, other, mixed.
```

所有条件用同一个评测模型。

### 每张图的标签

| 标签 | 定义 |
|---|---|
| count_error | 人数不正确 |
| correct | 左 = cL，右 = cR |
| swap | 左 = cR，右 = cL |
| converge | 左右同色，且是 cL 或 cR 之一 |
| other | 其余情况 |

特征错误 = swap + converge。

### 实际距离

gap = (右框 x0 − 左框 x1) / 两框平均宽度，重叠时为负。

### 先后画另加两项

- copy：B 的颜色等于 cL。
- drift：A 在最终图里的颜色与第一步不同。

### 人工核对

每档相似度随机抽 20 张，共 60 张，人工标注人数和颜色，报告与自动标签的一致率。一致率低于 90% 时，先修评测，再看结果。

## 6. 判读

### 支持结论

- 两种画法下，高相似的特征错误都远高于中、低两档，且随距离变化不大。
- 人数错集中在高相似的"贴""叠"两格。
- 先后画时，高相似的 copy 明显高于中、低两档。
- 中、低两档在所有格里，两种错误都低。

### 不支持结论

- 三档相似度的特征错误相近：串色与相似度无关。
- 中、低两档在"贴""叠"时也频繁人数错：靠近本身就会融合。
- 先后画让高相似的特征错误明显下降：顺序本身有用。

## 7. 执行顺序

1. **冒烟**：高相似 × 贴 × (red, blue) × 8 个种子，两种画法都跑。确认提示词能稳定画出两个全身、面朝镜头的实体，评测能跑通。
2. **全量**：跑全部 800 次生成，然后评测、汇总、人工核对。

## 8. 结果放哪里

按本仓库现有的组织方式发布：

- 表格和逐图记录放 `data/sim-distance/`：
  - `records.jsonl`：每张最终图一行，字段包括画法、相似度、距离、颜色、种子、提示词、检测框、裁剪的回答、标签、gap、耗时；
  - `summary.csv`：按画法 × 相似度 × 距离分格，每格给出 n、count_error%、特征错误%（再分 swap%、converge%）、correct%、95% Wilson 区间、gap 中位数，先后画另加 copy%、drift%；
  - 人工核对的一致率。
- 图片放 `media/sim-distance/`：
  - 全部原图；
  - 每种画法两张曲线图，横轴是距离，三条线对应三档相似度，一张画特征错误，一张画人数错；
  - 样例拼图，取种子 0、红蓝配色，每种画法、每档相似度在四档距离上各一张。
- 跑完后，在本文件末尾追加"结果"一节：一段话说明三点结论各自是否成立，再附表格和图片的链接；同时把状态改成"已完成"。

## 9. 可选：关系（时间允许再做）

- 设置：距离固定为"近"，在 DIST 后加 `The one on the left hands a paper bag to the one on the right.`。三档相似度 × 4 种配色 × 8 个种子，只用同时画，共 96 张。
- 另问两题：
  - `Is the one on the left handing a paper bag to the one on the right? Answer yes or no.`
  - `Who is holding the paper bag: the left one, the right one, both, or neither?`
- 预测：高相似的一组更常出现袋子在错误的人手里、两人都拿着，或者动作做反。

## 10. 运行约束

- 用现有机器，不影响后台任务，不设自动关机，单个任务不超过 1 天。
- 实验脚本放在单独的目录。不新增 README，核心代码不写注释和文档字符串。
