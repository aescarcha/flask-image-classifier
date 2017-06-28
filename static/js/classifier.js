$('document').ready(function(){
    printNextImage();
});

function printNextImage() {
    console.log(images);
    image = images.shift();

    $("#image-classifier-template img").attr('src', 'static/images/' + image);
    $("#image-classifier-template").removeClass('hidden');

    getOrCreateImage(image).then(function(response){
        console.log(response);
    });
}

function getOrCreateImage(image) {
    return post('/images', {name: image});
}

function post(url, data) {
    return $.ajax({
        type: "POST",
        url: url,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json"
    });
}