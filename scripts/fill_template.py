# -*- coding: utf-8 -*-
"""素材清单模板填充：从模板复制并写入 ①E 列、②规格行，清空 ③指定图片列。
用法: python fill_template.py <模板.xlsx> <输出.xlsx> <fills.json>
fills.json: {"one": {行号: 值}, "specs": [[..列A..I..], ...]}
"""
import sys, json, openpyxl

def main():
    tpl, dst, fj = sys.argv[1], sys.argv[2], sys.argv[3]
    data = json.load(open(fj, encoding="utf-8"))
    wb = openpyxl.load_workbook(tpl)
    ws = wb["①素材清单"]
    for r, v in data.get("one", {}).items():
        ws.cell(int(r), 5).value = v
    ws2 = wb["②尺寸规格表"]
    for i, row in enumerate(data.get("specs", [])):
        for c, v in enumerate(row, start=1):
            ws2.cell(4+i, c).value = v
    for r in range(4+len(data.get("specs", [])), 14):
        for c in range(1, 10):
            ws2.cell(r, c).value = None
    ws3 = wb["③图片素材参考"]
    for r in range(4, ws3.max_row+1):
        ws3.cell(r, 5).value = None
    wb.save(dst)
    print("saved:", dst)

if __name__ == "__main__":
    main()