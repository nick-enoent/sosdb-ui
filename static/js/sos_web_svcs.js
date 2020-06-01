function format_date(aDate)
{
    var h = aDate.getHours();
    var m = aDate.getMinutes();
    var s = aDate.getSeconds();
    if (h < 10)
        h = '0' + h;
    if (m < 10)
        m = '0' + m;
    if (s < 10)
        s = '0' + s;
    return aDate.getFullYear()
        + '/' + (aDate.getMonth() + 1)
        + '/' + aDate.getDate()
        + ' ' + h
        + ':' + s;
}
function hide_nav(){
    $("#menuwrapper").toggleClass('collapsed').promise().done(function() {
        setTimeout(function(){$(window).trigger("resize");},300);
    });
}
