<%def name="color_config(place, rule)">
% if c.has_key(place):
${rule} {background-color: ${c[place]}}
% endif
</%def>

<%def name="font_config(place, rule)">
% if f.has_key(place):
${rule} {
  font-family: ${f[place]['name']};
  font-size: ${f[place]['size']}px;
  % if f[place]['bold']:
  font-weight: bold;
  % endif
  % if f[place]['italic']:
  font-style: italic;
  % endif
}
% endif
</%def>


/***** FONTS *****/
/* Title */
${font_config('title', 'div#Header h1')}
/* Subtitle */
${font_config('subtitle', 'div#Header p')}
/* Tab */
/* Form */
${font_config('form', 'div#Form')}
/* Help */
${font_config('help', 'div#Form form ul li:hover .help')}

/***** COLORS *****/
/* Background */
${color_config('background', 'body')}
/* Header */
${color_config('header', 'div#Header')}
/* Tabs */
/* Form Content */
${color_config('form', 'div#Content')}
/* Highlighted Field */
${color_config('highlighted_field', 'div#Form form ul li:hover')}
/* Highlighted Field Help */
${color_config('help', 'div#Form form ul li:hover .help')}