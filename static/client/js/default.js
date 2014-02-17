(function($) {
    $(function() {
        $(".fancybox").fancybox();
        $('.tips').tooltip();
        $("img").unveil();

        $.getJSON("/ajax/today-girl").success(function(data) {
            var source   = $("#today-girl-template").html();
            var template = Handlebars.compile(source);
            var html     = template({
                'src' : data.image,
                'name': data.name,
                'date': data.date
            });
            $("#today-girl").html(html);
        });
    });
})(jQuery)
