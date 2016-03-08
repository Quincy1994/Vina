
####################################################
import string
import xlwt
import xlrd
from thesite.readLabel import ReadLable
homeindex='/home/fen/'


def rd(username=None):
    filenname = homeindex+"demo/static/dv/%s/result.txt"%username
    out = open(filenname)
    line = out.readline()
    a = []
    l = []
    while line:
        line = line.replace('\n', '')
        l = line.split(',')
        a.append(line)
        line = out.readline()
    out.close()
    print a.__len__()


    re=[ [] for i in range(a.__len__())]
    out = open(filenname)
    line = out.readline()
    l = []
    i = 0
    while line:
        line = line.replace('\n', '')
        l = line.split(',')
        for j in l:
            re[i].append(int(j))
        line = out.readline()
        i += 1
    out.close()
####################################################
    filenname = homeindex+"demo/static/dv/%s/listresult.txt"%username
    out = open(filenname)
    line = out.readline()
    li = []
    l = []
    while line:
        line = line.replace('\n', '')
        l = line.split(',')
        for j in l:
            li.append(int(j))
        line = out.readline()
    out.close()
    print li
####################################################
    Lin=[ [] for i in range(li.__len__())]
    filenname = homeindex+"demo/static/dv/%s/Lin.txt"%username
    out = open(filenname)
    line = out.readline()
    l = []
    i = 0
    while line:
        line = line.replace('\n', '')
        l = line.split(',')
        for j in l:
            Lin[i].append(string.atof(j))
        i += 1
        line = out.readline()
    out.close()
####################################################
    filenname = homeindex+"demo/static/dv/%s/labeldata.txt"%username
    label=[ [] for i in range(a.__len__())]
    out = open(filenname)
    line = out.readline()
    l = []
    i = 0
    while line:
        line = line.replace('\n', '')
        l = line.split(',')
        for j in l:
            label[i].append(j)
        line = out.readline()
        i += 1
    out.close()
    return re,li, Lin,label
######################################################
def writelistresult(listresult,username=None):
    filenname = homeindex+"demo/static/dv/%s/listresult.txt"%username
    output = open(filenname, 'wb')
    for i in range(listresult.__len__()-1):
        output.write(str(listresult[i])+",")
    output.write(str(listresult[i+1]))
    output.close()
######################################################
def writeresult(result,username=None):
    filenname = homeindex+"demo/static/dv/%s/result.txt"%username
    output = open(filenname, 'wb')
    for i in range(result.__len__()):
        for j in range(result[i].__len__()-1):
            output.write(str(result[i][j])+",")
        output.write(str(result[i][j+1]))##
        output.write('\n')
    output.close()
######################################################
def writelabeldata(labelresult,username=None):
    filenname = homeindex+"demo/static/dv/%s/labeldata.txt"%username
    output = open(filenname, 'wb')
    for i in range(labelresult.__len__()):
        for j in range(labelresult[i].__len__()-1):
            output.write(str(labelresult[i][j])+",")
        output.write(str(labelresult[i][j+1]))
        output.write('\n')
    output.close()
######################################################
def writeLin(L,username=None):
    filenname = homeindex+"demo/static/dv/%s/Lin.txt"%username
    output = open(filenname, 'wb')
    for i in range(L.__len__()):
        for j in range(L.__len__()-1):
            output.write(str(L[i][j])+",")
        output.write(str(L[i][j+1]))
        output.write('\n')
    output.close()

def writetop(top,labelfile,username=None):
    nfile = xlwt.Workbook(encoding='utf-8')
    label=ReadLable(labelfile)
    sheet = nfile.add_sheet("sheet1")
    sheet.write(0,0,'top five')
    sheet.write(0,1,'label')
    for i in range(5):
        sheet.write(i+1,0,top[i])
        sheet.write(i+1,1,label[top[i]])
    nfile.save(homeindex+"demo/static/dv/%s/top.xls"%username)
def writeleast(least,labelfile,username=None):
    nfile = xlwt.Workbook(encoding='utf-8')
    label=ReadLable(labelfile)
    sheet = nfile.add_sheet("sheet1")
    sheet.write(0,0,'least')
    sheet.write(0,1,'label')
    for i in range(5):
        sheet.write(i+1,0,least[i])
        sheet.write(i+1,1,label[least[i]])
    nfile.save(homeindex+"demo/static/dv/%s/least.xls"%username)

def writedata(L,listresult,result,labelresult,username=None):
    writeLin(L,username)
    writelistresult(listresult,username)
    writeresult(result,username)
    writelabeldata(labelresult,username)
def readnodes(user=None):
    filename=homeindex+"demo/static/dv/%s/nodes.xls"%user
    filename=filename.encode('utf-8')
    fname = filename
    bk = xlrd.open_workbook(fname)
    sh = bk.sheet_by_name("sheet1")
    nrows = sh.nrows
    # ncols=sh.ncols
    share=[[0 for i in range(8)]for j in range(5)]
    for row in range(1, 6, 1):
        share[row-1][0]= int((sh.cell_value(row, 0)))
        share[row-1][1]= (sh.cell(row,1).value).decode('utf-8')
        print type((sh.cell(row,1).value).decode('utf-8'))
        share[row-1][2]= int((sh.cell_value(row, 2)))
        share[row-1][3]= ((sh.cell_value(row, 3)))
        share[row-1][4]= int((sh.cell_value(row, 4)))
        share[row-1][5]= int((sh.cell_value(row, 5)))
        share[row-1][6]= int((sh.cell_value(row, 6)))
        share[row-1][7]= (sh.cell_value(row,7))
    print share
    return share
def readcommunity(username=None):
    filename=homeindex+"demo/static/dv/%s/communites.xls"%username
    filename=filename.encode('utf-8')
    fname = filename
    bk = xlrd.open_workbook(fname)
    sh = bk.sheet_by_name("sheet1")
    nrows = sh.nrows
    share=[[0 for i in range(7)]for j in range(nrows)]
    for row in range(1, nrows, 1):
        share[row-1][0]= int((sh.cell_value(row, 0)))+1
        share[row-1][1]= int((sh.cell_value(row, 1)))
        share[row-1][2]= ((sh.cell_value(row, 2)))
        share[row-1][3]= int((sh.cell_value(row, 3)))
        share[row-1][4]= ((sh.cell_value(row, 4)))
        share[row-1][5]= int((sh.cell_value(row, 5)))
        share[row-1][6]= ((sh.cell_value(row, 6)))
    return share

def readtop(username=None):
    filename=homeindex+"demo/static/dv/%s/top.xls"%username
    filename=filename.encode('utf-8')
    fname = filename
    bk = xlrd.open_workbook(fname)
    sh = bk.sheet_by_name("sheet1")

    top=[0 for j in range(5)]
    for row in range(1, 6, 1):
        top[row-1]=  (sh.cell_value(row, 1)).decode('utf-8')
    return top

def readleast(username=None):
    filename=homeindex+"demo/static/dv/%s/least.xls"%username
    filename=filename.encode('utf-8')
    fname = filename
    bk = xlrd.open_workbook(fname)
    sh = bk.sheet_by_name("sheet1")

    least=[0 for j in range(5)]
    for row in range(1, 6, 1):
        least[row-1]=  (sh.cell_value(row, 1)).decode('utf-8')
    return least