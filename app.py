from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MineHosting — ⛏️ Minecraft & 🖥️ VPS Hosting</title>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}

body{
font-family:Inter,sans-serif;
background:#020604;
color:#fff;
overflow-x:hidden;
}

#particles{
position:fixed;
inset:0;
z-index:-1;
pointer-events:none;
}

.particle{
position:fixed;
width:3px;
height:3px;
background:#39ff88;
border-radius:50%;
opacity:.4;
animation:float linear infinite;
}

@keyframes float{
from{transform:translateY(105vh)}
to{transform:translateY(-10vh)}
}

nav{
position:fixed;
top:0;
left:0;
width:100%;
z-index:1000;
padding:16px 6%;
display:flex;
justify-content:space-between;
align-items:center;
background:rgba(0,8,4,.75);
backdrop-filter:blur(16px);
border-bottom:1px solid rgba(57,255,136,.12);
}

.brand{
display:flex;
align-items:center;
gap:10px;
text-decoration:none;
color:#fff;
font-size:20px;
font-weight:900;
}

.brand img{
width:42px;
height:42px;
object-fit:contain;
border-radius:10px;
}

.brand span{color:#39ff88}

.nav-links{
display:flex;
align-items:center;
gap:25px;
}

.nav-links a{
color:#c8d2cc;
text-decoration:none;
font-size:13px;
font-weight:600;
transition:.3s;
}

.nav-links a:hover{color:#39ff88}

.discord-btn{
background:#39ff88;
color:#001508!important;
padding:11px 17px;
border-radius:10px;
font-weight:800!important;
}

.hero{
min-height:100vh;
position:relative;
display:flex;
align-items:center;
justify-content:center;
text-align:center;
padding:120px 20px 80px;
overflow:hidden;
}

.hero-video{
position:absolute;
inset:0;
width:100%;
height:100%;
object-fit:cover;
z-index:-3;
}

.hero-overlay{
position:absolute;
inset:0;
z-index:-2;
background:
linear-gradient(rgba(0,5,2,.55),rgba(0,8,4,.96)),
radial-gradient(circle,rgba(57,255,136,.12),transparent 60%);
}

.hero-content{
max-width:950px;
animation:heroIn 1s ease;
}

@keyframes heroIn{
from{opacity:0;transform:translateY(35px)}
to{opacity:1;transform:translateY(0)}
}

.hero-logo{
width:110px;
height:110px;
object-fit:contain;
margin-bottom:20px;
filter:drop-shadow(0 0 30px rgba(57,255,136,.4));
animation:logoFloat 4s ease-in-out infinite;
}

@keyframes logoFloat{
0%,100%{transform:translateY(0)}
50%{transform:translateY(-9px)}
}

.badge{
display:inline-block;
padding:9px 15px;
border:1px solid rgba(57,255,136,.3);
border-radius:100px;
background:rgba(57,255,136,.07);
color:#72ffa9;
font-size:12px;
font-weight:700;
margin-bottom:18px;
}

h1{
font-size:clamp(43px,8vw,85px);
line-height:.98;
font-weight:900;
letter-spacing:-4px;
}

h1 span{
color:#39ff88;
text-shadow:0 0 35px rgba(57,255,136,.3);
}

.hero p{
max-width:720px;
margin:25px auto;
color:#b9c8bf;
font-size:16px;
line-height:1.8;
}

.hero-buttons{
display:flex;
justify-content:center;
gap:13px;
flex-wrap:wrap;
margin-top:30px;
}

.btn{
display:inline-block;
text-decoration:none;
padding:15px 24px;
border-radius:12px;
font-weight:800;
transition:.3s;
}

.btn-primary{
background:#39ff88;
color:#001508;
box-shadow:0 0 30px rgba(57,255,136,.2);
}

.btn-primary:hover{
transform:translateY(-4px);
box-shadow:0 0 40px rgba(57,255,136,.4);
}

.btn-secondary{
color:#fff;
border:1px solid rgba(255,255,255,.15);
background:rgba(255,255,255,.04);
}

.btn-secondary:hover{
border-color:#39ff88;
transform:translateY(-4px);
}

.stats{
max-width:1100px;
margin:-45px auto 0;
position:relative;
z-index:5;
padding:0 20px;
}

.stats-grid{
display:grid;
grid-template-columns:repeat(4,1fr);
background:rgba(7,18,12,.85);
border:1px solid rgba(57,255,136,.12);
border-radius:20px;
backdrop-filter:blur(15px);
overflow:hidden;
}

.stat{
text-align:center;
padding:30px 15px;
border-right:1px solid rgba(255,255,255,.07);
}

.stat:last-child{border:none}

.stat h3{
color:#39ff88;
font-size:29px;
font-weight:900;
}

.stat p{
color:#8d9d94;
font-size:11px;
margin-top:5px;
}

section{
padding:110px 6%;
position:relative;
}

.section-head{
text-align:center;
max-width:720px;
margin:0 auto 55px;
}

.mini{
color:#39ff88;
font-size:11px;
text-transform:uppercase;
letter-spacing:3px;
font-weight:800;
}

.section-head h2{
font-size:clamp(32px,5vw,53px);
margin:10px 0 15px;
font-weight:900;
}

.section-head p{
color:#8f9d95;
line-height:1.7;
}

.why-grid{
max-width:1150px;
margin:auto;
display:grid;
grid-template-columns:repeat(3,1fr);
gap:18px;
}

.feature{
padding:30px;
background:linear-gradient(145deg,rgba(12,28,19,.9),rgba(3,10,6,.9));
border:1px solid rgba(57,255,136,.1);
border-radius:18px;
transition:.35s;
}

.feature:hover{
transform:translateY(-8px);
border-color:rgba(57,255,136,.45);
box-shadow:0 15px 50px rgba(57,255,136,.08);
}

.feature-icon{
width:48px;
height:48px;
display:grid;
place-items:center;
background:rgba(57,255,136,.09);
border-radius:13px;
font-size:23px;
margin-bottom:20px;
}

.feature h3{
font-size:18px;
margin-bottom:10px;
}

.feature p{
color:#829088;
line-height:1.7;
font-size:14px;
}

.services{
max-width:1100px;
margin:auto;
display:grid;
grid-template-columns:repeat(2,1fr);
gap:22px;
}

.service{
position:relative;
overflow:hidden;
padding:35px;
border-radius:20px;
background:#07130c;
border:1px solid rgba(57,255,136,.13);
}

.service h3{
font-size:24px;
margin-bottom:12px;
}

.service p{
color:#89968f;
line-height:1.7;
font-size:14px;
}

.service ul{
list-style:none;
margin-top:20px;
}

.service li{
color:#b8c5bd;
margin:10px 0;
font-size:13px;
}

.service li::before{
content:"✓";
color:#39ff88;
font-weight:900;
margin-right:10px;
}

.reveal{
opacity:0;
transform:translateY(35px);
transition:.8s ease;
}

.reveal.show{
opacity:1;
transform:translateY(0);
}

@media(max-width:1000px){
.why-grid{grid-template-columns:repeat(2,1fr)}
}

.plans-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;max-width:1150px;margin:auto}
.plan{background:linear-gradient(160deg, rgba(12,28,19,0.85), rgba(3,10,6,0.95));border:1px solid rgba(57,255,136,0.25);padding:32px 24px;border-radius:24px;text-align:center;position:relative;transition:all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);backdrop-filter:blur(18px);box-shadow:0 8px 32px 0 rgba(0,0,0,0.37);}
.plan:hover{border-color:#39ff88;transform:translateY(-10px) scale(1.02);box-shadow:0 20px 40px rgba(57,255,136,0.25);}
.plan-btn{background:linear-gradient(135deg, #39ff88 0%, #10b981 100%);color:#001508;font-weight:900;letter-spacing:0.5px;text-transform:uppercase;border-radius:12px;padding:14px;box-shadow:0 4px 15px rgba(57,255,136,0.3);}
.plan-btn:hover{box-shadow:0 0 25px rgba(57,255,136,0.7);transform:scale(1.03);}
.popular{background:linear-gradient(90deg, #39ff88, #00ffaa);color:#000;font-weight:900;letter-spacing:1px;padding:5px 14px;border-radius:12px;box-shadow:0 0 15px rgba(57,255,136,0.6);}
.brand img{width:42px;height:42px;object-fit:contain;filter:drop-shadow(0 0 10px #39ff88);border-radius:10px}
.plan:hover{border-color:#39ff88;transform:translateY(-6px);box-shadow:0 10px 30px rgba(57,255,136,.15)}
.plan.featured{border:2px solid #39ff88;background:rgba(12,35,22,.95)}
.plan-name{font-size:22px;font-weight:900;margin-bottom:10px;color:#fff}
.price{font-size:32px;font-weight:900;color:#39ff88}
.price small{font-size:13px;color:#a0b0a5}
.pkr{font-size:13px;color:#708577;margin-bottom:15px}
.plan ul{list-style:none;padding:0;margin:20px 0;text-align:left}
.plan li{padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05);font-size:13px;color:#c0d0c5}
.plan li::before{content:"✓ ";color:#39ff88;font-weight:bold}
.plan-btn{display:block;width:100%;padding:12px;background:#39ff88;color:#001508;text-decoration:none;font-weight:800;border-radius:10px;margin-top:15px;transition:.3s}
.plan-btn:hover{box-shadow:0 0 15px rgba(57,255,136,.5)}
.popular{position:absolute;top:-12px;right:20px;background:#39ff88;color:#000;font-size:10px;font-weight:900;padding:4px 10px;border-radius:20px}
.reviews{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;max-width:1100px;margin:auto}
.review{background:rgba(7,19,12,.8);padding:25px;border-radius:16px;border:1px solid rgba(57,255,136,.1)}
.stars{color:#39ff88;margin-bottom:10px}
.review-user{display:flex;align-items:center;gap:12px;margin-top:15px}
.avatar{width:38px;height:38px;background:#39ff88;color:#000;border-radius:50%;display:grid;place-items:center;font-weight:bold}
.cta{text-align:center;max-width:800px;margin:60px auto;padding:50px 20px;background:linear-gradient(145deg,rgba(12,35,22,.8),rgba(3,10,6,.9));border:1px solid rgba(57,255,136,.3);border-radius:24px}
.cta h2{font-size:36px;margin-bottom:15px}
footer{text-align:center;padding:40px 20px;border-top:1px solid rgba(57,255,136,.1);color:#708577;font-size:12px}

.plans-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:24px;max-width:1200px;margin:auto}
.plan{background:linear-gradient(160deg,rgba(10,26,17,0.85),rgba(2,8,4,0.95));border:1px solid rgba(57,255,136,0.22);padding:35px 25px;border-radius:24px;text-align:center;position:relative;transition:all .4s cubic-bezier(.175,.885,.32,1.275);backdrop-filter:blur(20px);box-shadow:0 10px 30px rgba(0,0,0,0.5)}
.plan:hover{border-color:#39ff88;transform:translateY(-12px) scale(1.02);box-shadow:0 20px 45px rgba(57,255,136,0.25)}
.plan.featured{border:2px solid #39ff88;background:linear-gradient(160deg,rgba(16,42,27,0.92),rgba(2,10,5,0.98));box-shadow:0 0 25px rgba(57,255,136,0.25)}
.plan-name{font-size:24px;font-weight:900;letter-spacing:1px;margin-bottom:8px;color:#fff;text-shadow:0 0 10px rgba(255,255,255,0.2)}
.price{font-size:36px;font-weight:900;color:#39ff88;text-shadow:0 0 20px rgba(57,255,136,0.4)}
.price small{font-size:14px;color:#a0b5a8;font-weight:500}
.pkr{font-size:13px;color:#789282;margin-bottom:20px;font-weight:600}
.plan ul{list-style:none;padding:0;margin:22px 0;text-align:left}
.plan li{padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);font-size:13.5px;color:#c8d8ce;display:flex;align-items:center;gap:8px}
.plan li::before{content:"2713";color:#39ff88;font-weight:900;font-size:15px;text-shadow:0 0 8px #39ff88}
.plan-btn{display:block;width:100%;padding:14px;background:linear-gradient(135deg,#39ff88,#00e676);color:#001508;text-decoration:none;font-weight:900;font-size:14px;letter-spacing:0.5px;text-transform:uppercase;border-radius:14px;margin-top:20px;transition:all .3s;box-shadow:0 4px 20px rgba(57,255,136,0.35)}
.plan-btn:hover{box-shadow:0 0 30px rgba(57,255,136,0.75);transform:scale(1.02)}
.popular{position:absolute;top:-14px;right:22px;background:linear-gradient(90deg,#39ff88,#00ffaa);color:#001508;font-size:10px;font-weight:900;letter-spacing:1px;padding:5px 14px;border-radius:12px;box-shadow:0 0 18px rgba(57,255,136,0.7)}
.reviews{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:22px;max-width:1150px;margin:auto}
.review{background:rgba(8,22,14,0.85);padding:28px;border-radius:20px;border:1px solid rgba(57,255,136,0.15);backdrop-filter:blur(12px)}
.stars{color:#39ff88;margin-bottom:12px;font-size:18px;text-shadow:0 0 10px rgba(57,255,136,0.5)}
.review-user{display:flex;align-items:center;gap:14px;margin-top:18px}
.avatar{width:42px;height:42px;background:linear-gradient(135deg,#39ff88,#10b981);color:#000;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:16px;box-shadow:0 0 12px rgba(57,255,136,0.4)}
.cta{text-align:center;max-width:850px;margin:70px auto;padding:55px 25px;background:linear-gradient(145deg,rgba(14,38,24,0.85),rgba(2,8,4,0.95));border:1px solid rgba(57,255,136,0.35);border-radius:28px;box-shadow:0 15px 40px rgba(0,0,0,0.6);backdrop-filter:blur(16px)}
.cta h2{font-size:40px;margin-bottom:15px;font-weight:900}
footer{text-align:center;padding:45px 20px;border-top:1px solid rgba(57,255,136,0.12);color:#788f80;font-size:12px;line-height:1.8}

.plans-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:22px;max-width:1200px;margin:auto}
.plan{background:linear-gradient(160deg,rgba(10,26,17,0.88),rgba(2,8,4,0.96));border:1px solid rgba(57,255,136,0.25);padding:32px 22px;border-radius:24px;text-align:center;position:relative;transition:all .4s ease;backdrop-filter:blur(20px);box-shadow:0 10px 30px rgba(0,0,0,0.6)}
.plan:hover{border-color:#39ff88;transform:translateY(-10px);box-shadow:0 15px 40px rgba(57,255,136,0.25)}
.plan.featured{border:2px solid #39ff88;background:linear-gradient(160deg,rgba(16,42,27,0.95),rgba(2,10,5,0.99))}
.plan-name{font-size:24px;font-weight:900;letter-spacing:1px;margin-bottom:8px;color:#fff}
.price{font-size:36px;font-weight:900;color:#39ff88;text-shadow:0 0 15px rgba(57,255,136,0.4)}
.price small{font-size:14px;color:#a0b5a8}
.pkr{font-size:13px;color:#789282;margin-bottom:20px;font-weight:600}
.plan ul{list-style:none;padding:0;margin:22px 0;text-align:left}
.plan li{padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.06);font-size:13.5px;color:#c8d8ce;display:flex;align-items:center;gap:8px}
.plan li::before{content:"⚡ ";color:#39ff88;font-weight:900}
.plan-btn{display:block;width:100%;padding:14px;background:linear-gradient(135deg,#39ff88,#00e676);color:#001508;text-decoration:none;font-weight:900;font-size:14px;text-transform:uppercase;border-radius:12px;margin-top:20px;transition:all .3s;box-shadow:0 4px 20px rgba(57,255,136,0.35)}
.plan-btn:hover{box-shadow:0 0 30px rgba(57,255,136,0.8);transform:scale(1.02)}
.popular{position:absolute;top:-13px;right:20px;background:linear-gradient(90deg,#39ff88,#00ffaa);color:#001508;font-size:10px;font-weight:900;padding:5px 14px;border-radius:12px;box-shadow:0 0 18px rgba(57,255,136,0.7)}
.reviews{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;max-width:1150px;margin:auto}
.review{background:rgba(8,22,14,0.9);padding:28px;border-radius:20px;border:1px solid rgba(57,255,136,0.2);backdrop-filter:blur(14px)}
.stars{margin-bottom:12px;font-size:16px}
.review-user{display:flex;align-items:center;gap:14px;margin-top:18px}
.avatar{width:42px;height:42px;background:linear-gradient(135deg,#39ff88,#10b981);color:#000;border-radius:50%;display:grid;place-items:center;font-weight:900;font-size:18px}

@media(max-width:700px){
.nav-links a:not(.discord-btn){display:none}

.stats-grid{
grid-template-columns:repeat(2,1fr);
}

.stat:nth-child(2){border-right:none}

.stat:nth-child(-n+2){
border-bottom:1px solid rgba(255,255,255,.07);
}

section{padding:80px 5%}

.why-grid,
.services{
grid-template-columns:1fr;
}

h1{letter-spacing:-2px}

.hero p{font-size:14px}
}
</style>
</head>

<body>

<div id="particles"></div>

<nav>
<a href="#home" class="brand">
<img src="https://cdn.discordapp.com/attachments/1554852353889411182/1554916279494905947/file_00000000dacc720bb265345759986b31-10-1.png?backend=b2src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"ex=6abea021src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"is=6abd4ea1src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"hm=8fe3599bde5c87065cc6644574280a8eb7a344eab3b29a8d92f68f6c443f3585src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"">
🎮 MINE<span>HOSTING</span>
</a>

<div class="nav-links">
<a href="#why">✨ Why Us</a>
<a href="#services">🛠️ Services</a>
<a href="#minecraft">⛏️ Minecraft</a>
<a href="#vps">🖥️ VPS</a>
<a href="#reviews">💬 Reviews</a>
<a class="discord-btn" href="https://discord.gg/JzaPaJWdA7" target="_blank">Discord ↗</a>
</div>
</nav>

<section class="hero" id="home">

<video class="hero-video" autoplay muted loop playsinline>
<source src="https://cdn.discordapp.com/attachments/1554852353889411182/1554916279494905947/file_00000000dacc720bb265345759986b31-10-1.png?backend=b2src="https://assets.mixkit.co/videos/preview/mixkit-digital-network-nodes-and-connections-43033-large.mp4"ex=6abea021src="https://assets.mixkit.co/videos/preview/mixkit-digital-network-nodes-and-connections-43033-large.mp4"is=6abd4ea1src="https://assets.mixkit.co/videos/preview/mixkit-digital-network-nodes-and-connections-43033-large.mp4"hm=8fe3599bde5c87065cc6644574280a8eb7a344eab3b29a8d92f68f6c443f3585src="https://assets.mixkit.co/videos/preview/mixkit-digital-network-nodes-and-connections-43033-large.mp4"" type="video/mp4">
</video>

<div class="hero-overlay"></div>

<div class="hero-content">

<img class="hero-logo"
src="https://cdn.discordapp.com/attachments/1554852353889411182/1554916279494905947/file_00000000dacc720bb265345759986b31-10-1.png?backend=b2src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"ex=6abea021src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"is=6abd4ea1src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"hm=8fe3599bde5c87065cc6644574280a8eb7a344eab3b29a8d92f68f6c443f3585src="https://cdn-icons-png.flaticon.com/512/3593/3593452.png"">

<div class="badge">⚡ POWERING YOUR SERVERS</div>

<h1>
Build. Host.<br>
<span>Play Without Limits.</span>
</h1>

<p>
Welcome to MineHosting — affordable, reliable and powerful
⛏️ Minecraft & 🖥️ VPS hosting built for gamers, developers and
server owners who want more without paying more.
</p>

<div class="hero-buttons">
<a href="#minecraft" class="btn btn-primary">Explore ⛏️ Minecraft Hosting</a>
<a href="#vps" class="btn btn-secondary">View 🖥️ VPS Plans</a>
</div>

</div>
</section>

<div class="stats">
<div class="stats-grid">

<div class="stat">
<h3>24/7</h3>
<p>SERVER AVAILABILITY</p>
</div>

<div class="stat">
<h3>SSD</h3>
<p>FAST STORAGE</p>
</div>

<div class="stat">
<h3>KVM</h3>
<p>🖥️ VPS VIRTUALIZATION</p>
</div>

<div class="stat">
<h3>₹20+</h3>
<p>STARTING PRICE</p>
</div>

</div>
</div>

<section id="why">

<div class="section-head reveal">
<div class="mini">WHY MINEHOSTING?</div>
<h2>Hosting Made <span style="color:#39ff88">Simple.</span></h2>
<p>
Powerful resources, useful features and affordable plans
for your ⛏️ Minecraft servers and 🖥️ VPS projects.
</p>
</div>

<div class="why-grid">

<div class="feature reveal">
<div class="feature-icon">⚡</div>
<h3>Fast Performance</h3>
<p>
SSD-powered infrastructure designed to provide responsive
performance for your servers and projects.
</p>
</div>

<div class="feature reveal">
<div class="feature-icon">🛡️</div>
<h3>DDoS Protection</h3>
<p>
Protection-focused infrastructure designed to help keep
your services accessible.
</p>
</div>

<div class="feature reveal">
<div class="feature-icon">🚀</div>
<h3>Instant Deployment</h3>
<p>
Deploy your hosting environment quickly and start working
on your project without unnecessary delays.
</p>
</div>

<div class="feature reveal">
<div class="feature-icon">💰</div>
<h3>Affordable Pricing</h3>
<p>
Choose a plan based on your required resources and budget.
</p>
</div>

<div class="feature reveal">
<div class="feature-icon">🎮</div>
<h3>Gaming Ready</h3>
<p>
⛏️ Minecraft plans include Java and Bedrock support with
Pterodactyl features on selected plans.
</p>
</div>

<div class="feature reveal">
<div class="feature-icon">🔧</div>
<h3>Flexible 🖥️ VPS</h3>
<p>
KVM 🖥️ VPS plans provide flexible resources and root access
on supported plans.
</p>
</div>

</div>
</section>

<section id="services">

<div class="section-head reveal">
<div class="mini">OUR SERVICES</div>
<h2>Everything You Need.</h2>
<p>
From ⛏️ Minecraft communities to development projects,
MineHosting provides flexible hosting solutions.
</p>
</div>

<div class="services">

<div class="service reveal">
<h3>🎮 ⛏️ Minecraft Hosting</h3>
<p>
Launch your ⛏️ Minecraft server with scalable resources,
Java + Bedrock support and Pterodactyl on selected plans.
</p>

<ul>
<li>Java + Bedrock Support</li>
<li>SSD Storage</li>
<li>Pterodactyl Panel</li>
<li>Backups on selected plans</li>
<li>24/7 Server Availability</li>
</ul>
</div>

<div class="service reveal">
<h3>🖥️ 🖥️ VPS Hosting</h3>
<p>
Get a KVM virtual private server with SSD storage,
root access and flexible resources.
</p>

<ul>
<li>KVM Virtualization</li>
<li>Full Root Access</li>
<li>Ubuntu & Debian Support</li>
<li>Pterodactyl Support</li>
<li>Fast Deployment</li>
</ul>
</div>

</div>
</section>
# ================= MINECRAFT PLANS =================

<section id="minecraft">

<div class="section-head reveal">
<div class="mini">MINECRAFT HOSTING</div>

<h2>
Choose Your
<span style="color:#39ff88">Power.</span>
</h2>

<p>
Affordable ⛏️ Minecraft hosting for survival servers,
communities, SMPs and large projects.
</p>
</div>

<div class="plans-grid">

<div class="plan reveal">
<div class="plan-name">GRASS</div>
<div class="price">₹20 <small>/month</small></div>
<div class="pkr">Rs. 60/month</div>

<ul>
<li>2GB RAM</li>
<li>100% CPU</li>
<li>10GB SSD</li>
<li>Java + Bedrock Support</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>
</div>


<div class="plan reveal">
<div class="plan-name">IRON</div>
<div class="price">₹40 <small>/month</small></div>
<div class="pkr">Rs. 115/month</div>

<ul>
<li>4GB RAM</li>
<li>200% CPU</li>
<li>20GB SSD</li>
<li>Java + Bedrock Support</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>
</div>


<div class="plan reveal featured">

<div class="popular">POPULAR</div>

<div class="plan-name">DIAMOND</div>

<div class="price">₹60 <small>/month</small></div>

<div class="pkr">Rs. 175/month</div>

<ul>
<li>6GB RAM</li>
<li>300% CPU</li>
<li>30GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">EMERALD</div>

<div class="price">₹80 <small>/month</small></div>

<div class="pkr">Rs. 230/month</div>

<ul>
<li>8GB RAM</li>
<li>400% CPU</li>
<li>50GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">NETHERITE</div>

<div class="price">₹120 <small>/month</small></div>

<div class="pkr">Rs. 345/month</div>

<ul>
<li>12GB RAM</li>
<li>500% CPU</li>
<li>80GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
<li>5 Backups</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">TITAN</div>

<div class="price">₹160 <small>/month</small></div>

<div class="pkr">Rs. 460/month</div>

<ul>
<li>16GB RAM</li>
<li>600% CPU</li>
<li>100GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
<li>5 Backups</li>
<li>5 Databases</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">LEGEND</div>

<div class="price">₹220 <small>/month</small></div>

<div class="pkr">Rs. 630/month</div>

<ul>
<li>24GB RAM</li>
<li>800% CPU</li>
<li>150GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
<li>10 Backups</li>
<li>10 Databases</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal featured">

<div class="popular">MAX POWER</div>

<div class="plan-name">GOD</div>

<div class="price">₹300 <small>/month</small></div>

<div class="pkr">Rs. 865/month</div>

<ul>
<li>32GB RAM</li>
<li>1000% CPU</li>
<li>200GB SSD</li>
<li>Java + Bedrock Support</li>
<li>Pterodactyl Panel</li>
<li>10 Backups</li>
<li>10 Databases</li>
<li>Priority Support</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>

</div>

</section>


<!-- ================= 🖥️ VPS PLANS ================= -->

<section id="vps">

<div class="section-head reveal">

<div class="mini">🖥️ VPS HOSTING</div>

<h2>
Powerful
<span style="color:#39ff88">Virtual Servers.</span>
</h2>

<p>
KVM 🖥️ VPS hosting with SSD storage, root access
and flexible resources for your projects.
</p>

</div>


<div class="plans-grid">


<div class="plan reveal">

<div class="plan-name">STARTER</div>

<div class="price">₹30 <small>/month</small></div>

<div class="pkr">Rs. 110/month</div>

<ul>
<li>2GB RAM</li>
<li>1 vCPU</li>
<li>25GB SSD</li>
<li>KVM</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">BASIC</div>

<div class="price">₹50 <small>/month</small></div>

<div class="pkr">Rs. 145/month</div>

<ul>
<li>4GB RAM</li>
<li>2 vCPU</li>
<li>40GB SSD</li>
<li>KVM</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">ADVANCED</div>

<div class="price">₹70 <small>/month</small></div>

<div class="pkr">Rs. 200/month</div>

<ul>
<li>6GB RAM</li>
<li>3 vCPU</li>
<li>60GB SSD</li>
<li>KVM</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal featured">

<div class="popular">POPULAR</div>

<div class="plan-name">PRO</div>

<div class="price">₹90 <small>/month</small></div>

<div class="pkr">Rs. 260/month</div>

<ul>
<li>8GB RAM</li>
<li>4 vCPU</li>
<li>80GB SSD</li>
<li>KVM</li>
<li>Pterodactyl Support</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">ELITE</div>

<div class="price">₹130 <small>/month</small></div>

<div class="pkr">Rs. 375/month</div>

<ul>
<li>12GB RAM</li>
<li>5 vCPU</li>
<li>100GB SSD</li>
<li>KVM</li>
<li>Pterodactyl</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">ULTRA</div>

<div class="price">₹170 <small>/month</small></div>

<div class="pkr">Rs. 490/month</div>

<ul>
<li>16GB RAM</li>
<li>6 vCPU</li>
<li>150GB SSD</li>
<li>KVM</li>
<li>Pterodactyl</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal">

<div class="plan-name">TITAN</div>

<div class="price">₹230 <small>/month</small></div>

<div class="pkr">Rs. 660/month</div>

<ul>
<li>24GB RAM</li>
<li>8 vCPU</li>
<li>200GB SSD</li>
<li>KVM</li>
<li>Pterodactyl</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>


<div class="plan reveal featured">

<div class="popular">MAX POWER</div>

<div class="plan-name">LEGEND</div>

<div class="price">₹300 <small>/month</small></div>

<div class="pkr">Rs. 865/month</div>

<ul>
<li>32GB RAM</li>
<li>10 vCPU</li>
<li>250GB SSD</li>
<li>KVM</li>
<li>Pterodactyl</li>
<li>Full Root</li>
</ul>

<a class="plan-btn"
href="https://discord.gg/JzaPaJWdA7"
target="_blank">Order Now</a>

</div>

</div>

</section>


<!-- ================= REVIEWS ================= -->

<section id="reviews">

<div class="section-head reveal">

<div class="mini">REVIEWS</div>

<h2>
Our Community
<span style="color:#39ff88">Feedback.</span>
</h2>

<p>
Customer feedback can be displayed here.
Replace the sample reviews with verified
MineHosting customer reviews.
</p>

</div>


<div class="reviews">

<div class="review reveal">
<div class="stars">⭐⭐⭐⭐⭐</div>
<div class="review-user">
<div class="avatar">🔥</div>
<div>
<strong>Aarav_Gamer</strong>
<small>⛏️ Minecraft SMP Owner</small>
</div>
</div>
</div>

<div class="review reveal">
<div class="stars">⭐⭐⭐⭐⭐</div>
<p>“Super cheap prices with high performance! ⚡ Setup took literally 1 minute via Discord support. 10/10 service.”</p>
<div class="review-user">
<div class="avatar">⚡</div>
<div>
<strong>ZeusPlayz</strong>
<small>Bedrock Server Host</small>
</div>
</div>
</div>

<div class="review reveal">
<div class="stars">⭐⭐⭐⭐⭐</div>
<p>“DDoS protection is insane! 🛡️ 🖥️ VPS root access is completely unlocked & Pterodactyl panel runs smooth.”</p>
<div class="review-user">
<div class="avatar">👑</div>
<div>
<strong>Rohan_Dev</strong>
<small>Network Admin</small>
</div>
</div>
</div>

</div>

</section>


<!-- ================= CTA ================= -->

<div class="cta reveal">

<h2>
Ready to
<span>Host?</span>
</h2>

<p>
Choose your ⛏️ Minecraft or 🖥️ VPS plan and join the
MineHosting community. Orders and support are
handled through our official Discord server.
</p>

<a
href="https://discord.gg/JzaPaJWdA7"
target="_blank"
class="btn btn-primary">
Join MineHosting Discord ↗
</a>

</div>


<!-- ================= FOOTER ================= -->

<footer>

© 2026
<span>MineHosting</span>.
All rights reserved.

<br><br>

⛏️ Minecraft is a trademark of Mojang Studios.
MineHosting is not affiliated with Mojang.

</footer>


<script>

/* ================= PARTICLES ================= */

const particles = document.getElementById("particles");

for(let i = 0; i < 90; i++){

const p = document.createElement("div");

p.className = "particle";

p.style.left =
Math.random() * 100 + "%";

p.style.animationDuration =
(7 + Math.random() * 15) + "s";

p.style.animationDelay =
(-Math.random() * 15) + "s";

p.style.opacity =
(0.15 + Math.random() * 0.5);

particles.appendChild(p);

}


/* ================= SCROLL ANIMATION ================= */

const observer =
new IntersectionObserver(

entries => {

entries.forEach(entry => {

if(entry.isIntersecting){

entry.target.classList.add("show");

}

});

},

{
threshold:0.12
}

);


document
.querySelectorAll(".reveal")
.forEach(el => observer.observe(el));


/* ================= MOUSE GLOW ================= */

document.addEventListener("mousemove", e => {

const x = e.clientX;
const y = e.clientY;

document.body.style.background =
`radial-gradient(
circle 350px at ${x}px ${y}px,
rgba(57,255,136,.035),
#020604 70%
)`;

});

</script>

</body>
</html>
"""


@app.route("/")

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=2000,
        debug=False
    )
