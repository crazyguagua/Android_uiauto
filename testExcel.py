import xlrd
from collections import Counter

workExcel = xlrd.open_workbook(r'../ll.xls')

sheet1name = workExcel.sheet_names()[0]

print(sheet1name)
sheet1 = workExcel.sheet_by_name(sheet1name)
sheet1Rows = sheet1.nrows
sheet1Cols = sheet1.ncols

print(sheet1Rows)
print(sheet1Cols)


s = []
i = 0

for i in range(sheet1Rows):
    text = sheet1.row(i)[0].value
    s.append(text)

s_f = set(s)
countS = {}

for item in s_f:
    countS[item]= s.count(item)

print(countS)

