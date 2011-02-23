// Constructor
function TextField(props) {
    if (props) {
        this.props = props;
    } else {
        this.props = { // default values:
            label : 'What is your favourite colour?',
            defaul : 'Blue. No, wait -- green!'
        };
    }
    if (!this.props.id) this.props.id = fieldId.next();
//    id = props.id;
//    this.label = props.label;
//    this.defaul = props.defaul;
}


// Fields

TextField.prototype.template = $.template(
    "<li id='${id}_container'><label for='${id}'>${label}</label>\n" +
    "<input type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
    "</li>");
TextField.prototype.optionsTemplate = $.template('');


// Methods

TextField.prototype.render = function() {
  return $.tmpl(this.template, this.props);
};
TextField.prototype.insert = function(position) {
  // for now, only insert at the end
  domNode = this.render();
  $.event.trigger('AddField', [this, domNode]);
};

// Register this type
fieldTypes['TextField'] = TextField;
