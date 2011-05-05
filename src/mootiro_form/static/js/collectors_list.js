$.get(route_url('root') + 'static/jquery-templates/collectors_list.tmpl.html',
    function (fragment) {
        $('body').append(fragment);
        $.template("collectorsTemplate", $('#collectorsTemplate'));
        $.template("collectorsRowsTemplate", $('#collectorsRowsTemplate'));
        $.tmpl("collectorsTemplate", {}).appendTo('#middle');
        $.tmpl("collectorsRowsTemplate", {"collector_name": 'Jonas'}).appendTo('#collectors_rows');
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
tabs = new Tabs('.ui-tabs-nav', '.ui-tabs-panel');  // Instantiate tabs.


manager = {
    $publicLinkWindow: $('#publicLinkWindow'),
    currentId: 'new',  // holds the ID of the collector currently being edited
    editPublicLink: function (id) {
        this.currentId = id;
        // TODO Load the instance by the id
        this.$publicLinkWindow.dialog({
            width: 'auto',
            minHeight:'300px',
            modal: true,
            buttons: [
                {text: 'Save', click: manager.savePublicLink},
                {text: 'Cancel', click: manager.cancelPublicLink}
            ]
        });
    },
    cancelPublicLink: function (e) {
        manager.$publicLinkWindow.dialog('close');
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
        //~ var d = manager.publicLinkProps();
        //~ if (window.console) console.log(d);

        // TODO: Treat the ajax results and possible errors...
        $.post(route_url('collector', {action: 'save_public_link',
            id: manager.currentId, form_id: formId}),
            $('#publicLinkForm').serialize());
        // http://api.jquery.com/submit/
    }
};

$('#btnNewPublicLink').click(function (e) {
    manager.editPublicLink('new');
});

// Collectors List Table

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

onHoverSwitchImage('.editIcon', $listTable,
    route_url('root') + 'static/img/icons-root/editHover.png',
    route_url('root') + 'static/img/icons-root/edit.png');
onHoverSwitchImage('.copyIcon', $listTable,
    route_url('root') + 'static/img/icons-root/copyHover.png',
    route_url('root') + 'static/img/icons-root/copy.png');
onHoverSwitchImage('.deleteIcon', $listTable,
    route_url('root') + 'static/img/icons-root/deleteHover.png',
    route_url('root') + 'static/img/icons-root/delete.png');