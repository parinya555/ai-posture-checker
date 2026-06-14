 Prototype v2 Evidence

สิ่งที่ได้รับการปรับปรุงแล้ว

ปรับปรุงระบบ AI Pose Detection
เพิ่ม Dashboard แสดงผลแบบ Real-Time
เพิ่มระบบนับจำนวนครั้ง (Rep Counter)
เพิ่มระบบคำนวณคะแนนการออกกำลังกาย
ปรับปรุง User Interface ให้ทันสมัยและใช้งานง่าย
ปรับปรุงการแสดงผลกล้องและ Overlay Skeleton

หลักฐาน:

Screenshot หน้า Dashboard
Screenshot ระบบ AI ตรวจจับท่าทาง
Source Code Prototype v2
<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>FitSense AI Coach Pro</title>

<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>

<style>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/pose/pose.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>

<style>
<style>
body{
    font-family:Arial,sans-serif;
    text-align:center;
    background:#ddd;
    color:#ddd;
    margin:0;
    padding:20px;
}

h1{
    color:#2563eb;
}

#canvas{
    width:100%;
    max-width:450px;
    background:#000;
    border-radius:12px;
    border:2px solid #ddd;
    transform: scaleX(-1);
}

button{
    padding:10px 16px;
    margin:5px;
    border:none;
    border-radius:8px;
    background:#2563eb;
    color:white;
    cursor:pointer;
}

button:hover{
    opacity:.9;
}

#description{
    max-width:450px;
    margin:auto;
    color:#2e5077e9;
}

.info,
#tutorialBox,
#cameraGuide{
    max-width:450px;
    margin:10px auto;
    padding:12px;
    background:white;
    border-radius:12px;
    border:1px solid #ddd;
}
</style>
</style>

</head>
</style>
</head>
<body>

<h1>AI Fitness Coach Pro</h1>
<div id="tutorialBox" style="max-width:450px;margin:10px auto;padding:10px;background:#1e1e1e;border-radius:10px">
<h3> Exercise Tutorial</h3>
<p id="tutorial"></p>
<div id="cameraGuide" style="max-width:450px;margin:10px auto;padding:10px;background:#1e1e1e;border-radius:10px">
<h3> Camera Position Guide</h3>
<p>
• วางกล้องห่าง 1.5–2.5 เมตร<br>
• ให้เห็นร่างกายครบทั้งตัว<br>
• ยืนตรงกลางภาพ<br>
• หลีกเลี่ยงแสงย้อน<br>
• ใช้พื้นที่ที่มีแสงสว่างเพียงพอ
</p>
</div>
</div>
<div class="info">Exercise: <span id="exercise">bicep</span></div>
<div class="info">Reps: <span id="counter">0</span></div>
<div class="info">Stage: <span id="stage">down</span></div>
<div class="info">Tracking: <span id="quality">Waiting...</span></div>

<p id="description"></p>



<video id="video" autoplay playsinline muted hidden></video>
<canvas id="canvas"></canvas>

<br><br>

<button onclick="setExercise('bicep')">Bicep</button>
<button onclick="setExercise('shoulder')">Shoulder</button>
<button onclick="setExercise('lateral')">Lateral</button>
<button onclick="setExercise('squat')">Squat</button>

<br><br>

<button onclick="startCamera()"> Start Camera</button>

<script>
const $=id=>document.getElementById(id);

const EX={
 bicep:{
   desc:"Bicep Curl - งอแขนขึ้นลง",
   p:[12,14,16],
   up:45,
   down:155
 },
 shoulder:{
   desc:"Shoulder Press - ดันแขนเหนือศีรษะ",
   p:[12,14,16],
   up:70,
   down:150
 },
 lateral:{
   desc:"Lateral Raise - ยกแขนด้านข้าง",
   p:[11,13,15],
   up:80,
   down:145
 },
 squat:{
   desc:"Squat - ย่อตัวและลุกขึ้น",
   p:[23,25,27],
   up:95,
   down:165,
   reverse:true
 }
};

let exercise="bicep";
let counter=0;
let stage="down";
let smoothAngle=0;
let lastRepTime=0;

function setExercise(name){
 exercise=name;
 counter=0;
 stage="down";

 const tutorials={
   bicep:"งอแขนขึ้นจนสุด แล้วลดลงช้า ๆ รักษาหลังให้ตรง แนะนำ 10-15 ครั้ง",
   shoulder:"ดันแขนขึ้นเหนือศีรษะและลดลงอย่างควบคุม ไม่แอ่นหลัง",
   lateral:"ยกแขนด้านข้างจนระดับหัวไหล่ แล้วลดลงช้า ๆ",
   squat:"ย่อตัวโดยให้หลังตรง เข่าไม่เลยปลายเท้ามากเกินไป"
 };

 $("exercise").textContent=name;
 $("description").textContent=EX[name].desc;
 $("tutorial").textContent=tutorials[name];
 $("counter").textContent=0;
 $("stage").textContent=stage;
}

setExercise("bicep");

function calcAngle(a,b,c){
 let r=Math.atan2(c.y-b.y,c.x-b.x)-Math.atan2(a.y-b.y,a.x-b.x);
 let d=Math.abs(r*180/Math.PI);
 return d>180?360-d:d;
}

const pose=new Pose({
 locateFile:f=>`https://cdn.jsdelivr.net/npm/@mediapipe/pose/${f}`
});

pose.setOptions({
 modelComplexity:1,
 smoothLandmarks:true,
 minDetectionConfidence:.6,
 minTrackingConfidence:.6
});

const video=$("video");
const canvas=$("canvas");
const ctx=canvas.getContext("2d");

pose.onResults(r=>{

 if(!r.image) return;

 ctx.clearRect(0,0,canvas.width,canvas.height);
 ctx.drawImage(
    r.image,
    0,
    0,
    canvas.width,
    canvas.height
);

 if(!r.poseLandmarks) return;

 const lm=r.poseLandmarks;

 drawConnectors(ctx,lm,POSE_CONNECTIONS,{color:"#00FF00",lineWidth:3});
 drawLandmarks(ctx,lm,{color:"#FF0000",lineWidth:1});

 const quality=(
   lm[11].visibility+
   lm[12].visibility+
   lm[13].visibility+
   lm[14].visibility
 )/4;

 $("quality").textContent=
 quality>.85?"Excellent":
 quality>.70?"Good":
 quality>.50?"Fair":"Move Closer";

 const e=EX[exercise];

 if(
   lm[e.p[0]].visibility<0.6 ||
   lm[e.p[1]].visibility<0.6 ||
   lm[e.p[2]].visibility<0.6
 ){
   return;
 }

 const rawAngle=calcAngle(
   lm[e.p[0]],
   lm[e.p[1]],
   lm[e.p[2]]
 );

 smoothAngle=smoothAngle*0.8+rawAngle*0.2;

 const a=smoothAngle;
 const now=Date.now();

 if(e.reverse){

   if(a>e.down) stage="up";

   if(
      a<e.up &&
      stage==="up" &&
      now-lastRepTime>800
   ){
      stage="down";
      counter++;
      lastRepTime=now;
   }

 }else{

   if(a>e.down) stage="down";

   if(
      a<e.up &&
      stage==="down" &&
      now-lastRepTime>800
   ){
      stage="up";
      counter++;
      lastRepTime=now;
   }
 }

 $("counter").textContent=counter;
 $("stage").textContent=stage;
});

async function startCamera(){

 try{

   const stream=await navigator.mediaDevices.getUserMedia({
     video:{facingMode:"user"},
     audio:false
   });

   video.srcObject=stream;

   video.onloadedmetadata=async()=>{

      await video.play();

      canvas.width=video.videoWidth;
      canvas.height=video.videoHeight;

      const detect=async()=>{
         await pose.send({image:video});
         requestAnimationFrame(detect);
      };

      detect();
   };

 }catch(err){
   alert("เปิดกล้องไม่ได้ : "+err.message);
 }
}
</script>
</body>
</html>
