
import os
import xml.dom.minidom
import xlrd
import xlsxwriter

def write_xml(folder: str, img_name: str, path: str, img_width: int, img_height: int, tag_num: int, tag_name: str,
              box_list: list):

    doc = xml.dom.minidom.Document()

    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)

    #
    folder_node = doc.createElement("folder")
    folder_value = doc.createTextNode(folder)
    folder_node.appendChild(folder_value)
    root_node.appendChild(folder_node)

    filename_node = doc.createElement("filename")
    filename_value = doc.createTextNode(img_name)
    filename_node.appendChild(filename_value)
    root_node.appendChild(filename_node)

    path_node = doc.createElement("path")
    path_value = doc.createTextNode(path)
    path_node.appendChild(path_value)
    root_node.appendChild(path_node)

    source_node = doc.createElement("source")
    database_node = doc.createElement("database")
    database_node.appendChild(doc.createTextNode("Unknown"))
    source_node.appendChild(database_node)
    root_node.appendChild(source_node)

    size_node = doc.createElement("size")
    for item, value in zip(["width", "height", "depth"], [img_width, img_height, 3]):
        elem = doc.createElement(item)
        elem.appendChild(doc.createTextNode(str(value)))
        size_node.appendChild(elem)
    root_node.appendChild(size_node)

    seg_node = doc.createElement("segmented")
    seg_node.appendChild(doc.createTextNode(str(0)))
    root_node.appendChild(seg_node)

    for i in range(tag_num):
        obj_node = doc.createElement("object")
        name_node = doc.createElement("name")
        name_node.appendChild(doc.createTextNode(tag_name))
        obj_node.appendChild(name_node)

        pose_node = doc.createElement("pose")
        pose_node.appendChild(doc.createTextNode("Unspecified"))
        obj_node.appendChild(pose_node)

        trun_node = doc.createElement("truncated")
        trun_node.appendChild(doc.createTextNode(str(0)))
        obj_node.appendChild(trun_node)

        trun_node = doc.createElement("difficult")
        trun_node.appendChild(doc.createTextNode(str(0)))
        obj_node.appendChild(trun_node)

        bndbox_node = doc.createElement("bndbox")
        for item, value in zip(["xmin", "ymin", "xmax", "ymax"], box_list[i]):
            elem = doc.createElement(item)
            elem.appendChild(doc.createTextNode(str(value)))
            bndbox_node.appendChild(elem)
        obj_node.appendChild(bndbox_node)
        root_node.appendChild(obj_node)

    with open(img_name[:-4] + ".xml", "w", encoding="utf-8") as f:
        doc.writexml(f, indent='', addindent='\t', newl='\n', encoding="utf-8")



if __name__ == '__main__':

    path='M:/Upload/Sequence_1/_2022-04-25-14-11-40/D435i/'  #   Storage directory for MOT files
    with open(path+'MOT.txt', 'r') as f:
        lines = f.readlines()

    # Create intermediate temporary files
    workbook = xlsxwriter.Workbook(path+'temp.xlsx')  # 创建一个excel文件
    worksheet = workbook.add_worksheet('1')
    k = 0
    L = 0
    j = 0
    for i in range(len(lines)):
        if i == 0:
            name_last = lines[i].split(',')[0]
        picture_name = lines[i].split(',')[0]
        print(int(lines[i].split(',')[2]), int(lines[i].split(',')[3]), int(lines[i].split(',')[4]),
              int(lines[i].split(',')[5]))
        if picture_name == name_last:
            L = L + 1
            worksheet.write(k, 0, picture_name)  #
            worksheet.write(k, 1, L)  #
            worksheet.write(k, 2, 4)  #
            worksheet.write(k, 3 + j * 4, int(lines[i].split(',')[2]))  #
            worksheet.write(k, 4 + j * 4, int(lines[i].split(',')[3]))  #
            worksheet.write(k, 5 + j * 4, int(lines[i].split(',')[4]))  #
            worksheet.write(k, 6 + j * 4, int(lines[i].split(',')[5]))  #
            j = j + 1
        else:
            L = 0
            j = 0
            k = k + 1
            name_last = lines[i].split(',')[0]
            worksheet.write(k, 0, picture_name)  # 第1行第1列（即A1）写入
            worksheet.write(k, 1, L)  # 第1行第1列（即A1）写入
            worksheet.write(k, 2, 4)  # 第1行第1列（即A1）写入
            worksheet.write(k, 3 + j * 4, int(lines[i].split(',')[2]))  # 第1行第1列（即A1）写入
            worksheet.write(k, 4 + j * 4, int(lines[i].split(',')[3]))  # 第1行第1列（即A1）写入
            worksheet.write(k, 5 + j * 4, int(lines[i].split(',')[4]))  # 第1行第1列（即A1）写入
            worksheet.write(k, 6 + j * 4, int(lines[i].split(',')[5]))  # 第1行第1列（即A1）写入
            j = j + 1
            L = L + 1
    workbook.close()

    # Create VOC annotation file
    data = xlrd.open_workbook(path+'temp.xlsx')
    table = data.sheets()[0]
    sheet = data.sheet_by_index(0)
    table_list_img_name = table.col_values(colx=0, start_rowx=0,end_rowx=None)  #
    table_list_number_rectangle = table.col_values(colx=1, start_rowx=0,end_rowx=None)  #

    image_high = 1280
    image_width = 720

    img_name=[]
    number_rectangle = []
    value=[[]]
    for i in range(len(table_list_img_name)):
        img_name.append(table_list_img_name[i].split('\\')[-1])
        number_rectangle.append(int(table_list_number_rectangle[i]))
        for j in range(number_rectangle[i]):
            value.append([])
            xmin=int(sheet.cell_value(i, 3 + j * 4))
            if xmin<0:
                xmin=0
            if xmin>image_width:
                xmin=image_width
            ymin=int(sheet.cell_value(i, 4 + j * 4))
            if ymin<0:
                ymin=0
            if ymin>image_high:
                ymin=image_high
            xmax=int(sheet.cell_value(i, 3 + j * 4))+int(sheet.cell_value(i, 5 + j * 4))
            if xmax<0:
                xmax=0
            if xmax>image_width:
                xmax=image_width
            ymax=int(sheet.cell_value(i, 4 + j * 4))+int(sheet.cell_value(i, 6 + j * 4))
            if ymax<0:
                ymax=0
            if ymax>image_high:
                ymax=image_high
            value[i].append([xmin,ymin ,xmax ,ymax])


    # Note: The generated XML file is saved in the current directory
    for k in range(len(table_list_img_name)):
        write_xml(folder=path, img_name=img_name[k],
                  path=path, img_width=image_width, img_height=image_high, tag_num=number_rectangle[k],
                  tag_name='lettuce', box_list=value[k])
        print(value[k])


