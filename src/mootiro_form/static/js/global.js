/* Prototype facilitators */
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