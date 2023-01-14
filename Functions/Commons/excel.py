# -*- coding:utf-8 -*-

from xlrd import open_workbook

#excel文件的初始化创建
def sheet_init(f):
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    sheet1.write(0, 0, "漏洞名称")
    sheet1.write(0, 1, "网址")
    sheet1.write(0, 2, "CNNVD编号")
    sheet1.write(0, 3, "危害等级")
    sheet1.write(0, 4, "CVE编号")
    sheet1.write(0, 5, "漏洞类型")
    sheet1.write(0, 6, "发布时间")
    sheet1.write(0, 7, "威胁类型")
    sheet1.write(0, 8, "更新时间")
    sheet1.write(0, 9, "厂商")
    sheet1.write(0, 10, "漏洞简介")
    sheet1.write(0, 11, "漏洞公告")
    sheet1.write(0, 12, "参考网址")
    sheet1.write(0, 13, "受影响实体")
    sheet1.write(0, 14, "补丁")
    return sheet1

def sheet_init_ms(f):
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
    sheet1.write(0, 0, "更新时间")
    sheet1.write(0, 1, "CVE编号")
    sheet1.write(0, 2, "CVE标题")
    sheet1.write(0, 3, "漏洞描述")
    sheet1.write(0, 4, "参考网址")
    sheet1.write(0, 5, "标签")
    return sheet1

# 创建获取excel数据的函数
def excel_sheet_processor(filepath):
    # 通过open_workbook函数 获取Book对象
    wb = open_workbook(filepath, formatting_info=True)
    # 创建一个新的sheet 对象
    ws = wb.sheet_by_index(0)
    # 创建2个空列表用于储存数据
    workbook_list = []
    my_keys = []
    # 通过遍历ncols 获取excel表中第一行（python中0是第一行的意思）和所有列的数据
    for col in range(ws.ncols):
        my_keys.append(ws.cell_value(rowx=0, colx=col))

    # 通过遍历nrows和 获取excel表中所有行里面的和对应列的数据
    for r in range(1,ws.nrows):
        dict = {}
        for pos in range(0, len(my_keys)):
            dict[my_keys[pos]] = ws.cell_value(rowx=r, colx=pos)
        # 将获取的字典数据  添加进一开始写好的空列表中
        workbook_list.append(dict)
    return workbook_list