$(function () {
    $('body').keypress(function (e) {
        return disableEnterKey(e);   
    });
});

function disableEnterKey(e) {
     var key;      
     if(window.event)
          key = window.event.keyCode; //IE
     else
          key = e.which; //firefox      

     return (key != 13);
}
