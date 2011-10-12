function RichEditor(o) {
    // Constructor
    this.$preview = o.$preview;
    this.textareaId = o.textareaId;
    this.$textarea  = $('#' + o.textareaId);
    this.$richPlace = o.$richPlace;
    this.contentCss = o.contentCss || '/static/css/master_global.css';
    this.resizeHorizontal = o.resizeHorizontal || false;
    // Store callbacks
    this.onRemove = o.onRemove;
    this.onKeyDown = o.onKeyDown;
    this.onLostFocus = o.onLostFocus;
    this.defaultContentWhenBlank = o.defaultContentWhenBlank;
    var instance = this;
    this.lostFocus = function (e) {
        $(document).unbind('click', instance.lostFocus);
        // Only take action if the click was elsewhere than the toolbar
        if (e && e.target.className === 'mceText')  return false;
        // First remove the last line if blank
        var editor = tinyMCE.get(instance.textareaId);
        var content = editor.getContent();
        if (content.endsWith("<p>&nbsp;</p>")) {
            content = content.slice(0, -13);
            editor.setContent(content);
        }
        tinyMCE.triggerSave(); // update the hidden textarea
        content = content || '<p>&nbsp;</p>';
        instance.$preview.html(content);  // update the preview area
        instance.$richPlace.hide();
        instance.$preview.show();
        instance.richEditing = false;
        if (instance.onLostFocus)  instance.onLostFocus(e, instance, content);
        return content;
    };
    this.showEditor = function () {
        // Shows the rich editor. Completes the content if empty.
        var editor = tinyMCE.get(instance.textareaId);
        if (!editor.getContent() && instance.defaultContentWhenBlank) {
            editor.setContent(instance.defaultContentWhenBlank());
        }
        instance.$preview.hide();
        instance.$richPlace.show();
        editor.focus();
        $(document).click(instance.lostFocus);
        instance.richEditing = true;
    };
    this.init = function () {
        // tinyMCE.init({mode:'specific_textareas', editor_selector:'TinyMCE',
        tinyMCE.init({mode: 'exact', elements: this.textareaId,
            content_css: this.contentCss,
            plugins: 'autolink', theme: "advanced",
            theme_advanced_toolbar_location: "top",
            theme_advanced_statusbar_location: 'bottom',
            theme_advanced_resizing: true,
            theme_advanced_resize_horizontal: this.resizeHorizontal,
            // newdocument,|,justifyleft,justifycenter,justifyright,fontselect,fontsizeselect,forecolor,backcolor,|,cut,copy,paste,spellchecker,preview,|,advhr,emotions
            theme_advanced_buttons1: "formatselect,bold,italic,underline,|,bullist,numlist,|,outdent,indent,|,removeformat",
            theme_advanced_buttons2: "link,unlink,anchor,image,|,sub,sup,|,charmap,|,undo,redo,|,help,code,cleanup",
            theme_advanced_buttons3: '',
            setup: function (editor) {
                if (instance.onKeyDown)
                    editor.onKeyDown.add(instance.onKeyDown);
            }
        });
        this.isActive = true;
    };
    this.$preview.click(this.showEditor);
    this.remove = function () {
        if (this.richEditing)  this.lostFocus();
        this.$preview.unbind('click', this.showEditor);
        var editor = tinyMCE.get(this.textareaId);
        editor.remove();
        this.isActive = false;
        if (this.onRemove)  this.onRemove();
    };
}
