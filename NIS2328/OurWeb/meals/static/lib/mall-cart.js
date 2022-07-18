var a=angular.module("cartlist",[]);

a.controller("cartlistctrl",function($scope,$http){
    $scope.cartlist=[];//餐饮类型信息
    $scope.total = 0;
   	$scope.useq="";
   	$scope.discount="";
   	$scope.des="";
   	$scope.isLogin = "0";
   	
   	//获取登录内初始化信息
    $scope.initAdminInfo = function(){
    	//window.localStorage.setItem("userId","");
        $http.get("http://127.0.0.1:8080/UserInfo/index",{ withCredentials:true}).success(function (data) {
            console.log(data)
            if(data.status=="0"){
                $scope.isLogin="0";
                swal({
	                title: "未登入",
	                text: "赶紧登入吧",
	                type: "warning"
            	},function () {
            		window.location.href="mall-index.html";
            	});
            }else{
                $scope.isLogin="1";
                //$scope.useq =data.userInfo.seq;
              	window.localStorage.setItem("userId",data.userInfo.seq);
              }
        });
    }
    $scope.initAdminInfo();
    
    //获取登录内初始化信息
    $scope.initUserInfo = function(){
    	$scope.useq=window.localStorage.getItem("userId");
    	console.log($scope.useq)
        $http.get("http://127.0.0.1:8080/Userinfo/useq/"+$scope.useq).success(function (data) {
            console.log(data)
            if(data==null){
                $scope.discount=1;
                $scope.des="普通会员";
            }else{
            	$scope.des=data.des;
                $scope.discount = data.discount;
              }
        });
    }
    $scope.initUserInfo();
   	
    
    var config = {
    	headers:{'Content-Type':'application/json'}
    };
    //初始化页面
    $scope.init1=function(){
    	$scope.useq=window.localStorage.getItem("userId");
    		console.log($scope.useq.length);
    	if($scope.useq.length == 0 ||$scope.useq == null ||$scope.useq ==""){
    		console.log($scope.useq);
    		swal({
	                title: "未登入",
	                text: "赶紧登入吧",
	                type: "warning"
            	},function () {
            		window.location.href="mall-index.html";
            	});
    	}else{
    	console.log($scope.useq);
    	
    	var f=$http.post("http://127.0.0.1:8080/Carts/useq/"+$scope.useq).success(function (data) {
                    console.log(data);
               });
        f.success(function(data){
            $scope.cartlist=data;
            if($scope.cartlist.length==0){
            	swal({
	                title: "当前购物车为空",
	                text: "赶紧去菜单中看看吧",
	                type: "success"
            	},function () {
            		window.location.href="mall-menu-list.html";
            	});
            	
            }
            $scope.totalMoney();
        });
    	}
    	
        
    };
    $scope.init1();
    
    $scope.pay=function(){
     	window.location.href="mall-orderfrom.html";
    };
    
    //点击加减按钮，数量加减;
	$scope.reduce=function(cart){
		cart.num--;
		if (cart.num<=0) cart.num=0;
		$scope.updateNum(cart);
		$scope.totalMoney();
	};
      
    $scope.add=function(cart){
        cart.num++;
        $scope.updateNum(cart);
        $scope.totalMoney();
    };
    
    $scope.updateNum=function(cart){
    	var seq = cart.seq;
    	var num = cart.num;
    	var data = {
    		"seq":seq,
    		"num":num
    	}
    	console.log(data);
    	var f=$http.put("http://127.0.0.1:8080/Cart/id/"+seq,data).success(function (data) {
                    console.log(data);
               });
        f.success(function(data){

        });
    };
    
    /*总金额计算*/
    $scope.totalMoney=function(){
    	var total=0;
    	for(var i=0;i<$scope.cartlist.length;i++){
         	total +=$scope.cartlist[i].price*$scope.cartlist[i].num;
    	}
    	$scope.total = total;
  	};
  	
  	 //删除
    $scope.del=function(seq){
    	//alert(seq);
        var f=$http.delete("http://127.0.0.1:8080/Cart/id/"+seq).success(function (data) {
                console.log(data);
           }).success(function(data){
           	swal({
	                title: "删除成功",
	                text: "赶紧去菜单中看看吧",
	                type: "warning"
            	},function () {
        		window.location.href="mall-cart.html";
    		});
           	
        });
    }
});