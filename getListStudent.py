import xlrd
import json

loc = ("data/ds.xlsx")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
 
def getListSTD():
    database = []
    for i in range(4, 149, 1):
        row = []
        #print(sheet.cell_value(i, 3))
        row.append(sheet.cell_value(i, 1))
        row.append(sheet.cell_value(i, 2))
        row.append(sheet.cell_value(i, 3))
        database.append(row)
    return database

def writeJsonSTD(data):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJsonSTD():
    arr = []
    with open('data.json', 'r', encoding='utf-8') as f:
        arr = json.load(f)
    return arr