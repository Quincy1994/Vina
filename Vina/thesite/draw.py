# coding=utf-8
from thesite.readLabel import ReadLable, numtolabel
import numpy as np
import numpy.linalg as nplg
import scipy.sparse.linalg as lg
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import codecs
from data import *
from igraph import *
from readdate import *
homeindex='/home/fen/'
def Lin2Graph(L,vex):
    G=nx.Graph()
    for i in range(0,vex,1):
        for j in range(0,vex,1):
            if L[i][j]>0:
                G.add_edge(i,j)
    return G

color_dict = {0: "pink", 1: "green",2:"purple",3:"orange",4:"blue",5:"yellow",6:"red",7:"#8B2500",8:"#87CEEB",9:"#707070",
              10:"#FFF68F",11:"#FFEFD5",12:"#FFE4E1",13:"#FFDEAD",14:"#FFC1C1",15:"#FFB90F",16:"#FFA54F",17:"#FF8C00",
              18:"black",19:"#FF6EB4",20:"#FF4500",21:"#FF3030",22:"#F5DEB3",23:"#F0FFFF",24:"#F08080",25:"#EED2EE",26:"#EECFA1",
              27:"#EECBAD",28:"#EEC900",29:"#DDA0DD",30:"#E3E3E3",31:"#DB7093",32:"#D8BFD8",33:"#D2B48C",34:"#CDCDB4",
              35:"#CDAD00",36:"#CD853F",37:"#CD5555",38:"#CAE1FF",39:"#BCEE68",40:"#A0522D",41:"#AEEEEE",42:"#9AFF9A",
              43:"#B03060",44:"#8B6508",45:"#8B475D",46:"#8B1A1A",47:"#836FFF",48:"#7A378B",49:"#76EEC6",50:"#698B69"}
def Draw(result,filename,g,listresult,labelfile=None,username=None):
    x=GetInfo()
    L,vex=x.Data2Lin(filename)
    total=x.Dianshu(filename)
    labelresult = numtolabel(labelfile, result)
    writedata(L,listresult,result,labelresult,username)
    density=drawdensity(L,result,listresult,labelresult)
    drawChart(result,total,listresult,username)
    com=ComWi(L,result)
    Nodecom(com,result,username)
    denCom(density,com,result,username)
    drawCentralization(L,result,username)
    return g,L

def drawChart(result,total,listresult,username=None):
    N=len(result)
    li1=[]
    ticklabels=[]
    percent=[]
    ind=np.arange(N)
    width=0.35
    c=1
    colors=[]
    for i in range(0,result.__len__(),1):
        j=result[i][0]
        colors.append(color_dict[listresult[j]%50])

    ax=plt.subplot(221)
    for r in result:
        li1.append(len(r))
        ticklabels.append('C%s'%c)
        percent.append(float(len(r)*1.0/total))
        c=c+1
    rects=ax.bar(ind,li1,width*1.5,color='r')
    ax.set_ylabel('nodes')
    ax.set_title('rect chart')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(ticklabels)
    for rect in rects:
        height=rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2,1.05*height, '%d'%int(height),ha='center', va='bottom')
    plt.subplot(222)
    plt.title('pie chart')
    plt.pie(percent,explode=None, colors=colors,labels=ticklabels,
            autopct='%1.1f%%', pctdistance=0.8, shadow=True)
    plt.subplot(212)
    x = []
    y = []
    c = 1
    plt.title('line chart')
    plt.xlabel(u'nodes')
    plt.ylabel(u'Community')
    for r in result:
        b = len(r)
        x.append(c)
        y.append(b)
        c += 1
    plt.plot(x, y, 'b', alpha=0.5)
    plt.savefig(homeindex+"demo/static/dv/%s/chart.png"%username)     # save as png
    plt.clf()




def centerzation(L,vex):
    Zhongxindu={}
    for i in range(0,vex,1):
        k=0
        for j in range(0,vex,1):
            k+=(L[i][j]+L[j][i])
        k=k/(2*vex-1)
        Zhongxindu[i]=k
    sortDian=sorted(Zhongxindu.items(),key=lambda e:e[1],reverse=True)
    return Zhongxindu,sortDian
def DegreeCenterzation(L,vex):
    Zhongxindu,sort,=centerzation(L,vex)
    Zhongxinshi=0
    for i in range(vex):
         Zhongxinshi+=(sort[0][1]-Zhongxindu[i])
    #print "tset ", Zhongxinshi/(1.0*(vex-2))
    if vex==2:
        Zhongxinshi=1
    else:
        Zhongxinshi=Zhongxinshi/(1.0*(vex-2))
    return Zhongxinshi
def Density(L,vex):
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

def drawea(L,result,listresult,labelresult):
    vs=20
    if L.__len__() >500:
            vs=8
    density={}
    for i in range(0,result.__len__(),1):
        gg=Graph(1)
        gg.add_vertices(result[i].__len__()-1)
        matrix = [[0 for col in range(result[i].__len__())] for row in range(result[i].__len__())]
        for j in range(0,result[i].__len__(),1):
            for k in range(0,result[i].__len__(),1):
                if (L[result[i][j]][result[i][k]]) > 0:
                    gg.add_edge(j,k)
                    matrix[j][k]=L[result[i][j]][result[i][k]]
        center,sortDian=centerzation(matrix,result[i].__len__())
        dc=DegreeCenterzation(matrix,result[i].__len__())
        Vsize=[]
        for j in range(0,result[i].__len__(),1):
            if j == sortDian[0][0]:
                Vsize.append(vs*3)
            else:
                Vsize.append(vs)
        gg=gg.simplify(gg)
        # print result[i].__len__()
        # print gg.ecount()
        density[i]=(Density(matrix,result[i].__len__()))
        # print dc
        # layout=gg.layout_graphopt()
        layout=gg.layout("fr")
        # layout=gg.layout("star")
        c=result[i][0]
        c=listresult[c]
        label=[]
        for j in labelresult[i]:
           label.append(j)
        gg.vs["label"]=label
        bbox=(10,10,590,590)
        plot(gg,homeindex+"demo/static/dv/community%s.png"%(i+1),bbox=bbox,layout =layout,vertex_size=Vsize,edge_color="grey",vertex_color = color_dict[c%50])
        del matrix
    print density
    return density

def drawdensity(L,result,listresult,labelresult):
    density={}
    for i in range(0,result.__len__(),1):
        gg=Graph(1)
        gg.add_vertices(result[i].__len__()-1)
        matrix = [[0 for col in range(result[i].__len__())] for row in range(result[i].__len__())]
        for j in range(0,result[i].__len__(),1):
            for k in range(0,result[i].__len__(),1):
                if (L[result[i][j]][result[i][k]]) > 0:
                    gg.add_edge(j,k)
                    matrix[j][k]=L[result[i][j]][result[i][k]]
        density[i]=(Density(matrix,result[i].__len__()))
    print density
    return density

def drawn(g, listresult, vex,labelfile,top,username=None):
    # g.delete_vertices(g.vs(0))
    #     layout=g.layout("fr")
        # layout=g.layout("star")
        g = g.simplify(g)
        layout = g.layout_graphopt()
        vs = 30
        if vex > 50:
            vs = 20
        if vex > 200:
         vs = 15
        if vex > 500:
            vs = 10
        if vex > 1000:
            vs = 5
        Vsize=[]
        for i in range(0,vex,1):
            if i in top:
                Vsize.append(vs*2)
            else:
                Vsize.append(vs)
        labelresult=[]
        if labelfile==None:
            for i in range(0,vex,1):
                labelresult.append(i)
        else:
            label=ReadLable(labelfile)
            for i in label:
                labelresult.append(label[i])
        g.vs["label"]=labelresult
        p = Plot()
        p.background = "#ffffff"
        p.add(g,
         bbox=(50, 50, 550, 550),
         layout =layout,
         vertex_size=Vsize,
         edge_arrow_size=1,
         edge_width=0.5,
         edge_color="grey",
         vertex_label_size=10,
         directed=True,
         byrow = True,
         vertex_color = [color_dict[i % 50] for i in listresult])
        print username
        p.save(homeindex+"demo/static/dv/%s/SNA.png"%username)
        p.remove(g)

# def drawe(L,result,listresult,labelresult,i,username=None):
#         i=i-1
#         vs=20
#         gg=Graph(1)
#         gg.add_vertices(result[i].__len__()-1)
#         matrix = [[0 for col in range(result[i].__len__())] for row in range(result[i].__len__())]
#         for j in range(0,result[i].__len__(),1):
#             for k in range(0,result[i].__len__(),1):
#                 if (L[result[i][j]][result[i][k]]) > 0:
#                     gg.add_edge(j,k)
#                     matrix[j][k]=L[result[i][j]][result[i][k]]
#         center,sortDian=centerzation(matrix,result[i].__len__())
#         dc=DegreeCenterzation(matrix,result[i].__len__())
#         Vsize=[]
#         for j in range(0,result[i].__len__(),1):
#             if j == sortDian[0][0]:
#                 Vsize.append(vs*3)
#             else:
#                 Vsize.append(vs)
#         gg=gg.simplify(gg)
#         print result[i].__len__()
#         print gg.ecount()
#         density= Density(matrix,result[i].__len__())
#         print dc
#         # layout=gg.layout_graphopt()
#         layout=gg.layout("fr")
#         c=result[i][0]
#         c=listresult[c]
#         label=[]
#         for j in labelresult[i]:
#            label.append(j)
#         gg.vs["label"]=label
#         if( os.path.exists("/home/ddjian/demo/static/dv/%s/community%s.png"%(username,(i+1)))):
#             del matrix
#             return result[i].__len__() , gg.ecount(),density, dc
#         plot(gg,"/home/ddjian/demo/static/dv/%s/community%s.png"%(username,(i+1)),layout =layout,vertex_size=Vsize,edge_color="grey",vertex_color = color_dict[c%50])
#         del matrix
#         return result[i].__len__() , gg.ecount(),density, dc

def ComWi(L,result): #L为大的临接矩阵 communties为社区数目
    ComWeight=[[0 for i in range(result.__len__())]for j in range(result.__len__())]
    for i in range(result.__len__()):
        for j in range(0,result.__len__(),1):
            for m in result[i] :
                for n in result[j] :
                    ComWeight[i][j]+=L[m][n]
    print ComWeight
    return ComWeight

def Nodecom(comLin,result,username=None):
    g=Graph(1)
    g.add_vertices(result.__len__()-1)
    label=[]
    for i in range(0,comLin.__len__(),1):
        label.append("com%s\nnodes:%s"%((i+1),result[i].__len__()))
        for j in range(0,comLin.__len__(),1):
            if(comLin[i][j] > 0):
                g.add_edges((i,j))
    Vsize=[]
    g = g.simplify(g)
    if comLin.__len__()<=15:
        vs=50
        layout= g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    else:
        vs=30
        layout = g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    for i in range(0,result.__len__(),1):
        if( i == 0):
            Vsize.append(vs*2)
        elif( i == 1):
            Vsize.append(vs*1.5)
        elif( i == 2):
            Vsize.append(vs*1.5)
        else:
            Vsize.append(vs)
    p = Plot()
    p.background = "#ffffff"
    p.add(g,
         bbox=bbox,
         layout =layout,
         vertex_size=Vsize,
         edge_arrow_size=1,
         edge_width=0.5,
         edge_color="orange",
         vertex_label_size=10,
         vertex_label=label,
         vertex_label_color="#000000",
         directed=True,
         byrow = True,
         vertex_color = [color_dict[i % 50] for i in range(0,result.__len__(),1)])
    p.save(homeindex+"demo/static/dv/%s/com.png"%username)
    p.remove(g)
    return g

def denCom(density,comLin,result,username=None):
    sortden=sorted(density.items(),key=lambda e:e[1],reverse=True)
    den=[]
    count =0
    for i in sortden:
        den.append(i[0])
        if count == 2 :break
        count +=1
    g=Graph(1)
    g.add_vertices(result.__len__()-1)
    label=[]
    for i in range(0,comLin.__len__(),1):
        # label.append("com%s"%(i+1))
        for j in range(0,comLin.__len__(),1):
            if(comLin[i][j] > 0):
                g.add_edges((i,j))
    Vsize=[]
    if comLin.__len__()<=15:
        vs=50
        layout=g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    else:
        vs=30
        layout = g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    for i in range(0,result.__len__(),1):
        if( i == den[0]):
            density[i] = round(density[i], 3)
            label.append("com%s\np:%s"%((i+1),density[i]))
            Vsize.append(vs*2)
        elif( i == den[1]):
            density[i] = round(density[i], 3)
            label.append("com%s\np:%s"%((i+1),density[i]))
            Vsize.append(vs*1.5)
        elif( i == den[2]):
            density[i] = round(density[i], 3)
            label.append("com%s\np:%s"%((i+1),density[i]))
            Vsize.append(vs*1.5)
        else:
            Vsize.append(vs)
            label.append("com%s"%(i+1))
    g = g.simplify(g)
    p = Plot()
    p.background = "#ffffff"
    p.add(g,
         bbox=bbox,
         layout =layout,
         vertex_size=Vsize,
         edge_arrow_size=1,
         edge_width=0.5,
         edge_color="orange",
         vertex_label_size=10,
         vertex_label=label,
         vertex_label_color="#000000",
         directed=True,
         byrow = True,
         vertex_color = [color_dict[i % 50] for i in range(0,result.__len__(),1)])
    p.save(homeindex+"demo/static/dv/%s/dencom.png"%username)
    p.remove(g)
    return g
def XiaoLin(DaL,result):
    maxt=-8899
    for i in result:
        maxt=max(maxt,i)
    XiaoL=[[0 for i in range(len(DaL))]for j in range(len(DaL))]
    for i in result:
        for j in result:
                XiaoL[i][j]=DaL[i][j]
    return XiaoL

def DianduZhongxindu(L,vex):
    Zhongxindu={}
    for i in range(0,vex,1):
        k=0
        for j in range(0,vex,1):
            k+=(L[i][j]+L[j][i])
        k=k/(2*vex-1)
        Zhongxindu[i]=k
    sortDian=sorted(Zhongxindu.items(),key=lambda e:e[1],reverse=True)
    topp=[]
    for i in range(0,10,1):
        topp.append([sortDian[i][0],sortDian[i][1]])
    least=sortDian[-10:]
    return Zhongxindu ,sortDian,topp,least

def DianduZhongxinshi(L,vex):
    Zhongxindu,sort,a,b=DianduZhongxindu(L,vex)
    Zhongxinshi=0
    for i in range(vex):
         Zhongxinshi+=(sort[0][1]-Zhongxindu[i])
    return Zhongxinshi/(1.0*(vex-2))

def centralization(L,result):
    AllZhongxinshi={}
    for i in range(result.__len__()):
        XL=XiaoLin(L,result[i])
        AllZhongxinshi[i]=DianduZhongxinshi(XL,XL.__len__())
        del XL
    print "quincy 点度中心势: ", AllZhongxinshi
    sortDian=sorted(AllZhongxinshi.items(),key=lambda e:e[1],reverse=True)
    print "quincy 点度中心势: ", sortDian
    top=[]
    for i in range(0,3,1):
        top.append([sortDian[i][0]])
    print  "quincy 点度中心势: ",top
    return top,sortDian

def drawCentralization(L,result,username=None):
    top,sortdian=centralization(L,result)
    comLin=ComWi(L,result)
    g=Graph(1)
    g.add_vertices(result.__len__()-1)
    label=[]
    for i in range(0,comLin.__len__(),1):
        for j in range(0,comLin.__len__(),1):
            if(comLin[i][j] > 0):
                g.add_edges((i,j))
    Vsize=[]
    g = g.simplify(g)
    if comLin.__len__()<=15:
        vs=50
        layout = g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    else:
        vs=30
        layout = g.layout_graphopt()
        bbox=(100, 100, 500, 500)
    for i in range(0,result.__len__(),1):
        if( i == top[0][0]):
            x=round(sortdian[0][1],3)
            label.append("com%s\ncenter:%s"%((i+1),x))
            Vsize.append(vs*2)
        elif( i == top[1][0]):
            x=round(sortdian[1][1],3)
            label.append("com%s\ncenter:%s"%((i+1),x))
            Vsize.append(vs*1.5)
        elif( i == top[2][0]):
            x=round(sortdian[2][1],3)
            label.append("com%s\ncenter:%s"%((i+1),x))
            Vsize.append(vs*1.5)
        else:
            label.append("com%s"%(i+1))
            Vsize.append(vs)
    p = Plot()
    p.background = "#ffffff"
    p.add(g,
         bbox=bbox,
         layout =layout,
         vertex_size=Vsize,
         edge_arrow_size=1,
         edge_width=0.5,
         edge_color="orange",
         vertex_label_size=10,
         vertex_label=label,
         vertex_label_color="#000000",
         directed=True,
         byrow = True,
         vertex_color = [color_dict[i % 50] for i in range(0,result.__len__(),1)])
    p.save(homeindex+"demo/static/dv/%s/center.png"%username)
    p.remove(g)

import numpy as np
import networkx as nx
import scipy
def tezhenzhi(L):
    Graph=Lin2Graph(L,L.__len__())
    #adjacency = np.array(nx.adjacency_matrix(Graph).todense())
    #normalize_laplacian = nx.normalized_laplacian_matrix(Graph)
    #normalize_laplacian = normalize_laplacian.todense()
    size = len(L)-1
    eigenvalue, eigenvector = scipy.sparse.linalg.eigsh(np.asarray(L),size)
    print "tezhenzhi",eigenvalue
    value={}
    i=0
    for v in eigenvalue:
        value[i]=v
        i += 1
    print value
    sortDian=sorted(value.items(),key=lambda e:e[1],reverse=True)
    print sortDian

def drawe(L,result,listresult,labelresult,i,username=None):
        i=i-1
        vs=20
        gg=Graph(1)
        gg.add_vertices(result[i].__len__()-1)
        matrix = [[0 for col in range(result[i].__len__())] for row in range(result[i].__len__())]
        for j in range(0,result[i].__len__(),1):
            for k in range(0,result[i].__len__(),1):
                if (L[result[i][j]][result[i][k]]) > 0:
                    gg.add_edge(j,k)
                    matrix[j][k]=L[result[i][j]][result[i][k]]
        center,sortDian=centerzation(matrix,result[i].__len__())
        dc=DegreeCenterzation(matrix,result[i].__len__())
        Vsize=[]
        for j in range(0,result[i].__len__(),1):
            if j == sortDian[0][0]:
                Vsize.append(vs*3)
            else:
                Vsize.append(vs)
        gg=gg.simplify(gg)
        print result[i].__len__()
        print gg.ecount()
        density= Density(matrix,result[i].__len__())
        print dc
        # layout=gg.layout_graphopt()
        layout=gg.layout("fr")
        c=result[i][0]
        c=listresult[c]
        label=[]
        for j in labelresult[i]:
           label.append(j)
        gg.vs["label"]=label
        file_o= codecs.open(homeindex+'demo/static/js/drawgraph/graph.js', 'r','utf-8')
        text =file_o.read()
        print text
        tag = 1
        if os.path.exists(homeindex+"demo/static/js/drawgraph/%s" % username):
             tag = 0
        if tag == 1:
             os.mkdir(homeindex+"demo/static/js/drawgraph/%s" % username)
        file_object= codecs.open(homeindex+'demo/static/js/drawgraph/%s/graph.js'%username, 'w','utf-8')
        file_object.write(text)
        file_object.write("var nodes=[\n")
        for la in label:
            file_object.write("    {id:'")
            file_object.write(la)
            file_object.write("',type:'switch',status:1},\n")
            # file_object.write("    {id:'%s',type:'switch',status:1},\n"%la)
        file_object.write("];\n\n\n")
        file_object.write("var links=[\n")
        for p in range(0,result[i].__len__(),1):
            for q in range(0,result[i].__len__(),1):
                if matrix[p][q] > 0:
                    file_object.write("    {source:'")
                    file_object.write(label[p])
                    file_object.write("',target:'")
                    file_object.write(label[q])
                    file_object.write("'},\n")
        file_object.write("];\n\n\n")
        file_object.write("topology.addNodes(nodes);\n")
        file_object.write("topology.addLinks(links);\n")
        file_object.write("topology.setNodeClickFn(function(node){\n")
        file_object.write("    if(!node['_expanded']){\n")
        file_object.write("        expandNode(node.id);\n")
        file_object.write("        node['_expanded']=true;\n")
        file_object.write("    }else{\n")
        file_object.write("        collapseNode(node.id);\n")
        file_object.write("        node['_expanded']=false;\n")
        file_object.write("     }\n")
        file_object.write("});\n")
        file_object.write("topology.update();\n\n\n\n")
        file_object.write("function expandNode(id){\n")
        file_object.write("    topology.addNodes(childNodes);\n")
        file_object.write("    topology.addLinks(childLinks);\n")
        file_object.write("    topology.update();\n")
        file_object.write("}\n\n\n")
        file_object.write("function collapseNode(id){\n")
        file_object.write("    topology.removeChildNodes(id);\n")
        file_object.write("    topology.update();\n")
        file_object.write("}\n")
        file_object.close()
        if( os.path.exists(homeindex+"demo/static/dv/%s/community%s.png"%(username,(i+1)))):
            del matrix
            return result[i].__len__() , gg.ecount(),density, dc
        plot(gg,homeindex+"demo/static/dv/%s/community%s.png"%(username,(i+1)),layout =layout,vertex_size=Vsize,edge_color="grey",vertex_color = color_dict[c%50])
        del matrix
        return result[i].__len__() , gg.ecount(),density, dc
