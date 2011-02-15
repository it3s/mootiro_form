// Like Python dir(). Useful for debugging.
function dir(object) {
  methods = [];
  for (z in object) {
    if (typeof(z) != 'number') methods.push(z);
  }
  return methods.join(', ');
}


// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(from, to, defaul) {
  $(to).text($(from)[0].value || defaul);
  $(from).keyup(function(e){
    $(to).text(this.value || defaul);
  });
}


function setupTabs(tabs, contents) {
  $(contents).hide();
  $(contents + ":first").show();
  $(tabs + " li:first").addClass("selected");
  $(tabs + " li").click(function(){
    $(contents).hide();
    $(tabs + " li").removeClass("selected");
    $(this).addClass("selected");
    $($(this).children().attr("href")).show();
    return false; // in order not to follow the link
  });
}
