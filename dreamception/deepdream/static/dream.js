
function Dream() {
    var image = document.getElementById('image').src,
        dream_var = ' ';
    var form = document.getElementById('dream-form'),
        submit_btn = document.getElementById('dream')
    submit_btn.addEventListener('click', start_dream, false);
    document.getElementById('image').addEventListener('click', switch_image, false);


    function switch_image() {

        if (document.getElementById('image').src == image) {

            if (dream_var != ' ') {
                document.getElementById('image').src =dream_var;
                console.log('swap');
            }
        }
        if (document.getElementById('image').src == dream_var) {
            document.getElementById('image').src = image;
            console.log('swap');
        }
    }


    function start_dream(e) {
        form = document.getElementById('dream-form');
        var formdata = new FormData(form);

        formdata.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        $.ajax({
            url: document.getElementById('dream-form').action,
            type: 'POST',
            data: formdata,
            async: true,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,


            success: function (response) {

                document.getElementById('image').src = response.img;
                dream_var = response.img;


                console.log(response);

            },
            error: function (response) {
                console.log("error", response);


            }
        });
        return false;


        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    }

}

Dream()