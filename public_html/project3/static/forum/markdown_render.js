$(document).ready(function () {
    $('.markdown-container').each(function (index, element) {
        console.log(element.innerHTML);
        element.innerHTML = marked(element.innerHTML).replace('\n','<br>');
    })
});