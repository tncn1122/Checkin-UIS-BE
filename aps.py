import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import firebase
import xlrd

loc = ("data/ds.xlsx")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
 
# For row 0 and column 0
database = []
for i in range(4, 7, 1):
    row = []
    #print(sheet.cell_value(i, 3))
    row.append(sheet.cell_value(i, 1))
    row.append(sheet.cell_value(i, 2))
    row.append(sheet.cell_value(i, 3))
    database.append(row)


firebase = firebase.FirebaseApplication('https://jsrealtime-37d04.firebaseio.com', None)
firebase.delete('/UIS/', 'Students')
ds = {}
for x in database:
    data =  { 'MSSV': x[0],
          'ho': x[1],
          'ten': x[2],
          'diemDanh' : '0',
          }
    result = firebase.post('/UIS/Students/',data)
    # print(result)
    ds[x[0]] = result['name']
print("Done")

while(True):
    mssv = input()
    if ds.__contains__(mssv):
        #firebase = firebase.FirebaseApplication('Database URL', None)
        firebase.put('/UIS/Students/'+ds.get(mssv),'diemDanh','1')
        print("Điểm danh thành công")
    else:
        print("Không có trong danh sách")








