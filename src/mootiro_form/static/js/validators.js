/* v : number value
 */
function integerValidator(v) {
    v = v.toString(); // presentation value
    var n = Number(v.replace(',', '.')); // persisted value
    if (isNaN(n))
        return _('Not a number');
    if (v.contains('.') || v.contains(','))
        return _('Not an integer number');
    return '';
}

/* v : number value
 * sep : separator. May be '.' or ','
 * prec : max decimals precision
 */
function decimalValidator(v, sep, prec) {
    v = v.toString(); // exibithion value
    var x = Number(v.replace(',', '.')); // persisted value
    if (isNaN(x))
        return _('Not a number');
    if ((sep == '.' && v.match(/\,/)) ||
        (sep == ',' && v.match(/\./)))
        return _('Wrong separator');
    arr = v.split(sep);
    if (arr[1] && arr[1].length > prec)
        return _('Precision overflow');
    return '';
}
