requirejs.config({
    baseUrl: '/static/js',
    paths:{
        jquery:'jquery.min',
        bootstrap: 'bootstrap',
        zepto: 'zepto.min',
        mustache: 'mustache.min',
        moment: 'moment',
        npm: 'npm',
    },
    shim: {
        'jquery': {
            deps: [],
            exports: 'jquery'
        },
    }

})