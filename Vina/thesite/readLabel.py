__author__ = 'root'
#-*-coding:utf-8-*
import xlrd
import re
import sys
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
def ReadLable(filename):
    if(re.match('(.*xls)|(.*txt)',filename)):
        return FileIsxls(filename)
    if(re.match('.*csv',filename)):
        return FileIscsv(filename)
def FileIsxls(filename):
    filename=filename.decode('utf-8')
    bk=xlrd.open_workbook(filename)
    shxrange=range(bk.nsheets)
    sh=bk.sheet_by_name("Sheet1")
    ncols=sh.ncols
    nrows=sh.nrows
    x={}
    #sheet.write(sortmidu[com][0]+1,2,com+1)
    tag=re.match('\d.*',str(sh.cell_value(0, 0)))
    start=1
    if  tag:
        start=0
    print "start",start
    for row in range(start,nrows,1):
        x[int(sh.cell_value(row,0))]=sh.cell_value(row,1)
    return x
def FileIscsv(filename):
    file_object=open(filename)
    line=file_object.readlines()
    x={}
    tag=re.match('\d.*',line)
    if  not tag:
        line = file_object.readline()
    while line:
        m=re.match('\d.*,.*',line)
        if m:
            temp=m.group().strip().split(',')
            x[temp[0]]=temp[1]

        line=file_object.readlines()

def numtolabel(filename,result):
    if filename==None:
        Labelresult=copy.deepcopy(result)
        return Labelresult
    label=ReadLable(filename)
    Labelresult=copy.deepcopy(result)
    for i in range(0,result.__len__(),1):
        for j in range(0,result[i].__len__(),1):
            Labelresult[i][j]=label[result[i][j]]
    return Labelresult

if __name__=="__main__":
    filename="/home/quincy/桌面/polbookslabels.xls"
    x=ReadLable(filename)
    print x[0]
    print x