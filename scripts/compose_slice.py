# -*- coding: utf-8 -*-
"""拼版 + 按模块切片。
用法: python compose_slice.py <产品文件夹> [模块PNG列表]
约定: 03_拼版/01_首屏.png ~ 10_底部备注.png（1440宽），切片按模块切（一个模块一张）。
最终切片统一输出 JPG；场景图切片必须小于 1000KB。
"""
import sys, os
from PIL import Image

SCENE_INDEX = 7
SCENE_MAX_BYTES = 1000 * 1024
SCENE_QUALITIES = (95, 92, 90, 88, 85, 82, 80, 78, 75, 72, 70, 68, 65, 62, 60)

def to_rgb(image):
    if "A" in image.getbands():
        rgba = image.convert("RGBA")
        canvas = Image.new("RGB", rgba.size, "white")
        canvas.paste(rgba, mask=rgba.getchannel("A"))
        return canvas
    return image.convert("RGB")

def save_jpeg(image, path, quality):
    to_rgb(image).save(path, "JPEG", quality=quality, optimize=True, subsampling=0)

def save_scene_jpeg(image, path):
    for quality in SCENE_QUALITIES:
        save_jpeg(image, path, quality)
        size = os.path.getsize(path)
        if size < SCENE_MAX_BYTES:
            return quality, size
    raise RuntimeError(f"场景图切片仍大于 1000KB：{path}")

def main():
    base = sys.argv[1]
    out = os.path.join(base, "详情页成品", "03_拼版")
    sli = os.path.join(base, "详情页成品", "04_切片")
    os.makedirs(out, exist_ok=True); os.makedirs(sli, exist_ok=True)
    files = ["01_首屏.png","02_品牌理念.png","03_卖点1.png","04_卖点2.png","05_卖点3.png",
             "06_细节实拍.png","07_场景大图.png","08_规格材质.png","09_洗涤护理.png","10_底部备注.png"]
    parts = [Image.open(os.path.join(out, f)) for f in files if os.path.exists(os.path.join(out, f))]
    if not parts:
        sys.exit("未找到模块图，请先拼好 03_拼版/*.png")
    W = 1440
    full = Image.new("RGB", (W, sum(p.height for p in parts)), (255,255,255))
    y = 0
    for p in parts:
        full.paste(p, (0, y)); y += p.height
    full.save(os.path.join(out, "详情页整页.png"))
    for f in os.listdir(sli):
        os.remove(os.path.join(sli, f))
    for i, p in enumerate(parts, start=1):
        dst = os.path.join(sli, f"详情页_{i:02d}.jpg")
        if i == SCENE_INDEX:
            quality, size = save_scene_jpeg(p, dst)
            print(f"场景切片: quality={quality}, size={size / 1024:.0f}KB")
        else:
            save_jpeg(p, dst, 90)
    print("整页", full.size, "切片", len(parts))

if __name__ == "__main__":
    main()