LineField = new Object;
LineField.render = function() {
  $.tmpl("<div><label for='{0}'>{1}</label>" +
         "<input type='text' value='{2}' /></div>");
  return $('<div>').child('<label>').text('bruHAHA');
};
LineField.insert = function(formFields) {
  this.render().appendTo(formFields);
};
fieldtypes['LineField'] = LineField;
