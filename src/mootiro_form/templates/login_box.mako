% if authenticated_userid:
    ${authenticated_userid}
    ${h.form(url(controller='user', action='logout'), method='post', id="logout")}
    ${h.submit('submit', 'Logout')}
    ${h.end_form()}
% else:
    <div id="login">login</div>
    <form id="loginBlock" action="/user/login" method="post">
        <div style="position: relative;">
            <label class="hideLabel" for="user" id="labeluser" style="color: #808080;">${_('username')}</label>
            <input id="user" type="text" name="userlogin" /><br />
        </div>
        <div style="position: relative;">
            <label class="hideLabel" for="pass" id="labelpass" style="color: #808080;">${_('password')}</label>
            <input id="pass" type="password" name="password" /><br />
        </div>
        <label id="labelsub" for="submit">&nbsp;</label>
        <input id="submit" name="submit" type="submit" value="Ok" />
    </form>
    <div id="esqueceu"><a href="${url('useraction', action='forgotten_password')}">${_('Forgot your password?')}</a><br /><a href="${url('user')}">${_('Sign in')}</a></div>
% endif

<%! onloadScripts = ["""
    $('#header_links').hover(function () {
        $(this).toggleClass('menu-active');
    });
    $('.hideLabel').inFieldLabels();
"""] %>
