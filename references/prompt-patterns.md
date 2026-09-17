# 提示词骨架、概念引擎与修正

在构思、写提示词或诊断结果为什么不像这个风格时读取。

## 概念引擎

从每一列各取一项，后一项必须能由前一项推出来，不要随机拼词。人物数量固定为一或二。

| 过道型地点 | 人物与朝向 | 扣留的信息 | 光 |
| --- | --- | --- | --- |
| 海边、防波堤 | 单人背影，占画面 1/6 至 1/3 | 他是谁、在等谁 | 低角度落日逆光，海面一条亮带 |
| 码头栏杆、湖边围栏 | 两人并肩、朝向一致 | 他们什么关系、要去哪里 | 黄昏漫射光，人物压成暗剪影 |
| 车站站台、候车长椅 | 单人侧背，身体微前倾 | 是否等到了 | 雾中平光，远处一点车灯 |
| 空旷街道、斑马线 | 单人正在走出画面 | 他刚才经历了什么 | 长长的地面投影与低角度光 |
| 原野边缘、大树下 | 两人一前一后，间距明显 | 有没有说出口 | 天空占三分之二以上的阴天 |
| 暗室窗边、吧台、桌旁 | 单人低头，只剩肩背轮廓 | 表情、年龄 | 室内唯一一盏暖灯或一扇窗 |
| 雾中的湖面、船坞 | 单人独立中景 | 地点名、季节 | 白雾吞掉远山，人物与背景同色 |
| 门口、台阶、走廊 | 单人半身入画，随时会走 | 结局 | 逆光门口，室内留大面积暗部 |

画幅默认略偏竖（3:4 或 4:5）；两人并肩或需要大范围地平线时才改横幅。单位面积内天空与水面越多，记忆感越强。

构图要点：地点负责建立普通感，光位负责建立时间感，扣留的信息负责建立记忆感。三者不要互相抢戏。

## 英文骨架

图像模型对英文提示词响应更稳，建议用英文生成、用中文与用户沟通。方括号内按概念替换。

```text
Use case: stylized-concept
Asset type: <preview / key art / editorial image / 系列图集第 N 张>
Primary request: A quiet painting of <one or two figures>, seen from <behind / three-quarter back / in shadow>, <doing something ordinary — waiting, walking away, standing at the water's edge, sitting at a table by a window>. Their face is never readable.
Input images: <Image 1...N are visual-language references only; do not reproduce their people, places, props, or composition.>
Style/medium: Original oil or acrylic on canvas, matte and chalky, dry-brush and scumbled strokes, lost and blurred edges where the figure dissolves into the ground, visible canvas weave, uneven finish — some passages resolved, others wiped down and left raw. A painted memory, not a photograph.
Composition/framing: <mid-distance figure, or an intentional close crop>; <give sky, water, wall, or open ground enough room for the memory to breathe>; off-centre and unhurried; horizon slightly high or low; light source behind the subject. Do not force empty space when a close crop, an edge exit, or a crowded fragment carries more emotional force.
Lighting/mood: <low backlit sun / sea fog / dusk / one lamp in a dark room>; the figure mostly in silhouette; quiet, distant, unresolved — the feeling of a moment remembered years later.
Color: chalk white, bone, grey-blue, olive, ochre, faded sepia, dusty rose; only one warm accent in the entire image — <a lit window / a yellow coat / the low sun>.
Constraints: face and identity withheld; one or two figures only, no crowd; no readable text, sign, logo, or signature; no clearly dated objects; a completely original subject and composition.
Avoid: photographic defocus, bokeh, lens blur, radial or gaussian blur, tilt-shift, digital airbrushing, smooth gradients, sharp facial features, high saturation, cinematic teal-and-orange grading, HDR, double-exposure ghosts, fantasy or horror atmosphere, a sepia filter over a photo, glossy varnish, crowds, staged emotion.
```

## 中文骨架

```text
用途：风格化概念图
画面请求：一张安静的小画。画中<一人/两人>，从<背后/四分之三背侧/阴影里>看过去，<正在做一件很普通的事——等待、走远、站在水边、坐在窗边的桌旁>。面孔始终不可辨认。
风格媒介：原创布面油画或丙烯，哑光粉质；干笔拖扫与擦涂晕染；人物边缘化开、融进背景；布纹可见；完成度不均匀，有的地方画实了，有的地方被擦掉重来。是一段被画下来的记忆，不是照片。
构图：<中远景、人物很小，或有意的近景裁切>；<天空、水面或空场给记忆留出呼吸的位置>；轻微偏心，地平线略高或略低；光源在人物背后。不要为了空场比例牺牲走出画面、贴边、近景暗块等更有力的偶然构图。
光线与氛围：<低角度逆光落日／海雾／黄昏／暗室里唯一一盏灯>；人物基本是剪影；安静、疏远、没有结局，像很多年后忽然想起的一个瞬间。
颜色：倾向骨白、石灰白、灰蓝、橄榄绿、赭黄、旧棕、尘玫瑰；保留一个服务于时间感的暖色钩子——<一扇亮着的窗／一件黄衣／落日／整段晚霞>，不把“只有一处小暖色”当成硬规则。
约束：不给面孔和身份；只有一到两个人，没有人群；不出现可读文字、招牌、标志、落款；不出现明确年代的道具；主体与构图完全原创。
避免：摄影虚焦、焦外光斑、镜头模糊、径向或高斯模糊、移轴、数字空气刷、平滑渐变、清晰五官、高饱和、青橙电影调色、HDR、双曝光幽灵、奇幻或恐怖氛围、照片叠棕褐色滤镜、清漆反光、人群、表演性情绪。
```

## 修正句式

先判断是硬伤还是软偏好。只修清晰脸、文字水印、照片滤镜感、数字平滑或完全读不懂的情境；不要因为落日、暖色面积、地点暧昧、道具不清或空场比例而重做。若修正，必须保留原图的情绪钩子、构图偶然性与叙事关系，只改造成硬伤的一个维度。

- **像加了模糊滤镜的照片**：删掉全部镜头术语（blur、defocus、bokeh、soft focus、depth of field、out of focus），换成 oil on canvas、dry brush drag、scumbled、lost edges、visible canvas weave、wiped down and repainted。把描述「看到什么」的字改成描述「怎么画的」的字。
- **面孔太清楚**：写明朝向与遮挡——back view、turned away、face hidden by a hat brim、head in shadow；同时把人物在画面中的比例缩小。
- **场景太具体、太现代**：删掉招牌、品牌、车辆、手机、时间线索，换成天气、地面、水面与空场。
- **不够记忆感**：减少画面里的信息量——去掉多余道具与第三人，把人物推远，扩大空场，让地平线偏移。
- **太甜、太伤感**：暖色只留一处，其余回到灰蓝与雾灰；把柔和黄昏换成平光或雾。
- **真的变成风景明信片**：只有在人物的未完成故事已经被景色完全盖住时，才削弱太阳或金光；保留能制造时间感的暖色，不要把画面一律改成灰雾。
- **太冷、丢了温柔**：加一处暖色光源或暖色地面，让距离里留一点温度；保持低对比但不全冷。
- **构图太工整、像摆拍**：轻微偏心，让前景的栏杆、树干或桌角挡掉一部分，视点处理成偶然抬眼看到的。
- **手和脸画得太实**：写明 hands are suggested with a brush stroke rather than detailed；把手放进暗部、衣褶或口袋里。
- **太像参考图**：换地点类别、人数、朝向、光位与天气，只保留调色与笔法。
- **出现文字或落款**：删除并可加入 no text, no signature, no watermark, no label。

## 系列（图集）模式

先固定一套，再逐张更换：

- **固定**：调色板（同一组色）、光线性格（同一时段的光）、人物尺度（同一个画面占比）、笔法松紧度、边缘化开的程度。
- **更换**：地点、人数与朝向、扣留的信息、天气、空场类型与情绪钩子；允许一张图偏离共同配色，成为整组里的记忆断片。
- **建议 6 至 18 张**，人物数量分布约为六成单人、三成半两人、一成空景（无人，只留天气和一件遗留物——一把椅子、一艘船、一条栏杆）。
- 每张必须能单独成立，不依赖前后顺序；连着看像一个记忆集，而不是同一天拍的一组照片。
- 图注只用一句话陈述画面里发生的事，不要解释含义，也不要写「她在等谁」这类反问来引导观众——留白由画面完成。
