var currentImage;

$('document').ready(function(){
    printNextImage();
    $('.label-selector').on('click', function(){
        handleLabelClick( $(this) );
    });
});


function handleLabelClick( $this ) {
    if( $this.hasClass('active') ){
        deleteLabel('/images/' + currentImage.id + '/labels', {label: $this.text().trim()});
        $this.removeClass('active');
        // $this.removeClass('focus');
    } else {
        post('/images/' + currentImage.id + '/labels', {label: $this.text().trim()});
        $this.addClass('active');
        // $this.addClass('focus');
    }
}

function printNextImage() {
    console.log(images);
    image = images.shift();

    $("#image-classifier-template img").attr('src', 'static/images/' + image);
    $("#image-classifier-template").removeClass('hidden');

    getOrCreateImage(image).then(function(response){
        currentImage = response;
        $('.label-selector').each(function(index, value){
            text = $(value).text().trim();
            if(currentImage.labels.indexOf(text) >= 0 ){
                $(value).addClass('active');
                // $(value).addClass('focus');
            }
        });
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

function deleteLabel(url, data) {
    return $.ajax({
        type: "DELETE",
        url: url,
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: "application/json"
    });
}

