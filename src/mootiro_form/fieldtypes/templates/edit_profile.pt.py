registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _attrs_65895312 = _loads('(dp1\nVid\np2\nV${field.formid}\np3\nsVaccept-charset\np4\nVutf-8\np5\nsVaction\np6\nV${field.action}\np7\nsVmethod\np8\nV${field.method}\np9\nsVenctype\np10\nVmultipart/form-data\np11\ns.')
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _attrs_65895056 = _loads('(dp1\nVclass\np2\nVerrorMsg\np3\ns.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_65892560 = _loads('(dp1\nVtype\np2\nVhidden\np3\nsVname\np4\nV_charset_\np5\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_65894992 = _loads('(dp1\nVname\np2\nV__formid__\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nV${field.formid}\np7\ns.')
    _attrs_64436368 = _loads('(dp1\nVhref\np2\nV/user/edit_password\np3\ns.')
    _attrs_64366800 = _loads('(dp1\nVtype\np2\nVtext/javascript\np3\ns.')
    _attrs_65894160 = _loads('(dp1\nVclass\np2\nVerrorLi\np3\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
    _marker = _loads("ccopy_reg\n_reconstructor\np1\n(cchameleon.core.i18n\nStringMarker\np2\nc__builtin__\nstr\np3\nS''\ntRp4\n.")
    _attrs_65894096 = _loads('(dp1\n.')
    _attrs_64985552 = _loads('(dp1\n.')
    _attrs_64365392 = _loads('(dp1\nVname\np2\nV${button.name}\np3\nsVvalue\np4\nV${button.value}\np5\nsVclass\np6\nVbtnText submit\np7\nsVtype\np8\nV${button.type}\np9\nsVid\np10\nV${field.formid+button.name}\np11\ns.')
    _attrs_65895696 = _loads('(dp1\n.')
    _attrs_65893584 = _loads('(dp1\nVclass\np2\nVerrorMsgLbl\np3\ns.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_64544848 = _loads('(dp1\nVclass\np2\nVbuttons\np3\ns.')
    _attrs_65894032 = _loads('(dp1\nVclass\np2\nVsection first\np3\ns.')
    _attrs_65892880 = _loads('(dp1\n.')
    _attrs_65894608 = _loads('(dp1\nVclass\np2\nVdeformFormFieldset\np3\ns.')
    _attrs_65894480 = _loads('(dp1\n.')
    def render(econtext, rcontext=None):
        macros = econtext.get('macros')
        _translate = econtext.get('_translate')
        _slots = econtext.get('_slots')
        target_language = econtext.get('target_language')
        u'_init_stream()'
        (_out, _write, ) = _init_stream()
        u'_init_tal()'
        (_attributes, repeat, ) = _init_tal()
        u'_init_default()'
        _default = _init_default()
        u'None'
        default = None
        u'None'
        _domain = None
        _tmp_domain0 = _domain
        u"'mootiro_form'"
        _domain = 'mootiro_form'
        attrs = _attrs_65895312
        "join(value('field.formid'),)"
        _write(u'<form')
        _tmp1 = _lookup_attr(econtext['field'], 'formid')
        if (_tmp1 is _default):
            _tmp1 = u'${field.formid}'
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = unicode(str(_tmp1), 'utf-8')
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' id="' + _tmp1) + '"'))
        "join(value('field.action'),)"
        _tmp1 = _lookup_attr(econtext['field'], 'action')
        if (_tmp1 is _default):
            _tmp1 = u'${field.action}'
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = unicode(str(_tmp1), 'utf-8')
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' action="' + _tmp1) + '"'))
        "join(value('field.method'),)"
        _tmp1 = _lookup_attr(econtext['field'], 'method')
        if (_tmp1 is _default):
            _tmp1 = u'${field.method}'
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = unicode(str(_tmp1), 'utf-8')
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' method="' + _tmp1) + '"'))
        'field.css_class'
        _write(u' enctype="multipart/form-data" accept-charset="utf-8"')
        _tmp1 = _lookup_attr(econtext['field'], 'css_class')
        if (_tmp1 is _default):
            _tmp1 = None
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = unicode(str(_tmp1), 'utf-8')
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' class="' + _tmp1) + '"'))
        _write(u'>\n\n  ')
        attrs = _attrs_65894608
        'field.title'
        _write(u'<fieldset class="deformFormFieldset">\n\n    ')
        _tmp1 = _lookup_attr(econtext['field'], 'title')
        if _tmp1:
            pass
            attrs = _attrs_65892880
            u'field.title'
            _write(u'<legend>')
            _tmp1 = _lookup_attr(econtext['field'], 'title')
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            _write(u'</legend>')
        _write(u'\n\n    ')
        attrs = _attrs_65892560
        _write(u'<input type="hidden" name="_charset_" />\n    ')
        attrs = _attrs_65894992
        "join(value('field.formid'),)"
        _write(u'<input type="hidden" name="__formid__"')
        _tmp1 = _lookup_attr(econtext['field'], 'formid')
        if (_tmp1 is _default):
            _tmp1 = u'${field.formid}'
        if ((_tmp1 is not None) and (_tmp1 is not False)):
            if (_tmp1.__class__ not in (str, unicode, int, float, )):
                _tmp1 = unicode(_translate(_tmp1, domain=_domain, mapping=None, target_language=target_language, default=None))
            else:
                if not isinstance(_tmp1, unicode):
                    _tmp1 = unicode(str(_tmp1), 'utf-8')
            if ('&' in _tmp1):
                if (';' in _tmp1):
                    _tmp1 = _re_amp.sub('&amp;', _tmp1)
                else:
                    _tmp1 = _tmp1.replace('&', '&amp;')
            if ('<' in _tmp1):
                _tmp1 = _tmp1.replace('<', '&lt;')
            if ('>' in _tmp1):
                _tmp1 = _tmp1.replace('>', '&gt;')
            if ('"' in _tmp1):
                _tmp1 = _tmp1.replace('"', '&quot;')
            _write(((' value="' + _tmp1) + '"'))
        _write(u' />\n    ')
        attrs = _attrs_65895696
        'field.error'
        _write(u'<ul>\n      \n      ')
        _tmp1 = _lookup_attr(econtext['field'], 'error')
        if _tmp1:
            pass
            attrs = _attrs_65894160
            _write(u'<li class="errorLi">\n        ')
            attrs = _attrs_65893584
            u"u'There was a problem with your submission'"
            _write(u'<h3 class="errorMsgLbl">')
            _msgid = u'There was a problem with your submission'
            u"%(translate)s(' '.join(%(msgid)s.split()), domain=%(domain)s, mapping=None, target_language=%(language)s, default=%(msgid)s)"
            _result = _translate(_lookup_attr(' ', 'join')(_msgid.split()), domain=_domain, mapping=None, target_language=target_language, default=_msgid)
            u'_result'
            _tmp1 = _result
            _write((_tmp1 + u'</h3>\n        '))
            attrs = _attrs_65895056
            u"u'Errors have been highlighted below'"
            _write(u'<p class="errorMsg">')
            _msgid = u'Errors have been highlighted below'
            u"%(translate)s(' '.join(%(msgid)s.split()), domain=%(domain)s, mapping=None, target_language=%(language)s, default=%(msgid)s)"
            _result = _translate(_lookup_attr(' ', 'join')(_msgid.split()), domain=_domain, mapping=None, target_language=target_language, default=_msgid)
            u'_result'
            _tmp1 = _result
            _write((_tmp1 + u'</p>\n      </li>'))
        'field.title'
        _write(u'\n      \n      ')
        _tmp1 = _lookup_attr(econtext['field'], 'title')
        if _tmp1:
            pass
            attrs = _attrs_65894032
            _write(u'<li class="section first">\n        ')
            attrs = _attrs_65894096
            u'field.title'
            _write(u'<h3>')
            _tmp1 = _lookup_attr(econtext['field'], 'title')
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            'field.description'
            _write(u'</h3>\n        ')
            _tmp1 = _lookup_attr(econtext['field'], 'description')
            if _tmp1:
                pass
                attrs = _attrs_65894480
                u'field.description'
                _write(u'<div>')
                _tmp1 = _lookup_attr(econtext['field'], 'description')
                _tmp = _tmp1
                if (_tmp.__class__ not in (str, unicode, int, float, )):
                    try:
                        _tmp = _tmp.__html__
                    except:
                        _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                    else:
                        _tmp = _tmp()
                        _write(_tmp)
                        _tmp = None
                if (_tmp is not None):
                    if not isinstance(_tmp, unicode):
                        _tmp = unicode(str(_tmp), 'utf-8')
                    if ('&' in _tmp):
                        if (';' in _tmp):
                            _tmp = _re_amp.sub('&amp;', _tmp)
                        else:
                            _tmp = _tmp.replace('&', '&amp;')
                    if ('<' in _tmp):
                        _tmp = _tmp.replace('<', '&lt;')
                    if ('>' in _tmp):
                        _tmp = _tmp.replace('>', '&gt;')
                    _write(_tmp)
                _write(u'</div>')
            _write(u'\n      </li>')
        u"''"
        _write(u'\n      \n      ')
        _default.value = default = ''
        'field.renderer'
        rndr = _lookup_attr(econtext['field'], 'renderer')
        'field.widget.item_template'
        tmpl = _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'item_template')
        'field.children'
        _tmp1 = _lookup_attr(econtext['field'], 'children')
        f = None
        (_tmp1, _tmp2, ) = repeat.insert('f', _tmp1)
        for f in _tmp1:
            _tmp2 = (_tmp2 - 1)
            'rndr(tmpl,field=f,cstruct=cstruct.get(f.name, null))'
            _content = rndr(tmpl, field=f, cstruct=_lookup_attr(econtext['cstruct'], 'get')(_lookup_attr(f, 'name'), econtext['null']))
            u'_content'
            _tmp3 = _content
            _tmp = _tmp3
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                _write(_tmp)
            if (_tmp2 == 0):
                break
            _write(' ')
        _write(u'\n\n    ')
        attrs = _attrs_64436368
        _write(u'<a href="/user/edit_password">Change Password</a>\n      \n      ')
        attrs = _attrs_64544848
        'field.buttons'
        _write(u'<li class="buttons">\n        ')
        _tmp1 = _lookup_attr(econtext['field'], 'buttons')
        button = None
        (_tmp1, _tmp2, ) = repeat.insert('button', _tmp1)
        for button in _tmp1:
            _tmp2 = (_tmp2 - 1)
            _write(u'')
            attrs = _attrs_64365392
            "join(value('field.formid+button.name'),)"
            _write(u'<button')
            _tmp3 = (_lookup_attr(econtext['field'], 'formid') + _lookup_attr(button, 'name'))
            if (_tmp3 is _default):
                _tmp3 = u'${field.formid+button.name}'
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = unicode(str(_tmp3), 'utf-8')
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' id="' + _tmp3) + '"'))
            "join(value('button.name'),)"
            _tmp3 = _lookup_attr(button, 'name')
            if (_tmp3 is _default):
                _tmp3 = u'${button.name}'
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = unicode(str(_tmp3), 'utf-8')
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' name="' + _tmp3) + '"'))
            "join(value('button.type'),)"
            _tmp3 = _lookup_attr(button, 'type')
            if (_tmp3 is _default):
                _tmp3 = u'${button.type}'
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = unicode(str(_tmp3), 'utf-8')
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' type="' + _tmp3) + '"'))
            "join(value('button.value'),)"
            _write(u' class="btnText submit"')
            _tmp3 = _lookup_attr(button, 'value')
            if (_tmp3 is _default):
                _tmp3 = u'${button.value}'
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = unicode(str(_tmp3), 'utf-8')
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' value="' + _tmp3) + '"'))
            'button.disabled'
            _tmp3 = _lookup_attr(button, 'disabled')
            if (_tmp3 is _default):
                _tmp3 = None
            if ((_tmp3 is not None) and (_tmp3 is not False)):
                if (_tmp3.__class__ not in (str, unicode, int, float, )):
                    _tmp3 = unicode(_translate(_tmp3, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp3, unicode):
                        _tmp3 = unicode(str(_tmp3), 'utf-8')
                if ('&' in _tmp3):
                    if (';' in _tmp3):
                        _tmp3 = _re_amp.sub('&amp;', _tmp3)
                    else:
                        _tmp3 = _tmp3.replace('&', '&amp;')
                if ('<' in _tmp3):
                    _tmp3 = _tmp3.replace('<', '&lt;')
                if ('>' in _tmp3):
                    _tmp3 = _tmp3.replace('>', '&gt;')
                if ('"' in _tmp3):
                    _tmp3 = _tmp3.replace('"', '&quot;')
                _write(((' disabled="' + _tmp3) + '"'))
            _write(u'>\n            ')
            attrs = _attrs_64985552
            u'button.title'
            _write(u'<span>')
            _tmp3 = _lookup_attr(button, 'title')
            _tmp = _tmp3
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            _write(u'</span>\n          </button>\n        ')
            if (_tmp2 == 0):
                break
            _write(' ')
        'field.use_ajax'
        _write(u'\n      </li>\n      \n    </ul>\n    \n  </fieldset>\n\n')
        _tmp1 = _lookup_attr(econtext['field'], 'use_ajax')
        if _tmp1:
            pass
            attrs = _attrs_64366800
            u'field.formid'
            _write(u'<script type="text/javascript">\n  deform.addCallback(\n     \'')
            _tmp1 = _lookup_attr(econtext['field'], 'formid')
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            u'field.ajax_options'
            _write(u"',\n     function(oid) { \n         var options = {\n           target: '#' + oid,\n           replaceTarget: true,\n         };\n         var extra_options = ")
            _tmp1 = _lookup_attr(econtext['field'], 'ajax_options')
            _tmp = _tmp1
            if (_tmp.__class__ not in (str, unicode, int, float, )):
                try:
                    _tmp = _tmp.__html__
                except:
                    _tmp = _translate(_tmp, domain=_domain, mapping=None, target_language=target_language, default=None)
                else:
                    _tmp = _tmp()
                    _write(_tmp)
                    _tmp = None
            if (_tmp is not None):
                if not isinstance(_tmp, unicode):
                    _tmp = unicode(str(_tmp), 'utf-8')
                if ('&' in _tmp):
                    if (';' in _tmp):
                        _tmp = _re_amp.sub('&amp;', _tmp)
                    else:
                        _tmp = _tmp.replace('&', '&amp;')
                if ('<' in _tmp):
                    _tmp = _tmp.replace('<', '&lt;')
                if ('>' in _tmp):
                    _tmp = _tmp.replace('>', '&gt;')
                _write(_tmp)
            _write(u";\n         var name;\n         if (extra_options) {\n           for (name in extra_options) {\n             options[name] = extra_options[name];\n           };\n         };\n         $('#' + oid).ajaxForm(options);\n   });\n</script>")
        _write(u'\n  \n</form>')
        _domain = _tmp_domain0
        return _out.getvalue()
    return render

__filename__ = u'/home/walrus/mootiro_form/src/mootiro_form/fieldtypes/templates/edit_profile.pt'
registry[(None, True, '72cfe6c8335eaf0ea088745bbecd77841ea68acf')] = bind()