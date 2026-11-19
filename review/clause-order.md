# 只交换两个动作句的顺序

固定两个同头形、近距离的木人偶。各动作的左右归属、所有文字、布局图、采样器和初始噪声相同，仅交换左、右动作句的先后。8 个种子，各做一次左侧触底和右侧触底。

右侧触底时，原句序下 0/8 张多出人偶；对调句序后 5/8 张多出人偶。左侧触底时，原句序下 2/8 张多出人偶；对调句序后 0/8 张多出人偶。此处的顺序指提示词句序。

[完整逐条件英文原句和交换后的原句](../data/hypothesis-tests/error-panel/clause-order/design.json) · [逐种子主体数和接触例子](../data/hypothesis-tests/error-panel/clause-order/visual-readout.json)

|条件|原句序|交换句序|
|---|---|---|
|high-near-right-bottom-s31|![](../media/hypothesis-tests/error-panel/clause-order/original-high-near-right-bottom-s31.png)|![](../media/hypothesis-tests/error-panel/clause-order/swapped-high-near-right-bottom-s31.png)|
|high-near-right-bottom-s33|![](../media/hypothesis-tests/error-panel/clause-order/original-high-near-right-bottom-s33.png)|![](../media/hypothesis-tests/error-panel/clause-order/swapped-high-near-right-bottom-s33.png)|
|high-near-left-bottom-s33|![](../media/hypothesis-tests/error-panel/clause-order/original-high-near-left-bottom-s33.png)|![](../media/hypothesis-tests/error-panel/clause-order/swapped-high-near-left-bottom-s33.png)|
|high-near-left-bottom-s35|![](../media/hypothesis-tests/error-panel/clause-order/original-high-near-left-bottom-s35.png)|![](../media/hypothesis-tests/error-panel/clause-order/swapped-high-near-left-bottom-s35.png)|
