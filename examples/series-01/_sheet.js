const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const dir = process.argv[2];
const items = [
  ["01-snow-platform.png", "01 雪后站台 · 单人极小 · 单色"],
  ["02-field-two-walking.png", "02 原野并肩走远 · 两人 · 长影"],
  ["03-dark-room-table.png", "03 暗室桌边 · 单人 · 一盏灯"],
  ["04-wet-street-leaving.png", "04 雨后街道 · 走出画面 · 湿地面"],
  ["05-fog-quay-chair.png", "05 雾中岸边 · 空景 · 一把椅子"],
  ["06-close-dark-mass.png", "06 极近特写 · 只剩一团暗色块"],
];
const COLS = 3, CW = 440, CH = 550, PAD = 22, TOP = 104, CAP = 30;
const rows = Math.ceil(items.length / COLS);
const W = PAD + COLS * (CW + PAD);
const H = TOP + rows * (CH + CAP + PAD) + PAD;
(async () => {
  const comps = [];
  comps.push({ input: Buffer.from(`<svg width="${W}" height="${TOP}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${W}" height="${TOP}" fill="#f6f4f0"/>
    <text x="${PAD}" y="50" font-family="Segoe UI, Arial" font-size="30" font-weight="600" fill="#2b2823">朦胧记忆油画 · 系列一「过道与非结局」</text>
    <text x="${PAD}" y="80" font-family="Segoe UI, Arial" font-size="16" fill="#8a8378">$blurred-memory-painting v0.2.0 · 6 张 · 同一套调色板与光线性格，逐张更换地点、人数与天气</text>
  </svg>`), left: 0, top: 0 });
  for (let i = 0; i < items.length; i++) {
    const [file, cap] = items[i];
    const r = Math.floor(i / COLS), c = i % COLS;
    const x = PAD + c * (CW + PAD), y = TOP + r * (CH + CAP + PAD);
    const buf = await sharp(path.join(dir, file)).resize(CW, CH, { fit: "inside" }).toBuffer();
    const m = await sharp(buf).metadata();
    comps.push({ input: buf, left: Math.round(x + (CW - m.width) / 2), top: Math.round(y + (CH - m.height) / 2) });
    comps.push({ input: Buffer.from(`<svg width="${CW}" height="${CAP}" xmlns="http://www.w3.org/2000/svg"><text x="0" y="20" font-family="Segoe UI, Arial" font-size="15" fill="#5f5a51">${cap}</text></svg>`), left: x, top: y + CH + 6 });
  }
  await sharp({ create: { width: W, height: H, channels: 3, background: { r: 246, g: 244, b: 240 } } })
    .composite(comps).jpeg({ quality: 90 }).toFile(path.join(dir, "contact-sheet.jpg"));
  console.log("sheet " + W + "x" + H);
})();