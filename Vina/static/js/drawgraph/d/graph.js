function Topology(ele){
    typeof(ele)=='string' && (ele=document.getElementById(ele));
    var w=ele.clientWidth,
        h=ele.clientHeight,
        self=this;
    this.force = d3.layout.force().gravity(.05).distance(200).charge(-800).size([w, h]);
    this.nodes=this.force.nodes();
    this.links=this.force.links();
    this.clickFn=function(){};
    this.vis = d3.select(ele).append("svg:svg")
                 .attr("width", w).attr("height", h).attr("pointer-events", "all");

    this.force.on("tick", function(x) {
      self.vis.selectAll("g.node")
          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

      self.vis.selectAll("line.link")
          .attr("x1", function(d) { return d.source.x; })
          .attr("y1", function(d) { return d.source.y; })
          .attr("x2", function(d) { return d.target.x; })
          .attr("y2", function(d) { return d.target.y; });
    });
}


Topology.prototype.doZoom=function(){
    d3.select(this).select('g').attr("transform","translate(" + d3.event.translate + ")"+ " scale(" + d3.event.scale + ")");

}


//\D4\F6\BCӽڵ\E3
Topology.prototype.addNode=function(node){
    this.nodes.push(node);
}

Topology.prototype.addNodes=function(nodes){
    if (Object.prototype.toString.call(nodes)=='[object Array]' ){
        var self=this;
        nodes.forEach(function(node){
            self.addNode(node);
        });

    }
}

//\D4\F6\BC\D3\C1\AC\CF\DF
Topology.prototype.addLink=function(source,target){
    this.links.push({source:this.findNode(source),target:this.findNode(target)});
}
//\D4\F6\BCӶ\E0\B8\F6\C1\AC\CF\DF
Topology.prototype.addLinks=function(links){
    if (Object.prototype.toString.call(links)=='[object Array]' ){
        var self=this;
        links.forEach(function(link){
            self.addLink(link['source'],link['target']);
        });
    }
}


//ɾ\B3\FD\BDڵ\E3
Topology.prototype.removeNode=function(id){
    var i=0,
        n=this.findNode(id),
        links=this.links;
    while ( i < links.length){
        links[i]['source']==n || links[i]['target'] ==n ? links.splice(i,1) : ++i;
    }
    this.nodes.splice(this.findNodeIndex(id),1);
}

//ɾ\B3\FD\BDڵ\E3\CFµ\C4\D7ӽڵ㣬ͬʱ\C7\E5\B3\FDlink\D0\C5Ϣ
Topology.prototype.removeChildNodes=function(id){
    var node=this.findNode(id),
        nodes=this.nodes;
        links=this.links,
        self=this;

    var linksToDelete=[],
        childNodes=[];
    
    links.forEach(function(link,index){
        link['source']==node 
            && linksToDelete.push(index) 
            && childNodes.push(link['target']);
    });

    linksToDelete.reverse().forEach(function(index){
        links.splice(index,1);
    });

    var remove=function(node){
        var length=links.length;
        for(var i=length-1;i>=0;i--){
            if (links[i]['source'] == node ){
               var target=links[i]['target'];
               links.splice(i,1);
               nodes.splice(self.findNodeIndex(node.id),1);
               remove(target);
               
            }
        }
    }

    childNodes.forEach(function(node){
        remove(node);
    });

    //\C7\E5\B3\FDû\D3\D0\C1\AC\CFߵĽڵ\E3
    for(var i=nodes.length-1;i>=0;i--){
        var haveFoundNode=false;
        for(var j=0,l=links.length;j<l;j++){
            ( links[j]['source']==nodes[i] || links[j]['target']==nodes[i] ) && (haveFoundNode=true) 
        }
        !haveFoundNode && nodes.splice(i,1);
    }
}



//\B2\E9\D5ҽڵ\E3
Topology.prototype.findNode=function(id){
    var nodes=this.nodes;
    for (var i in nodes){
        if (nodes[i]['id']==id ) return nodes[i];
    }
    return null;
}


//\B2\E9\D5ҽڵ\E3\CB\F9\D4\DA\CB\F7\D2\FD\BA\C5
Topology.prototype.findNodeIndex=function(id){
    var nodes=this.nodes;
    for (var i in nodes){
        if (nodes[i]['id']==id ) return i;
    }
    return -1;
}

//\BDڵ\E3\B5\E3\BB\F7\CA¼\FE
Topology.prototype.setNodeClickFn=function(callback){
    this.clickFn=callback;
}

//\B8\FC\D0\C2\CD\D8\C6\CBͼ״̬\D0\C5Ϣ
Topology.prototype.update=function(){
  var link = this.vis.selectAll("line.link")
      .data(this.links, function(d) { return d.source.id + "-" + d.target.id; })
      .attr("class", function(d){
            return d['source']['status'] && d['target']['status'] ? 'link' :'link link_error';
      });

  link.enter().insert("svg:line", "g.node")
      .attr("class", function(d){
         return d['source']['status'] && d['target']['status'] ? 'link' :'link link_error';
      });

  link.exit().remove();

  var node = this.vis.selectAll("g.node")
      .data(this.nodes, function(d) { return d.id;});

  var nodeEnter = node.enter().append("svg:g")
      .attr("class", "node")
      .call(this.force.drag);

  //\D4\F6\BC\D3ͼƬ\A3\AC\BF\C9\D2Ը\F9\BE\DD\D0\E8Ҫ\C0\B4\D0޸\C4
  var self=this;
  nodeEnter.append("svg:image")
      .attr("class", "circle")
      .attr("xlink:href", function(d){
         //\B8\F9\BE\DD\C0\E0\D0\CD\C0\B4ʹ\D3\C3ͼƬ
         return d.expand ? "/home/quincy/demo/static/js/drawgraph/0.png" : "/home/quincy/demo/static/js/drawgraph/1.png";
      })
      .attr("x", "-32px")
      .attr("y", "-32px")
      .attr("width", "64px")
      .attr("height", "64px")
      .on('click',function(d){ d.expand && self.clickFn(d);})

  nodeEnter.append("svg:text")
      .attr("class", "nodetext")
      .attr("dx", 15)
      .attr("dy", -35)
      .text(function(d) { return d.id });

  
  node.exit().remove();

  this.force.start();
}




var topology=new Topology('container');




var nodes=[
    {id:'Myriel ',type:'switch',status:1},
    {id:'Napoleon ',type:'switch',status:1},
    {id:'MlleBaptistine ',type:'switch',status:1},
    {id:'MmeMagloire ',type:'switch',status:1},
    {id:'CountessDeLo ',type:'switch',status:1},
    {id:'Geborand ',type:'switch',status:1},
    {id:'Champtercier ',type:'switch',status:1},
    {id:'Cravatte ',type:'switch',status:1},
    {id:'Count ',type:'switch',status:1},
    {id:'OldMan ',type:'switch',status:1},
    {id:'Labarre ',type:'switch',status:1},
    {id:'Valjean ',type:'switch',status:1},
    {id:'Marguerite ',type:'switch',status:1},
    {id:'MmeDeR ',type:'switch',status:1},
    {id:'Isabeau ',type:'switch',status:1},
    {id:'Gervais ',type:'switch',status:1},
    {id:'Tholomyes ',type:'switch',status:1},
    {id:'Listolier ',type:'switch',status:1},
    {id:'Fameuil ',type:'switch',status:1},
    {id:'Blacheville ',type:'switch',status:1},
    {id:'Favourite ',type:'switch',status:1},
    {id:'Dahlia ',type:'switch',status:1},
    {id:'Zephine ',type:'switch',status:1},
    {id:'Fantine ',type:'switch',status:1},
    {id:'MmeThenardier ',type:'switch',status:1},
    {id:'Thenardier ',type:'switch',status:1},
    {id:'Cosette ',type:'switch',status:1},
    {id:'Javert ',type:'switch',status:1},
    {id:'Fauchelevent ',type:'switch',status:1},
    {id:'Bamatabois ',type:'switch',status:1},
    {id:'Perpetue ',type:'switch',status:1},
    {id:'Simplice ',type:'switch',status:1},
    {id:'Scaufflaire ',type:'switch',status:1},
    {id:'Woman1 ',type:'switch',status:1},
    {id:'Judge ',type:'switch',status:1},
    {id:'Champmathieu ',type:'switch',status:1},
    {id:'Brevet ',type:'switch',status:1},
    {id:'Chenildieu ',type:'switch',status:1},
    {id:'Cochepaille ',type:'switch',status:1},
    {id:'Pontmercy ',type:'switch',status:1},
    {id:'Boulatruelle ',type:'switch',status:1},
    {id:'Eponine ',type:'switch',status:1},
    {id:'Anzelma ',type:'switch',status:1},
    {id:'Woman2 ',type:'switch',status:1},
    {id:'MotherInnocent ',type:'switch',status:1},
    {id:'Gribier ',type:'switch',status:1},
    {id:'Jondrette ',type:'switch',status:1},
    {id:'MmeBurgon ',type:'switch',status:1},
    {id:'Gavroche ',type:'switch',status:1},
    {id:'Gillenormand ',type:'switch',status:1},
    {id:'Magnon ',type:'switch',status:1},
    {id:'MlleGillenormand ',type:'switch',status:1},
    {id:'MmePontmercy ',type:'switch',status:1},
    {id:'MlleVaubois ',type:'switch',status:1},
    {id:'LtGillenormand ',type:'switch',status:1},
    {id:'Marius ',type:'switch',status:1},
    {id:'BaronessT ',type:'switch',status:1},
    {id:'Mabeuf ',type:'switch',status:1},
    {id:'Enjolras ',type:'switch',status:1},
    {id:'Combeferre ',type:'switch',status:1},
    {id:'Prouvaire ',type:'switch',status:1},
    {id:'Feuilly ',type:'switch',status:1},
    {id:'Courfeyrac ',type:'switch',status:1},
    {id:'Bahorel ',type:'switch',status:1},
    {id:'Bossuet ',type:'switch',status:1},
    {id:'Joly ',type:'switch',status:1},
    {id:'Grantaire ',type:'switch',status:1},
    {id:'MotherPlutarch ',type:'switch',status:1},
    {id:'Gueulemer ',type:'switch',status:1},
    {id:'Babet ',type:'switch',status:1},
    {id:'Claquesous ',type:'switch',status:1},
    {id:'Montparnasse ',type:'switch',status:1},
    {id:'Toussaint ',type:'switch',status:1},
    {id:'Child1 ',type:'switch',status:1},
    {id:'Child2 ',type:'switch',status:1},
    {id:'Brujon ',type:'switch',status:1},
    {id:'MmeHucheloup ',type:'switch',status:1},
];


var links=[
    {source:'Napoleon ',target:'Myriel '},
    {source:'MlleBaptistine ',target:'Myriel '},
    {source:'MmeMagloire ',target:'Myriel '},
    {source:'MmeMagloire ',target:'MlleBaptistine '},
    {source:'CountessDeLo ',target:'Myriel '},
    {source:'Geborand ',target:'Myriel '},
    {source:'Champtercier ',target:'Myriel '},
    {source:'Cravatte ',target:'Myriel '},
    {source:'Count ',target:'Myriel '},
    {source:'OldMan ',target:'Myriel '},
    {source:'Valjean ',target:'Myriel '},
    {source:'Valjean ',target:'MlleBaptistine '},
    {source:'Valjean ',target:'MmeMagloire '},
    {source:'Valjean ',target:'Labarre '},
    {source:'Marguerite ',target:'Valjean '},
    {source:'MmeDeR ',target:'Valjean '},
    {source:'Isabeau ',target:'Valjean '},
    {source:'Gervais ',target:'Valjean '},
    {source:'Listolier ',target:'Tholomyes '},
    {source:'Fameuil ',target:'Tholomyes '},
    {source:'Fameuil ',target:'Listolier '},
    {source:'Blacheville ',target:'Tholomyes '},
    {source:'Blacheville ',target:'Listolier '},
    {source:'Blacheville ',target:'Fameuil '},
    {source:'Favourite ',target:'Tholomyes '},
    {source:'Favourite ',target:'Listolier '},
    {source:'Favourite ',target:'Fameuil '},
    {source:'Favourite ',target:'Blacheville '},
    {source:'Dahlia ',target:'Tholomyes '},
    {source:'Dahlia ',target:'Listolier '},
    {source:'Dahlia ',target:'Fameuil '},
    {source:'Dahlia ',target:'Blacheville '},
    {source:'Dahlia ',target:'Favourite '},
    {source:'Zephine ',target:'Tholomyes '},
    {source:'Zephine ',target:'Listolier '},
    {source:'Zephine ',target:'Fameuil '},
    {source:'Zephine ',target:'Blacheville '},
    {source:'Zephine ',target:'Favourite '},
    {source:'Zephine ',target:'Dahlia '},
    {source:'Fantine ',target:'Valjean '},
    {source:'Fantine ',target:'Marguerite '},
    {source:'Fantine ',target:'Tholomyes '},
    {source:'Fantine ',target:'Listolier '},
    {source:'Fantine ',target:'Fameuil '},
    {source:'Fantine ',target:'Blacheville '},
    {source:'Fantine ',target:'Favourite '},
    {source:'Fantine ',target:'Dahlia '},
    {source:'Fantine ',target:'Zephine '},
    {source:'MmeThenardier ',target:'Valjean '},
    {source:'MmeThenardier ',target:'Fantine '},
    {source:'Thenardier ',target:'Valjean '},
    {source:'Thenardier ',target:'Fantine '},
    {source:'Thenardier ',target:'MmeThenardier '},
    {source:'Cosette ',target:'Valjean '},
    {source:'Cosette ',target:'Tholomyes '},
    {source:'Cosette ',target:'MmeThenardier '},
    {source:'Cosette ',target:'Thenardier '},
    {source:'Javert ',target:'Valjean '},
    {source:'Javert ',target:'Fantine '},
    {source:'Javert ',target:'MmeThenardier '},
    {source:'Javert ',target:'Thenardier '},
    {source:'Javert ',target:'Cosette '},
    {source:'Fauchelevent ',target:'Valjean '},
    {source:'Fauchelevent ',target:'Javert '},
    {source:'Bamatabois ',target:'Valjean '},
    {source:'Bamatabois ',target:'Fantine '},
    {source:'Bamatabois ',target:'Javert '},
    {source:'Perpetue ',target:'Fantine '},
    {source:'Simplice ',target:'Valjean '},
    {source:'Simplice ',target:'Fantine '},
    {source:'Simplice ',target:'Javert '},
    {source:'Simplice ',target:'Perpetue '},
    {source:'Scaufflaire ',target:'Valjean '},
    {source:'Woman1 ',target:'Valjean '},
    {source:'Woman1 ',target:'Javert '},
    {source:'Judge ',target:'Valjean '},
    {source:'Judge ',target:'Bamatabois '},
    {source:'Champmathieu ',target:'Valjean '},
    {source:'Champmathieu ',target:'Bamatabois '},
    {source:'Champmathieu ',target:'Judge '},
    {source:'Brevet ',target:'Valjean '},
    {source:'Brevet ',target:'Bamatabois '},
    {source:'Brevet ',target:'Judge '},
    {source:'Brevet ',target:'Champmathieu '},
    {source:'Chenildieu ',target:'Valjean '},
    {source:'Chenildieu ',target:'Bamatabois '},
    {source:'Chenildieu ',target:'Judge '},
    {source:'Chenildieu ',target:'Champmathieu '},
    {source:'Chenildieu ',target:'Brevet '},
    {source:'Cochepaille ',target:'Valjean '},
    {source:'Cochepaille ',target:'Bamatabois '},
    {source:'Cochepaille ',target:'Judge '},
    {source:'Cochepaille ',target:'Champmathieu '},
    {source:'Cochepaille ',target:'Brevet '},
    {source:'Cochepaille ',target:'Chenildieu '},
    {source:'Pontmercy ',target:'Thenardier '},
    {source:'Boulatruelle ',target:'Thenardier '},
    {source:'Eponine ',target:'MmeThenardier '},
    {source:'Eponine ',target:'Thenardier '},
    {source:'Anzelma ',target:'MmeThenardier '},
    {source:'Anzelma ',target:'Thenardier '},
    {source:'Anzelma ',target:'Eponine '},
    {source:'Woman2 ',target:'Valjean '},
    {source:'Woman2 ',target:'Cosette '},
    {source:'Woman2 ',target:'Javert '},
    {source:'MotherInnocent ',target:'Valjean '},
    {source:'MotherInnocent ',target:'Fauchelevent '},
    {source:'Gribier ',target:'Fauchelevent '},
    {source:'MmeBurgon ',target:'Jondrette '},
    {source:'Gavroche ',target:'Valjean '},
    {source:'Gavroche ',target:'Thenardier '},
    {source:'Gavroche ',target:'Javert '},
    {source:'Gavroche ',target:'MmeBurgon '},
    {source:'Gillenormand ',target:'Valjean '},
    {source:'Gillenormand ',target:'Cosette '},
    {source:'Magnon ',target:'MmeThenardier '},
    {source:'Magnon ',target:'Gillenormand '},
    {source:'MlleGillenormand ',target:'Valjean '},
    {source:'MlleGillenormand ',target:'Cosette '},
    {source:'MlleGillenormand ',target:'Gillenormand '},
    {source:'MmePontmercy ',target:'Pontmercy '},
    {source:'MmePontmercy ',target:'MlleGillenormand '},
    {source:'MlleVaubois ',target:'MlleGillenormand '},
    {source:'LtGillenormand ',target:'Cosette '},
    {source:'LtGillenormand ',target:'Gillenormand '},
    {source:'LtGillenormand ',target:'MlleGillenormand '},
    {source:'Marius ',target:'Valjean '},
    {source:'Marius ',target:'Tholomyes '},
    {source:'Marius ',target:'Thenardier '},
    {source:'Marius ',target:'Cosette '},
    {source:'Marius ',target:'Pontmercy '},
    {source:'Marius ',target:'Eponine '},
    {source:'Marius ',target:'Gavroche '},
    {source:'Marius ',target:'Gillenormand '},
    {source:'Marius ',target:'MlleGillenormand '},
    {source:'Marius ',target:'LtGillenormand '},
    {source:'BaronessT ',target:'Gillenormand '},
    {source:'BaronessT ',target:'Marius '},
    {source:'Mabeuf ',target:'Eponine '},
    {source:'Mabeuf ',target:'Gavroche '},
    {source:'Mabeuf ',target:'Marius '},
    {source:'Enjolras ',target:'Valjean '},
    {source:'Enjolras ',target:'Javert '},
    {source:'Enjolras ',target:'Gavroche '},
    {source:'Enjolras ',target:'Marius '},
    {source:'Enjolras ',target:'Mabeuf '},
    {source:'Combeferre ',target:'Gavroche '},
    {source:'Combeferre ',target:'Marius '},
    {source:'Combeferre ',target:'Mabeuf '},
    {source:'Combeferre ',target:'Enjolras '},
    {source:'Prouvaire ',target:'Gavroche '},
    {source:'Prouvaire ',target:'Enjolras '},
    {source:'Prouvaire ',target:'Combeferre '},
    {source:'Feuilly ',target:'Gavroche '},
    {source:'Feuilly ',target:'Marius '},
    {source:'Feuilly ',target:'Mabeuf '},
    {source:'Feuilly ',target:'Enjolras '},
    {source:'Feuilly ',target:'Combeferre '},
    {source:'Feuilly ',target:'Prouvaire '},
    {source:'Courfeyrac ',target:'Eponine '},
    {source:'Courfeyrac ',target:'Gavroche '},
    {source:'Courfeyrac ',target:'Marius '},
    {source:'Courfeyrac ',target:'Mabeuf '},
    {source:'Courfeyrac ',target:'Enjolras '},
    {source:'Courfeyrac ',target:'Combeferre '},
    {source:'Courfeyrac ',target:'Prouvaire '},
    {source:'Courfeyrac ',target:'Feuilly '},
    {source:'Bahorel ',target:'Gavroche '},
    {source:'Bahorel ',target:'Marius '},
    {source:'Bahorel ',target:'Mabeuf '},
    {source:'Bahorel ',target:'Enjolras '},
    {source:'Bahorel ',target:'Combeferre '},
    {source:'Bahorel ',target:'Prouvaire '},
    {source:'Bahorel ',target:'Feuilly '},
    {source:'Bahorel ',target:'Courfeyrac '},
    {source:'Bossuet ',target:'Valjean '},
    {source:'Bossuet ',target:'Gavroche '},
    {source:'Bossuet ',target:'Marius '},
    {source:'Bossuet ',target:'Mabeuf '},
    {source:'Bossuet ',target:'Enjolras '},
    {source:'Bossuet ',target:'Combeferre '},
    {source:'Bossuet ',target:'Prouvaire '},
    {source:'Bossuet ',target:'Feuilly '},
    {source:'Bossuet ',target:'Courfeyrac '},
    {source:'Bossuet ',target:'Bahorel '},
    {source:'Joly ',target:'Gavroche '},
    {source:'Joly ',target:'Marius '},
    {source:'Joly ',target:'Mabeuf '},
    {source:'Joly ',target:'Enjolras '},
    {source:'Joly ',target:'Combeferre '},
    {source:'Joly ',target:'Prouvaire '},
    {source:'Joly ',target:'Feuilly '},
    {source:'Joly ',target:'Courfeyrac '},
    {source:'Joly ',target:'Bahorel '},
    {source:'Joly ',target:'Bossuet '},
    {source:'Grantaire ',target:'Gavroche '},
    {source:'Grantaire ',target:'Enjolras '},
    {source:'Grantaire ',target:'Combeferre '},
    {source:'Grantaire ',target:'Prouvaire '},
    {source:'Grantaire ',target:'Feuilly '},
    {source:'Grantaire ',target:'Courfeyrac '},
    {source:'Grantaire ',target:'Bahorel '},
    {source:'Grantaire ',target:'Bossuet '},
    {source:'Grantaire ',target:'Joly '},
    {source:'MotherPlutarch ',target:'Mabeuf '},
    {source:'Gueulemer ',target:'Valjean '},
    {source:'Gueulemer ',target:'MmeThenardier '},
    {source:'Gueulemer ',target:'Thenardier '},
    {source:'Gueulemer ',target:'Javert '},
    {source:'Gueulemer ',target:'Eponine '},
    {source:'Gueulemer ',target:'Gavroche '},
    {source:'Babet ',target:'Valjean '},
    {source:'Babet ',target:'MmeThenardier '},
    {source:'Babet ',target:'Thenardier '},
    {source:'Babet ',target:'Javert '},
    {source:'Babet ',target:'Eponine '},
    {source:'Babet ',target:'Gavroche '},
    {source:'Babet ',target:'Gueulemer '},
    {source:'Claquesous ',target:'Valjean '},
    {source:'Claquesous ',target:'MmeThenardier '},
    {source:'Claquesous ',target:'Thenardier '},
    {source:'Claquesous ',target:'Javert '},
    {source:'Claquesous ',target:'Eponine '},
    {source:'Claquesous ',target:'Enjolras '},
    {source:'Claquesous ',target:'Gueulemer '},
    {source:'Claquesous ',target:'Babet '},
    {source:'Montparnasse ',target:'Valjean '},
    {source:'Montparnasse ',target:'Thenardier '},
    {source:'Montparnasse ',target:'Javert '},
    {source:'Montparnasse ',target:'Eponine '},
    {source:'Montparnasse ',target:'Gavroche '},
    {source:'Montparnasse ',target:'Gueulemer '},
    {source:'Montparnasse ',target:'Babet '},
    {source:'Montparnasse ',target:'Claquesous '},
    {source:'Toussaint ',target:'Valjean '},
    {source:'Toussaint ',target:'Cosette '},
    {source:'Toussaint ',target:'Javert '},
    {source:'Child1 ',target:'Gavroche '},
    {source:'Child2 ',target:'Gavroche '},
    {source:'Child2 ',target:'Child1 '},
    {source:'Brujon ',target:'Thenardier '},
    {source:'Brujon ',target:'Eponine '},
    {source:'Brujon ',target:'Gavroche '},
    {source:'Brujon ',target:'Gueulemer '},
    {source:'Brujon ',target:'Babet '},
    {source:'Brujon ',target:'Claquesous '},
    {source:'Brujon ',target:'Montparnasse '},
    {source:'MmeHucheloup ',target:'Gavroche '},
    {source:'MmeHucheloup ',target:'Enjolras '},
    {source:'MmeHucheloup ',target:'Courfeyrac '},
    {source:'MmeHucheloup ',target:'Bahorel '},
    {source:'MmeHucheloup ',target:'Bossuet '},
    {source:'MmeHucheloup ',target:'Joly '},
    {source:'MmeHucheloup ',target:'Grantaire '},
];


topology.addNodes(nodes);
topology.addLinks(links);
topology.setNodeClickFn(function(node){
    if(!node['_expanded']){
        expandNode(node.id);
        node['_expanded']=true;
    }else{
        collapseNode(node.id);
        node['_expanded']=false;
     }
});
topology.update();



function expandNode(id){
    topology.addNodes(childNodes);
    topology.addLinks(childLinks);
    topology.update();
}


function collapseNode(id){
    topology.removeChildNodes(id);
    topology.update();
}
