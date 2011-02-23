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
  function handler(e) {
    $(to).text(this.value || defaul);
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

// Generate new field IDs
fieldIndex = 0;
function nextFieldId() {
    fieldIndex++;
    return 'field_' + fieldIndex.toString();
}

// Field types initialization
// ==========================

fieldtypes = {};

function addField(e, field, domNode) {
  $('#' + field.properties.id + '_container').field = field;
  fields.push(field);
  domNode.appendTo(formFields);
}

$(function() {
  formFields = $('#FormFields');
  formFields.insert = function(fieldtype, position) {
    f = fieldtypes[fieldtype];
    f.insert(position);
  };
  formFields.bind('AddField', addField);
});