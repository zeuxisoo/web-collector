(function($) {
    $('body').tooltip({
        selector: '.tips'
    });

    $(".fancybox").fancybox();
    $("img").unveil();

    $(function() {
        var source = $("#today-girl-template").html();
        if (typeof source !== "undefined") {
            var template = Handlebars.compile(source);
            $.getJSON("/ajax/today-girl").success(function(data) {
                var html = template({
                    'src' : data.image,
                    'name': data.name,
                    'date': data.date,
                    'href': data.href
                });
                $("#today-girl").html(html);
            });
        }
    });
})(jQuery)
