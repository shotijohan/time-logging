requirejs.config({
    baseUrl: '/static/js',
    paths:{
        jquery:'jquery.min',
        bootstrap: 'bootstrap',
        zepto: 'zepto.min',
        mustache: 'mustache.min',
        moment: 'moment',
        'datatables.net': 'jquery.dataTables.min',
        jquery_dataTables: 'jquery.dataTables.min',
        dataTables_bootstrap: 'dataTables.bootstrap.min',
        jquery_1_12_4: 'jquery-1.12.4',
        npm: 'npm',
        datepicker: 'datepicker',
    },
    shim: {
        'jquery': {
            deps: [],
            exports: 'jquery'
        },
    }

})