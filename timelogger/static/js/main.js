    require(['zepto', 'moment'], function($, moment){

        //clock
        window.setInterval(function(){
            $('#timer').text(
                moment().format("MM/DD/YYYY h:mm:ss")
            );
        },1000);


        //functions
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


        //listeners
        $(document).on("click", "#timein-timeout", function(){
             $(this).attr("disabled", "disabled");
             var csrftoken = getCookie('csrftoken');
             var this_ = this;
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
        })
    });
