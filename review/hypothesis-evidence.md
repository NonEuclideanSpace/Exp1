# 高噪声响应、定向内容干预和草图对照

[十条猜想的操作定义](ten-predictions.md) · [机器数据位置](../DATA_LOCATION.md)

## N04 的七块注意力输出

行保持种子不变，列改变 V 的来源或接收区域。各条件均保留所在注意力计算的 QK 权重。用“粉色兔爪是否入碗”和“绿色猫爪是否留在沿上”两个读数判图。

|种子|基线|全图 V|只写兔与碗，来源不限|只读猫侧|只读匹配背景|只读自身|
|---|---|---|---|---|---|---|
|0|![pass](../media/hypothesis-tests/edge-pass-s0.png)|![full](../media/hypothesis-tests/edge-full-s0.png)|![full_target](../media/hypothesis-tests/edge-full_target-s0.png)|![cat](../media/hypothesis-tests/edge-cat-s0.png)|![bg](../media/hypothesis-tests/edge-bg-s0.png)|![self](../media/hypothesis-tests/edge-self-s0.png)|
|1|![pass](../media/hypothesis-tests/edge-pass-s1.png)|![full](../media/hypothesis-tests/edge-full-s1.png)|![full_target](../media/hypothesis-tests/edge-full_target-s1.png)|![cat](../media/hypothesis-tests/edge-cat-s1.png)|![bg](../media/hypothesis-tests/edge-bg-s1.png)|![self](../media/hypothesis-tests/edge-self-s1.png)|
|2|![pass](../media/hypothesis-tests/edge-pass-s2.png)|![full](../media/hypothesis-tests/edge-full-s2.png)|![full_target](../media/hypothesis-tests/edge-full_target-s2.png)|![cat](../media/hypothesis-tests/edge-cat-s2.png)|![bg](../media/hypothesis-tests/edge-bg-s2.png)|![self](../media/hypothesis-tests/edge-self-s2.png)|

[逐种子视觉读数](../data/hypothesis-tests/early-and-edge/visual-readout.json) · [第一、二步的有限差分原数据](../data/hypothesis-tests/early-and-edge/early-response.json)

## 同位置交换轮廓

下列图使用相同提示词和种子 0。完整盲评分包含种子 0–7。

|输入草图|模型成图|
|---|---|
|![](../media/hypothesis-tests/sketch-mg.png)|![](../media/hypothesis-tests/sketch-mg-s0.png)|
|![](../media/hypothesis-tests/sketch-gm.png)|![](../media/hypothesis-tests/sketch-gm-s0.png)|
|![](../media/hypothesis-tests/sketch-bbox.png)|![](../media/hypothesis-tests/sketch-bbox-s0.png)|

[草图条件全部原始读数](../data/hypothesis-tests/sketch/graded.json)

## 天鹅围巾筛选

依次为种子 8、9、10、11。评分来源和是否继续扩增见 JSON。

![种子 8](../media/hypothesis-tests/scarf-same-near-s8.png)
![种子 9](../media/hypothesis-tests/scarf-same-near-s9.png)
![种子 10](../media/hypothesis-tests/scarf-same-near-s10.png)
![种子 11](../media/hypothesis-tests/scarf-same-near-s11.png)

[四个固定种子的视觉标签与退出规则](../data/hypothesis-tests/scarf-screen.json)
