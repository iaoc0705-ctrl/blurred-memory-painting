const sharp = require("sharp");
const path = require("path");
const ex = process.argv[2];
const sd = process.argv[3];
const CW = 420, CH = 525, PAD = 24, CAP = 34, GAP = 28, TOP = 96;
const W = PAD + 2 * (CW + PAD);
const H = TOP + 3 * (CAP + CH + GAP) + PAD;
const rows = [
  { label: "海边防波堤（第一次测试）", a: path.join(ex, "01-waiting-at-the-water.png"), b: path.join(ex, "02-fog-dusk.png"), bIsCrop: false },
  { label: "雨后街道（本次系列第 4 张）", a: null, b: path.join(sd, "04-wet-street-leaving.png"), aCrop: { l: 22, t: 706, w: 440, h: 550 } },
  { label: "雾中岸边（本次系列第 5 张）", a: null, b: path.join(sd, "05-fog-quay-chair.png"), aCrop: { l: 484, t: 706, w: 440, h: 550 } },
];
const sheet = path.join(sd, "contact-sheet.jpg");
(async () => {
  const comps = [];
  comps.push({ input: Buffer.from(`<svg width="${W}" height="${TOP}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${W}" height="${TOP}" fill="#f6f4f0"/>
    <text x="${PAD}" y="42" font-family="Segoe UI, Arial" font-size="27" font-weight="600" fill="#2b2823">同一句话，两种取舍</text>
    <text x="${PAD}" y="70" font-family="Segoe UI, Arial" font-size="15" fill="#8a8378">左：第一版（你偏好的）　右：我按判断表"修正"后的</text>
  </svg>`), left: 0, top: 0 });
  const head = (t) => `<svg width="${CW}" height="${CAP}" xmlns="http://www.w3.org/2000/svg"><text x="0" y="22" font-family="Segoe UI, Arial" font-size="16" font-weight="600" fill="#5f5a51">${t}</text></svg>`;
  for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    const y0 = TOP + r * (CAP + CH + GAP);
    comps.push({ input: Buffer.from(head(row.label)), left: PAD, top: y0 - 26 });
    const cells = [
      { src: row.a, crop: row.aCrop, tag: "第一版" },
      { src: row.b, crop: null, tag: "我“修正”后" },
    ];
    for (let c = 0; c < 2; c++) {
      const x = PAD + c * (CW + PAD);
      const cell = cells[c];
      let buf;
      if (cell.src) buf = await sharp(cell.src).resize(CW, CH, { fit: "inside" }).toBuffer();
      else {
        const m = await sharp(sheet).metadata();
        const cr = cell.crop;
        buf = await sharp(sheet).extract({ left: cr.l, top: cr.t, width: Math.min(cr.w, m.width - cr.l), height: Math.min(cr.h, m.height - cr.t) })
          .resize(CW, CH, { fit: "inside" }).toBuffer();
      }
      const mm = await sharp(buf).metadata();
      comps.push({ input: buf, left: Math.round(x + (CW - mm.width) / 2), top: y0 + Math.round((CH - mm.height) / 2) });
      comps.push({ input: Buffer.from(`<svg width="${CW}" height="26" xmlns="http://www.w3.org/2000/svg"><text x="0" y="18" font-family="Segoe UI, Arial" font-size="14" fill="#8a8378">${cell.tag}</text></svg>`), left: x, top: y0 + CH + 2 });
    }
  }
  await sharp({ create: { width: W, height: H, channels: 3, background: { r: 246, g: 244, b: 240 } } })
    .composite(comps).jpeg({ quality: 90 }).toFile(path.join(sd, "before-after.jpg"));
  console.log("ok " + W + "x" + H);
})();