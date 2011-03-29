// Like Python dir(). Useful for debugging.
function dir(object) {
  var methods = [];
  for (z in object) {
    if (typeof(z) !== 'number') methods.push(z);
  }
  return methods.join(', ');
}

String.prototype.contains = function (t) {
    return this.indexOf(t) != -1;
}

function positiveIntValidator(s) {
    if (typeof(s) === 'number') s = s.toString();
    var n = Number(s);
    if (isNaN(n)) return 'Invalid';
    if (n < 0 || s.contains('.')) return 'Must be a positive integer';
    return '';
}

function methodCaller(o, method, arg) {
    return function () {
        return o[method](arg);
    }
}

// Sets up an input so changes to it are reflected somewhere else
function setupCopyValue(o) { // from, to, defaul
    if (o.defaul==null) o.defaul = '';
    var to = $(o.to);
    to.text($(o.from)[0].value || o.defaul);
    function handler(e) {
        var v = this.value || o.defaul;
        // update value and innerText, but not innerHTML!
        if (to.val) to.val(v);
        if (to.text) to.text(v);
        if (o.callback) {
            o.obj[o.callback](v);
        }
    }
    $(o.from).keyup(handler).change(handler);
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
    $('#PanelTitle').text($(this).children().attr('title'));
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


// As the page loads, GET the templates file and compile the templates
$.get('/static/fieldtypes/form_edit_templates.html',
  function (fragment) {
    $('body').append(fragment);
    $.template('FieldBase', $('#fieldBaseTemplate'));
  }
);


// Constructor; must be called in the page.
function FieldsManager(formId, json) {
  this.formId = formId;
  this.all = {};
  this.types = {};
  this.toDelete = [];
  this.current = null; // the field currently being edited
  var instance = this;

  var whenReady = function () {
    instance.place = $('#FormFields');
    $.each(json, function (index, props) {
      instance.insert(instance.instantiateField(props));
    });
    instance.formPropsFeedback();
    // this.place.bind('AddField', addField);
    instance.resetPanelEdit();
    // Finally remove this ajaxStop handler since this function is
    // supposed to be executed only once:
    $(document).unbind('ajaxStop', whenReady);
  }
  $(document).ajaxStop(whenReady);
}
FieldsManager.prototype.optionsBaseTpl = $.template('optionsBase',
"<input id='field_idx' type='hidden' name='field_idx' value='${props.id}'/>\n" +
"<input id='field_id' type='hidden' name='field_id' value='${props.field_id}'/>\n" +
"<ul class='Props'><li>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<textarea id='EditLabel' name='label'>${props.label}</textarea>\n" +
"</li><li>\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${props.description}" +
  "</textarea>\n" +
"</li><li>\n" +
  "<input type='checkbox' id='EditRequired' name='required' " +
  "{{if props.required }} checked='checked' {{/if}} />\n" +
  "<label for='EditRequired'>required</label></li></ul>\n" +
"{{tmpl(props) optionsTpl}}\n");

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

FieldsManager.prototype.renderPreview = function (field) {
    // Returns a DOM node containing the rendered field for the right column.
    // If the field implements renderPreview(), use that instead.
    if (field.renderPreview) {
        return field.renderPreview();
    } else {
        var tplContext = {props: field.props, fieldTpl: field.previewTemplate};
        return $.tmpl('FieldBase', tplContext);
    }
}

FieldsManager.prototype.renderOptions = function (field) {
    // Returns a DOM node containing the HTML for the Edit tab.
    // If the field implements renderOptions(), use that instead.
    if (field.renderOptions)
        return field.renderOptions();
    else {
        var tplContext = {props: field.props, optionsTpl: field.optionsTemplate};
        return $.tmpl('optionsBase', tplContext);
    }
}

FieldsManager.prototype.insert = function (field, position) {
    // Renders and displays the passed `field` at `position`.
    // For now, only insert at the end; ignore `position`.
    // If field is a string, that is the field type; create a brand new field
    if (window.console) console.log('insert()');
    if (typeof(field)==='string') {
        field = this.instantiateField(field);
    }
    // `field` is now a real field object.
    this.all[field.props.id] = field;
    field.domNode = this.renderPreview(field);
    this.addBehaviour(field);
    field.domNode.appendTo(this.place); // make appear on the right
    // $.event.trigger('AddField', [field, domNode, position]);
}

FieldsManager.prototype.redrawPreview = function (field) {
    if (window.console) console.log('redrawPreview()');
    if (field.redrawPreview) {
        field.redrawPreview();
    } else {
        var domNode = this.renderPreview(field);
        //field.domNode = this.renderPreview(field);
        // Replace the old node contents:
        $('#' + field.props.id + '_container').html(domNode.html());
        field.domNode = $('#' + field.props.id + '_container');
        this.addBehaviour(field);
    }
}

FieldsManager.prototype.validateCurrent = function () {
    // Returns true if there are no problems in the field currently being edited
    var c = this.current;
    if (c.getErrors) {
        var e = this.current.getErrors();
        for (i in e) {
            if (typeof(e[i])==='string' && e[i]) return false;
        }
    }
    return true;
}

FieldsManager.prototype.saveCurrent = function () {
    if (window.console) console.log('saveCurrent()');
    // If there is no current field, we just don't care:
    if (!this.current)  return true;
    // First validate the alterations to the field.
    if (!this.validateCurrent()) {
        tabs.to('#TabEdit'); // Display the errors so the user gets a hint
        if (confirm('The current field has errors, displayed on ' +
                    'the left column.\nLose your alterations?')) {
            this.redrawPreview(this.current);
            $('#PanelEdit').html(this.renderOptions(this.current));
            return true; // don't save but proceed
        } else {
            return false; // don't save and stop
        }
    }
    // Store (in the client) the information in the left form
    var p = this.current.props;
    p.label = $('#EditLabel').val();
    p.required = $('#EditRequired').attr('checked');
    p.description = $('#EditDescription').val();
    // These are the common attributes; now to the specific ones:
    if (this.current.save)  this.current.save();
    return true;
}

FieldsManager.prototype.switchToEdit = function (field) {
  if (window.console) console.log('switchToEdit()');
  tabs.to('#TabEdit');
  // There is no need to switch to the same field.
  if (field === this.current) return true;
  // First, save the field previously being edited
  if (!this.saveCurrent()) return false;
  if (this.current) {
      this.current.domNode.toggleClass('fieldEditActive', false);
      this.current = null; // for safety, until the end of this method
  } 
  // Make `field` visually active at the right
  field.domNode.toggleClass('fieldEditActive', true);
  // Render the field properties at the left
  $('#PanelEdit').html(this.renderOptions(field));
  // TODO: Remove 'magic' position 120
  function scrollWindow() {
    $('html, body').animate({scrollTop: field.domNode.offset().top});
  }
  $('#PanelEdit').animate({'margin-top': field.domNode.position().top - 100},
    200, scrollWindow);
  if (field.showErrors)  field.showErrors();
  // Set the current field, for next click
  this.current = field;
  return true;
}

FieldsManager.prototype.formPropsFeedback = function () {
    setupCopyValue({from:'#deformField1', to:'#DisplayTitle',
        defaul:'Untitled form'});
    setupCopyValue({from:'#deformField2', to:'#DisplayDescription',
        defaul:'Public description of this form'});
    setupCopyValue({from:'#deformField3', to:'#submit',
        defaul:'Submit'});
    $('#submit').click(function () {
        tabs.to('#TabForm');
        $('#deformField3').focus();
    });
}

FieldsManager.prototype.instantFeedback = function () {
    setupCopyValue({from:'#EditLabel',
        to:$('#' + this.current.props.id + 'Label'),
        defaul:'Question'});
    setupCopyValue({from:'#EditDescription', to:'#' + this.current.props.id +
                   'Description', defaul:null});
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

var PanelEditHtmlContent = $('#PanelEdit').html();
FieldsManager.prototype.resetPanelEdit = function () {
    $('#PanelEdit').html(PanelEditHtmlContent);
    this.current = null;
}

FieldsManager.prototype.addBehaviour = function (field) {
    $('#' + field.props.id + 'Label', field.domNode)
        .click(funcForOnClickEdit(field, '#EditLabel', field.defaultLabel));
    $('#' + field.props.id + 'Description', field.domNode)
        .click(funcForOnClickEdit(field, '#EditDescription'));
    var instance = this;
    $('.moveField', field.domNode).hover(function () {
      $(this).attr({src: route_url('root') + '/static/img/icons-edit/moveHover.png'});  
    }, function () {
      $(this).attr({src: route_url('root') + '/static/img/icons-edit/move.png'});  
    });

    $('.deleteField', field.domNode).click(function () {
        if (field.props.field_id !== 'new') {
            instance.toDelete.push(field.props.field_id);
        }
        field.domNode.remove();
        delete instance.all[field.props.id];
        // If the field being deleted is the current field, remove its
        // properties from the left column.
        if (field === instance.current) instance.resetPanelEdit();
    }).hover(function () {
      $(this).attr({src: route_url('root') + '/static/img/icons-edit/deleteHover.png'});  
    }, function () {
      $(this).attr({src: route_url('root') + '/static/img/icons-edit/delete.png'});  
    });
  if (field.addBehaviour)  field.addBehaviour();
};

FieldsManager.prototype.persist = function () {
    if (window.console) console.log('persist()');
    // Saves the whole form, through an AJAX request.
    // First, save the field previously being edited
    if (!this.saveCurrent()) return false;
    /* Prepare form fields */
    var ff = [];
    $.each(this.all, function (id, field) {
        ff.push(field.props);
    });
    /* Prepare form properties */
    var json = {};
    json.fields = ff;
    json.form_id = this.formId || 'new';
    json.form_desc = $('textarea[name=description]').val();
    json.form_title = $('input[name=name]').val();
    json.submit_label = $('input[name=submit_label]').val();
    json.start_date = $('input[name=start_date]').val();
    json.end_date = $('input[name=end_date]').val();
    json.form_public = $('input[name=public]').attr('checked');
    json.form_thanks_message = $('textarea[name=thanks_message]').val();
    json.deleteFields = this.toDelete;
    json.fields_position = $('#FormFields').sortable('toArray');
    // POST and set 2 callbacks: success and error.
    var instance = this;
    var jsonRequest = {json: $.toJSON(json)};
    var url = '/' + route_url('form', {action:'edit', id: json.form_id});
    $.post(url, jsonRequest)
    .success(function (data) {
        if (data.panel_form) {
            $('#PropertiesForm').html(data.panel_form);
            instance.formPropsFeedback();
        }
        if (data.error) {
            tabs.to('#TabForm');
        } else {
            instance.formId = data.form_id;
            /* When the user clicks on save multiple times, this
             * prevents us from adding a new field more than once. */
            $.each(data.new_fields_id, function (f_idx, f) {
                instance.all[f_idx].props.field_id = f.field_id;
            });
            $.each(data.save_options_result, function (f_idx, f) {
                instance.all[f_idx].update(f);
            });
            // Assume any deleted fields have been deleted at the DB
            instance.toDelete = [];
            // Show the generated public link
            if (data.form_public_url)
                $('#form_public_url').attr('value', data.form_public_url);
        }
    })
    .error(function (data) {
        alert("Sorry, error updating fields on the server.\n" +
            "Your form has NOT been saved.\n" +
            "Status: " + data.status);
    });
    return true;
}


// When user clicks on the right side, the Edit tab appears and the
// corresponding input gets the focus.
function funcForOnClickEdit(field, target, defaul) {
    return function () {
        if (!fields.switchToEdit(field))  return false;
        fields.instantFeedback();
        $(target).focus();
        // Sometimes also select the text. (If it is the default value.)
        if ($(target).val() === defaul) $(target).select();
        return false;
    };
}
