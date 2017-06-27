$('document').ready(function(){
    printNextImage();
});

function printNextImage() {
    console.log(images);
    image = images.shift();

    $("#image-classifier-template img").attr('src', imageFolder + '/' + image);
    $("#image-classifier-template").removeClass('hidden');
}