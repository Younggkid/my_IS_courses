var a=angular.module("pay",[]);

a.controller("payctrl",function($scope,$http){
    //初始化页面
    $scope.goto=function(){
	    swal({
            title: "付款成功",
            text: "谢谢老板！！",
            type: "success"
    	},function () {
    		window.location.href="mall-order.html";
    	});
    };
  
    
    
});