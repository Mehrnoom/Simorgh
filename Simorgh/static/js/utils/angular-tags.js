//angular.markup('(())', function(text, textNode, parentElement){
//    if (parentElement[0].nodeName.toLowerCase() == 'script') return;
//    text = text.replace(/\(\(/g,'{{').replace(/\)\)/g, '}}');
//    textNode.text(text);
//    return angular.markup('{{}}').call(this, text, textNode, parentElement);
//});
//
//angular.attrMarkup('(())', function(value, name, element){
//    value = value.replace(/\(\(/g,'{{').replace(/\)\)/, '}}');
//    element[0].setAttribute(name, value);
//    return angular.attrMarkup('{{}}').call(this, value, name, element);
//});

window.Simorgh = angular.module('Simorgh', []);

Simorgh.config(function($httpProvider, $interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    $httpProvider.defaults.transformRequest = function(data){
        if (data === undefined) {
            return data;
        }
        return $.param(data);
    };
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
});

