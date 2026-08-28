# -*- coding: utf-8 -*-
"""场景图统一调成 3:4（1440×1920）：等比缩放+居中裁剪，禁止变形；Pillow 加底部小字。
用法: python scene_34.py <场景图路径> <输出路径>
"""
import sys
from PIL import Image, ImageDraw, ImageFont

def main():
    src, dst = sys.argv[1], sys.argv[2]
    W, H = 1440, 1920
    im = Image.open(src).convert("RGB")
    scale = max(W/im.width, H/im.height)
    im = im.resize((round(im.width*scale), round(im.height*scale)), Image.LANCZOS)
    l = (im.width-W)//2; t = (im.height-H)//2
    im = im.crop((l, t, l+W, t+H))
    font = ImageFont.truetype(r"D:\HuaweiMoveData\Users\HUAWEI\Documents\电商平台\品牌资料库\品牌字体\NotoSansSC-Regular.otf", 30)
    d = ImageDraw.Draw(im, "RGBA")
    d.rectangle([0, 1780, W, 1920], fill=(255,255,255,150))
    d.text((W//2, 1850), "场景实拍 ｜ 非卖品仅为搭配展示", font=font, fill=(90,70,90), anchor="ma")
    im.save(dst)
    print("场景 3:4", im.size)

if __name__ == "__main__":
    main()