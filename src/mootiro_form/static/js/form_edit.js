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
  $(from).keyup(function(e){
    $(to).text(this.value || defaul);
  });
}

setupCopyValue('#form_name', '#DisplayTitle', 'Form Title');
