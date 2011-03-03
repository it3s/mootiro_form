// Constructor
function ListField(props) {
    this.defaultLabel = 'List field';
    if (props) {
        this.props = props;
        this.props.id = fieldId.nextString();
    } else {
        this.props = {
            id : fieldId.nextString(),
            field_id : 'new',
            type : 'ListField',
            label : this.defaultLabel,
            defaul : '',
            description : '',
            required : '',
            list_type : 'select'
        };
    }
}

ListField.prototype.render = function () {
    return $.tmpl(this.template[this.props.list_type], this.props);
}

// Fields

ListField.prototype.optionsTemplate = $.template(
  "<input id='field_idx' type='hidden' name='field_idx' value='${id}'/>\n" +
  "<input id='field_id' type='hidden' name='field_id' value='${field_id}'/>\n" +
  "<label for='EditLabel'>Label*</label>\n" +
  "<input type='text' name='label' value='${label}' id='EditLabel' />\n" +
  "<label for='EditDefault'>Default value</label>\n" +
  "<input type='text' name='defaul' value='${defaul}' id='EditDefault' />\n" +
  "<label for='EditDescription'>Brief description</label>\n" +
  "<textarea id='EditDescription' name='description'>${description}" +
  "</textarea>\n" +
  "<input type='checkbox' id='EditRequired' name='required' />\n" +
  "<label for='EditRequired'>required</label>\n");

ListField.prototype.option_template = {};
ListField.prototype.option_template['select'] = $.template("option",
        "<option value=${id}>${label}</option>"
        );

ListField.prototype.template = {};
ListField.prototype.template['select'] = $.template(
  "<li id='${id}_container'><label id='${id}Label' class='desc' " +
  "for='${id}'>${label}</label>" +
  "<span id='${id}Required' class='req'>" +
  "{{if required}}*{{/if}}</span>\n" +
  "<div class='Description' id='${id}Description'>${description}</div>\n" +
  "<select name='select-${id}' id='${id}'>\n" +
  "{{each options}}{{tmpl($value) 'option'}}{{/each}}</select>" +
  "</li>\n");

// Methods

ListField.prototype.save = function() {
  // Copies to props the information in the left form
  this.props.label = $('#EditLabel').val();
  this.props.defaul = $('#EditDefault').val();
  this.props.required = $('#EditRequired').attr('checked');
  this.props.description = $('#EditDescription').val();
}

ListField.prototype.addBehaviour = function () {
  var instance = this;
  var labelSelector = '#' + this.props.id + 'Label';

  var instantFeedback = function () {
      setupCopyValue('#EditLabel', labelSelector, 'Question');
      setupCopyValue('#EditDescription', '#' + instance.props.id +
          'Description', null, true);
      $('#EditRequired').change(function (e) {
        var origin = $('#EditRequired');
        var dest = $('#' + instance.props.id + 'Required');
        if (origin.attr('checked'))
            dest.html('*');
        else
            dest.html('');
      });
  }

  // When user clicks on the right side, the Edit tab appears and the
  // corresponding input gets the focus.
  var funcForOnClickEdit = function (target, defaul) {
    return function () {
      fields.switchToEdit(instance);
      instantFeedback();
      $(target).focus();
      // Sometimes also select the text. (If it is the default value.)
      if ($(target).val() === defaul) $(target).select();
      return false;
    };
  };

  $(labelSelector).click(funcForOnClickEdit('#EditLabel', this.defaultLabel));
  $('#' + this.props.id).click(funcForOnClickEdit('#EditDefault'));
  $('#' + this.props.id + 'Description')
    .click(funcForOnClickEdit('#EditDescription'));
};

// Register it
fields.types['ListField'] = ListField;
