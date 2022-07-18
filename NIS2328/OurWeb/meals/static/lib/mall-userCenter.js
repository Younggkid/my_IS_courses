var a=angular.module("usercenter",[]);

a.controller("usercenterctrl",function($scope,$http){
    $scope.cateringlist=[];//餐饮信息
    $scope.cateringname= "";
    $scope.currentPage = 1; // 当前页 （请求数据）
    $scope.pageSize = 8; // 每页记录数 （请求数据）
    $scope.totalCount = 0; // 总记录数 （响应数据）
    $scope.totalPages = 0; // 总页数 （根据 总记录数、每页记录数 计算 ）


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
        if(!$scope.username){
            alert("用户名不能为空！");
            return;
        }
        if(!$scope.password){
            alert("密码不能为空！");
            return;
        }
        if($scope.password1!=$scope.password2){
            alert("两次输入的密码不一致！");
        }
        var adddata = {"username":$scope.username,"password":$scope.password};
        var f=$http.post("http://127.0.0.1:8080/Userinfo/register",adddata,{ withCredentials:true}).success(function (data) {
            console.log(data);
        });
        f.success(function(data){
            if(data.status=="1"){
                alert("注册成功，去登录！");
                setTimeout($scope.refresh,1000);
            }else{
              alert("用户名或密码不正确！");
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
    	$scope.useq =window.localStorage.getItem("userId");
    	if($scope.useq == ""||$scope.useq == null){
     		console.log($scope.useq);
    		swal({
	                title: "未登入",
	                text: "赶紧登入吧",
	                type: "warning"
            	},function () {
            		window.location.href="mall-index.html";
            	});
     	}else{
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
                $scope.userId =data.userInfo.seq;
                $scope.tel = data.userInfo.tel;
                $scope.memberid=data.userInfo.memberid;
                $scope.userInfo =data.userInfo;
                $scope.username=data.userInfo.username;
                $scope.password=data.userInfo.password;
                $scope.account = data.userInfo.account;
                
            }
        });
     	}
        
    }
    $scope.initAdminInfo();

    //修改用户信息
    $scope.edit =function(){
        var useq =window.localStorage.getItem("userId");
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
            var data={"username":$scope.username,"password":$scope.password,"tel":$scope.tel,"seq":$scope.seq,"memberid":$scope.memberid,"account":$scope.account}
            $http.put("http://127.0.0.1:8080/Userinfo/editUserInfo",data,{ withCredentials:true}).success(function (data) {
                console.log(data)
                if(data.status=="1"){
                    alert(data.msg);
                    $scope.initAdminInfo();
                    window.location.reload();
                }else if(data.status=="2"){
                    alert(data.msg);
                    window.location.reload();
                }else {
                    alert("修改失败！");
                    window.location.reload();
                }
            });
        }

    }
});