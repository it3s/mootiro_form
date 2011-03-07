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
    if (defaul==null) defaul = '';
    to = $(to);
    to.text($(from)[0].value || defaul);
    function handler(e) {
        var v = this.value || defaul;
        if (br) {
            v = v.replace(/\n/g, '<br />\n');
        }
        // update value and innerText, but not innerHTML!
        if (to.val) to.val(v);
        if (to.text) to.text(v);
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
  this.all = {};    // previously named fields_json
  this.types = {};   // previously named fieldTypes
  this.toDelete = []; // previously named deleteFields
  this.current = null; // the field currently being edited
  var instance = this;
  // At dom ready:
  $(function () {
    instance.place = $('#FormFields');
    $.each(json, function (index, props) {
      instance.insert(instance.instantiateField(props));
    });
    // this.place.bind('AddField', addField);
  });
}

// Methods

FieldsManager.prototype.instantiateField = function (props) {
    // Finds the field type and instantiates it. The argument may be
    // the field type (as a string) or a real properties object.
    var cls;
    if (typeof(props)==='string') {
        cls = this.types[props];
        props = null;
    } else {
        cls = this.types[props.type];
    }
    return new cls(props);
}

FieldsManager.prototype.render = function (field) {
    // Returns a DOM node containing the rendered field for the right column.
    // If the field implements render(), use that instead.
    if (field.render)
        return field.render();
    else
        return $.tmpl(field.template, field.props);
}

FieldsManager.prototype.renderOptions = function (field) {
    // Returns a DOM node containing the HTML for the Edit tab.
    // If the field implements renderOptions(), use that instead.
    if (field.renderOptions)
        return field.renderOptions();
    else
        return $.tmpl(field.optionsTemplate, field.props);
}

FieldsManager.prototype.insert = function (field, position) {
  // Renders and displays the passed `field` at `position`.
  // For now, only insert at the end; ignore `position`.
  // If field is a string, that is the field type; create a brand new field
  if (typeof(field)==='string') {
      field = this.instantiateField(field);
  }
  // `field` is now a real field object.
  // Create the DOM node and make each one point to the other.
  field.domNode = this.render(field); // a jquery object.
  field.domNode[0].field = field;
  this.all[field.props.id] = field;
  field.domNode.appendTo(this.place); // make appear on the right
  var moveButton = $("<img>").attr({
                   src: '/static/img/icons-edit/move_large.png',
                   class: 'moveButton'});
  var deleteButton = $("<img>").attr({
                     src: '/static/img/icons-edit/delete_large.png',
                     class: 'deleteButton'});
  field.domNode.append(deleteButton);
  field.domNode.append(moveButton);

  var instance = this;
  deleteButton.click(function () {
      if (field.props.field_id !== 'new') {
          instance.toDelete.push(field.props.field_id);
      }
      field.domNode.remove();
      delete instance.all[field.props.id];
      tabs.to('#TabAdd');
  });
  return this.addBehaviour(field);
  // $.event.trigger('AddField', [field, domNode, position]);
}

FieldsManager.prototype.saveCurrent = function () {
  // Stores (in the client) the information in the left form
  var p = this.current.props;
  p.label = $('#EditLabel').val();
  p.required = $('#EditRequired').attr('checked');
  p.description = $('#EditDescription').val();
  // These are the common attributes; now to the specific ones:
  if (this.current.save)  this.current.save();
}

FieldsManager.prototype.switchToEdit = function(field) {
  // First, save the field previously being edited
  if (this.current) {
      this.saveCurrent();
      this.current.domNode.toggleClass('fieldEditActive');
  }
  this.current = null; // for safety, until the end of this method
  // Make `field` visually active at the right
  field.domNode.toggleClass('fieldEditActive');
  // Render the field properties at the left
  $('#PanelEdit').html(this.renderOptions(field));
  // TODO: Put this code on FieldType prototype?
  if (field.props.required) {
    $('#EditRequired').attr('checked', true);
  }
  // Switch to the Edit tab
  tabs.to('#TabEdit');
  // Set the current field, for next click
  this.current = field;
}

FieldsManager.prototype.instantFeedback = function () {
    setupCopyValue('#EditLabel', $('#' + this.current.props.id + 'Label'),
                   'Question');
    setupCopyValue('#EditDescription', '#' + this.current.props.id +
                   'Description', null, true);
    var instance = this;
    $('#EditRequired').change(function (e) {
        var origin = $('#EditRequired');
        var dest = $('#' + instance.current.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
    });
    if (this.current.instantFeedback) this.current.instantFeedback();
}

FieldsManager.prototype.addBehaviour = function (field) {
  $('#' + field.props.id + 'Label')
    .click(funcForOnClickEdit(field, '#EditLabel', field.defaultLabel));
  $('#' + field.props.id + 'Description')
    .click(funcForOnClickEdit(field, '#EditDescription'));
  if (field.addBehaviour)  field.addBehaviour();
};

FieldsManager.prototype.persist = function () {
    // Saves the whole form, through an AJAX request.
    // First, save the field previously being edited
    if (this.current)  this.saveCurrent();
    /* Prepare form fields */
    var ff = [];
    $.each(this.all, function (id, field) {
        ff.push(field.props);
    });
    /* Prepare form properties */
    var json = {};
    json.fields = ff;
    json.form_id = $('#form_id').val() || 'new';
    json.form_desc = $('textarea[name=description]').val();
    json.form_title = $('input[name=name]').val();
    json.form_public = $('input[name=public]').attr('checked');
    json.form_thanks_message = $('textarea[name=thanks_message]').val();
    json.deleteFields = this.toDelete;
    json.fields_position = $('#FormFields').sortable('toArray');
    // POST and set 2 callbacks: success and error.
    var instance = this;
    var jsonRequest = {json: $.toJSON(json)};
    console.log(json);
    $.post('/form/update/' + json.form_id, jsonRequest)
    .success(function (data) {
        if (data.error) {
            alert(error);
        } else {
            console.log(data);
            $('#form_id').val(data.form_id); // TODO: Stop using hidden fields
            /* When the user clicks on save multiple times, this
             * prevents us from adding a new field more than once. */
            $.each(data.new_fields_id, function (f_idx, f) {
                instance.all[f_idx].props.field_id = f.field_id;
            });
            console.log(data.save_options_result);
            $.each(data.save_options_result, function (f_idx, or) {
                var opt_ids = or['insertedOptions'];
                        console.log(or);

                $.each(instance.all[f_idx].props.options, function (o_idx, opt) {
                        console.log(opt);

                    if (opt.id == 'new') {
                        new_id = opt_ids.pop();
                        console.log(new_id);
                        opt.id = new_id;
                    }
                });
            }); 
            console.log(instance.all);
            // Assume any deleted fields have been deleted at the DB
            instance.toDelete = [];
        }
    })
    .error(function (data) {
        alert("Sorry, error updating fields on the server.\n" +
            "Your form has NOT been saved.\n" +
            "Status: " + data.status);
    });
}


// When user clicks on the right side, the Edit tab appears and the
// corresponding input gets the focus.
function funcForOnClickEdit(field, target, defaul) {
    return function () {
        fields.switchToEdit(field);
        fields.instantFeedback();
        $(target).focus();
        // Sometimes also select the text. (If it is the default value.)
        if ($(target).val() === defaul) $(target).select();
        return false;
    };
}
