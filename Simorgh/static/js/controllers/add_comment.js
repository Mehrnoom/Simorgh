Simorgh.controller('CommentCtrl', ['$scope', '$http',
    function ($scope, $http) {

        $scope.list = {
            "result": 1,
            "commentList": [
                {
                    "name": "جبار",
                    "message": "خیلی خوبه!",
                    "star_number": 1

                }
            ]
        };

        $scope.pages = [];

        $scope.renge=[1,2,3,4,5]
        $scope.active_page = 1;

        $scope.COMMENT_PER_PAGE = 10;

        $scope.updatePages = function () {
            $scope.pages = [];
            var start = $scope.list.commentList.length - 1;
            var toBeAdded = {
                'commentList': []
            };
            for (var i = start; i >= 0; i--) {
                console.log(i, $scope.list.commentList[i]);
                if (toBeAdded.commentList.length < $scope.COMMENT_PER_PAGE) {
                    toBeAdded.commentList.push($scope.list.commentList[i]);
                }

                if (i == 0 || toBeAdded.commentList.length == $scope.COMMENT_PER_PAGE) {
                    if (toBeAdded.commentList.length > 0) {
                        toBeAdded.pageNum = $scope.pages.length + 1;
                        $scope.pages.push(toBeAdded);
                        toBeAdded = {
                            'commentList': []
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

        $scope.addComment = function () {

            st=$("#star").val()
            console.log(st)
            $http({
                method: 'POST',
                url: '/simorgh/ajax/hotel/' + $scope.hotel_id + '/comments/add',
                data: {message: $scope.comment, star: st}
//                data: {message: "123"}
            });
            $scope.init($scope.hotel_id);
        };


        $scope.init = function (hotel_id) {
            $scope.hotel_id = hotel_id;
            var id = WaitMsg.add("در حال دریافت کامنت ها");
            $http({method: 'POST', url: '/simorgh/ajax/hotel/' + hotel_id + '/comments'}).
                success(function (data, status, headers, config) {
                    $scope.list = data;
                    WaitMsg.success(id);
                    $scope.updatePages();
                }).
                error(function (data, status, headers, config) {
                    console.log("ERROR", data);
                    WaitMsg.error(id);
                });
        };
    }
]);