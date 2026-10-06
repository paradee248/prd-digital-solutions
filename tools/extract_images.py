"""ดึงโลโก้ที่ฝังเป็น base64 ในไฟล์ index.html เดิม ออกมาเป็นไฟล์ .png
วิธีใช้:  python tools/extract_images.py path/to/index-เดิม.html
ผลลัพธ์จะอยู่ใน assets/img/ (logo-prd.png, logo-peashack.png, logo-prd-footer.png)
"""
import base64, pathlib, re, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
out.mkdir(parents=True, exist_ok=True)

# เก็บเฉพาะรูปที่ไม่ซ้ำ ตามลำดับที่เจอในไฟล์ (favicon กับโลโก้เมนูเป็นรูปเดียวกัน)
seen, images = set(), []
for b64 in re.findall(r'data:image/png;base64,([A-Za-z0-9+/=]+)', src):
    if b64 not in seen:
        seen.add(b64)
        images.append(b64)

names = ["logo-prd.png", "logo-peashack.png", "logo-prd-footer.png"]
for name, b64 in zip(names, images):
    (out / name).write_bytes(base64.b64decode(b64))
    print("saved", out / name)
if len(images) != len(names):
    print(f"หมายเหตุ: พบรูป {len(images)} รูป (คาดไว้ {len(names)}) ตรวจชื่อไฟล์อีกครั้ง")
