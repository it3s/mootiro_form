// Like Python dir(). Useful for debugging.
function dir(object) {
  var methods = [];
  for (z in object) {
    if (typeof(z) != 'number') methods.push(z);
  }
  return methods.join(', ');
}


// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(from, to, defaul, br) {
  $(to).text($(from)[0].value || defaul);
  function handler(e) {
    var v = this.value || defaul;
    if (br) v = v.replace(/\n/g, '<br />\n');
    $(to).val(v).text(v).html(v); // update both value and innerText
  }
  $(from).keyup(handler).change(handler);
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

function switchTab(tab) {
  $(tab).trigger('click');
}


// Object that generates new field IDs
fieldId = {};
fieldId.current = 0;
fieldId.next = function() {
    this.current++;
    return 'field_' + this.current.toString();
}

// Field types initialization
// ==========================

fieldTypes = {};

function addField(e, field, domNode) { // event handler
  $('#' + field.props.id + '_container').field = field;
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));
  fields.push(field);
  domNode.appendTo(formFields);
}

// Switches to the Edit tab and renders the corresponding form
function switchToEdit(field) {
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));
  //field.addActions();
  switchTab('#TabEdit');
}

$(function() { // at domready:
  formFields = $('#FormFields');
  formFields.insert = function(fieldtype, position) {
    var f = fieldTypes[fieldtype];
    new f().insert(position);
  };
  formFields.bind('AddField', addField);
});
