var DATATABLE_OBJ = null;
var COLLECTED_DATA = [];
require(['zepto', 'moment', 'mustache', 'jquery','dataTables_bootstrap', 'datatables.net'], function($, moment, Mustache, jquery){

    //clock
    window.setInterval(function(){
        $('#timer').text(
            moment().format("MM/DD/YYYY h:mm:ss")
        );
    },1000);


    //functions
    function renderOptions(data){
        var time_data = [];
        if (data.length !== 0){
            for (var index in data){
                if (COLLECTED_DATA.indexOf(data[index].user) === -1){
                    COLLECTED_DATA.push(data[index].user);
                    time_data.push({
                        "id": data[index].user,
                        "first_name": data[index].first_name,
                        "last_name": data[index].last_name
                    })
                }
                console.log(time_data);
            }
            var home_options_template = $("#home_filter_users").html();
            var home_options = Mustache.to_html(home_options_template, {"time": time_data});
            $("#users").append(home_options);
        }

    }


    function renderTable(data){
        var home_table_data_template = $("#dataTable_data").html();
        var home_table_data = Mustache.to_html(home_table_data_template, data);
        DATATABLE_OBJ.destroy();
        $("#dataTable").find("tbody").append(home_table_data);
        reinitializeTable();
    }


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    function toggleButton(this_, response){
        console.log(response.action);
        $(this_).removeClass("btn-primary");
        $(this_).removeClass("btn-danger");
        $(this_).addClass((response.action == "time-in") ? "btn-primary" : "btn-danger");
        $(this_).attr("action", response.action);
        $(this_).removeAttr("disabled");
        $(this_).attr("time-id", response.time_id);
        $(this_).text(response.action.toUpperCase());
    }


    function timeInTimeOut(this_, csrftoken){
        $.ajax({
             beforeSend: function(xhr, settings) {
                 if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                     xhr.setRequestHeader("X-CSRFToken", csrftoken);
                 }
             },
             url:"/timer-start-end",
             type:"post",
             data:{
                 "action": $(this_).attr("action"),
                 "time_id" : $(this_).attr("time-id"),
                 "csrftoken" : csrftoken
             },
             success: function(response){
                toggleButton(this_, response);
             }
         })
    }


    function getRecord(start, end, user_id, top, bottom, initial){
        if (!end)
            end = moment().format("MM/DD/YYYY HH:mm");
        if (!start)
            start = moment().format("MM/DD/YYYY") + " " + "00:00";
        var todayUrlFormat = "start_date=" + encodeURIComponent(start)+ "&end_date=" + encodeURIComponent(end);
        var topFormat = "&top=" + top;
        var bottomFormat = "&bottom=" + bottom;
        var orderFormat = "&order=-user__last_name";
        var userIdFormat = "&user_id=" + user_id;

        if (initial){
            DATATABLE_OBJ.clear();
            DATATABLE_OBJ.destroy();
        }
        reinitializeTable();

        $.ajax({
            url:"/api/v1/timeintimeout?" + todayUrlFormat + topFormat + bottomFormat + orderFormat + userIdFormat,
            method:"get",
            success:function(response){
                if (response.data){
                    renderTable(response);
                    renderOptions(response.data);
                }
                if (response.has_more){
                    getRecord(start, end, user_id, response.top, response.bottom, false);
                }

            }
        })
    }


    function reinitializeTable(){
        clearUpdateDescriptionModal();
        DATATABLE_OBJ = jquery("#dataTable").DataTable();
    }


    function clearUpdateDescriptionModal(){
        $("#description").val("");
    }


    //listeners
    $(document).on("click", "#filter_table", function(){
        if ($("#start_date").val()){
            var start = moment($("#start_date").val()).format("MM/DD/YYYY") + " 00:00";
        }
        if ($("#end_date").val()){
            var end = moment($("#end_date").val()).format("MM/DD/YYYY") + " 23:59";
        }
        var user_id = $("#users").val();
        var initial = true;
        getRecord(start, end, user_id, 0, 5, initial);

    });


    $(document).on("click", "#timein-timeout", function(){
         $(this).attr("disabled", "disabled");
         var csrftoken = getCookie('csrftoken');
         var this_ = this;
         timeInTimeOut(this_, csrftoken);
    });

    $(document).on("ready", function(){
        reinitializeTable();
        var initial = true;
        getRecord(null, null, null, 0, 5, initial);
    });


    $(document).on("click", ".edit-time", function(){
        var id = $(this).data("id");
        $("#update-time-description").attr("data-id", id);
        clearUpdateDescriptionModal();
        jquery("#update_description_modal").modal("show");
    });


    $(document).on("click", "#update-time-description", function(){
        var id = $(this).data("id");
        var description = $("#description").val();
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url:"/api/v1/timeintimeout",
            type:"post",
            data: {
                "id": id,
                "csrftoken" : csrftoken,
                "description" : description
            },
            success:function(response){
                console.log(response);
            }
        })
    });


    $(document).on("keyup", function(e){
        if(e.keyCode === 13){
            $("#timein-timeout").click();
        }
    });
});