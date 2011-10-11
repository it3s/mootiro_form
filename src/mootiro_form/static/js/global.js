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


function onHoverSwitchImage(selector, where, hoverImage, normalImage) {
    $(selector, where).live('mouseover mouseout', function(event) {
        if (event.target.tagName == 'BUTTON')
            var img = $('img', this);
        else
            var img = $(this);
        if (event.type == 'mouseover') {
            img.attr({src: hoverImage});
        } else {
            img.attr({src: normalImage});
        }
    });
}


