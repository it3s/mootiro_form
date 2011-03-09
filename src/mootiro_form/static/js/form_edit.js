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

String.prototype.n2br = function () {
    // Turn Enters into <br />s for output with $.html(). Not being used so far.
    var re;
    var text = this.replace(/&/g, '&amp;')
                   .replace(/</g, '&lt;')
                   .replace(/"/g, '&quot;');
    if (text.contains('\r\n')) {
        re = /\r\n/g;
    } else if (text.contains('\n')) {
        re = /\n/g;
    } else if (text.contains('\r')){
        re = /\r/g;
    } else {
        return text;
    }
    return text.replace(re, '<br />');
}

//Object.prototype.update = function (other) {
//    // Update this object with all the values from `other`.
//    for (prop in other) {
//        this[prop] = other[prop];
//    }
//}

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
function FieldsManager(formId, json) {
  this.formId = formId;
  this.all = {};
  this.types = {};
  this.toDelete = [];
  this.current = null; // the field currently being edited
  var instance = this;
  // At dom ready:
  $(function () {
    instance.place = $('#FormFields');
    $.each(json, function (index, props) {
      instance.insert(instance.instantiateField(props));
    });
    instance.formPropsFeedback();
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

FieldsManager.prototype.fieldBaseTpl = $.template('fieldBase',
  "<li id='${props.id}_container'>" +
  "<div style='float: left'>\n" +
  "<label id='${props.id}Label' class='desc' for='${props.id}'>${props.label}" +
  "</label><span id='${props.id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description NewLines' id='${props.id}Description'>" +
  "${props.description}</div>\n" +
  "{{tmpl(props) fieldTpl}}" +
  "</div><div class='fieldButtons'>\n" +
  "<img class='moveField' alt='Move' title='Move' src='" + route_url('root') +
  "/static/img/icons-edit/move_large.png'>\n" +
  "<img class='deleteField' alt='Delete' title='Delete' src='" +
  route_url('root') + "/static/img/icons-edit/delete_large.png'>\n" +
  "</div><div style='clear:both;'/></li>\n");

FieldsManager.prototype.renderPreview = function (field) {
    // Returns a DOM node containing the rendered field for the right column.
    // If the field implements renderPreview(), use that instead.
    if (field.renderPreview) {
        return field.renderPreview();
    } else {
        var tplContext = {props: field.props, fieldTpl: field.previewTemplate};
        return $.tmpl('fieldBase', tplContext);
    }
}

FieldsManager.prototype.renderOptions = function (field) {
    // Returns a DOM node containing the HTML for the Edit tab.
    // If the field implements renderOptions(), use that instead.
    if (field.renderOptions)
        return field.renderOptions();
    else {
        return $.tmpl(field.optionsTemplate, field.props);
    }
}

FieldsManager.prototype.prepareDom = function (field, placer) {
    // Create the DOM node with behaviour.
    // Make field point to the DOM node and vice versa.
    if (window.console) console.log('prepareDom()');
    field.domNode = this.renderPreview(field); // a jquery object.
    field.domNode[0].field = field;
    // `placer` is a callback that will place the DOM node somewhere.
    placer(field.domNode);
    var instance = this;
    this.addBehaviour(field);
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
    var instance = this;
    function placer(node) {
        node.appendTo(instance.place);
    }
    this.prepareDom(field, placer); // make appear on the right
    // $.event.trigger('AddField', [field, domNode, position]);
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
            var c = this.current;
            var old = this.current.domNode;
            // Lose erroneous visualization
            var placer = function (node) {
                node.insertAfter(old);
                var newNode = $(old.next());
                old.remove();
                c.domNode = newNode;
            }
            this.prepareDom(c, placer);
            $('#PanelEdit').html(this.renderOptions(c));
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
  // TODO: Put this code on FieldType prototype?
  if (field.props.required) {
    $('#EditRequired').attr('checked', true);
  }
  if (field.showErrors) field.showErrors();
  // Switch to the Edit tab
  tabs.to('#TabEdit');
  // Set the current field, for next click
  this.current = field;
  return true;
}

FieldsManager.prototype.formPropsFeedback = function () {
    setupCopyValue({from:'#deformField1', to:'#DisplayTitle',
        defaul:'Untitled form'});
    setupCopyValue({from:'#deformField2', to:'#DisplayDescription',
        defaul:'Public Description of your form'});
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

FieldsManager.prototype.addBehaviour = function (field) {
  $('#' + field.props.id + 'Label')
    .click(funcForOnClickEdit(field, '#EditLabel', field.defaultLabel));
  $('#' + field.props.id + 'Description')
    .click(funcForOnClickEdit(field, '#EditDescription'));
  var instance = this;
  $('.deleteField', field.domNode).click(function () {
      if (field.props.field_id !== 'new') {
          instance.toDelete.push(field.props.field_id);
      }
      field.domNode.remove();
      delete instance.all[field.props.id];
      tabs.to('#TabAdd');
  });

  if (field.addBehaviour)  field.addBehaviour();
};

FieldsManager.prototype.persist = function () {
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
    json.form_public = $('input[name=public]').attr('checked');
    json.form_thanks_message = $('textarea[name=thanks_message]').val();
    json.deleteFields = this.toDelete;
    json.fields_position = $('#FormFields').sortable('toArray');
    // POST and set 2 callbacks: success and error.
    var instance = this;
    var jsonRequest = {json: $.toJSON(json)};
    var url = '/' + route_url('form', {action:'edit', id: json.form_id});
    if (window.console) console.log(url);
    $.post(url, jsonRequest)
    .success(function (data) {
        if (data.panel_form) {
            $('#PanelForm').html(data.panel_form);
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
            // Shows the generated public link
            $('#form_public_url').text(data.form_public_url)
            $('#form_public_url').attr('href', data.form_public_url)
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
