let camera_button = document.getElementById("start-camera");
let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let preview = document.querySelector('img');
var buttonSubmit=document.getElementById('submit');
var fileInput=document.getElementById('fileinput')

buttonSubmit.addEventListener("click",function (){
    camera_button.textContent="Bật camera"
    if(video.srcObject!=null){
        video.srcObject.getTracks().forEach(function(track) {
            track.stop();
        });
    }

    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.addEventListener("load", function () {
    preview.src = reader.result;
    sendImageToServer(reader.result)
    }, false);

    if (file) {
        reader.readAsDataURL(file);
    }
    document.getElementById("bottom").hidden=false
    img.hidden=false
    video.hidden=true
    canvas.hidden=true
})

camera_button.addEventListener('click', async function() {
    if(camera_button.textContent=="Bật camera")
    {
        clear();
        camera_button.textContent="Chụp ảnh"

        let stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        video.srcObject = stream;
        video.hidden=false
        canvas.hidden=true
        img.hidden=true

    }else
    {
        document.getElementById("bottom").hidden=false
        camera_button.textContent="Bật camera"
        canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
        let img_base64 = canvas.toDataURL('image/jpeg')
        sendImageToServer(img_base64)
        video.srcObject.getTracks().forEach(function(track) {
            track.stop();
        });
        video.hidden=true
        canvas.hidden=false
        img.hidden=true
    }

});

function sendImageToServer(img_base64)
{
    img_base64=img_base64.replace(/^.*,/, '');
    const body = new FormData();
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var x=JSON.parse(xhr.responseText)
            document.getElementById("result_id").innerHTML=x['msg']
            document.getElementById("extra").innerHTML=x['extra']
            document.getElementById("result_id_number").innerHTML=x['face_shape']
        }
    };
    body.append('img', img_base64);
    xhr.open('POST', '/', true);
    xhr.send(body);
}

fileInput.addEventListener('click',clear)

function clear()
{
    document.getElementById("result_id").innerHTML=""
    document.getElementById("extra").innerHTML=""
    document.getElementById("result_id_number").innerHTML=""
    document.getElementById("bottom").hidden=true
}