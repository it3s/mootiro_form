function dir(object) {
  methods = [];
  for (z in object) {
    if (typeof(z) != 'number') methods.push(z);
  }
  return methods.join(', ');
}

editKeys = [
   0, // charCode zero means a non-Unicode key has been pressed in Firefox and is avaliable at keyCode.
   8, // BACKSPACE
   9, // TAB
  13, // ENTER
];

// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(from, to) {
    // TODO: use window.setTimeout()
    $(from).keyup(function(e){
        //if (e.charCode in editKeys) {
        //    $(to).text(this.value);
        //} else {
            $(to).text(this.value + String.fromCharCode(e.charCode));
        //}
    });
}

setupCopyValue('#form_name', '#DisplayTitle');
