(function($) {
    $('body').tooltip({
        selector: '.tips'
    });

    $(".fancybox").fancybox();
    $("img").unveil();

    $(function() {
        var source = $("#today-girl-template").html();
        var archive = $(".alert[archive]").attr('archive');

        if (archive == 'archive') {
            $("#today-girl").parent().remove()
        }

        if (typeof source !== "undefined" && archive == 'archive') {
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
