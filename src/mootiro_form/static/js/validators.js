/* v : number value
 */
function integerValidator(v) {
    v = v.toString(); // presentation value
    var n = Number(v.replace(',', '.')); // persisted value
    if (isNaN(n))
        return _('Enter a number.');
    if (v.contains('.') || v.contains(','))
        return _('Enter an integer number.');
    return '';
}

/* v : number value
 * sep : separator. May be '.' or ','
 * prec : max decimals precision
 */
function decimalValidator(v, sep, prec) {
    v = v.toString(); // exhibition value
    var x = Number(v.replace(',', '.')); // persisted value
    if (isNaN(x))
        return _('Enter a number.');
    if ((sep == '.' && v.match(/\,/)) ||
        (sep == ',' && v.match(/\./)))
        return _('Wrong separator.');
    arr = v.split(sep);
    if (arr[1] && arr[1].length > prec)
        return _('Too many decimal places.');
    return '';
}
