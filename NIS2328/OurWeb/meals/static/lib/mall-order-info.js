var a=angular.module("orderinfo",[]);

a.controller("orderinfoctrl",function($scope,$http){
	$scope.orderinfolist = [];
   //初始化页面
    $scope.init1=function(){
    	var oseq = window.localStorage.getItem("qoseq");
    	var f=$http.get("http://127.0.0.1:8080/Orderinfos/oseq/"+oseq).success(function (data) {
                    console.log(data);
                });
        //var f=$http.post("menus.jspx?uid="+uid);
        f.success(function(data){
            $scope.orderinfolist=data;
        });
        
    };
    $scope.init1();

});