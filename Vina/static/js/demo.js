$(document).ready(function(){
	$.ajax({
		url:"../php/demo.php",//目标数据源页面
		type:"post",
		date:{id:"1"},//自己要给目标页面传的参数
		sucess:function(result){//访问成功后的回调方法，result是服务端返回的内容，如果是json字符串则自动会解析
			var result2 = new array();
			for(var i=0;i<result.length;i++){//注意要将字符串转成int
				result2[i] = parseInt(result[i]);
			}
			$("#container").highcharts({
	            chart: {
	                type: 'pie',
	                height: 200,
	                width: 400,
	                backgroundColor: 'rgba(0,0,0,0)'
	            },
	            title: {
	                text: null,
	            },
	            tooltip: {
	                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	            },
	            series: [{
	                    type: 'pie',
	                    name: 'Browser share',
	                    data: result2, //将返回后处理的数据赋给highcharts
	                }]
	        });
	    }
	})
	
});