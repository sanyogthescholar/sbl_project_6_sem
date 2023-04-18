const video = document.getElementById('video');
var detections;
const canvas = document.getElementById("canvas");
navigator.mediaDevices.getUserMedia = ( navigator.mediaDevices.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia);

function startVideo() {
  navigator.getUserMedia(
    {
      video: {}
    },
    stream => video.srcObject = stream,
    err => console.error(err)
  )
}

video.addEventListener('play', () => {
  //const canvas = faceapi.createCanvasFromMedia(video);
  const displaySize = { width: video.width, height: video.height };
})

const canvas2 = document.getElementById('canvas2');

$("#btnCapture").click(function () {  
  //var canvas = document.getElementById('canvas');  
  var context = canvas2.getContext('2d');  

  // Capture the image into canvas from Webcam streaming Video element  
  context.drawImage(video, 0, 0);  
});

$("#btnSave").click(function () {  
  
  // Below new canvas to generate flip/mirron image from existing canvas  
  var destinationCanvas = document.createElement("canvas");  
  var destCtx = destinationCanvas.getContext('2d');  


  destinationCanvas.height = 560;  
  destinationCanvas.width = 720;  

  //destCtx.translate(video.videoWidth, 0);  
  //destCtx.scale(-1, 1);  
  destCtx.drawImage(canvas2, 0, 0);  

  // Get base64 data to send to server for upload  
  var imagebase64data = destinationCanvas.toDataURL();  
  document.getElementById("input_student").value = String(imagebase64data);
  document.getElementById('student_data').submit();
  //imagebase64data = imagebase64data.replace('data:image/png;base64,', '');  
  /*$.ajax({  
      type: 'POST',
      url: '/upload',
      data: {imagebase64: imagebase64data},   
  }).done(function (){
    console.log(imagebase64data)
  });*/  
});
startVideo();