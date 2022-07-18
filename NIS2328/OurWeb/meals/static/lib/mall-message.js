var a=angular.module("msg",[]);

a.controller("msgctrl",function($scope,$http){
    $scope.msglist=[];//餐饮信息
    $scope.currentPage = 1; // 当前页 （请求数据）
    $scope.pageSize = 8; // 每页记录数 （请求数据）
    $scope.totalCount = 0; // 总记录数 （响应数据）
    $scope.totalPages = 0; // 总页数 （根据 总记录数、每页记录数 计算 ）
    
    $scope.useq = "";
    $scope.context= "";
    $scope.username = "";
    $scope.password = "";

    $scope.username1 = "";
    $scope.password1 = "";
    $scope.password2 = "";
    $scope.isLogin = "0";
    $scope.userId = "";
    $scope.tel ="";
    $scope.memberid="";
     $scope.account = "";
    $scope.usrInfo = [];
    $scope.noticeList=[]
    $scope.tel2="";


    //用户登录
    $scope.login =function(){
        var data = {"username":$scope.username,"password":$scope.password};
        if(!$scope.username){
            alert("用户名不能为空！");
            return;
        }
        if(!$scope.password){
            alert("密码不能为空！");
            return;
        }
        var adddata = {"username":$scope.username,"password":$scope.password};
        var f=$http.post("http://127.0.0.1:8080/Userinfo/login",adddata,{ withCredentials:true}).success(function (data) {
            console.log(data);
        });
        f.success(function(data){
            if(data.status=="1"){
              alert(data.msg);
               $scope.initAdminInfo();
                setTimeout($scope.refresh,1000);
            }else{
                alert("用户名或密码不正确");
            }
        });
    }
    //页面跳转
    $scope.refresh = function () {
        this.location.href="mall-index.html";
    }

    //用户注册
    $scope.register=function(){
        var data = {"username":$scope.username1,"password":$scope.password1};
        if(!$scope.username1){
            alert("用户名不能为空！");
            return;
        }
        if(!$scope.password1){
            alert("密码不能为空！");
            return;
        }
        if(!$scope.tel2){
            alert("手机号不能为空！");
            return;
        }
        if($scope.password1!=$scope.password2){
            alert("两次输入的密码不一致！");
        }
        var adddata = {"username":$scope.username1,"password":$scope.password1,"tel":$scope.tel2};
        var f=$http.post("http://127.0.0.1:8080/Userinfo/register",adddata,{ withCredentials:true}).success(function (data) {
            console.log(data);
        });
        f.success(function(data){
            if(data.status=="1"){
                alert("注册成功，去登录！");
                setTimeout($scope.refresh,1000);
            }else if(data.status=="2"){
                alert(data.msg);
            }
            else{
              alert("注册失败！");
            }
        });
    }

    //登出
    $scope.logOut=function(){
        var f=$http.get("http://127.0.0.1:8080/Userinfo/logOut",{ withCredentials:true}).success(function (data) {
            console.log(data);
            if(data.status==1){
                alert("退出成功！");
                setTimeout($scope.refresh,800);
                window.localStorage.clear();//清除数据
            }
        });
    }
    
     //获取登录内初始化信息
    $scope.initAdminInfo = function(){
    	//window.localStorage.setItem("userId","");
        $http.get("http://127.0.0.1:8080/UserInfo/index",{ withCredentials:true}).success(function (data) {
            console.log(data)
            if(data.status=="0"){
                $scope.isLogin="0";
                
            }else{
                $scope.isLogin="1";
                $scope.useq =data.userInfo.seq;
              
              }
        });
    }
//  $scope.initAdminInfo();
    
    $scope.add=function(cseq){
     	//  	var useq = window.localStorage.getItem("");
		$scope.useq =window.localStorage.getItem("userId");
		if($scope.useq == ""||$scope.useq == null){
    		console.log($scope.useq);
    		swal({
	                title: "请登入",
	                text: "赶紧登入吧",
	                type: "warning"
            	},function () {
            		window.location.href="mall-index.html";
            	});
    	}else{
	    	var data = {
	    		"context":$scope.context,
	    		"useq":$scope.useq
	    	}
	     	var f=$http.post("http://127.0.0.1:8080/Massage",data).success(function (data) {
	            console.log(data);
	        });
	        f.success(function(data){
	            window.location.href="mall-message.html";//跳转
	        });
    	}
    }
   
    
    //加载上一页
    $scope.prev = function() {
        $scope.selectPage($scope.currentPage - 1);
    }
    //加载下一页
    $scope.next = function() {
        $scope.selectPage($scope.currentPage + 1);
    }
	//加载指定页
    $scope.selectPage = function(page) {
        // page 超出范围
        if($scope.totalPages != 0 && (page < 1 || page > $scope.totalPages)) {
            return;
        }
        var data = {
    		"page":page,
			"size":$scope.pageSize
    	}
        //发送请求
       var f=$http.post("http://127.0.0.1:8080/Massages/page",data).success(function (data) {
            console.log(data);
        });
       f.success(function(data, status, headers, config) {
            // 要在分页工具条显示所有页码 
            $scope.pageList = new Array();
            // 显示表格数据 
            $scope.msglist = data.records;
            //先根据总记录数去计算总页数
            $scope.totalCount = data.total; //总记录数
            $scope.totalPages = data.pages; //总页数
            // 更新当前显示页码 
            $scope.currentPage = page;
            //显示分页工具条中间码
            var begin; // 显示第一个页码
            var end; // 显示最后一个页码 
            // 如果每页显示10页,理论上 begin 是当前页 -5 
            begin = $scope.currentPage - 5;
            if(begin < 1) { //begin不能小于1
                begin = 1;
            }
            // 显示10个页码，理论上end 是 begin + 9
            end = begin + 9;
            if(end > $scope.totalPages) {
                //最后一页不能大于总页数
                end = $scope.totalPages;
            }
            // 修正begin 的值, 理论上 begin 是 end - 9
            begin = end - 9;
            if(begin < 1) { //begin不能小于1
                begin = 1;
            }
            // 将页码加入 PageList集合
            for(var i = begin; i <= end; i++) {
                $scope.pageList.push(i);
            }
        })
    }
    //判断是否是当前页
    $scope.isActivePage = function(page) {
        return page === $scope.currentPage;
    }
    // 初始化，选中第一页
    $scope.selectPage(1);

});