Simorgh.controller('HomeSearch', ['$scope', '$http',
    function ($scope, $http) {

        $scope.list = {
            "result": 1,
            "obj_list": [
                {
                    "hotel_name": "جبار",
                    "star":  1,
                    "point": 1,
                    "link": "/simorgh/",
                    "img_url": "/ghg/",
                    "price": 1
                }
            ]
        };
        $scope.renge=[1,2,3,4,5]
        $scope.mode=1;
        $scope.pages = [];

        $scope.active_page = 1;

        $scope.OBJ_PER_PAGE = 6;

        $scope.updatePages = function () {
            console.log("update shodam")
            $scope.pages = [];
            var start = $scope.list.obj_list.length - 1;
            var toBeAdded = {
                'obj_list': []
            };
            console.log($scope.list)
            for (var i = start; i >= 0; i--) {
                if (toBeAdded.obj_list.length < $scope.OBJ_PER_PAGE) {
                    toBeAdded.obj_list.push($scope.list.obj_list[i]);
                }

                if (i == 0 || toBeAdded.obj_list.length == $scope.OBJ_PER_PAGE) {
                    if (toBeAdded.obj_list.length > 0) {
                        toBeAdded.pageNum = $scope.pages.length + 1;
                        $scope.pages.push(toBeAdded);
                        toBeAdded = {
                            'obj_list': []
                        };
                    }
                }
            }
        };

        $scope.getActive = function (page) {
            return page.pageNum == $scope.active_page;
        };

        $scope.getCurrentList = function () {
            return $scope.pages[$scope.active_page - 1];
        };

        $scope.changePage = function (x) {
            $scope.active_page = x;
        };

        $scope.roomSearch = function () {
            var id = WaitMsg.add("در حال جستجو");
            sortField=$("#room_sort").val()
            $http({
                method: 'POST',
                url: '/simorgh/ajax/search/room/',
                data: {pool: $scope.room_pool, breakfast:$scope.room_breakfast,wifi:$scope.room_wifi, cafe:$scope.room_cafe,
                    hotel: $scope.room_hotel, city: $scope.room_city,
                    min_star:$scope.room_min_star, max_star:$scope.room_max_star, max_point: $scope.room_max_point, min_point: $scope.room_min_point,
                    cost: $scope.cost, capacity: $scope.capacity,
                    lake: $scope.extra_bed, tv: $scope.tv, kitchen:$scope.kitchen, sort_field:sortField   }
            }).
                success(function (data, status, headers, config) {
                    $scope.list = data;
                    WaitMsg.success(id);
                    $scope.updatePages();
                    $scope.set_mode(2);
                }).
                error(function (data, status, headers, config) {
                    console.log("ERROR", data);
                    WaitMsg.error(id);
                });
        };

        $scope.allRooms = function () {
            var id = WaitMsg.add("در حال جستجو");
            sortField=$("#room_sort").val()
            $http({
                method: 'POST',
                url: '/simorgh/ajax/search/room/',
                data: {pool: '', breakfast:'',wifi:'', cafe:'',
                    hotel: '', city:'',
                    min_star:'', max_star:'', max_point: '', min_point: '',
                    cost: '', capacity: '',
                    lake: '', tv: '', kitchen:'', sort_field:sortField   }
            }).
                success(function (data, status, headers, config) {
                    $scope.list = data;
                    WaitMsg.success(id);
                    $scope.updatePages();
                    $scope.set_mode(2);
                }).
                error(function (data, status, headers, config) {
                    console.log("ERROR", data);
                    WaitMsg.error(id);
                });
        };


        $scope.hotelSearch = function () {
            var id = WaitMsg.add("در حال جستجو");
            sortField=$("#hotel_sort").val()
            $http({
                method: 'POST',
                url: '/simorgh/ajax/search/hotel/',
                data: {pool: $scope.pool, breakfast:$scope.breakfast,wifi:$scope.wifi, cafe:$scope.cafe,
                    hotel: $scope.hotel_name, city: $scope.city,
                    min_star:$scope.min_star, max_star:$scope.max_star, max_point: $scope.max_point, min_point: $scope.min_point,
                    sort_field:sortField}
            }).
                success(function (data, status, headers, config) {
                    $scope.list = data;
                    WaitMsg.success(id);
                    $scope.updatePages();
                    $scope.set_mode(3);
                }).
                error(function (data, status, headers, config) {
                    console.log("ERROR", data);
                    WaitMsg.error(id);
                });

        };

        $scope.allHotels = function () {
            var id = WaitMsg.add("در حال جستجو");
            sortField=$("#hotel_sort").val()
            $http({
                method: 'POST',
                url: '/simorgh/ajax/search/hotel/',
                data: {pool: '', breakfast:'',wifi:'', cafe:'',
                    hotel: '', city: '',
                    min_star:'', max_star:'', max_point: '', min_point: '',
                    sort_field:sortField}
            }).
                success(function (data, status, headers, config) {
                    $scope.list = data;
                    WaitMsg.success(id);
                    $scope.updatePages();
                    $scope.set_mode(3);
                }).
                error(function (data, status, headers, config) {
                    console.log("ERROR", data);
                    WaitMsg.error(id);
                });

        };



        $scope.init=function(){
            $scope.set_mode(1)
            //alert("here")
            $http({
                method: 'POST',
                url: '/simorgh/ajax/home/'
            }).
                success(function (data, status, headers, config) {
                    //alert("khoobe")
                    $scope.list = data;
                    $scope.updatePages();
                }).
                error(function (data, status, headers, config) {
                    //alert("bade")
                    console.log("ERROR", data);
                });
        }

        $scope.set_mode=function(x){
            $scope.mode=x;
        }
    }
]);
