registry = dict(version=0)
def bind():
    from cPickle import loads as _loads
    _lookup_attr = _loads('cchameleon.core.codegen\nlookup_attr\np1\n.')
    _init_scope = _loads('cchameleon.core.utils\necontext\np1\n.')
    _re_amp = _loads("cre\n_compile\np1\n(S'&(?!([A-Za-z]+|#[0-9]+);)'\np2\nI0\ntRp3\n.")
    _init_stream = _loads('cchameleon.core.generation\ninitialize_stream\np1\n.')
    _attrs_71311952 = _loads('(dp1\nVfor\np2\nV${field.oid}\np3\nsVtitle\np4\nV${field.description}\np5\nsVclass\np6\nVdesc\np7\ns.')
    _init_default = _loads('cchameleon.core.generation\ninitialize_default\np1\n.')
    _attrs_71312080 = _loads('(dp1\nVclass\np2\nVreq\np3\nsVid\np4\nVreq-${field.oid}\np5\ns.')
    _attrs_71312016 = _loads('(dp1\nVclass\np2\nVDescription\np3\ns.')
    _attrs_71311760 = _loads('(dp1\nVid\np2\nVitem-${field.oid}\np3\nsVtitle\np4\nV${field.description}\np5\ns.')
    _attrs_71312208 = _loads('(dp1\nVclass\np2\nV${field.widget.error_class}\np3\ns.')
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
        attrs = _attrs_71311760
        'field.widget.hidden'
        _tmp1 = _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'hidden')
        if not _tmp1:
            pass
            "join(value('field.description'),)"
            _write(u'<li')
            _tmp2 = _lookup_attr(econtext['field'], 'description')
            if (_tmp2 is _default):
                _tmp2 = u'${field.description}'
            if ((_tmp2 is not None) and (_tmp2 is not False)):
                if (_tmp2.__class__ not in (str, unicode, int, float, )):
                    _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp2, unicode):
                        _tmp2 = unicode(str(_tmp2), 'utf-8')
                if ('&' in _tmp2):
                    if (';' in _tmp2):
                        _tmp2 = _re_amp.sub('&amp;', _tmp2)
                    else:
                        _tmp2 = _tmp2.replace('&', '&amp;')
                if ('<' in _tmp2):
                    _tmp2 = _tmp2.replace('<', '&lt;')
                if ('>' in _tmp2):
                    _tmp2 = _tmp2.replace('>', '&gt;')
                if ('"' in _tmp2):
                    _tmp2 = _tmp2.replace('"', '&quot;')
                _write(((' title="' + _tmp2) + '"'))
            "join(u'item-', value('field.oid'))"
            _tmp2 = ('%s%s' % ('item-', _lookup_attr(econtext['field'], 'oid'), ))
            if (_tmp2 is _default):
                _tmp2 = u'item-${field.oid}'
            if ((_tmp2 is not None) and (_tmp2 is not False)):
                if (_tmp2.__class__ not in (str, unicode, int, float, )):
                    _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp2, unicode):
                        _tmp2 = unicode(str(_tmp2), 'utf-8')
                if ('&' in _tmp2):
                    if (';' in _tmp2):
                        _tmp2 = _re_amp.sub('&amp;', _tmp2)
                    else:
                        _tmp2 = _tmp2.replace('&', '&amp;')
                if ('<' in _tmp2):
                    _tmp2 = _tmp2.replace('<', '&lt;')
                if ('>' in _tmp2):
                    _tmp2 = _tmp2.replace('>', '&gt;')
                if ('"' in _tmp2):
                    _tmp2 = _tmp2.replace('"', '&quot;')
                _write(((' id="' + _tmp2) + '"'))
            'field.error and field.widget.error_class'
            _tmp2 = (_lookup_attr(econtext['field'], 'error') and _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'error_class'))
            if (_tmp2 is _default):
                _tmp2 = None
            if ((_tmp2 is not None) and (_tmp2 is not False)):
                if (_tmp2.__class__ not in (str, unicode, int, float, )):
                    _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp2, unicode):
                        _tmp2 = unicode(str(_tmp2), 'utf-8')
                if ('&' in _tmp2):
                    if (';' in _tmp2):
                        _tmp2 = _re_amp.sub('&amp;', _tmp2)
                    else:
                        _tmp2 = _tmp2.replace('&', '&amp;')
                if ('<' in _tmp2):
                    _tmp2 = _tmp2.replace('<', '&lt;')
                if ('>' in _tmp2):
                    _tmp2 = _tmp2.replace('>', '&gt;')
                if ('"' in _tmp2):
                    _tmp2 = _tmp2.replace('"', '&quot;')
                _write(((' class="' + _tmp2) + '"'))
            _write('>')
        "not (field.widget.hidden or                               field.widget.category == 'structural')"
        _write(u'\n  <!-- mapping_item -->\n  ')
        _tmp2 = not (_lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'hidden') or (_lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'category') == 'structural'))
        if _tmp2:
            pass
            attrs = _attrs_71311952
            "join(value('field.description'),)"
            _write(u'<label class="desc"')
            _tmp2 = _lookup_attr(econtext['field'], 'description')
            if (_tmp2 is _default):
                _tmp2 = u'${field.description}'
            if ((_tmp2 is not None) and (_tmp2 is not False)):
                if (_tmp2.__class__ not in (str, unicode, int, float, )):
                    _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp2, unicode):
                        _tmp2 = unicode(str(_tmp2), 'utf-8')
                if ('&' in _tmp2):
                    if (';' in _tmp2):
                        _tmp2 = _re_amp.sub('&amp;', _tmp2)
                    else:
                        _tmp2 = _tmp2.replace('&', '&amp;')
                if ('<' in _tmp2):
                    _tmp2 = _tmp2.replace('<', '&lt;')
                if ('>' in _tmp2):
                    _tmp2 = _tmp2.replace('>', '&gt;')
                if ('"' in _tmp2):
                    _tmp2 = _tmp2.replace('"', '&quot;')
                _write(((' title="' + _tmp2) + '"'))
            "join(value('field.oid'),)"
            _tmp2 = _lookup_attr(econtext['field'], 'oid')
            if (_tmp2 is _default):
                _tmp2 = u'${field.oid}'
            if ((_tmp2 is not None) and (_tmp2 is not False)):
                if (_tmp2.__class__ not in (str, unicode, int, float, )):
                    _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                else:
                    if not isinstance(_tmp2, unicode):
                        _tmp2 = unicode(str(_tmp2), 'utf-8')
                if ('&' in _tmp2):
                    if (';' in _tmp2):
                        _tmp2 = _re_amp.sub('&amp;', _tmp2)
                    else:
                        _tmp2 = _tmp2.replace('&', '&amp;')
                if ('<' in _tmp2):
                    _tmp2 = _tmp2.replace('<', '&lt;')
                if ('>' in _tmp2):
                    _tmp2 = _tmp2.replace('>', '&gt;')
                if ('"' in _tmp2):
                    _tmp2 = _tmp2.replace('"', '&quot;')
                _write(((' for="' + _tmp2) + '"'))
            u'field.title'
            _write('>')
            _tmp2 = _lookup_attr(econtext['field'], 'title')
            _tmp = _tmp2
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
            'field.required'
            _tmp2 = _lookup_attr(econtext['field'], 'required')
            if _tmp2:
                pass
                attrs = _attrs_71312080
                "join(u'req-', value('field.oid'))"
                _write(u'<span class="req"')
                _tmp2 = ('%s%s' % ('req-', _lookup_attr(econtext['field'], 'oid'), ))
                if (_tmp2 is _default):
                    _tmp2 = u'req-${field.oid}'
                if ((_tmp2 is not None) and (_tmp2 is not False)):
                    if (_tmp2.__class__ not in (str, unicode, int, float, )):
                        _tmp2 = unicode(_translate(_tmp2, domain=_domain, mapping=None, target_language=target_language, default=None))
                    else:
                        if not isinstance(_tmp2, unicode):
                            _tmp2 = unicode(str(_tmp2), 'utf-8')
                    if ('&' in _tmp2):
                        if (';' in _tmp2):
                            _tmp2 = _re_amp.sub('&amp;', _tmp2)
                        else:
                            _tmp2 = _tmp2.replace('&', '&amp;')
                    if ('<' in _tmp2):
                        _tmp2 = _tmp2.replace('<', '&lt;')
                    if ('>' in _tmp2):
                        _tmp2 = _tmp2.replace('>', '&gt;')
                    if ('"' in _tmp2):
                        _tmp2 = _tmp2.replace('"', '&quot;')
                    _write(((' id="' + _tmp2) + '"'))
                _write(u'>*</span>')
            _write(u'\n  </label>')
        _write(u'\n  ')
        attrs = _attrs_71312016
        u'field.schema.description'
        _write(u'<div class="Description">\n    ')
        _tmp2 = _lookup_attr(_lookup_attr(econtext['field'], 'schema'), 'description')
        _tmp = _tmp2
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
        u"''"
        _write(u'\n  </div>\n  ')
        _default.value = default = ''
        'field.serialize(cstruct)'
        _content = _lookup_attr(econtext['field'], 'serialize')(econtext['cstruct'])
        u'_content'
        _tmp2 = _content
        _tmp = _tmp2
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
        "'error-%s' % field.oid"
        _write(u'\n\n  ')
        errstr = ('error-%s' % _lookup_attr(econtext['field'], 'oid'))
        'field.error and not field.widget.hidden'
        _tmp2 = (_lookup_attr(econtext['field'], 'error') and not _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'hidden'))
        if _tmp2:
            pass
            'field.error.messages()'
            _tmp2 = _lookup_attr(_lookup_attr(econtext['field'], 'error'), 'messages')()
            msg = None
            (_tmp2, _tmp3, ) = repeat.insert('msg', _tmp2)
            for msg in _tmp2:
                _tmp3 = (_tmp3 - 1)
                attrs = _attrs_71312208
                "join(value('field.widget.error_class'),)"
                _write(u'<p')
                _tmp4 = _lookup_attr(_lookup_attr(econtext['field'], 'widget'), 'error_class')
                if (_tmp4 is _default):
                    _tmp4 = u'${field.widget.error_class}'
                if ((_tmp4 is not None) and (_tmp4 is not False)):
                    if (_tmp4.__class__ not in (str, unicode, int, float, )):
                        _tmp4 = unicode(_translate(_tmp4, domain=_domain, mapping=None, target_language=target_language, default=None))
                    else:
                        if not isinstance(_tmp4, unicode):
                            _tmp4 = unicode(str(_tmp4), 'utf-8')
                    if ('&' in _tmp4):
                        if (';' in _tmp4):
                            _tmp4 = _re_amp.sub('&amp;', _tmp4)
                        else:
                            _tmp4 = _tmp4.replace('&', '&amp;')
                    if ('<' in _tmp4):
                        _tmp4 = _tmp4.replace('<', '&lt;')
                    if ('>' in _tmp4):
                        _tmp4 = _tmp4.replace('>', '&gt;')
                    if ('"' in _tmp4):
                        _tmp4 = _tmp4.replace('"', '&quot;')
                    _write(((' class="' + _tmp4) + '"'))
                "repeat.msg.index==0 and errstr or                         ('%s-%s' % (errstr, repeat.msg.index))"
                _tmp4 = (((_lookup_attr(repeat.msg, 'index') == 0) and errstr) or ('%s-%s' % (errstr, _lookup_attr(repeat.msg, 'index'), )))
                if (_tmp4 is _default):
                    _tmp4 = None
                if ((_tmp4 is not None) and (_tmp4 is not False)):
                    if (_tmp4.__class__ not in (str, unicode, int, float, )):
                        _tmp4 = unicode(_translate(_tmp4, domain=_domain, mapping=None, target_language=target_language, default=None))
                    else:
                        if not isinstance(_tmp4, unicode):
                            _tmp4 = unicode(str(_tmp4), 'utf-8')
                    if ('&' in _tmp4):
                        if (';' in _tmp4):
                            _tmp4 = _re_amp.sub('&amp;', _tmp4)
                        else:
                            _tmp4 = _tmp4.replace('&', '&amp;')
                    if ('<' in _tmp4):
                        _tmp4 = _tmp4.replace('<', '&lt;')
                    if ('>' in _tmp4):
                        _tmp4 = _tmp4.replace('>', '&gt;')
                    if ('"' in _tmp4):
                        _tmp4 = _tmp4.replace('"', '&quot;')
                    _write(((' id="' + _tmp4) + '"'))
                u'msg'
                _write('>')
                _tmp4 = msg
                _tmp = _tmp4
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
                _write(u'</p>')
                if (_tmp3 == 0):
                    break
                _write(' ')
        _write(u'\n\n  ')
        _write(u'<!-- /mapping_item -->\n')
        if not _tmp1:
            pass
            _write(u'</li>')
        return _out.getvalue()
    return render

__filename__ = u'/home/walrus/FormCreator/src/mootiro_form/fieldtypes/templates/form_mapping_item.pt'
registry[(None, True, '72cfe6c8335eaf0ea088745bbecd77841ea68acf')] = bind()
