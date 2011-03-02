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


// Constructor; must be called in the page.
function FieldsManager(json) { // the parameter contains the fields
  this.toDelete = []; // previously named deleteFields
  this.types = {};   // previously named fieldTypes
  this.all = {};    // previously named fields_json
  var instance = this;
  // At dom ready:
  $(function () {
    $.each(json, function (props) {
      instance.instantiateField(props).insert();
    });
  });
}

// Methods
FieldsManager.prototype.instantiateField = function (props) {
    // Finds the field type and instantiates it
    var cls = this.types[props.type];
    return new cls(props);
}
FieldsManager.prototype.switchToEdit = function(field) {
  // Switches to the Edit tab and renders the corresponding form.
  // Save last added field
  var idx = $('#field_idx').val(); alert(idx);
  if (idx) {
    $('#' + idx + '_container').toggleClass('fieldEditActive');
    this.instantiateField(field.props).save(this.all[idx]);
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
FieldsManager.prototype.save = function () {
    var idx = $('#field_idx').val();
    if (idx) {
      //var f = fieldTypes[this.all[idx].props.type];
      //new f().save(this.all[idx]);
      this.instantiateField(this.all[idx].props).save(this.all[idx]);
    }

    /* Get form options */
    var form_id = $('#form_id').val();
    var form_title = '';
    var form_desc = '';

    if (!form_id) {
        form_id = 'new';
    }

    /* Get the form title */
    form_title = $('input[name=name]').val(); 

    /* Get the form description */
    form_desc = $('textarea[name=description]').val();

    /* Get form fields */
    var ff = [];
    $.each(this.all, function (id, field) {
        ff.push(field.props);
    });
    /* Send the data! */
    $.post('/form/update/' + form_id, 
            { form_id: form_id
            , form_title: form_title
            , form_desc: form_desc
            , fields_position: $('#FormFields').sortable('toArray')
            , fields: ff
            , deleteFields: this.toDelete },
            updateFormFields);

}
FieldsManager.prototype.update = function (data) {
    $('#form_id').val(data.form_id);

    /* Need this to not add a new field more than one time 
     * when the user click on save multiple times */
    $.each(data.new_fields_id, function (f_idx, f) {
        this.all[f_idx].props.field_id = f.field_id;
    });
}

// TODO: Move some code out of here into the class above
function addField(e, field, domNode) { // Event handler.
  fields.all[field.props.id] = {};
  fields.all[field.props.id].props = field.props;

  domNode.appendTo(formFields);
  var moveButton = $("<img>").attr({
                                src: '/static/img/icons-edit/move_large.png',
                                class: 'moveButton'});
  var deleteButton = $("<img>").attr({
                                src: '/static/img/icons-edit/delete_large.png',
                                class: 'deleteButton'});
  domNode.append(deleteButton);
  domNode.append(moveButton);

  deleteButton.click(function () {
      if (field.props.field_id == 'new') {
          $('#' + field.props.id + '_container').remove();
          delete fields.all[field.props.id];
      } else {
          deleteFields.push(field.props.field_id);
          $('#' + field.props.id + '_container').remove();
          delete fields.all[field.props.id];
      }
      $('#PanelEdit').html();
      tabs.to('#TabAdd');
  });
}


$(function () { // at domready:
  formFields = $('#FormFields');
  formFields.insert = function(fieldtype, position) {
    var f = fields.types[fieldtype];
    new f().insert(position);
  };
  formFields.bind('AddField', addField);
});
