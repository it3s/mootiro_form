TextField = new Object;
TextField.template = $.template(
    "<li id='${id}_container'><label for='${id}'>${label}</label>\n" +
    "<input type='text' name='${id}' id='${id}' value='${defaul}' />\n" +
    "</li>");
TextField.optionsTemplate = $.template('');
TextField.render = function(context) {
  return $.tmpl(this.template, context);
};
TextField.insert = function(properties) {
  if (properties) {
      this.properties = properties;
  } else {
      this.properties = TextField.properties;
  }
  this.properties.id = nextFieldId();
  domNode = this.render(this.properties);
  $.event.trigger('AddField', [this, domNode]);
};
TextField.properties = { // default values:
    label : 'What is your favourite colour?',
    defaul : 'Blue. No, wait -- green!'
};

fieldtypes['TextField'] = TextField;

/*
lista = [];
f = $('#FormFields')[0]
f.edgar = {txt : 'walrus'};
lista.push(f.edgar);
console.log(lista[0].txt);
lista[0].txt = 'aivuk';
console.log(f.edgar.txt);
console.log(lista[0].txt);
*/
