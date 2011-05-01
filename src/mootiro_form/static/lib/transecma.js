/*!
 * Transecma, a javaScript i18n library v0.1
 * http:// ???
 *
 * Copyright 2011, Nando Florestan
 * Dual licensed under the MIT or GPL Version 3 licenses.
 *
 * Usage:

// The input is a translation map such as
translationsObject = {
    'I think we must review our processes.':
        'Who the hell was so stupid as to cause this #$%&*???',
    "If you don't know why I'm mad at you, do you think I'm going to tell you?":
        "I am your girlfriend and I am extremely anxious!",
    'I came, I saw, I conquered!': 'Veni, vidi, vici!',
    'Item {0} of {1}':
        'We have {1} items (really, {1}) and this is item number {0}.'
}
localizer = Transecma(translationsObject);
gettext = tr = _ = localizer.translate;
test1 = _('I came, I saw, I conquered!');
test2 = _('Item {0} of {1}').interpol([8, 9]);
alert(test1 + '\n' + test2);

*/

String.prototype.interpol = function (alist) {
    // String interpolation for format strings like "Item {0} of {1}".
    // The argument is an array of [strings or numbers].
    // For usage, see the test function below.
    try {
        return this.replace(/\{(\d+)\}/g, function () {
            // The replacement string is given by the nth element in the list,
            // where n is the second group of the regular expression:
            return alist[arguments[1]];
        });
    } catch (e) {
        if (window.console) console.log(['Exception on interpol() called on',
            this, 'with arguments', arguments]);
        throw(e);
    }
}
String.prototype.interpol.test = function() {
    if ('Item #{0} of {1}. Really, item {0}.'.interpol([5, 7])
        != "Item #5 of 7. Really, item 5.")  throw('Blimey -- oh no!');
}


function Transecma(tt) {
    // The argument must be a dictionary containing the translations.
    o = {
        translate: function (msg1, msg2, n) {
            if (!n || n == 1)
                var s = new String(tt[msg1] || msg1);
            else
                var s = new String(tt[msg2] || msg2);
            // I created a new String because now I add a few attributes
            s.singular = msg1;
            s.plural = msg2;
            s.n = n;
            return s;
            /*
            return {
                singular: msg1,
                plural: msg2,
                n: n,
                toString: function () {
                    if (!n || n == 1)
                        return tt[msg1] || msg1;
                    else
                        return tt[msg2] || msg2;
                }
            };
            */
        } //,
    };
    return o;
}


// Other String improvements
String.prototype.contains = function (t) {
    return this.indexOf(t) != -1;
};
String.prototype.endsWith = function (suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
String.prototype.wordCount = function () {
    var initialBlanks = /^\s+/;
    var leftTrimmed = this.replace(initialBlanks, "");
    var words = leftTrimmed.split(/\s+/);
    // The resulting array may have an empty last element which must be removed
    if (!words[words.length-1])  words.pop();
    return words.length;
};
