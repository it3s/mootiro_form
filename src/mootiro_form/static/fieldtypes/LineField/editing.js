LineField = new Object;
LineField.template = $.template(
    "<div id='${id}_container'><label for='${id}'>${label}</label>\n" +
    "<input type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
    "</div>");
LineField.render = function(context) {
  return $.tmpl(this.template, context);
};
LineField.insert = function(formFields, context) {
  this.render(context).appendTo(formFields);
};

fieldtypes['LineField'] = LineField;
