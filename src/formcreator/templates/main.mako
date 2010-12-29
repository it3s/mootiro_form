# -*- coding: utf-8 -*-
<%! onloadScripts = [] %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Form Creator</title>
    <link rel="stylesheet" type="text/css" href="/static/css/style.css" />
	${self.css()}
	<script type="text/javascript" src="/static/js/jquery.js"></script>
	<script type="text/javascript" src="/static/js/jquery-ui.js"></script>
	<script type="text/javascript" src="/static/js/jquery.infieldlabel.min.js"></script>
	${self.jscripts()}
	<script type="text/javascript">
      $(document).ready(function(){
        $('#header_links').hover(function () {
          $(this).toggleClass('menu-active');
        });
        $('.hideLabel').inFieldLabels();
        ${self.onload_scripts()}
      });
	</script>
  </head>
  <body>
    ${self.other()}
    <div id="container">
	  <div id="header">
		<div id="header_left">
			<div class="Horizontal">
				<div id="header_links" class="menu-active"><a href="/">home</a></div>
				<div id="header_links"> <a href="#">contribua</a></div>
				<div id="header_links"> <a href="#">como baixar</a></div>
				<div id="header_links"> <a href="#">documentação</a></div>
				<img src="/static/images/form.png">
			</div>
		</div>
        <div id="header_right">
          <%include file='login_box.mako'/>
        </div>
	  </div>
	  <div id="content" style="width: 560px; text-align: center">
	    ${self.content()}
	    ${next.body()}
	  </div>            
      <div id="footer" style="width: 560px; text-align: center"></div>
  </body>
</html>

## Page functions

<%def name="jscripts()"></%def>
<%def name="css()"></%def>
<%def name="content()"></%def>
<%def name="other()"></%def>

<%def name="onload_scripts()">
<%
    all_scripts = []
    t = self
    while t:
        all_scripts = getattr(t.module, 'onloadScripts', []) + all_scripts
        t = t.inherits
%>
% for script in all_scripts:
    ${script|n}
% endfor
</%def>
