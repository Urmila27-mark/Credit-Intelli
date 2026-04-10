import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Intelli-Credit AI",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}
.block-container{padding:0}
</style>
""", unsafe_allow_html=True)

html = """

<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">

<style>

body{
margin:0;
background:#0A0F1E;
font-family:Inter;
color:white;
overflow-x:hidden;
}

/* HERO */

.hero{
height:100vh;
display:flex;
align-items:center;
justify-content:center;
flex-direction:column;
text-align:center;
position:relative;
}

.hero h1{
font-size:80px;
font-weight:900;
background:linear-gradient(90deg,#00E5FF,#7C3AED);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.hero p{
color:#9CA3AF;
max-width:700px;
font-size:20px;
}

.cta{
margin-top:40px;
padding:18px 40px;
border-radius:40px;
border:none;
background:linear-gradient(90deg,#00E5FF,#7C3AED);
font-size:18px;
cursor:pointer;
}

/* AI NETWORK CANVAS */

#ai-canvas{
position:absolute;
top:0;
left:0;
width:100%;
height:100%;
z-index:-1;
}

/* DATA PIPELINE */

.pipeline{
padding:120px 10%;
display:flex;
justify-content:space-around;
align-items:center;
}

.pipe-card{
background:rgba(255,255,255,0.04);
border:1px solid rgba(0,229,255,0.2);
padding:40px;
border-radius:25px;
width:260px;
text-align:center;
transition:0.3s;
}

.pipe-card:hover{
transform:translateY(-10px);
border-color:#00E5FF;
}

.pipe-card i{
font-size:40px;
color:#00E5FF;
margin-bottom:15px;
}

/* RISK GAUGE */

.gauge{
padding:120px 10%;
text-align:center;
}

.gauge-circle{
width:200px;
height:200px;
border-radius:50%;
background:conic-gradient(#00E5FF 0deg,#00E5FF 120deg,#1F2937 120deg);
display:flex;
align-items:center;
justify-content:center;
margin:auto;
font-size:40px;
font-weight:bold;
}

/* PARTICLES */

.particle{
position:absolute;
width:4px;
height:4px;
background:#00E5FF;
border-radius:50%;
opacity:0.6;
}

</style>
</head>

<body>

<canvas id="ai-canvas"></canvas>

<section class="hero">

<h1>Intelli-Credit</h1>

<p>
AI Powered Corporate Credit Decision Engine  
Transform Financial Data Into Real-Time Risk Intelligence
</p>

<button class="cta">Launch AI Analysis</button>

</section>

<section class="pipeline">

<div class="pipe-card">
<i class="fas fa-file-invoice"></i>
<h3>Upload Financials</h3>
<p>Bank statements & balance sheets</p>
</div>

<div class="pipe-card">
<i class="fas fa-brain"></i>
<h3>AI Processing</h3>
<p>ML models analyze financial behavior</p>
</div>

<div class="pipe-card">
<i class="fas fa-chart-line"></i>
<h3>Risk Insights</h3>
<p>Liquidity, leverage & fraud detection</p>
</div>

<div class="pipe-card">
<i class="fas fa-check-circle"></i>
<h3>Credit Decision</h3>
<p>Approve or flag application</p>
</div>

</section>

<section class="gauge">

<h2 style="font-size:40px;margin-bottom:50px;">AI Credit Score</h2>

<div class="gauge-circle" id="score">72</div>

<p style="margin-top:20px;color:#9CA3AF">
Medium Risk Borrower
</p>

</section>

<script>

/* THREE JS AI NETWORK */

const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(
75,
window.innerWidth/window.innerHeight,
0.1,
1000
)

const renderer = new THREE.WebGLRenderer({
canvas:document.getElementById("ai-canvas"),
alpha:true
})

renderer.setSize(window.innerWidth,window.innerHeight)

camera.position.z = 5

const geometry = new THREE.BufferGeometry()

const vertices = []

for(let i=0;i<2000;i++){

vertices.push(
Math.random()*10-5,
Math.random()*10-5,
Math.random()*10-5
)

}

geometry.setAttribute(
'position',
new THREE.Float32BufferAttribute(vertices,3)
)

const material = new THREE.PointsMaterial({
color:0x00e5ff,
size:0.02
})

const particles = new THREE.Points(geometry,material)

scene.add(particles)

function animate(){

requestAnimationFrame(animate)

particles.rotation.y += 0.0007

renderer.render(scene,camera)

}

animate()


/* GSAP INTRO */

gsap.from("h1",{
y:80,
opacity:0,
duration:1.5
})

gsap.from("p",{
y:40,
opacity:0,
delay:0.5
})

gsap.from(".pipe-card",{
scrollTrigger:".pipeline",
y:60,
opacity:0,
stagger:0.2
})


/* RISK SCORE ANIMATION */

let score = document.getElementById("score")

gsap.to(score,{
innerText:85,
duration:2,
snap:{innerText:1}
})

</script>

</body>
</html>

"""

components.html(html, height=1800)