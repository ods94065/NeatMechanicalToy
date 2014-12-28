'use strict';
var booksApp = angular.module('books', ['ngResource', 'ngRoute']);

booksApp.config(function($routeProvider) {
   $routeProvider.when('/', {
       templateUrl: 'partials/main.html',
       controller: 'booksMainController',
       requiresLogin: true
   }).when('/login', {
       templateUrl: 'partials/login.html',
       controller: 'booksLoginController',
       hideNav: true
   }).when('/logout', {
       templateUrl: 'partials/logout.html',
       controller: 'booksLogoutController'
   });
});

booksApp.run(function($rootScope, $location, booksSession) {
    // redirect to login if a route requires it
    $rootScope.$on('$routeChangeStart', function(event, next) {
        return booksSession.isLoggedIn().then(function(isLoggedIn) {
            if (! isLoggedIn
                && next.$$route.requiresLogin
                && next.loadedTemplateUrl !== 'bookang/partials/login.html')
            {
                console.log('Route requires login; redirecting');
                booksSession.setPostLoginRedirect(next.$$route.originalPath);
                $location.path('/login');
            }
        });
    });
});

booksApp.run(function($rootScope, $location, booksNav) {
    // hide nav bar if route requests it
    $rootScope.$on('$routeChangeStart', function(event, next) {
        booksNav.setShowNavBar(! next.hideNav);
    })
});

booksApp.factory('booksNav', function($rootScope) {
    var _showNavBar = false;
    return {
        getShowNavBar: function() { return _showNavBar; },
        setShowNavBar: function(shouldShow) {
            shouldShow = !!shouldShow;
            if (shouldShow !== _showNavBar) {
                var oldShowNavBar = _showNavBar;
                _showNavBar = shouldShow;
                $rootScope.$broadcast('booksNavVisibilityChange', {showNavBar: _showNavBar},
                    {showNavBar: oldShowNavBar});
            }
        }
    };
});

booksApp.factory('booksSession', function($http, $q, $rootScope) {
    var _setSessionUser = function(user) {
        $rootScope.booksSessionUser = user;
        $rootScope.booksSessionUser.name = $rootScope.booksSessionUser.username;
    };

    var _getSessionUser = function() {
        var deferred = $q.defer();
        if ($rootScope.booksSessionUser) {
            deferred.resolve($rootScope.booksSessionUser);
        } else {
            $http.get('/api/session/user').success(function(data) {
                _setSessionUser(data['user']);
                deferred.resolve($rootScope.booksSessionUser);
            }).error(function(data) {
                var errMsg = data['error'];
                $rootScope.booksSessionUser = null;
                deferred.reject(errMsg);
            });
        }
        return deferred.promise;
    };

    return {
        getSessionUser: function () {
            return _getSessionUser();
        },
        isLoggedIn: function () {
            return _getSessionUser().then(
                function() { return true; }, function() { return false; }
            );
        },
        getPostLoginRedirect: function () {
            return $rootScope.booksSessionLoginRedirect;
        },
        setPostLoginRedirect: function (path) {
            if (path !== '/login') {
                $rootScope.booksSessionLoginRedirect = path;
            }
        },
        login: function (username, password) {
            var deferred = $q.defer();
            $http.post(
                '/api/session/login',
                {username: username, password: password}
            ).success(function (data) {
                var user = data['user'];
                _setSessionUser(data['user']);
                deferred.resolve(user);
            }).error(function (data) {
                console.log('error logging in!');
                var errMsg = data['error'];
                $rootScope.booksSessionUser = null;
                deferred.reject(errMsg);
            });
            return deferred.promise;
        },
        logout: function () {
            var p = $q.defer();
            return $http.post(
                '/api/session/logout',
                {}
            ).success(function () {
                console.log('logged out!');
                $rootScope.booksSessionUser = null;
                p.resolve();
            }).error(function (data) {
                var errMsg = data['error'];
                p.reject(errMsg);
            });
        }
    };
});

//booksApp.factory('booksErrors', function($scope) {
//    return {
//        emit: function(errorMessage) {
//            return $scope.$emit('booksError', {errorMessage: errorMessage});
//        }
//    };
//});

booksApp.controller('booksController', function() {});

booksApp.controller('errorController', function($rootScope, $scope) {
    $scope.currentError = null;
    $rootScope.$on('booksError', function(event, state) {
        $scope.currentError = 'Error: ' + state.errorMessage;
    });
});

booksApp.controller('booksNavController', function($rootScope, $scope, booksNav, booksSession) {
    $scope.showNavBar = booksNav.getShowNavBar();
    $scope.isLoggedIn = false;
    $scope.sessionUser = null;

    $rootScope.$on('booksSessionChange', function(event, state) {
        $scope.isLoggedIn = state.isLoggedIn;
        $scope.sessionUser = state.sessionUser;
    });

    $scope.$on('booksNavVisibilityChange', function(event, state) {
        $scope.showNavBar = state.showNavBar;
    })
});

booksApp.controller('booksMainController', function($scope) {
    $scope.message = 'Hello, world!'
});

booksApp.controller('booksLoginController', function($location, $scope, booksSession) {
    $scope.loginUser = {username: '', password: ''};
    $scope.onLoginSubmit = function() {
        var loginUser = $scope.loginUser;
        booksSession.login(
            loginUser.username, loginUser.password
        ).then(function() {
            var sessionUser = booksSession.getSessionUser();
            var path = booksSession.getPostLoginRedirect();
            if (! path) {
                path = '/';
            }
            $location.path(path);
            $scope.$emit('booksSessionChange', {isLoggedIn: true, sessionUser: sessionUser});
        }, function(msg) {
            //booksErrors.$emit(msg);
        });
    };
});

booksApp.controller('booksLogoutController', function($scope, booksSession) {
    $scope.$on('$routeChangeSuccess', function() {
        return booksSession.logout().then(null, function(msg) {
            $scope.$emit('booksError', {errorMessage: msg});
        });
    });
});

booksApp.factory('User', function($resource) {
    return $resource('/api/users/:id');
});