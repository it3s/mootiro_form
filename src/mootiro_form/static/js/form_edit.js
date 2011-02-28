// Field types initialization

deleteFields = [];
fieldTypes = {};
fields_json = {};
numberFields = 0;
fieldTypes['TextField'] = TextField;
fieldTypes['TextAreaField'] = TextAreaField;


// Object that generates new field IDs
fieldId = {};
fieldId.current = 0;
fieldId.currentString = function () {
    return 'field_' + this.current;
}
fieldId.next = function () {
    return ++this.current;
}
fieldId.nextString = function () {
    this.next();
    return this.currentString();
}


function init_fields(fields) {
  if (fields) {
    $.each(fields, function (id, f) {
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
    if (typeof(z) !== 'number') methods.push(z);
  }
  return methods.join(', ');
}

// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(from, to, defaul, br) {
  $(to).text($(from)[0].value || defaul);
  function handler(e) {
    var v = this.value || defaul;
    if (br) v = v.replace(/\n/g, '<br />\n');
    $(to).val(v).text(v).html(v); // update value, innerText and innerHTML
  }
  $(from).keyup(handler).change(handler);
}


// Constructor
function Tabs(tabs, contents) {
  $(contents).hide();
  $(contents + ":first").show();
  $(tabs + " li:first").addClass("selected");
  $(tabs + " li").click(function () {
    $(contents).hide();
    $(tabs + " li").removeClass("selected");
    $(this).addClass("selected");
    $($(this).children().attr("href")).show();
    return false; // in order not to follow the link
  });
}
// Method
Tabs.prototype.to = function (tab) {
  $(tab).trigger('click');
}


function addField(e, field, domNode) { // event handler
  fields_json[field.props.id] = {};
  fields_json[field.props.id].props = field.props;

  // Save last added field
/*  var idx = $('#field_idx').val();
  if (idx) {
    var f = fieldTypes[fields_json[idx].props.type];
    new f().save(fields_json[idx]);
  }
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));*/

  domNode.appendTo(formFields);
  numberFields++;
  var moveButton = $("<img>").attr({ 
                                src: '/static/img/icons-edit/move_large.png',
                                class: 'moveButton'});
  var deleteButton = $("<img>").attr({ 
                                src: '/static/img/icons-edit/delete_large.png',
                                class: 'deleteButton'});
  // TODO: Put the above CSS in a CSS file!!!
  domNode.append(deleteButton);
  domNode.append(moveButton);

  deleteButton.click(function () {
      console.log(fields_json);
      if (field.props.field_id == 'new') {
        $('#' + field.props.id + '_container').remove();
        delete fields_json[field.props.id];
      } else {
        deleteFields.push(field.props.field_id);
        $('#' + field.props.id + '_container').remove();
        delete fields_json[field.props.id];
        /* Better to use AJAX or Save button? */
      }
      numberFields--;
      $('#PanelEdit').html();
      tabs.to('#TabAdd');
  });
}

// Switches to the Edit tab and renders the corresponding form
function switchToEdit(field) {
  // Save last added field
  var idx = $('#field_idx').val();
  if (idx) {
    var f = fieldTypes[fields_json[idx].props.type];
    $('#' + idx + '_container').toggleClass('fieldEditActive');
    new f().save(fields_json[idx]);
  }
  // Now it is safe to switch the tab
  $('#PanelEdit').html($.tmpl(field.optionsTemplate, field.props));
  $('#' + field.props.id + '_container').toggleClass('fieldEditActive');
  // Change required!
  // TODO: Put this code on FieldType prototype
  if (field.props.required) {
    $('#EditRequired').attr('checked', true);
  }
  tabs.to('#TabEdit');
}

$(function () { // at domready:
  formFields = $('#FormFields');
  formFields.insert = function(fieldtype, position) {
    var f = fieldTypes[fieldtype];
    new f().insert(position);
  };
  formFields.bind('AddField', addField);
});

/*  Send form and field data */

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
    //console.log(fields_json);
    /* Send the data! */
    $.post('/form/update/' + form_id, 
            { form_id: form_id
            , form_title: form_title
            , form_desc: form_desc
            , fields_position: $('#FormFields').sortable('toArray')
            , fields: fields 
            , deleteFields: deleteFields },
            updateFormFields);

}

function updateFormFields(data) {
    $('#form_id').val(data.form_id);

    /* Need this to not add a new field more than one time 
     * when the user click on save multiple times */
    $.each(data.new_fields_id, function (f_idx, f) {
        fields_json[f_idx].props.field_id = f.field_id;
    });
}
