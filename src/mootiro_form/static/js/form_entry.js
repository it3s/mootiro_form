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
    $('#entryData').html($.tmpl(entry_template, entry));
    $('#entryNumber').val(entry['entry_number']);
    $('.fieldLine:odd').toggleClass('fieldLineOdd');
}

$(function () {
  $('#previousButton').click(function () {
    // Obtain the current item in the select
    current_entry = $('#entryNumber :selected');
    // If it is the first item, do nothing (return) / disable the button??
    if (current_entry.index() == 1) {
      $('#previousButton').addClass('disabledButton');
    }
    if (current_entry.index() + 1 == $('#entryNumber option').length) {
      $('#nextButton').removeClass('disabledButton');
    }
    // Obtain the previous item
    previous_entry = current_entry.prev();
    //console.log(previous_entry);
    // Display the entry
    previous_entry.trigger('click');
  });

  $('#nextButton').click(function () {
    current_entry = $('#entryNumber :selected');
    //console.log(current_entry.index());
    //console.log("Agora o valor de length");
    //console.log($('#entryNumber option').length);
    if (current_entry.index() + 2 == $('#entryNumber option').length) {
      $('#nextButton').addClass('disabledButton');
      //next_entry = $('#entryNumber option:first-child');
      //next_entry.trigger('click');
    }
    if (current_entry.index() == 0) {
      $('#previousButton').removeClass('disabledButton');
    }
    next_entry = current_entry.next();
    next_entry.trigger('click');
  });
});


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




