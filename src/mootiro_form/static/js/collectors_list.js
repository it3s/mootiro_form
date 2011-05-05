$.get(route_url('root') + 'static/jquery-templates/collectors_list.tmpl.html',
    function (fragment) {
        $('body').append(fragment);
        $.template("collectorsTable", $('#collectorsTable'));
        $.template("collectorRow", $('#collectorRow'));
        $.tmpl("collectorsTable", {}).appendTo('#middle');
        $.tmpl("collectorRow", collectors_json).appendTo('#collectorsRows');
    }
);


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
    };
    $(tabs + " li").click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
}
tabs = new Tabs('#publicLinkDialog .menu', '#publicLinkDialog .Panel');  // Instantiate tabs.


function dictToString(d) {
    // Turn something like a colander errors dict into a user-friendly string.
    s = '';
    for (i in d) {
        v = d[i];
        if (typeof(v)==='string' && v)  s += '' + i + ': ' + v + '\n';
    }
    return s;
}


manager = {
    $publicLinkDialog: $('#publicLinkDialog'),
    currentId: 'new',  // holds the ID of the collector currently being edited
    showPublicLinkDialog: function (d) {
        $('#pl_name').val(d['name']);
        $('#pl_thanks_message').val(d['thanks_message']);
        $('#pl_thanks_url').val(d['thanks_url']);
        $('#pl_start_date').val(d['start_date']);
        $('#pl_end_date').val(d['end_date']);
        $('#pl_message_before_start').val(d['message_before_start']);
        $('#pl_message_after_end').val(d['message_after_end']);
        $('#pl_limit_by_date').attr('checked', (d['limit_by_date']));
        // TODO: set radiobuttons, too

        manager.$publicLinkDialog.dialog({
            width: 'auto',
            minHeight:'300px',
            modal: true,
            buttons: [
                {text: 'Save', click: manager.savePublicLink},
                {text: 'Cancel', click: manager.closePublicLink}
            ]
        });
    },
    editPublicLink: function (id) {
        this.currentId = id;
        var url = route_url('collector',
            {'form_id': this.formId, 'id': id, action: 'as_json'});
        if (id == 'new') {
            this.showPublicLinkDialog({});
        } else {
            $.get(url).success(this.showPublicLinkDialog)
            .error(function (d) {
                alert("Sorry, could not retrieve the data for this collector."
                    + "\nStatus: " + d.status);
            });
        }
    },
    closePublicLink: function (e) {
        manager.$publicLinkDialog.dialog('close');
    },
    publicLinkProps: function () {
        // Converts values from the popup into a dictionary.
        // This function is NOT being used; I went with another solution.
        texts = ['name', 'thanks_message', 'thanks_url', 'start_date',
            'message_before_start', 'end_date', 'message_after_end']
        d = {
            on_completion:
                $('input[name=on_completion]:checked').val()
        };
        $.each(texts, function (i, t) {  // Copy values of the text inputs
            d[t] = $('#pl_' + t).val();
        });
        return d;
    },
    savePublicLink: function (e) {
        $.post(route_url('collector', {action: 'save_public_link',
            id: manager.currentId, form_id: manager.formId}),
            $('#publicLinkForm').serialize()
        ).success(function (d) {
            if (d.id) {  // success, saved
                if (window.console) console.log('success', d);
                // Considering a new public link, add it to the list
                // TODO: Redraw the row when it already exists
                $.tmpl("collectorRow", d).appendTo('#collectorsRows');
                manager.closePublicLink(e);
            } else {  // d contains colander errors
                alert("Sorry, the collector was not saved. Errors:\n" +
                    dictToString(d));
            }
        }).error(function (d) {
            alert("Sorry, the collector was not saved. Status: " + d.status);
        });
    }
};

$('#btnNewPublicLink').click(function (e) {
    manager.editPublicLink('new');
});

var $listTable = $('#CollectorsListTable');
$listTable.find('tr td:nth-child(2n)').addClass('darker');
$listTable.find('thead th:nth-child(2n)').addClass('darker');

// TODO: Move this function to a new global.js lib
function onHoverSwitchImage(selector, where, hoverImage, normalImage) {
    $(selector, where).live('mouseover mouseout', function(event) {
        if (event.type == 'mouseover') {
            $(this).attr({src: hoverImage});
        } else {
            $(this).attr({src: normalImage});
        }
    });
}


$('.editIcon').live('click', function () {
    var parts = this.id.split('-');
    var id = parts[parts.length-1];
    manager.editPublicLink(id);
});
onHoverSwitchImage('.editIcon', $listTable,
    route_url('root') + 'static/img/icons-root/editHover.png',
    route_url('root') + 'static/img/icons-root/edit.png'
);
onHoverSwitchImage('.copyIcon', $listTable,
    route_url('root') + 'static/img/icons-root/copyHover.png',
    route_url('root') + 'static/img/icons-root/copy.png');
onHoverSwitchImage('.deleteIcon', $listTable,
    route_url('root') + 'static/img/icons-root/deleteHover.png',
    route_url('root') + 'static/img/icons-root/delete.png');
