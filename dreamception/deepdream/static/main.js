// File Upload
//
var photo_name;
function ekUpload(){
  function Init() {

    console.log("Upload Initialised");

    var fileSelect    = document.getElementById('file-upload'),
        fileDrag      = document.getElementById('file-drag'),
        submitButton  = document.getElementById('submit-button');


      fileSelect.addEventListener('change', fileSelectHandler, false);

    // Is XHR2 available?
    var xhr = new XMLHttpRequest();
    if (xhr.upload) {
      // File Drop
      fileDrag.addEventListener('dragover', fileDragHover, false);
      fileDrag.addEventListener('dragleave', fileDragHover, false);
      fileDrag.addEventListener('drop', fileSelectHandler, false);
    }
  }
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

  function fileDragHover(e) {
    var fileDrag = document.getElementById('file-drag');

    e.stopPropagation();
    e.preventDefault();

    fileDrag.className = (e.type === 'dragover' ? 'hover' : 'modal-body file-upload');
  }

  function fileSelectHandler(e) {
    // Fetch FileList object
    var files = e.target.files || e.dataTransfer.files;

    // Cancel event and hover styling
    fileDragHover(e);
    console.log(files.length)
    // Process all File objects
    for (var i = 0, f=files.length;i<f ; i++) {
      parseFile(files[i]);

      uploadFile(files[i]);
    }
  }

  // Output
  function output(msg) {
    // Response
    var m = document.getElementById('messages');
    m.innerHTML = msg;
  }

  function parseFile(file) {

    console.log(file.name);
    output(
      '<strong>' + encodeURI(file.name) + '</strong>'
    );
    
     var fileType = file.type;
     console.log(fileType);
    var imageName = file.name;

    var isGood = (/\.(?=gif|jpg|png|jpeg)/gi).test(imageName);
    if (isGood) {
      console.log("it is a good a")
      document.getElementById('start').classList.add("hidden");
      document.getElementById('response').classList.remove("hidden");
      document.getElementById('notimage').classList.add("hidden");
      // Thumbnail Preview
      document.getElementById('file-image').classList.remove("hidden");
      document.getElementById('file-image').src = URL.createObjectURL(file);
    }
    else {
      document.getElementById('file-image').classList.add("hidden");
      document.getElementById('notimage').classList.remove("hidden");
      document.getElementById('start').classList.remove("hidden");
      document.getElementById('response').classList.add("hidden");
      document.getElementById("file-upload-form").reset();
    }
  }

  function setProgressMaxValue(e) {
    var pBar = document.getElementById('file-progress');

    if (e.lengthComputable) {
      pBar.max = e.total;
    }
  }

  function updateFileProgress(e) {
    var pBar = document.getElementById('file-progress');

    if (e.lengthComputable) {
      pBar.value = e.loaded;
    }
  }


  function uploadFile(file) {
    console.log("in upload");







        // File received / failed

       var form = document.getElementById('file-upload-form');
       var formdata = new FormData(form);
        formdata.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        formdata.append('title',file.name);

        photo_name = file.name;

        //xhr.send(formData);



        $.ajax({
        url: document.getElementById('file-upload-form').action,
        type: 'POST',
        data: formdata,
        async: true,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,




        success: function (response) {
            $('.upload-progress').hide();
            if (response.status == 200) {
                console.log(response);
                window.location = '/deepdream/dream';

            }else {
                try {
                    var error = JSON.parse(response.error);
                    alert('Vailed to upload! ' + error['data']['error'] + ', error_code: ' + error['status']);
                }catch(error){
                    alert('Vailed to upload! ' + response.error + ', error_code :' + response.status);
                }
                console.log(response);
            }
        },
        error: function(response) {
            console.log("error", response);
            $('.upload-progress').hide();
        }
    });
    return false;


  }

  // Check for the various File API support.
  if (window.File && window.FileList && window.FileReader) {
    console.log(window.location);
    Init();
  } else {
    document.getElementById('file-drag').style.display = 'none';
  }
}




function getform(){
    function  Init() {
        console.log("workin nigga");
        btn = document.getElementById("dream");



        btn.addEventListener('click',openConnect,false);





        function openConnect(e){

        }

    }
    Init();
}




if(window.location.pathname =='/'){
    ekUpload();
}

if(window.location.pathname == '/deepdream/dream'){
    getform();
}
