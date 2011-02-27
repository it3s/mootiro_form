// Field types initialization

fieldTypes = {};
fields_json = {};
fieldTypes['TextField'] = TextField;
// Object that generates new field IDs
fieldId = {};
fieldId.current = 0;
fieldId.next = function() {
    this.current++;
    return 'field_' + this.current.toString();
}

function init_fields(fields) {
    if (fields) {
        $.each(fields, function(id, f) {
            var field = fieldTypes[f.type];
            new field(f).insert();
        });
    } else {
        fields_json = {};
    }
}

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

function addField(e, field, domNode) { // event handler
  fields_json[field.props.id] = {};
  fields_json[field.props.id].props = field.props;
  // Save last added field
  var idx = $('#field_idx').val();
  if (idx) {
    var f = fieldTypes[fields_json[idx].props.type];
    new f().save(fields_json[idx]);
  }
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));
  domNode.appendTo(formFields);
}

// Switches to the Edit tab and renders the corresponding form
function switchToEdit(field) {
  // Save last added field
  var idx = $('#field_idx').val()
  if (idx) {
    var f = fieldTypes[fields_json[idx].props.type];
    new f().save(fields_json[idx]);
  }
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));
  // Change required!
  // TODO: Put this code on FieldType prototype
    if (field.props.required) {
        $('#EditRequired').attr('checked', true);
    } 

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

/* The BEAST! */

function saveForm() {
    var idx = $('#field_idx').val()
    if (idx) {
      var f = fieldTypes[fields_json[idx].props.type];
      new f().save(fields_json[idx]);
    }

    /* Get Form options */

    var form_id = $('#form_id').val();
    var form_title = '';
    var form_desc = '';

    if (!form_id) {
        form_id = 'new';
    }

    /* Get the Form Title */

    form_title = $('input[name=name]').val(); 

    /* Get the Form Description */

    form_desc = $('textarea[name=description]').val();

    /* Get Form Fields */

    var fields = [];
    $.each(fields_json, function (id, field) {
        fields.push(field.props);
    });

    /* Send the data! */
    $.post('/form/update/' + form_id, 
            { form_id: form_id
            , form_title: form_title
            , form_desc: form_desc
            , fields_position: $('#FormFields').sortable('toArray')
            , fields: fields }
            , updateFormFields);

}

function updateFormFields(data) {
    $('#form_id').val(data.form_id);

    /* Need this to not add a new field more than one time 
     * when the user click on save multiple times */
    $.each(data.new_fields_id, function (f_idx, f) {
        fields_json[f_idx].props.field_id = f.field_id;
    });
}
