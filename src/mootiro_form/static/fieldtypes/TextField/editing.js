TextField = new Object;
TextField.template = $.template(
    "<li id='${id}_container'><label for='${id}'>${label}</label>\n" +
    "<input type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
    "</li>");
TextField.render = function(context) {
  return $.tmpl(this.template, context);
};
TextField.insert = function(formFields, context) {
  this.render(context).appendTo(formFields);
};

fieldtypes['TextField'] = TextField;
