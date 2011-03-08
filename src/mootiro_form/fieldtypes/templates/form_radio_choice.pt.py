registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _attrs_73465040 = _loads('(dp1\nVname\np2\nV__start__\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nV${field.name}:rename\np7\ns.')
    _attrs_73465552 = _loads('(dp1\nVclass\np2\nVdeformSet-item\np3\ns.')
    _attrs_73474128 = _loads('(dp1\nVfor\np2\nV${field.oid}-${repeat.choice.index}\np3\ns.')
    _attrs_73465744 = _loads('(dp1\nVname\np2\nV${field.oid}\np3\nsVvalue\np4\nV${value}\np5\nsVtype\np6\nVradio\np7\nsVid\np8\nV${field.oid}-${repeat.choice.index}\np9\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_73465424 = _loads('(dp1\nVtype\np2\nVhidden\np3\nsVname\np4\nV__end__\np5\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_73464912 = _loads('(dp1\nVclass\np2\nVdeformSet\np3\ns.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _init_tal = _loads('cchameleon.core.generation\ninitialize_tal\np1\n.')
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
        attrs = _attrs_73464912
        _write(u'<ul class="deformSet"> \n    ')
        attrs = _attrs_73465040
        "join(value('field.name'), u':rename')"
        _write(u'<input type="hidden" name="__start__"')
        _tmp1 = ('%s%s' % (_lookup_attr(econtext['field'], 'name'), ':rename', ))
        if (_tmp1 is _default):
            _tmp1 = u'${field.name}:rename'
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
        'field.widget.values'
        _write(u' />\n    ')
        _tmp1 = _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'values')
        choice = None
        (_tmp1, _tmp2, ) = repeat.insert('choice', _tmp1)
        for choice in _tmp1:
            _tmp2 = (_tmp2 - 1)
            'choice'
            _write(u'\n      ')
            (value, title, ) = choice
            _write(u'')
            attrs = _attrs_73465552
            _write(u'<li class="deformSet-item">\n          ')
            attrs = _attrs_73465744
            "join(value('field.oid'),)"
            _write(u'<input type="radio"')
            _tmp3 = _lookup_attr(econtext['field'], 'oid')
            if (_tmp3 is _default):
                _tmp3 = u'${field.oid}'
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
            "join(value('value'),)"
            _tmp3 = value
            if (_tmp3 is _default):
                _tmp3 = u'${value}'
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
            "join(value('field.oid'), u'-', value('repeat.choice.index'))"
            _tmp3 = ('%s%s%s' % (_lookup_attr(econtext['field'], 'oid'), '-', _lookup_attr(repeat.choice, 'index'), ))
            if (_tmp3 is _default):
                _tmp3 = u'${field.oid}-${repeat.choice.index}'
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
            default = _default
            'value == field.schema.opt_default'
            _tmp3 = (value == _lookup_attr(_lookup_attr(econtext['field'], 'schema'), 'opt_default'))
            default = None
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
                _write(((' checked="' + _tmp3) + '"'))
            'field.widget.css_class'
            _tmp3 = _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'css_class')
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
                _write(((' class="' + _tmp3) + '"'))
            _write(u' />\n          ')
            attrs = _attrs_73474128
            "join(value('field.oid'), u'-', value('repeat.choice.index'))"
            _write(u'<label')
            _tmp3 = ('%s%s%s' % (_lookup_attr(econtext['field'], 'oid'), '-', _lookup_attr(repeat.choice, 'index'), ))
            if (_tmp3 is _default):
                _tmp3 = u'${field.oid}-${repeat.choice.index}'
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
                _write(((' for="' + _tmp3) + '"'))
            u'title'
            _write('>')
            _tmp3 = title
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
            _write(u'</label>\n        </li>\n      ')
            if (_tmp2 == 0):
                break
            _write(' ')
        _write(u'\n    ')
        attrs = _attrs_73465424
        _write(u'<input type="hidden" name="__end__" />\n</ul>')
        return _out.getvalue()
    return render

__filename__ = u'/home/walrus/FormCreator/src/mootiro_form/fieldtypes/templates/form_radio_choice.pt'
registry[(None, True, '72cfe6c8335eaf0ea088745bbecd77841ea68acf')] = bind()
