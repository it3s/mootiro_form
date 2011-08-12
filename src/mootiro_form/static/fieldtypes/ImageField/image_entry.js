function handleFiles(files, previewId, filenameLabelId) {
    var file = files[0];
    var imageType = /image.*/;

    var img = document.getElementById(previewId);
    var filenameLabel = document.getElementById(filenameLabelId);
    $(filenameLabel).html(file.name);

    if (!file.type.match(imageType)) {
        img.file = null;
        img.src = '/static/img/1x1.png';
        return;
    }

    img.file = file;

    var reader = new FileReader();
    reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    reader.readAsDataURL(file);
}
