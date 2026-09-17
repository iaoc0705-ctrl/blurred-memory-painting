const sharp = require("sharp");
const path = require("path");

const directory = __dirname;
const items = [
  ["01-last-ferry.png", "01 渡轮已经走远"],
  ["02-yellow-coat-field.png", "02 风把草都吹向一边"],
  ["03-pool-after-closing.png", "03 下午还留在池底"],
  ["04-kitchen-window.png", "04 天就这样暗了"],
  ["05-raincoat-edge.png", "05 他走出画面时"],
  ["06-chair-in-the-dawn.png", "06 外套还在等"],
];

const columns = 3;
const cellWidth = 440;
const cellHeight = 550;
const padding = 22;
const captionHeight = 30;
const headerHeight = 106;
const rows = Math.ceil(items.length / columns);
const width = padding + columns * (cellWidth + padding);
const height = headerHeight + rows * (cellHeight + captionHeight + padding) + padding;

async function main() {
  const composites = [
    {
      input: Buffer.from(`<svg width="${width}" height="${headerHeight}" xmlns="http://www.w3.org/2000/svg">
        <rect width="${width}" height="${headerHeight}" fill="#f6f4f0"/>
        <text x="${padding}" y="50" font-family="Segoe UI, Arial" font-size="30" font-weight="600" fill="#2b2823">朦胧记忆油画 · 当光还在</text>
        <text x="${padding}" y="80" font-family="Segoe UI, Arial" font-size="16" fill="#8a8378">$blurred-memory-painting v0.3.0 · 情绪钩子优先 · 六种未完成的瞬间</text>
      </svg>`),
      left: 0,
      top: 0,
    },
  ];

  for (let index = 0; index < items.length; index += 1) {
    const [filename, caption] = items[index];
    const row = Math.floor(index / columns);
    const column = index % columns;
    const left = padding + column * (cellWidth + padding);
    const top = headerHeight + row * (cellHeight + captionHeight + padding);
    const image = await sharp(path.join(directory, filename))
      .resize(cellWidth, cellHeight, { fit: "inside" })
      .toBuffer();
    const metadata = await sharp(image).metadata();
    composites.push({
      input: image,
      left: Math.round(left + (cellWidth - metadata.width) / 2),
      top: Math.round(top + (cellHeight - metadata.height) / 2),
    });
    composites.push({
      input: Buffer.from(`<svg width="${cellWidth}" height="${captionHeight}" xmlns="http://www.w3.org/2000/svg">
        <text x="0" y="20" font-family="Segoe UI, Arial" font-size="15" fill="#5f5a51">${caption}</text>
      </svg>`),
      left,
      top: top + cellHeight + 5,
    });
  }

  await sharp({
    create: { width, height, channels: 3, background: { r: 246, g: 244, b: 240 } },
  })
    .composite(composites)
    .jpeg({ quality: 90 })
    .toFile(path.join(directory, "contact-sheet.jpg"));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
