var a=angular.module("caterInfo",[]);

a.controller("caterInfoctrl",function($scope,$http){
    $scope.cateringInfo="";
    $scope.seq ="";
    $scope.num =1;
   	
    //初始化
    $scope.init1=function(){
    	$scope.seq=window.localStorage.getItem("menucseq");
    	var f=$http.get("http://127.0.0.1:8080/Cateringinfo/id/"+$scope.seq).success(function (data) {
                    console.log(data);
               });
        f.success(function(data){
            $scope.cateringInfo=data;
        });
    };
    $scope.init1();
    
});