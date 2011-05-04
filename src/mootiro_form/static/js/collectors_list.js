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
        $('#PanelTitle').text($(tab).children().attr('title'));
    };
    $(tabs + " li").click(function () {
        instance.to(this);
        return false; // in order not to follow the link
    });
}
// Instantiate tabs
tabs = new Tabs('.ui-tabs-nav', '.ui-tabs-panel');

$('#middle').append($('#collectors_template').tmpl());
$('#collectors_rows').append($('#collectors_rows_template').tmpl({}));

var listTable = $('#CollectorsListTable');
listTable.find('tr td:nth-child(2n)').addClass('darker');
listTable.find('thead th:nth-child(2n)').addClass('darker');


// Float Windows and Tabs
$('#PublicLinkWindow').dialog();
$('#PublicLinkTabs').tabs();
