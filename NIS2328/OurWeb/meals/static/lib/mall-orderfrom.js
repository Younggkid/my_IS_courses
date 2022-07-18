var a=angular.module("orderfrom",[]);

a.controller("orderfromctrl",function($scope,$http){
    $scope.cartlist=[];//餐饮购物车信息
    $scope.orderinfo="";
    $scope.orderadress="";
   
    //初始化页面
    $scope.init1=function(){
    	
    	var f=$http.post("http://127.0.0.1:8080/Carts/useq/"+$scope.useq).success(function (data) {
                    console.log(data);
               });
        f.success(function(data){
            $scope.cartlist=data; 
        });
        console.log($scope.cartlist)
    };
    $scope.init1();
    
    $scope.commit=function(){
    	$scope.useq=window.localStorage.getItem("userId");
    	var data = {
    		"useq":$scope.useq,
    		"info":$scope.orderinfo,
    		"adress":$scope.orderadress
    	}
    	var f=$http.post("http://127.0.0.1:8080/Cateringorder",data).success(function (data) {
                    console.log(data);
               });
        f.success(function(data){
            swal({
	                title: "跳转至支付",
	                text: "客官请付款",
	                type: "success"
            	});
            	window.location.href="mall-pay.html";
        });
        
    };
    
});