% if collector.status == 'published':
window.open(
    % if action == 'popup_survey':
    "${url('entry_form_slug', action='view_form', slug=collector.slug)}",
    "${action}-${collector.slug}",
    "width=800, height=500, scrollbars=yes, resizable=yes, status=yes"
    % elif action == 'popup_invitation':
    "${url('collector_slug', action='invite', slug=collector.slug)}",
    "${action}-${collector.slug}",
    "width=400, height=150, scrollbars=yes, resizable=yes, status=yes"
    % endif
);
% endif
