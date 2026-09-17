# 照片改画

用户发来自己的照片并要求「画成这种风格 / 风格化 / 改成油画」时读本文件。

目标是两个条件同时成立：**本人还能认出这是我、这是当时的姿势和关系**；**陌生人看到的是一张不知道是谁的画**。只满足前者就是写实肖像，只满足后者就是一张无关的画。

## 与风格参考的分工

| 用户发来的东西 | 用户想要什么 | 走哪条路 |
| --- | --- | --- |
| 他自己的照片 | 改造这张照片 | 照片改画，即本文件 |
| 别人的画、截图、影视截图 | 提炼那种感觉 | 风格参考：只取调色、笔法、光位、留白与尺度，另画原创画面 |

分不清时看他想改造的对象是谁：说「把这张照片……」就是改画，说「参考这种风格……」就是风格参考。

## 第一步先看原图

用 `view_image` 看原照片，然后定三件事：

1. **主体是谁**：选一到两个人作为主体，优先有姿势张力、有距离关系、有光的那个。三人以上时收敛到一到两人，其余删掉或推到远景变成形状。
2. **哪些必须留**：见保留清单。
3. **哪些必须删**：见改写清单。

## 保留清单（让本人认得出）

- 人物数量、姿势、重心、动作方向——正在走、正在等、并肩、面对面
- 人物之间的关系与间距
- 构图骨架：人物在画面中的位置与大小比例、地平线或墙线的高度、主要透视方向
- 服装的颜色关系与块面。原照片本身若已有一处暖色，沿用它当焦点
- 一件关键道具的存在——行李箱、伞、狗、椅子、杯子，但简化为形状

## 改写清单（让它成为一段记忆）

- **媒介**　一律重画成布面油画：干笔拖扫、擦涂晕染、边缘化开、布纹可见、完成度不均匀。照片的像素感、镜头锐度与虚化都不能留。
- **面孔**　一律不给。能看清的脸、五官、表情、胡须、妆都化掉，用背侧、低头、转头、逆光、帽檐或阴影代替。
- **光线**　重做。默认逆光，人物受光面小于两成。原照片的室内平光、顶光、闪光灯都要换成低角度光、雾中漫射光，或唯一一盏灯、一扇窗。
- **环境**　删掉全部可读信息：招牌、指示牌、方向箭头、品牌、车辆标识、屏幕、手机、镜子、天花细节、踢脚线、玻璃反光里的建筑、人群。
- **空间可以换**　机场可以变站台、走廊、门口、岸边。只要保住「过道」的空间关系与光的来向，本人仍然认得出当时在做什么。
- **色彩**　压到低饱和粉质色域，但保留原照片中有叙事作用的暖色；不要为了“只留一处小暖色”抹掉衣物、夕阳或室内光带带来的记忆钩子。
- **留白**　把空墙、天空、雾、水面或地面扩大到足以承接情绪；人物可以推远或缩小，但不为了比例破坏原照片里有效的贴边、近景或偶然裁切。

## 提示词骨架（编辑版）

在 [prompt-patterns.md](prompt-patterns.md) 的通用骨架之上，编辑版必须多写三段：Input images 的角色声明、保留项、删除项。保留项与删除项要**逐项列名**，不能笼统写「简化背景」。

```text
Use case: style-transfer / photo-to-painting
Asset type: <preview / key art / 成品>
Input images: Image 1 is the edit target. Keep its composition skeleton - the <one> figure, his direction of travel, his stride, <the prop> he trails behind him, his position and scale within the frame, and the <colour> jacket as the one warm note. Everything else is to be re-painted and may be freely replaced.
Primary request: Repaint this as a quiet oil painting of <一件很普通的事>. He is seen from <behind and in three-quarter back view, mid-stride>; his head is turned away from us into the light, so his face is never readable - no features, no profile, no beard, no eye. <The prop> is simplified into a dark shape.
Style/medium: <布面油画、干笔、擦涂、边缘化开、布纹可见、完成度不均匀；是一段被画下来的记忆，不是照片>
Composition/framing: Keep the original aspect ratio and framing. <leave enough wall, ground, fog, water, or light for the memory to breathe>; <floor or horizon slightly high>; off-centre and unhurried. Do not enlarge empty space at the cost of an emotionally useful original crop.
Lighting/mood: <重做的光，通常逆光>; the figure reads mostly as a dark silhouette with its edges bitten away by light; quiet, distant, unresolved.
Color: <低饱和粉质色域>; the single warm accent in the whole image is <他外套的颜色／一盏灯>, drained toward rust and ochre.
Constraints: exactly <one> figure, no other people; remove all signage, wayfinding arrows, logos, brand marks, screens, phones, mirrors, ceiling detail, skirting trim, and glass reflections; no legible text; no readable face; no dated objects.
Avoid: <通用禁区>; beard or stubble detail; any element of the original photograph's background that carries information.
```

## 按原照片类型应对

| 原照片 | 风险 | 做法 |
| --- | --- | --- |
| 正脸大头照 | 没有姿势与距离，不给脸就等于没有内容 | 先告知这一构图只会变成侧影或背影，建议换一张有姿势、有距离、有光的照片；坚持要改就做成近景暗色块加大片背景，只留肩线与轮廓 |
| 两人合照 | 容易滑成写实双人肖像 | 保留间距与朝向，脸全部化掉，背景换成空场，用距离讲关系 |
| 三人以上或人群 | 违反「绝不出现人群」 | 收敛到一到两人做主体，其余删除或推到远景变成形状 |
| 背影照、侧身照 | 几乎没有风险，最合适 | 直接改画，重点放在光、空场与边缘化开的程度 |
| 风景或空景照 | 容易变成普通风景画 | 抽掉具体地点特征，扩大雾与光，可以补一个远景小人作尺度参照 |
| 光线平淡的室内照 | 画面会发灰、没有方向 | 给它发明一个光源——一扇窗、一盏灯、门外射进来的光带，并重做阴影方向 |
| 杂乱的街道、商店、家居照 | 可读信息删不完，画面会碎 | 只留空间骨架与一到两个大色块，其余整体替换成墙、雾、水面或地面 |
| 已失焦或翻拍的老照片 | 容易只是「加了一层滤镜」 | 不沿用原照片的模糊，按绘画语言重画边缘、笔触与布纹 |

## 修正句式（编辑专属）

- **还是太像照片**　追加绘画术语，删掉全部镜头术语；把「照片里有什么」的描述改成「怎么用笔画的」。
- **脸还是太清楚**　写明 turn the head away、face into the shadow、dissolve the features，并把人物在画面中的比例缩小。
- **原照片背景还在**　逐项点名要删除的物件，例如 signage、ceiling、skirting trim、mirror、phone，不要笼统说「简化背景」。
- **本人认不出来了**　恢复姿势、动作方向、间距与服装色块——这几项负责「这是谁」，脸不负责。
- **暖色焦点太橙太亮**　向赭黄与铁锈压，去掉橙红的高饱和；焦点面积不要扩大。
- **姿势被改了**　重申 keep the original stance, the direction of travel, and the relationship between the figures；生成模型倾向于「修正」它认为不自然的姿势。
- **构图被重排**　重申 keep the original aspect ratio and the figure's size and placement in the frame。

## 尺寸与画幅

- 沿用原照片的长宽比；人物站立的竖构图最稳。
- 常用 `1024x1280`（4:5）、`1024x1536`（2:3）、`1536x1024`（3:2）。
- 两条硬约束：边长是 16 的倍数，长宽比不超过 3:1。

## 执行

- 优先用内置 `image_gen` 的编辑能力，把原照片明确标为编辑目标，并把上面三段保留／删除声明写进请求。
- 当前环境没有内置图像工具时，用本 skill 的 `scripts/stylize_photo.py`（走 o10.top，读 `O10_API_KEY`）：

```powershell
python scripts/stylize_photo.py --image photo.jpg --prompt-file prompt.txt --output out.png --size 1024x1280
```

- 迭代规则与文生图一致：只出一张，只修硬伤。若第一版已经有情绪钩子，不要因为暖色偏多、空间偏满、地点变得暧昧或道具不够清楚而重新生成。修正时把保留项和情绪钩子再写一遍，防止上一轮已经对了的姿势、构图或调色被改掉。
- 生成后把成品复制到工作区或用户指定目录再交付，不要只留在默认输出位置。
