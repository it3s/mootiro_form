function noenter() {
    return !(window.event && window.event.keyCode == 13);
}
$(function () {
    $('input').keypress(noenter);
});
