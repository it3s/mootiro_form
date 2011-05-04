$('#middle').append($('#collectors_template').tmpl());
$('#collectors_rows').append($('#collectors_rows_template').tmpl({}));

var listTable = $('#CollectorsListTable');
listTable.find('tr td:nth-child(2n)').addClass('darker');
listTable.find('thead th:nth-child(2n)').addClass('darker');


// Float Windows and Tabs
$('#PublicLinkWindow').dialog();
$('#PublicLinkTabs').tabs();