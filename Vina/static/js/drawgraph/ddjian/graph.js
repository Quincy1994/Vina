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
                 .attr("width", w).attr("height", h).attr("pointer-events", "all").style("fill","white");

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
         return d.expand ? "/static/js/drawgraph/0.png" : "/static/js/drawgraph/1.png";
      })
      .attr("x", "-12px")
      .attr("y", "-12px")
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
    {id:'金程',type:'switch',status:1},
    {id:'钰杏',type:'switch',status:1},
    {id:'心怡',type:'switch',status:1},
    {id:'黄河',type:'switch',status:1},
    {id:'钰琳',type:'switch',status:1},
];


var links=[
    {source:'金程',target:'钰琳'},
    {source:'钰杏',target:'心怡'},
    {source:'钰杏',target:'黄河'},
    {source:'心怡',target:'钰杏'},
    {source:'心怡',target:'黄河'},
    {source:'黄河',target:'钰杏'},
    {source:'黄河',target:'心怡'},
    {source:'钰琳',target:'金程'},
    {source:'钰琳',target:'钰杏'},
    {source:'钰琳',target:'心怡'},
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
