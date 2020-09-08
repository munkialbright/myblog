document.addEventListener("DOMContentLoaded", function (evet) {
    console.log("This is editor.js")
    let sc = document.createElement('script');
    sc.setAttribute('src', '/static/js/ckeditor.js');

    document.head.appendChild(sc);

    sc.onload = ()=>{
        ClassicEditor
            .create( document.querySelector( '#id_content' ) )
            .catch( error => {
                console.error( error );
            } );
    }
});