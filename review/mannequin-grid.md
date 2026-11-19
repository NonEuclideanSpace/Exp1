# 木人偶指尖与盘底白点 · 正式配对实验

64 张有布局图的成图使用 8 个新种子。每个种子覆盖两种头形组合、两种肩距、两种角色方向。种子 31、32 同时做 16 张相同英文提示词、不输入布局图的对照。每张图逐项判断有没有指尖触到白点、触点是否属于指定人偶，以及有没有多出的白点、盘子或人偶。二维投影边缘相接而证据不足时保留待定。通过只代表这些观察项成立。

[全部 80 张逐图视觉记录](../data/hypothesis-tests/error-panel/confirmatory-visual.json) · [模型盲评原始回答](../data/hypothesis-tests/error-panel/confirmatory-blind.json) · [原提示词、种子、角色与布局配置](../data/hypothesis-tests/error-panel/confirmatory-design.json)

|条件|成图数|明确错|满足观察项|待定|
|---|---:|---:|---:|---:|
|全部有布局图|64|40|15|9|
|头形 high|32|21|7|4|
|头形 low|32|19|8|5|
|间距 far|32|23|4|5|
|间距 near|32|17|11|4|
|指定触底角色 left-bottom|32|26|1|5|
|指定触底角色 right-bottom|32|14|14|4|
|无布局图，两个匹配种子|16|6|10|0|

相同提示词和种子的 16 对中，有布局图时 16/16 明确错，无布局图时 6/16 明确错。布局可能同时影响构图、手的尺寸和目标可见性。

有布局图的 64 张中，32 张能看到指尖和白点之间的空隙。7 张在指尖下新增白点，原来位于盘中央的点仍空着。2 张多出一个人偶，其中一张也多出白点。同一张成图只算一次。

|对应成图|模型原图|
|---|---|
|high-near-right-bottom-s31|![](../media/hypothesis-tests/error-panel/grid/high-near-right-bottom-s31.png)|
|high-near-right-bottom-s31-text|![](../media/hypothesis-tests/error-panel/grid/high-near-right-bottom-s31-text.png)|
|high-near-left-bottom-s32|![](../media/hypothesis-tests/error-panel/grid/high-near-left-bottom-s32.png)|
|low-near-left-bottom-s32|![](../media/hypothesis-tests/error-panel/grid/low-near-left-bottom-s32.png)|
|high-near-right-bottom-s33|![](../media/hypothesis-tests/error-panel/grid/high-near-right-bottom-s33.png)|
|high-far-right-bottom-s33|![](../media/hypothesis-tests/error-panel/grid/high-far-right-bottom-s33.png)|
|high-near-left-bottom-s35|![](../media/hypothesis-tests/error-panel/grid/high-near-left-bottom-s35.png)|
|high-far-left-bottom-s35|![](../media/hypothesis-tests/error-panel/grid/high-far-left-bottom-s35.png)|
|high-near-right-bottom-s35|![](../media/hypothesis-tests/error-panel/grid/high-near-right-bottom-s35.png)|

[同一文字与噪声的四组正、反干预](mannequin-patch.md)

[只交换动作句顺序的成对原图](clause-order.md)
