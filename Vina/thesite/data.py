__author__ = 'root'
# ! /usr/bin/env python
# coding=utf-8
__author__ = 'fen'
import re
import xlrd
import numpy as np
import numpy.linalg as nplg
import scipy.sparse.linalg as lg
import networkx as nx

homeindex='/home/fen/'
class GetMatrix:

    def Data2Lin(self, filename):
        if re.match('(.*xls)|(.*txt)', filename):
            data = self.DataIsxls(filename)
            return data[0],data[1]
        if re.match('.*csv',filename):
            data = self.DataIscsv(filename)
            return data[0], data[1]

    def DataIscsv(self, filename):
        file_object = open(filename)
        max1 = -1
        max2 = -1
        line = file_object.readline()
        temp = [0, 0, 0]
        value = [[0 for col in range(5000)]for row in range(5000)]
        tag=re.match('\d.*',line)
        if  not tag:
            line = file_object.readline()
        while line:
            m = re.match('\d.*,\d.*,\d.*', line)
            if m:
                temp = m.group().strip().split(',')
                value[int(temp[0])][int(temp[1])] = int(temp[2])
                max1 = max(max1, int(temp[0]))
                max2 = max(max2, int(temp[1]))

            line = file_object.readline()
        max1 = max(max1, max2)+1
        values = [[0 for i in range(max1)]for j in range(max1)]
        file_object.close()
        return values, max1

    def DataIsxls(self, filename):
        fname = filename
        bk = xlrd.open_workbook(fname)
        sh = bk.sheet_by_name("Sheet1")
        nrows = sh.nrows
        max1 = -1
        max2 = -1
        tag=re.match('\d.*',str(sh.cell_value(0, 0)))
        start=1
        if  tag:
            start=0
        print "start",start
        for row in range(start, nrows, 1):
            max1 = max(max1, int(sh.cell_value(row, 0)))
            max2 = max(max2, int(sh.cell_value(row, 1)))
        max1 = max(max1, max2)+1
        # print max1
        # max1=max(max1,max2)
        values = [[0 for col in range(max1)]for row in range(max1)]

        for row in range(start, nrows, 1):
            values[int(sh.cell_value(row, 0))][int(sh.cell_value(row, 1))] = sh.cell_value(row,2)
        return values,max1

    def Lin2Matrix(self,filename):
        L,vex=self.Data2Lin(filename)
        for i in range(0,vex,1):
            L[i][i]=self.CountEdge(L,i)-L[i][i] #L=D-A
            for j in range(0,vex,1):
                if (i!=j):
                    L[i][j]=0-L[i][j]
        for i in range(0,vex,1):
            min1=8888888
            max1=-1
            for j in range(0,vex,1):
                min1=(min(min1,L[i][j]))
                max1=(max(max1,L[i][j]))
            for k in range(0,vex,1):
                if (max1-min1)>0:
                    L[i][k]=(L[i][k]-min1)/(max1-min1)
        eigenvalue, eigenvector = lg.eigsh(np.array(L),8)
        #print eigenvector
        return eigenvector
    def CountEdge(self,b,i):
        edge=0
        for q in range(0,len(b[0]),1):
            if(b[i][q]>0):
                edge+=1
        return edge


class GetInfo(GetMatrix):

    def Dianshu(self,filename):
        data=self.Data2Lin(filename)
        return data[1]


    def Bianshu(self,filename):
        L,vex=self.Data2Lin(filename)
        m=0
        for i in range(0,vex,1):
            for j in range(0,vex,1):
                if L[i][j]>0:
                    m+=1
        return m
    def Dianshu(self,filename):
        data=self.Data2Lin(filename)
        return data[1]

    def PingjunQz(self,filename):
        L,vex=self.Data2Lin(filename)
        m=0
        for i in range(0,vex,1):
            for j in range(0,vex,1):
                m+=L[i][j]

        return m/self.Bianshu(filename)
    def Comnum(self,result):
        return len(result)
    def Shunxuresult(result):
        x={}
        d=0.1
        for i in range(0,result.__len__(),1):
            if(len(result[i]) in x.keys()):
                x[len(result[i])+d]=result[i]
                d+=0.1
            else:
                x[len(result[i])]=result[i]

        keys=x.keys()
        keys.sort()
        keys.reverse()
        #map(x.get,keys)
        return [x[key]for key in keys]
    def CountQQ(self,result,filename):
        g=GetMatrix()
        L,vex=g.Data2Lin(filename)
        k={}
        m=0
        for i in range(0,vex,1):
            k[i]=0
            for j in range(0,vex,1):
                m=m+L[i][j]
                k[i]=k[i]+L[i][j]
        Q=0
        for re in result:
            for i in range(0,len(re),1):
                x=re[i]
                for j in range(0,len(re),1):
                    y=re[j]
                    if(x==y):
                        continue
                    Q=Q+L[x][y]-k[x]*k[y]*0.5/m

        Q=Q*0.5/m
        return Q



