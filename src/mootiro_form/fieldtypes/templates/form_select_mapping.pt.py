registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _attrs_67554576 = _loads('(dp1\nVname\np2\nV__start__\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nV${field.name}:mapping\np7\ns.')
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_67554832 = _loads('(dp1\nVname\np2\nV__end__\np3\nsVtype\np4\nVhidden\np5\nsVvalue\np6\nV${field.name}:mapping\np7\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
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
        attrs = _attrs_67554576
        "join(value('field.name'), u':mapping')"
        _write(u'<input type="hidden" name="__start__"')
        _tmp1 = ('%s%s' % (_lookup_attr(econtext['field'], 'name'), ':mapping', ))
        if (_tmp1 is _default):
            _tmp1 = u'${field.name}:mapping'
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
        u"''"
        _write(' />')
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
            'rndr(tmpl,field=f,cstruct=cstruct.get(f.name,null))'
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
        _write('')
        attrs = _attrs_67554832
        "join(value('field.name'), u':mapping')"
        _write(u'<input type="hidden" name="__end__"')
        _tmp1 = ('%s%s' % (_lookup_attr(econtext['field'], 'name'), ':mapping', ))
        if (_tmp1 is _default):
            _tmp1 = u'${field.name}:mapping'
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
        _write(' />')
        return _out.getvalue()
    return render

__filename__ = u'/home/walrus/FormCreator/src/mootiro_form/fieldtypes/templates/form_select_mapping.pt'
registry[(None, True, '72cfe6c8335eaf0ea088745bbecd77841ea68acf')] = bind()
