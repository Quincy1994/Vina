#! /usr/bin/env python
#coding=utf-8
#简单工厂实现K-means，onepass，BGLL，walktrap
import numpy as np
import random
import math
import copy
import re
import string
import xlrd
import numpy.linalg as nplg
import scipy.sparse.linalg as lg
import igraph
from igraph import *
from data import *
from draw import *
import shutil

import xlwt
import readLabel
homeindex='/home/fen/'
class community_algorithm():    # 父类，所有的算法类继承父类
    result = []
    Q=0
    g=Graph(1)
    listresult=[]
    def GetResult(self):		#用此方法返回结果
        return self.result,self.Q,self.g,self.listresult

class BGLL(community_algorithm):	#BGLL算法 不需要参数
    def __init__(self,data,alpha=None):
        aaa=GetMatrix()
        testi,vx=aaa.Data2Lin(data)
        #g=Graph(len(testi))
        self.g=Graph(1)
        self.g.add_vertices(vx-1)
        weights=[]
        for i in range(len(testi)):
            for j in range(len(testi)):
                if testi[i][j]>0:
                    self.g.add_edge(i,j)
                    weights.append(testi[i][j])
        self.result=self.g.community_multilevel(weights)
        self.Q=self.g.modularity(self.result,weights)
        a=[0 for i in range(vx)]
        for i in range(0,self.result.__len__(),1):
            for j in range(0,self.result[i].__len__(),1):
                a[self.result[i][j]]=i
        self.listresult=a
    def GetResult(self):
        return self.result,self.Q,self.g,self.listresult


class walktrap(community_algorithm):    # 随机游走算法 不需要参数
    def __init__(self, data, alpha=None):
        aaa = GetMatrix()
        testi, vx = aaa.Data2Lin(data)
        self.g = Graph(1)
        self.g.add_vertices(vx-1)
        weights = []
        for i in range(len(testi)):
            for j in range(len(testi)):
                if testi[i][j] > 0:
                    self.g.add_edge(i, j)
                    weights.append(testi[i][j])
        se = self.g.community_walktrap(weights, steps=4)
        ss = se.as_clustering()
        resultwt = [[]for i in range(ss.__len__())]
        for i in range(0, ss.__len__(), 1):
            resultwt[i] = (ss.__getitem__(i))
        self.result = resultwt
        self.Q = self.g.modularity(ss, weights)
        a = [0 for i in range(vx)]
        for i in range(0, self.result.__len__(), 1):
            for j in range(0, self.result[i].__len__(), 1):
                a[self.result[i][j]] = i
        self.listresult = a
        del se, ss

    def GetResult(self):
        return self.result, self.Q, self.g, self.listresult


class K_means(community_algorithm):			# K_means算法 需要参数 number of clusters

    def __init__(self, data, k):
        k = int(k)
        aaa = GetInfo()
        info = aaa.Lin2Matrix(data)
        L, vx = aaa.Data2Lin(data)
        weights = []
        self.g = Graph(1)
        self.g.add_vertices(vx-1)
        for i in range(len(L)):
            for j in range(len(L)):
                if L[i][j] > 0:
                    self.g.add_edge(i, j)
                    weights.append(L[i][j])
        center = [[1, info[i]] for i in range(k)]
        resultk = [[i] for i in range(k)]
        width = len(info[0])
        for i in range(k, len(info)):
            min_center = self.min_dis_center(center, info[i])
            for j in range(width):
                center[min_center][1][j] = (center[min_center][1][j] * center[min_center][0] + info[i][j])/ (1.0+center[min_center][0])
            center[min_center][0] += 1
            resultk[min_center].append(i)
        self.result = resultk
        self.Q = aaa.CountQQ(self.result, data)
        a = [0 for i in range(vx)]
        for i in range(0, self.result.__len__(), 1):
            for j in range(0, self.result[i].__len__(), 1):
                a[self.result[i][j]] = i
        self.listresult = a

    def GetResult(self):
        return self.result, self.Q, self.g, self.listresult

    def fun_dis(self, x, y, n):
        return sum(map(lambda v1, v2: pow(abs(v1-v2), n), x, y))

    def distance(self, x, y):
        return self.fun_dis(x, y, 2)

    def min_dis_center(self, center, node):
        min_index = 0
        min_dista = self.distance(center[0][1], node)
        for i in range (1, len(center)):
            tmp = self.distance(center[i][1], node)
            if tmp < min_dista:
                min_dista = tmp
                min_index = i
        return min_index


class onepass(community_algorithm):			# 一趟聚类算法  需要参数 threshold (optimal -1~1)
    x = 2										# 幂指数
    onepass_classindex = 0
    one_pass_colu = 0
    one_pass_row = 0

    def __init__(self, info, alpha):					# 此处的data应该为一个Lin2Matrix的返回值
        aaa = GetInfo()
        alpha = float(alpha)
        data = aaa.Lin2Matrix(info)
        testi, vx = aaa.Data2Lin(info)
        self.g = Graph(1)
        self.g.add_vertices(vx-1)
        weights = []
        for i in range(len(testi)):
            for j in range(len(testi)):
                if testi[i][j] > 0:
                    self.g.add_edge(i, j)
                    weights.append(testi[i][j])
        self.one_pass_row, self.one_pass_colu = data.shape	    # 行数和列数
        onepass_result = []
        threshlod, EX, DX=self.compute_threshold(data,alpha)
        cluster_array=self.one_pass_cluster(data,threshlod)
        for a in range(len(cluster_array)):
            onepass_result.append(cluster_array[a]['onepass_classindex'])
        self.result=onepass_result
        self.Q=aaa.CountQQ(self.result,info)
        a=[0 for i in range(vx)]
        for i in range(0,self.result.__len__(),1):
            for j in range(0,self.result[i].__len__(),1):
                a[self.result[i][j]]=i
        self.listresult=a
    def GetResult(self):
        return self.result,self.Q,self.g,self.listresult



    def compute_threshold(self,data,threshlod_alpha):

        distance=[]
        for k in range(8000):
            random_data1=data[random.randrange(0,self.one_pass_row-1)]
            random_data2=data[random.randrange(0,self.one_pass_row-1)]
            n_dif=0
            for i in range(self.one_pass_colu):
                n_dif=n_dif+pow(random_data1[i]-random_data2[i],self.x)
            records_distance=pow(n_dif/self.one_pass_colu,1.0/self.x)
            distance.append(records_distance)
        EX=sum(distance)/8000.0
        DX=pow((sum(pow((d-EX),2)for d in distance))/8000.0,0.5)
        threshold=EX+threshlod_alpha*DX
        return threshold,EX,DX

    def one_pass_cluster(self,data,threshlod):

        cluster_array=[]
        for k in range(self.one_pass_row):
            self.onepass_classindex=k
            if len(cluster_array):
                dist,cluster_index=self.find_nearest_cluster(data[k,:],cluster_array)
                if dist<threshlod:
                    self.add_record_to_cluster(data[k,:],cluster_array[cluster_index],dist)

                else:
                    cluster_array.append(self.new_cluster(data[k,:]))

            else:
                cluster_array.append(self.new_cluster(data[k,:]))
        if len(cluster_array)==1:
            raise OneComAlphaException(threshlod)
            #raise ValueError("count==cluster['info']['count'],only one cluster,no meaning to continue!Increase the alpha")
        return cluster_array

    def new_cluster(self,record):

        cluster={}
        for i in range(self.one_pass_colu):
            cluster[i]=record[i]
        cluster['onepass_classindex']=[]
        cluster['onepass_classindex'].append(self.onepass_classindex)

        cluster['info']={'EX_dist':0.0,'DX_dist':0.0,'radius':0.0,'count':1}
        return cluster

    def find_nearest_cluster(self,record,cluster_array):
        min_dist=10000
        cluster_index=0
        index=0
        for cluster in cluster_array:
            dist=self.dist_record_cluster(record,cluster)

            if dist<min_dist:
                min_dist=dist
                cluster_index=index
            index=index+1
        return min_dist,cluster_index

    def dist_record_cluster(self,record,cluster):

        dif=0.0
        for i in range(self.one_pass_colu):
            i_dist=abs(record[i]-cluster[i])
            dif = dif+pow(i_dist,self.x)
        dist = pow(dif/self.one_pass_row,1.0/self.x)
        return dist

    def	add_record_to_cluster(self,record,cluster,dist):

        """

        :type cluster: object
        """
        for n in range(self.one_pass_colu):
            cluster[n] = (cluster[n]*cluster['info']['count']+record[n])/float((cluster['info']['count']+1))
        cluster['onepass_classindex'].append(self.onepass_classindex)
        if cluster['info']['count'] == 1:
            cluster['info']['EX_dist'] = dist
            cluster['info']['DX_dist'] = 0.0
        else:
            cluster['info']['DX_dist'] = cluster['info']['DX_dist']*(cluster['info']['count']-1)/cluster['info']['count']+(dist-cluster['info']['EX_dist'])**2/(cluster['info']['count']+1)
            cluster['info']['EX_dist'] = (cluster['info']['EX_dist']*cluster['info']['count']+dist)/(cluster['info']['count']+1)
        if dist>cluster['info']['radius']:
            cluster['info']['radius'] = dist
        cluster['info']['count'] += cluster['info']['count']
        return cluster

class Infomap(community_algorithm):        # Infomap 不需要参数
    def __init__(self, data):
        aaa = GetMatrix()
        testi, vex = aaa.Data2Lin(data)
        self.g = Graph(1)
        self.g.add_vertices(vex-1)
        weights = []
        for i in range(len(testi)):
            for j in range(len(testi)):
                if testi[i][j] > 0:
                    self.g.add_edge(i, j)
                    weights.append(testi[i][j])
        self.result=self.g.community_infomap(edge_weights=weights)
        self.Q=self.g.modularity(self.result,weights)
        a=[0 for i in range(vex)]
        for i in range(0,self.result.__len__(),1):
            for j in range(0,self.result[i].__len__(),1):
                a[self.result[i][j]]=i
        # self.listresult=a
    def GetResult(self):

        return self.result,self.Q,self.g,self.listresult


class fastgreedy(community_algorithm):     # fastgreedy 不需要参数
    def __init__(self, data):
        aaa=GetMatrix()
        testi,vex=aaa.Data2Lin(data)
        print vex
        self.g=Graph(1)
        self.g.add_vertices(vex-1)
        weights=[]
        for i in range(0,len(testi), 1):
            for j in range(i+1,len(testi), 1):
                testi[i][j]=(testi[i][j]+testi[j][i])/(2*1.0)
                testi[j][i]=testi[i][j]
        for i in range(0,len(testi), 1):
            for j in range(i+1,len(testi), 1):
                if testi[i][j] > 0:
                    self.g.add_edges((i, j))
                    weights.append(testi[i][j])
        se = self.g.community_fastgreedy(weights)
        ss = se.as_clustering()
        self.Q = ss.recalculate_modularity()

        resultwt = [[]for i in range(ss.__len__())]
        for i in range(0, ss.__len__(), 1):
            resultwt[i] = (ss.__getitem__(i))
        self.result = resultwt
        a = [0 for i in range(vex)]
        for i in range(0, self.result.__len__(), 1):
            for j in range(0, self.result[i].__len__(), 1):
                a[self.result[i][j]] = i
        self.listresult = a
        # print self.listresult
        del se, ss

    def GetResult(self):
        return self.result, self.Q, self.g, self.listresult

class LPA(community_algorithm):
    def __init__(self,data):
        aaa=GetMatrix()
        testi,vex=aaa.Data2Lin(data)
        self.g=Graph(1)
        self.g.add_vertices(vex-1)
        weights=[]
        for i in range(len(testi)):
            for j in range(len(testi)):
                if testi[i][j]>0:
                    self.g.add_edges((i,j))
                    weights.append(testi[i][j])
        se=self.g.community_label_propagation(weights=weights)
        #ss=se.as_clustering()
        self.Q=se.recalculate_modularity()

        #print "mo is", mo
        resultwt=[[]for i in range(se.__len__()) ]
        for i in range(0,se.__len__(),1):
            resultwt[i]=(se.__getitem__(i))
        self.result=resultwt
        a=[0 for i in range(vex)]
        for i in range(0,self.result.__len__(),1):
            for j in range(0,self.result[i].__len__(),1):
                a[self.result[i][j]]=i
        self.listresult=a
        # print self.listresult
    def GetResult(self):
        return self.result,self.Q,self.g,self.listresult
class algorithm_factory():
    def __init__(self, num):
        self.num = num

    def createalgorithm(self, data, alpha=None):
        algo = community_algorithm()
        if self.num == 1:
            algo = BGLL(data)
        elif self.num == 2:
            algo = walktrap(data)
        elif self.num == 3:
            algo = K_means(data,alpha)
        elif self.num == 4:
            algo = onepass(data,alpha)
        elif self.num == 5:
            algo = Infomap(data)
        elif self.num == 6:
            algo = fastgreedy(data)
        elif self.num == 7:
            algo = LPA(data)
        else:
            print "no such algorithm"
        return algo

    def Shunxuresult(self, result):
        x = {}
        d = 0.1
        for i in range(0, result.__len__(), 1):
            if len(result[i]) in x.keys():
                x[len(result[i])+d] = result[i]
                d += 0.1
            else:
                x[len(result[i])] = result[i]
        keys = x.keys()
        keys.sort()
        keys.reverse()
        #map(x.get,keys)
        return [x[key]for key in keys]

def DianduZhongxindu(L,vex):##
    Zhongxindu={}
    for i in range(0,vex,1):
        k=0
        for j in range(0,vex,1):
            k+=(L[i][j]+L[j][i])
        k=k/(2*vex-1)
        Zhongxindu[i]=k
    sortDian=sorted(Zhongxindu.items(),key=lambda e:e[1],reverse=True)


    #print  "all 点度中心度",Zhongxindu#

    #print "all sorted 点度中心度",sortDian


    #print "top 1o 点度中心度 "
    topp=[]
    for i in range(0,10,1):
        topp.append([sortDian[i][0],sortDian[i][1]])
    #print topp

    #print "least 10 点度中心度"
    least=sortDian[-10:]
    #for i in range(0,10,1):
        #print least[i][0],least[i][1]
    #print least

    return Zhongxindu ,sortDian,topp,least
def DianduZhongxinshi(L,vex):
    Zhongxindu,sort,a,b=DianduZhongxindu(L,vex)
    Zhongxinshi=0
    for i in range(vex):
         Zhongxinshi+=(sort[0][1]-Zhongxindu[i])
    #print "tset ", Zhongxinshi/(1.0*(vex-2))
    if(vex==2):
        Zhongxinshi=1
    else:
        Zhongxinshi=Zhongxinshi/(1.0*(vex-2))
    return Zhongxinshi
def Midu(L,vex):
    midu=0
    for i in range(vex):
        for j in range(vex):
            if L[i][j]>0:
                midu+=1
    if midu==0:
        mindu=0
    else:
        midu=midu/(1.0*vex*(vex-1))
    return midu
def XiaoLin(DaL,result):  #mis

    maxt=-8899
    for i in result:
        maxt=max(maxt,i)
    XiaoL=[[0 for i in range(len(DaL))]for j in range(len(DaL))]
    for i in result:
        for j in result:
                XiaoL[i][j]=DaL[i][j]
    return XiaoL
def Dij(L,vex):
    gg=Graph(1)
    gg.add_vertices(vex-1)
    weights=[]
    for i in range(0,vex,1):
        for j in range(0,vex,1):
            if L[i][j]>0:
                gg.add_edge(i,j)
                weights.append(1.0/(1.0*L[i][j]))
            else:
                gg.add_edge(i,j)
                weights.append(65536)
    dij= gg.shortest_paths_dijkstra(weights=weights,mode=OUT)
    #print "yuan dij",dij
    weights=[]


    #print np.array(dij)
    del gg
    for i in range(0,vex,1):
        for j in range(0,vex,1):
            dij[i][j]=dij[i][j]/(vex-1)
    #print dij
    return dij
def Tujiejin(L,vex):
    dij=Dij(L,vex)
    maxdij=-8888
    for i in range(vex):
        for j in range(vex):
            maxdij=max(dij[i][j],maxdij)
    #print maxdij
    Tujiejin=0
    for i in range(vex):
        for j in range(vex):
            Tujiejin+=(maxdij-dij[i][j])
    Tujiejin=(Tujiejin*(2*(vex-3)))/((vex-2)*(vex-1))
    return Tujiejin
def findtop(L,result):
    top=[]
    AllZhongxinshi={}
    for i in range(result.__len__()):
        XL=XiaoLin(L,result[i])
        a,b,c,d=DianduZhongxindu(XL,XL.__len__())
        top.append(b[0][0])
        AllZhongxinshi[i]=DianduZhongxinshi(XL,XL.__len__())
        del XL
    return top
def writexls(L,vex,labelfile,listresult,result,nfilepath,cfilepath):
    a,b,c,d=DianduZhongxindu(L,vex)

    x=ReadLable(labelfile)
    print x
    share=[[0 for i in range(vex)]for j in range(vex)]
    shares=[0 for i in range(vex)]
    for i in range(vex):
        for j in range(i+1,vex,1):
            for k in range(0,vex,1):
                if (L[i][k]!=0 and L[j][k]!=0):
                    share[i][j]+=1
    print "share",share
    s=[[]for j in range(vex)]
    for i in range(vex):
        sortshare={}
        for j in range(vex):
            sortshare[j]=share[i][j]
        sortshare=sorted(sortshare.items(),key=lambda e:e[1],reverse=True)
        shares[i]=sortshare

        if shares[i][0][0]==0 :
            shares[i]=None
        else:
            for m in range(5):
                if L[i][shares[i][m][0]]==0 :
                    s[i].append(shares[i][m][0])
            for n in range(s[i].__len__()):
                s[i][n]=x[s[i][n]].decode('utf-8')+" "
            #shares[i]=(shares[i][0][0],shares[i][1][0],shares[i][2][0],shares[i][3][0],shares[i][4][0],shares[i][5][0])
            shares[i]=s[i]
    print "top ",shares

    rudu = [0 for i in range(vex)]
    chudu = [0 for i in range(vex)]
    for i in range(0, vex, 1):
        for j in range(0,vex, 1):
            chudu[i]+=L[i][j]
            rudu[i]+=L[j][i]
    print "rudu",rudu
    print "chudu",chudu


    AllMidu={}
    for i in range(result.__len__()):

        XL=XiaoLin(L,result[i])
        AllMidu[i]=Midu(XL,XL.__len__())
        del XL
    sortmidu=sorted(AllMidu.items(),key=lambda e:e[1],reverse=True)
    print "all 密度: ", AllMidu
    print "sort midu",sortmidu
    AllZhongxinshi={}
    for i in range(result.__len__()):
        XL=XiaoLin(L,result[i])
        AllZhongxinshi[i]=DianduZhongxinshi(XL,XL.__len__())
        del XL
    print "all 点度中心势: ", AllZhongxinshi


    sortshi = sorted(AllZhongxinshi.items(), key=lambda e: e[1], reverse=True)  # #

    print "sortshi", sortshi



    nfile = xlwt.Workbook(encoding='utf-8')
    sheet = nfile.add_sheet("sheet1")
    srow = vex
    scol = 8
    sheet.write(0, 0, '节点')
    sheet.write(0, 1, '标签')
    sheet.write(0, 2, '所在社区')
    sheet.write(0, 3, "点度中心度")
    sheet.write(0, 4, "点度中心度排名")
    sheet.write(0, 5, "内含度")
    sheet.write(0, 6, "外含度")
    sheet.write(0, 7, "好友推荐")
    for row in range(vex):
        sheet.write(row+1, 0, row)
        sheet.write(row+1, 1, x[row])
        sheet.write(row+1, 2, listresult[row]+1)


        dd = round(a[row], 3)
        sheet.write(row+1, 3, dd)
        del dd

        sheet.write(b[row][0]+1, 4, row+1)
        sheet.write(row+1, 5, rudu[row])
        sheet.write(row+1, 6, chudu[row])
        sheet.write(row+1, 7, shares[row])


    nfile.save(nfilepath)

    cfile = xlwt.Workbook(encoding='UTF-8')
    sheet = cfile.add_sheet("sheet1")
    crow = result.__len__()
    ccol = 7
    top = findtop(L, result)
    sheet.write(0, 0, '社区')
    sheet.write(0, 1, '节点')
    sheet.write(0, 2, '密度')
    sheet.write(0, 3, '密度排名')
    sheet.write(0, 4, "点度中心势")
    sheet.write(0, 5, "点度中心势排名")
    sheet.write(0, 6, "最大点度中心度")
    for com in range(crow):
        sheet.write(com+1, 0, com)
        sheet.write(com+1, 1, result[com].__len__())

        midu = round(AllMidu[com],6)
        sheet.write(com+1, 2, midu)
        del midu

        # sheet.write(com+1,3,com+1)
        sheet.write(sortmidu[com][0]+1, 3, com+1)
        # paiming

        zxs = round(AllZhongxinshi[com], 3)
        sheet.write(com+1, 4, zxs)
        del zxs
        # paiming
        sheet.write(sortshi[com][0]+1, 5, com+1)
        sheet.write(com+1, 6, x[top[com]])
    cfile.save(cfilepath)

def findleast(L):
    least=[]
    AllZhongxinshi={}
    a,b,c,d=DianduZhongxindu(L,L.__len__())
    print "lllle",d
    for i in range(5):
        least.append(d[i][0])

    return least
def writeXml(filepath,comNum,dict, username):
    if os.path.exists(homeindex+"demo/static/%s/" % username):
        shutil.rmtree(homeindex+"demo/static/%s/" % username)
    os.mkdir(homeindex+"demo/static/%s/" % username)
    xmlFile=open(filepath,"w")
    xmlFile.write("<?xml version='1.0' encoding='utf-8'?>"+"\n")
    xmlFile.write("<chart"+"\n")
    xmlFile.write("caption='community'"+"\n"+
    "subcaption='subcaption:dont konw ' "+"\n"+
    "lineThickness='4' "+"\n"+
    "showValues='0' "+"\n"+
    "formatNumberScale='1' "+"\n"+
    "anchorRadius='4' "+"\n"
    "divLineAlpha='15' "+"\n"
    "divLineColor='666666' "+"\n"
    "divLineIsDashed='1' "+"\n"
    "showAlternateHGridColor='1' "+"\n"+
    "alternateHGridColor='666666' "+"\n"+
        "shadowAlpha='40' "+"\n"+
        "labelStep='2' "+"\n"+
        "numvdivlines='5' "+"\n"+
        "chartRightMargin='35' "+"\n"+
        "bgColor='FFFFFF,FFFFFF' "+"\n"+
        "bgAngle='270' "+"\n"+
        "bgAlpha='10,10' "+"\n"+
        "alternateHGridAlpha='5'  "+"\n"+
        "legendPosition ='RIGHT ' "+"\n"+
        "baseFontSize='12' "+"\n"+
        "baseFont='Microsoft YaHei,Helvitica,Verdana,Arial,san-serif' canvasBorderThickness='1' "+"\n"+
        "canvasBorderColor='888888' "+"\n"+
        "showShadow='1' "+"\n"+
        "animation='1' "+"\n"+
        "showBorder='0' "+"\n"+
        "showToolTip='1' "+"\n"+
        "adjustDiv='1' "+"\n"+
        "setAdaptiveYMin='1' "+"\n"+
        "defaultAnimation='1' "+"\n"+
        "xAxisName='com' "+"\n"+
        "yAxisName='comNUm' "+"\n"+
        "numberPrefix='' "+"\n"+"> ")

    xmlFile.write("<categories >"+"\n")
    for i in range(comNum):
        xmlFile.write("<category label="+"'com"+str(i+1)+"'/>"+"\n")
    xmlFile.write("</categories >"+"\n")

    xmlFile.write("<dataset seriesName='comNum' color='99ccff' anchorBorderColor='99ccff' anchorBgColor='ffffff'>"+"\n")
    for i in range(comNum):
        xmlFile.write("<set value='"+str(dict[i])+"' />"+"\n")
    xmlFile.write("</dataset>"+"\n")

    xmlFile.write("  <styles>"+"\n"+
    "<definition>"+"\n"+
      "<style name='CaptionFont' type='font' size='12'/>"+"\n"+

    "</definition>"+"\n"+
    "<application>"+"\n"+
      "<apply toObject='CAPTION' styles='CaptionFont' />"+"\n"+

      "<apply toObject='SUBCAPTION' styles='CaptionFont' />"+"\n"+

    "</application>"+"\n"+
  "</styles>"+"\n"+
"</chart>")
    print "okxml"
    xmlFile.close()  #
def writeJS(filepath,comNum,dict,username):
    if os.path.exists(homeindex+"demo/static/%s/" % username):
        shutil.rmtree(homeindex+"demo/static/%s/" % username)
    os.mkdir(homeindex+"demo/static/%s/" % username)
    JSfile=open(filepath,"w")

    JSfile.write("var  chart2;"+"\n")
    JSfile.write("$(document).ready(function() {"+"\n"+
    "chart2 = new Highcharts.Chart({"+"\n"+
        "chart: {"+"\n"+
            "renderTo: 'chart_2',"+"\n"+
            "plotBackgroundColor: null,"+"\n"+
            "plotBorderWidth: null,"+"\n"+
            "plotShadow: false,"+"\n"+
            "height: 500,"+"\n"+
        "},"+"\n"+
        "title: {"+"\n"+
            "text: '各个社区所占的比例'"+"\n"+
        "},"+"\n"+
        "tooltip: {"+"\n"+
            "pointFormat: '<b>{point.percentage}%</b>',"+"\n"+
            "percentageDecimals: 1"+"\n"+
        "},"+"\n"+
        "plotOptions: {"+"\n"+
            "pie: {"+"\n"+
                "allowPointSelect: true,"+"\n"+
                "cursor: 'pointer',"+"\n"+
                "dataLabels: {"+"\n"+
                    "enabled: false"+"\n"+
                "},"+"\n"+
                "showInLegend: true"+"\n"+
            "}"+"\n"+
        "},"+"\n"+
             "series: [{"+"\n"+
         "type: 'pie',"+"\n"+
            "name: 'Dev #1',"+"\n"+
            "data: ["+"\n")
    for i in range(comNum):
        JSfile.write("['com"+str(i+1)+"',"+str(dict[i])+"],"+"\n")
    JSfile.write("]"+"\n"+"}]"+"\n"+"});"+"\n"+"});")
    JSfile.close()
def algorithm(k, filename, alpha=None,labelfile=None, username=None):
    a = algorithm_factory(k)
    b = a.createalgorithm(data=filename, alpha=alpha)
    result, Q, g, listresult = b.GetResult()
    result = a.Shunxuresult(result)
    g, L = Draw(result, filename, g, listresult, labelfile,username)
    comNum=result.__len__()  #
    dict={}#
    for i in range(comNum):#
        dict[i]=result[i].__len__()
    #writeXml("/home/ddjian/demo/static/%s/MSLine.xml"%username,comNum,dict,username)#
    writeJS(homeindex+"demo/static/%s/piechart.js"%username,comNum,dict,username)#
    top = findtop(L, result)
    least=findleast(L)
    # print top
    drawn(g, listresult, L.__len__(), labelfile, top,username)
    writetop(top,labelfile,username)
    writeleast(least,labelfile,username)
    writexls(L,L.__len__(),labelfile,listresult,result,homeindex+"demo/static/dv/%s/nodes.xls"%username,homeindex+"demo/static/dv/%s/communites.xls"%username)
    return result, Q, listresult, g


class OneComAlphaException(Exception):
    def __int__(self, alpha):
        Exception.__init__(self)
        self.alpha=alpha

