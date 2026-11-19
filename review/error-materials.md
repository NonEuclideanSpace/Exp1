# 已逐图判读的初始错例

两批简单场景 28/60 张出现可见错误。首批 8/30，第二批 20/30。另有 LongBench 10/10。每张成图计一次，待定留在分母。以下沿用逐图判读原文。

[原英文提示词、全部 70 张判读和原图](../data/prior-samples.json) · [38 张错误的逐图记录和机器上的追踪目录](../data/error-materials.json) · [N04 同种子注意力干预](evidence.md)

|样本|种子|图中证据|模型原图|
|---|---:|---|---|
|P05|0|猫的前爪压在兔耳上，猫下巴停在耳边，兔背上接触的是猫胸腹。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P05-0.png)|
|P05|2|猫直坐在兔旁，猫脸碰到兔耳；猫下巴和兔背之间留有距离。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P05-2.png)|
|P06|0|兔的前肢搭在猫背上，下巴靠近猫耳。猫脚边还出现珊瑚粉色长尾状部件。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P06-0.png)|
|P06|1|兔坐在猫背上，前爪接触猫背；下巴位于猫耳旁并高于猫背。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P06-1.png)|
|P06|2|兔趴在猫背上，下巴接触猫头顶或耳根，前爪接触背部。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P06-2.png)|
|P09|0|猫旁清楚出现两朵红郁金香，提示词只要求一朵；黄色雏菊仍在兔侧。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P09-0.png)|
|P09|2|猫侧出现两朵红郁金香，兔侧出现两朵黄雏菊。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P09-2.png)|
|P10|2|兔嘴边有两朵红郁金香，超过要求的一朵；猫侧的单朵黄雏菊符合。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/P10-2.png)|
|L01|0|购物袋中的半个苹果被画到袋外，上方气球线附近出现完整苹果和香蕉皮。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L01-0.png)|
|L02|0|童鞋应倒扣在踏脚石上；画中童鞋鞋底朝下、鞋口向上。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L02-0.png)|
|L03|0|机械鸟应栖在窗台；成图把鸟放在右侧镜框前，左侧窗台上是蕨盆。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L03-0.png)|
|L04|0|倾斜书架内应漂着茶杯、镜子和沙漏。成图右侧书架立着书，沙漏移到了下方，茶杯漂在书架外。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L04-0.png)|
|L05|0|原文要求一把弯曲的叉子刺入牛奶杯。成图只见勺子插在杯中，叉子留在右侧餐巾上。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L05-0.png)|
|L06|0|原文中孩子出现在穿纱丽的女子身侧，猫落在悬浮的石块上。成图女子身侧没有孩子，猫悬在右上方。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L06-0.png)|
|L07|0|原文中有一只橡皮鸭浮在泥地浅水里；成图还在干地上多画了一只。渔网落到了围栏脚边。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L07-0.png)|
|L08|0|红保温壶应放在木箱堆顶。成图把壶放到电视机上，电视机在木箱上。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L08-0.png)|
|L09|0|无人机应悬停在水池附近，三脚架独立立在池中。成图将无人机和三脚架上下连接在一起。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L09-0.png)|
|L10|0|大蛾应在镜旁盘旋。成图中镜子位于左墙，而大蛾出现在右侧门边。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/L10-0.png)|
|N01|1|兔嘴接到围巾，但兔的颈部也出现一圈围巾。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N01-1.png)|
|N01|2|猫和兔都戴着围巾，兔颈可见完整围圈。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N01-2.png)|
|N02|0|兔戴围巾，猫嘴也接到末端，但猫脖子同时被围巾绕了一圈。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N02-0.png)|
|N02|1|围巾连接兔和猫，但猫颈上也有珊瑚色围圈。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N02-1.png)|
|N02|2|猫和兔各戴一条围巾，两条之间可见空隙。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N02-2.png)|
|N04|0|兔的前爪停在右侧碗沿，蓝色碗底空着。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N04-0.png)|
|N04|1|兔的前爪都在碗沿，没有一爪抵住内底。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N04-1.png)|
|N04|2|伸向碗底的是猫爪，兔爪仍在碗沿，角色与指令相反。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N04-2.png)|
|N05|1|兔端的金环扣在钥匙柄的孔上，钥匙齿端朝向猫嘴。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N05-1.png)|
|N06|2|带齿的蓝色钥匙尖向下悬空，连接金环的是从柄上横向伸出的另一段。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N06-2.png)|
|N07|0|猫抬爪搭在兔头顶，另一爪落地，兔下巴没有靠在落地的爪上。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N07-0.png)|
|N07|1|猫一爪抬到兔颈前，另一爪落在两者之间，兔下巴没有搭在地面猫爪上。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N07-1.png)|
|N07|2|猫抬爪托兔下巴，另一爪直落地面，缺少一爪搭背、另一爪在地上托下巴的组合。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N07-2.png)|
|N08|0|猫下巴靠在兔抬起的前爪旁，接触点远高于地面。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N08-0.png)|
|N08|1|兔一爪抬高托住猫下巴，另一爪落地，与指定的双爪动作不符。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N08-1.png)|
|N08|2|兔抬爪碰猫胸颈，另一爪在地面，与猫下巴之间有明显高度差。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N08-2.png)|
|N09|0|猫嘴咬花瓣，兔用前爪握茎，嘴没有接到茎端。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N09-0.png)|
|N09|2|猫嘴含绿色茎段；兔嘴张开与绿色茎端之间可见空隙。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N09-2.png)|
|N10|0|猫嘴接触花瓣，花茎经过兔爪伸向画外，未到猫嘴。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N10-0.png)|
|N10|1|猫仍在花瓣一侧，绿色花茎接到兔嘴，两端的角色颠倒。|[打开](https://raw.githubusercontent.com/NonEuclideanSpace/Exp1/main/articles/flux/prior-samples/N10-1.png)|
