// As the page loads, GET the templates file and compile the templates
$.get(route_url('root') + 'static/jquery-templates/form_edit.tmpl.html',
    function (fragment) {
        $('body').append(fragment);
        $.template('FieldBase', $('#fieldBaseTemplate'));
        $.template('optionsBase', $('#optionBaseTemplate'));
    }
);

function dir(object) {
    // Like Python dir(). Useful for debugging in IE8
    var methods = [];
    for (z in object) {
        if (typeof(z) !== 'number') methods.push(z);
    }
    return methods.join(', ');
}

function shallowCopy(o) { return jQuery.extend({}, o); }
function deepClone  (o) { return jQuery.extend(true, {}, o); }
function deepCompare(a, b) {
    return $.toJSON(a) === $.toJSON(b);
}

function positiveIntValidator(s, min) {
    if (typeof(s) === 'number') s = s.toString();
    if (s.contains('.')) return _('Invalid');
    var n = Number(s);
    if (isNaN(n)) return _('Invalid');
    if (min==null) min = 0;
    if (n < min) return _('Minimum is [0]').interpol(min);
    return '';
}

function methodCaller(o, method, arg) {
    return function () {
        return o[method](arg);
    }
}

function copyValue(from, to, defaul) {
    var from = $(from);
    var to = $(to);
    var v = from.val() || defaul;
    to.val(v);
    if (to[0].canHaveHTML === undefined || to[0].canHaveHTML) {
        // Normal browsers can always change both value and innerText.
        // On IE the following line raises an exception if
        // canHaveHTML (a JScript-only property) is false.
        to.text(v);
    }
}

function setupCopyValue(o) { // from, to, defaul, obj, callback
    // Sets up an input so changes to it are reflected somewhere else
    if (o.defaul==null) o.defaul = '';
    copyValue(o.from, o.to, o.defaul);
    function handler(e) { // called when a change occurs
        copyValue(this, o.to, o.defaul);
        if (o.callback) {
            var v = $(o.from).val() || o.defaul;
            if (o.obj) {
                o.obj[o.callback](v);
            } else{
                o.callback(v);
            }
        }
    }
    $(o.from).keyup(handler).change(handler);
}


// Constructor
function Tabs(tabs, contents) {
    $(contents).hide();
    $(contents + ":first").show();
    $(tabs + " li:first").addClass("selected");
    var instance = this;
    this.to = function (tab) { // Most important method, switches to a tab.
        $(contents).hide();
        $(tabs + " li").removeClass("selected");
        $(tab).addClass("selected");
        $($(tab).children().attr("href")).show();
        $('#PanelTitle').text($(tab).children().attr('title'));
    };
    $(tabs + " li").click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
}
Tabs.prototype.showNear = function (tabName, domNode) {
    // Changes tabs and shows the panel right besides domNode.
    // If domNode is not passed, the panel position is reset.
    if (!domNode) domNode = $('#RightCol');
    var tab = $('#Tab' + tabName);
    var panel = $('#Panel' + tabName);
    var desiredTop = domNode.position().top - $('#RightCol').position().top;
    panel.css('margin-top', desiredTop);
    this.to(tab);
};


function Sequence(start) {
    this.current = start || 0;
    this.next = function () {
        return ++this.current;
    };
}
fieldId = new Sequence();
fieldId.currentString = function () {
    return 'field_' + this.current;
}
fieldId.nextString = function () {
    this.next();
    return this.currentString();
}


function onHoverSwitchImage(selector, where, hoverImage, normalImage) {
    $(selector, where).hover(
        function () {$(this).attr({src: hoverImage});},
        function () {$(this).attr({src: normalImage});}
    );
}


dirt = {  // Keeps track of whether the form is dirty, and consequences
    // such as enabling the Save button and leaving the page.
    watching: false,  // we only mark as dirty when this is true
    saving: false,  // holds the ID of the current save attempt
    alt: new Sequence(), // holds the current alteration number
    saved: 0,  // holds the alteration number last successfully saved
    $indicator: $('#FormHasBeenSaved'),
    $aveButton: $('#SaveForm').attr('disabled', true),
    disableSaveButton: function () {
        if (!this.$aveButton.attr('disabled')) {
            $('#SaveForm img').toggle();
            this.$aveButton.attr('disabled', true);
        }
    },
    enableSaveButton: function () {
        if (this.$aveButton.attr('disabled')) {
            $('#SaveForm img').toggle();
            this.$aveButton.attr('disabled', false);
        }
    },
    saveStart: function () {  // returns the current alteration number
        this.disableSaveButton();
        this.saving = true;
        this.$indicator.text(_('Saving...')).show();
        return this.alt.current;
    },
    saveSuccess: function (altNumber) {
        // The caller must pass the alteration number.
        this.saving = false;
        this.saved = altNumber;
        this.$indicator.text(_('Saved.')).show().fadeOut(7000);
    },
    saveFailure: function () {
        this.saving = false;
        this.$indicator.text(_('ERROR')).show();
        this.enableSaveButton();
    },
    isDirty: function () {
        return this.alt.current > this.saved;
    },
    onAlteration: function (e) { // Marks form as dirty, enables Save button.
        // Using "dirt" instead of "this" because this function is a handler.
        if (!dirt.watching) return;
        dirt.alt.next();  // increment the alteration number
        dirt.enableSaveButton();
    },
    watch: function (selector, events) {
        // Configures the selected nodes so, when *events* occur, the form is
        // considered dirty and the save button is enabled.
        $(selector).live(events, this.onAlteration);
    }
};
// Other parts of the code may make calls such as this:
dirt.watch($("input, textarea[readonly!='readonly'], select", '#LeftCol'),
           'change keyup');
window.onbeforeunload = function () {
    // Confirm before leaving page if form is dirty.
    if (dirt.isDirty())
        return _("You have not saved your alterations to this form.");
};


// Constructor; must be called in the page.
function FieldsManager(formId, json, field_types) {
    var instance = this;
    this.formId = formId;
    this.all = {};
    this.types = {};
    this.toDelete = [];
    this.current = null; // the field currently being edited
    this.normalMoveIcon = route_url('root') + 'static/img/icons-edit/move.png';
    this.$panelEdit = $('#PanelEdit');

    $.each(field_types, function (index, type) {
        instance.types[type] = eval(type);
    });

    $.each(this.types, function (type_name, type) {
      if (type.prototype.load) {
          type.prototype.load();
      }
    });

    var whenReady = function () {
        onDomReadyInitFormEditor();
        instance.place = $('#FormFields');
        $.each(json, function (index, props) {
            instance.insert(instance.instantiateField(props), null, false);
        });
        instance.formPropsFeedback();
        // instance.place.bind('AddField', addField);
        instance.resetPanelEdit();
        // Finally remove this ajaxStop handler since this function is
        // supposed to be executed only once:
        $(document).unbind('ajaxStop', whenReady);
    }
    $(document).ajaxStop(whenReady);
}

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
};

FieldsManager.prototype.renderPreview = function (field) {
    // Returns a DOM node containing the rendered field for the right column.
    // If the field implements renderPreview(), use that instead.
    if (field.renderPreview) {
        return field.renderPreview();
    } else {
        var tplContext = {props: field.props, fieldTpl: field.previewTemplate};
        return $.tmpl('FieldBase', tplContext);
    }
};

FieldsManager.prototype.renderOptions = function (field) {
    // Returns a DOM node containing the HTML for the Edit tab.
    // If the field implements renderOptions(), use that instead.
    if (field.renderOptions) {
        return field.renderOptions();
    } else {
        var tplContext = {props: field.props,
            BottomBasicOptionsTpl: field.bottomBasicOptionsTemplate,
            AdvancedOptionsTpl: field.advancedOptionsTemplate};
        return $.tmpl('optionsBase', tplContext);
    }
};

FieldsManager.prototype.insert = function (field, field_before, effect) {
    // Renders and displays the passed `field`.
    // If `field_before` is provided, display the `field` just after it.
    // If `field` is a string, that is the field type; create a brand new field.
    if (window.console) console.log('insert()');
    if (typeof(field)==='string') {
        field = this.instantiateField(field);
    }  // `field` is now a real field object.
    this.all[field.props.id] = field;
    field.domNode = this.renderPreview(field);
    this.addBehaviour(field);
    if (field_before) {
        if (effect)
            field.domNode.hide().insertAfter(field_before.domNode).slideDown();
        else
            field.domNode.insertAfter(field_before.domNode);
    } else {
        if (effect)
            field.domNode.hide().appendTo(this.place).slideDown();
        else
            field.domNode.appendTo(this.place);
    }
};

FieldsManager.prototype.addField = function (typ) {
    // Adds a field when the user clicks on an icon in the Add tab.
    this.insert(typ, null, true);
    dirt.onAlteration('addField');
    // $.event.trigger('AddField', [field, domNode, position]);
};

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
};

FieldsManager.prototype.showOptions = function (field) {
    if (window.console) console.log('showOptions()');
    // Render the field properties at the left, then animate them
    this.$panelEdit.html(this.renderOptions(field));
    if (field.afterRenderOptions) field.afterRenderOptions();
    this.repositionOptions(field);
    if (field.showErrors)  field.showErrors();
};

FieldsManager.prototype.repositionOptions = function (field) {
    if (!field) return;
    // Move the panel close to the field being edited.
    // Calculate new position BEFORE animating (solves IE animation bug)
    var offset = field.domNode.offset().top;
    var marginTop = offset - $('#PanelTitle').offset().top - 40;
    function scrollWindow() {
        $('html, body').animate({scrollTop: offset}, 
            function () {
                $.event.trigger('FinishPanelMovement');
            });
    }
    this.$panelEdit.animate({'margin-top': marginTop}, 200, scrollWindow);
};

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
};

FieldsManager.prototype.saveCurrent = function () {
    if (window.console) console.log('saveCurrent()');
    var S1 =
        _("The current field has errors, displayed on the left column.");
    var S2 = _("Lose your alterations?");
    // If there is no current field, we just don't care:
    if (!this.current)  return true;
    // First validate the alterations to the field.
    if (!this.validateCurrent()) {
        tabs.to('#TabEdit'); // Display the errors so the user gets a hint
        if (confirm([S1, S2].join('\n'))) {
            this.$panelEdit.html(this.renderOptions(this.current));
            this.redrawPreview(this.current);
            this.instantFeedback(this.current);
            return true; // don't save but proceed
        } else {
            return false; // don't save and stop
        }
    }
    var p = this.current.props;
    // Store (in the client) the information in the left form
    p.label = $('#EditLabel').val();
    p.required = $('#EditRequired').attr('checked');
    p.description = $('#EditDescription').val();
    // These are the common attributes; now to the specific ones:
    if (this.current.save)  this.current.save();
    return true;
};

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
    this.showOptions(field);
    // Set the current field, for next click
    this.current = field;
    return true;
};

FieldsManager.prototype.formPropsFeedback = function () {
    setupCopyValue({from:'#deformField1', to:'#DisplayTitle',
        defaul:_('Untitled form')});
    setupCopyValue({from:'#deformField2', to:'#DisplayDescription',
        defaul:_('Public description of this form')});
    setupCopyValue({from:'#deformField3', to:'#submit',
        defaul:_('Submit')});
    $('#submit').click(function () {
        tabs.to('#TabForm');
        $('#deformField3').focus();
    });
};

FieldsManager.prototype.instantFeedback = function (field) {
    setupCopyValue({from:'#EditLabel', to:$('#' + field.props.id + 'Label'),
        defaul:'\n'});
    var instance = this;
    var hideDescriptionIfEmpty = function (v) {
        if (v == "") {
            $('#' + field.props.id + 'Description').hide();
        } else {
            $('#' + field.props.id + 'Description').show();
        }
    };
    setupCopyValue({from:'#EditDescription', to:'#' + field.props.id +
                   'Description', defaul:null,
                   callback: hideDescriptionIfEmpty});
    $('#EditRequired').change(function (e) {
        var origin = $('#EditRequired');
        var dest = $('#' + field.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
    });
    if (field.instantFeedback) field.instantFeedback();
};

var panelEditHtmlContent = $('#PanelEdit').html();
FieldsManager.prototype.resetPanelEdit = function () {
    this.$panelEdit.html(panelEditHtmlContent).animate({'margin-top': 0});
    this.current = null;
};

FieldsManager.prototype.addBehaviour = function (field) {
    if (window.console) console.log('addBehaviour()');
    $('#' + field.props.id + 'Label', field.domNode)
        .click(funcForOnClickEdit(field, '#EditLabel', field.defaultLabel));
    $('#' + field.props.id + 'Description', field.domNode)
        .click(funcForOnClickEdit(field, '#EditDescription'));
    // Buttons at field right: clone, move, delete
    onHoverSwitchImage('.cloneField', field.domNode,
        route_url('root') + 'static/img/icons-edit/cloneHover.png',
        route_url('root') + 'static/img/icons-edit/clone.png');
    onHoverSwitchImage('.moveField', field.domNode,
        route_url('root') + 'static/img/icons-edit/moveHover.png',
        this.normalMoveIcon);
    onHoverSwitchImage('.deleteField', field.domNode,
        route_url('root') + 'static/img/icons-edit/deleteHover.png',
        route_url('root') + 'static/img/icons-edit/delete.png');
    var instance = this;
    $('.deleteField', field.domNode).click(function () {
        dirt.onAlteration('deleteField');
        if (field.props.field_id !== 'new') {
            instance.toDelete.push(field.props.field_id);
        }
        // If the field being deleted is the current field, remove its
        // properties from the left column.
        if (field === instance.current) instance.resetPanelEdit();
        delete instance.all[field.props.id];
        field.domNode.slideUp(400, function () {field.domNode.remove();});
    });
    $('.cloneField', field.domNode).click(function (e) {
        instance.cloneField(field);
    });
    if (field.addBehaviour)  field.addBehaviour();
};

FieldsManager.prototype.cloneField = function (field) {
    if (!field && this.current)  field = this.current;
    if (field === this.current && !this.saveCurrent())  return;
    var props = deepClone(field.props);
    props.field_id = 'new';
    props.label += ' (copy)';
    var clone = this.instantiateField(props);
    // The field itself might have to make adjustments to its data
    if (clone.clone)  clone.clone(field);
    // Make clone appear just after the original field
    this.insert(clone, field, true);
    dirt.onAlteration('cloneField');
    return clone;
};

FieldsManager.prototype.getCurrentFormProps = function () {
    // Returns a dictionary with all props except fields props.
    var d = {};
    // Form tab
    d.form_desc = $('textarea[name=description]').val();
    d.form_title = $('input[name=name]').val();
    d.submit_label = $('input[name=submit_label]').val();
    // Visual tab
    d.system_template_id = $('input[name=system_template_id]').val();
    // Other info
    d.form_id = this.formId || 'new';
    d.deleteFields = this.toDelete;
    d.fields_position = $('#FormFields').sortable('toArray');
    return d;
}

FieldsManager.prototype.persist = function () {
    if (window.console) console.log('persist()');
    // Saves the whole form, through an AJAX request.
    // First, save the field previously being edited
    if (!this.saveCurrent()) return false;
    var altNumber = dirt.saveStart();
    /* Prepare form fields */
    var ff = [];
    $.each(this.all, function (id, field) {
        ff.push(field.props);
    });
    var json = this.getCurrentFormProps();
    json.fields = ff;
    // POST and set 2 callbacks: success and error.
    var instance = this;
    var jsonRequest = {json: $.toJSON(json)};
    var url = route_url('form', {action:'edit', id: json.form_id});
    var NYAHH = _("Sorry, your alterations have NOT been saved.") + '\n';
    var NYAH2 = _("Please correct the errors as proposed in the highlighted text.");
    $.post(url, jsonRequest)
    .success(function (data) {
        if (data.field_validation_error) {
           dirt.saveFailure();
           alert(NYAHH + data.field_validation_error);
           return false;
        }
        if (data.panel_form) {
            $('#PropertiesForm').html(data.panel_form);
            instance.formPropsFeedback();
        }
        if (data.error) {
            tabs.to('#TabForm');
            dirt.saveFailure();
            alert(NYAHH + NYAH2);
        } else {
            instance.formId = data.form_id;
            /* New fields and new options have received IDs on the server;
             * update them so we can save again. */
            $.each(data.new_fields_id, function (f_idx, f) {
                instance.all[f_idx].props.field_id = f.field_id;
            });
            $.each(data.save_options_result, function (f_idx, f) {
                instance.all[f_idx].update(f);
            });
            // Assume any deleted fields have been deleted at the DB
            instance.toDelete = [];
            // Congratulations, the form is saved. Remember so.
            dirt.saveSuccess(altNumber);
        }
    })
    .error(function (data) {
        dirt.saveFailure();
        alert(NYAHH + _("Status: [0]").interpol(data.status));
    });
    return true;
};


// When user clicks on the right side, the Edit tab appears and the
// corresponding input gets the focus.
function funcForOnClickEdit(field, target, defaul) {
    return function () {
        if (!fields.switchToEdit(field))  return false;
        fields.instantFeedback(field);
        var focus_on_target = function () {
            $(target).focus();
            $('body').unbind('FinishPanelMovement');
        }
        $('body').bind('FinishPanelMovement', focus_on_target);
        // Sometimes also select the text. (If it is the default value.)
        if ($(target).val() === defaul) $(target).select();
        return false;
    };
}


// Object that shares code between Text and TextArea fields,
textLength = {};  // especially for char and word length validation.
textLength.getErrors = function () {
    // Returns an object containing validation errors to be shown
    errors = {defaul: ''};
    var minLength = $('#EditMinLength').val();
    var maxLength = $('#EditMaxLength').val();
    var minWords = $('#EditMinWords').val();
    var maxWords = $('#EditMaxWords').val();
    errors.minLength = positiveIntValidator(minLength, 1);
    errors.maxLength = positiveIntValidator(maxLength, 1);
    errors.minWords = positiveIntValidator(minWords, 1);
    errors.maxWords = positiveIntValidator(maxWords, 1);
    // Only now convert to number, to further validate
    minLength = Number(minLength);
    maxLength = Number(maxLength);
    minWords = Number(minWords);
    maxWords = Number(maxWords);
    if (!errors.maxLength && minLength > maxLength)
        errors.minLength = _('Higher than max');
    if (!errors.maxWords && minWords > maxWords)
        errors.minWords = _('Higher than max');
    var defaul = $('#EditDefault').val();
    var lendefault = defaul.length;
    var enableWords = $('#EnableWords').attr('checked');
    var enableLength = $('#EnableLength').attr('checked');

    var defaulErrors = [];
    if (lendefault && enableLength) {
        if (minLength > lendefault)
            defaulErrors.push(_('Shorter than min length. '));
        if (maxLength < lendefault)
            defaulErrors.push(_('Longer than max length. '));
    }
    if (lendefault && enableWords) {
        var words = defaul.wordCount();
        if (minWords > words)
            defaulErrors.push(_('Shorter than min words.'));
        if (maxWords < words)
            defaulErrors.push(_('Longer than max words.'));
    }
    errors.defaul = defaulErrors.join(' ');

    return errors;
}
textLength.showErrors = function (errors) {
    if (!errors) errors = this.getErrors();
    $('#ErrorDefault').text(errors.defaul);
    $('#ErrorMinWords').text(errors.minWords);
    $('#ErrorMaxWords').text(errors.maxWords);
    $('#ErrorMinLength').text(errors.minLength);
    $('#ErrorMaxLength').text(errors.maxLength);
}
textLength.instantFeedback = function (field) {
    setupCopyValue({from: '#EditDefault', to: '#' + field.props.id,
        obj: field, callback: 'showErrors'});
    var h = methodCaller(field, 'showErrors');
    $('input.LengthEdit').keyup(h).change(h);
    $('#EnableLength').change(h);
    $('#EnableWords').change(h);
    // Display length options when "Specify length" is clicked
    collapsable({divSelector: '#LengthProps'});
}
textLength.save = function (field) {
    var p = field.props;
    p.defaul = $('#EditDefault').val();
    p.maxWords = $('#EditMaxWords').val();
    p.minWords = $('#EditMinWords').val();
    p.maxLength = $('#EditMaxLength').val();
    p.minLength = $('#EditMinLength').val();
    p.enableWords = $('#EnableWords').attr('checked');
    p.enableLength = $('#EnableLength').attr('checked');
}


collapsable = function (o) {
    // Makes a div appear collapsed; it expands when user clicks on the handle.
    // Adds a dynamic triangular icon to the left of the handle.
    // The argument is an options object which may contain:
    // divSelector (required), handleSelector, iconCollapsed, iconCollapsable.
    if (!o.handleSelector)  o.handleSelector = o.divSelector + 'Handle';
    var handle = $(o.handleSelector);

    // If a method is already there, this function has already run, so do nothing.
    if (handle[0].toggleIcon)  return;

    var div = $(o.divSelector);
    div.hide();
    handle.addClass('Collapser');
    handle.html("<span class='CollapserIcon'>\u25b6</span> " + handle.html());
    var icon = $('span.CollapserIcon', handle);
    if (!o.iconCollapsed)   o.iconCollapsed = '\u25b6';  // '▶';
    if (!o.iconCollapsable) o.iconCollapsable = '\u25bc'; // ▼
    handle.toggleIcon = handle[0].toggleIcon = function () {
        if (icon.text() == o.iconCollapsed)
            icon.text(o.iconCollapsable);
        else
            icon.text(o.iconCollapsed);
    };
    handle.click(function () {
        div.slideToggle();
        handle[0].toggleIcon();
    });
}

onDomReadyInitFormEditor = function () {
    $('#SaveForm').click(function (e) { fields.persist(); });
    tabs = new Tabs('.ui-tabs-nav', '.ui-tabs-panel');
    $('#FormFields').sortable({
        placeholder: 'fieldSpace',
        forcePlaceholderSize: true,
        handle: '.moveField',
        containment: 'document',
        stop: onFieldDragStop});
    // The "add field" button, at the bottom left, must show icons besides the
    // field currently being edited.
    $('#AddField').click(function () {
        if (fields.current)
            tabs.showNear('Add', fields.current.domNode);
        else
            tabs.showNear('Add');
    });
    // The "Add field" tab, when clicked, must show its contents at the TOP.
    $('#TabAdd').unbind().click(function () {
        tabs.showNear('Add');
    });

    // Setup system template icon buttons
    $('#SystemTemplatesList li').click(function () {
        $('#SystemTemplatesList .icon_selected').hide();
        $('#SystemTemplatesList .icon').show();
        $(this).find(".icon").hide();
        $(this).find(".icon_selected").show();
        $('input[name=system_template_id]').val(this.id);
        setSystemTemplate(this.id);
        dirt.onAlteration('setFormTemplate');
    });
    var st_id = $('input[name=system_template_id]').val();
    $('#SystemTemplatesList li:nth-child('+ st_id +')').click();
    // The last step is to start watching for alterations
    dirt.watching = true;
};

function onFieldDragStop(event, ui) {
    dirt.onAlteration('fieldDrag');
    // 1. Move the panel close to the field being edited
    fields.repositionOptions(fields.current);
    // 2. Ensure the handle is not blue after moving a field
    var moveIcon = $('.moveField', ui.item);
    moveIcon.attr('src', fields.normalMoveIcon);
}

// Template
function setSystemTemplate(id) {
    var url = route_url('form_template', {action:'system_template', id: id});
    $.post(url)
    .success(setFormTemplate)
    .error(function (data) {
        alert(_("Sorry, error retrieving template on the server.\nStatus: [0]")
            .interpol(data.status));
    });
}

function templateFontConfig(font) {
    var cssObj = {};
    cssObj["font-family"] = font.name;
    cssObj["font-size"] = font.size;
    if (font.bold) cssObj["font-weight"] = 'bold';
    if (font.italic) cssObj["font-style"] = 'italic';
    return cssObj;
}

function setFormTemplate(template) {
    // Colors
    var c = template.colors;
    $('#OuterContainer').css('background-color', c.background);
    $('#RightCol #Header').css('background-color', c.header);
    $('#RightCol #FormDisplay').css('background-color', c.form);
    $('ul#FormFields li').live('mouseover mouseout', function(event) {
        if (event.type == 'mouseover') {
            $(this).css('background-color', c.highlighted_field);
        } else {
            $(this).css('background-color', 'transparent');
        }
    });
    // Fonts
    var f = template.fonts;
    $('#RightCol #Header h1').css(templateFontConfig(f.title));
    $('#RightCol #Header p').css(templateFontConfig(f.subtitle));
    $('#FormDisplay').css(templateFontConfig(f.form));
}
