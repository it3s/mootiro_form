var field_template = $.template('field_template', "<div class='fieldLine'><div class='fieldLabel'>${position}. ${label}</div><div class='fieldData'>${data}</div></div>");

var entry_template = "{{each fields}}{{tmpl($value) 'field_template'}}{{/each}}";

function get_entry_data(id) {
  return function () {
    entry_data_url = 'http://' + url_root + route_url('entry', {action: 'data', id: id});
    $.ajax({
      url: entry_data_url, 
      success: show_entry_data
      }); 
  }
}

function show_entry_data(entry) {
  $('#entryBox').dialog({dialogClass: 'dialog'});
  $('#entryBox').html($.tmpl(entry_template, entry));
  $('.fieldLine:odd').toggleClass('fieldLineOdd');
}

function delete_entry(id) {
  console.log(id);
    $('#deleteEntryBox').dialog({
      resizable: false,
      height: 140,
      modal: true,
      buttons: {
        "Delete": function() {
          delete_entry_url = 'http://' + url_root + route_url('entry', {action: 'delete', id: id});
          console.log(delete_entry_url);
          $.post({
            url: delete_entry_url,
            success: delete_entry_callback,
            error: alert("Couldn't delete the entry"),
            });
          $(this).dialog("close");
          },
        "Cancel": function() {
          $(this).dialog("close");
        }
      }
    });
}

//This function deletes the entry line in the template
function delete_entry_callback(data){
  alert("Data.entry_id = " + data.entry_id);
  $.remove("#entry_" + data.entry_id);
}

