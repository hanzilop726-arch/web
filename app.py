import hmac
import http.client
import ipaddress
import os
import secrets
import socket
import sqlite3
import ssl
import time
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template_string,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY") or secrets.token_hex(32),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1",
)

DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", Path(app.instance_path) / "status.db")
)
CHECK_INTERVAL = 60
MAX_SITES = 50
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

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

.brand-mark{
width:42px;
height:42px;
display:grid;
place-items:center;
background:rgba(57,255,136,.1);
border:1px solid rgba(57,255,136,.25);
border-radius:12px;
color:#39ff88;
font-size:23px;
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
display:grid;
place-items:center;
border:1px solid rgba(57,255,136,.3);
border-radius:30px;
background:rgba(57,255,136,.08);
color:#39ff88;
font-size:64px;
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
.brand-mark{filter:drop-shadow(0 0 10px rgba(57,255,136,.3))}
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
.nav-links a:not(.discord-btn):not(.status-link){display:none}
.nav-links{gap:10px}
.status-link{font-size:12px!important}

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
<span class="brand-mark" aria-hidden="true">⛏</span>
🎮 MINE<span>HOSTING</span>
</a>

<div class="nav-links">
<a href="#why">✨ Why Us</a>
<a href="#services">🛠️ Services</a>
<a href="#minecraft">⛏️ Minecraft</a>
<a href="#vps">🖥️ VPS</a>
<a href="#reviews">💬 Reviews</a>
<a class="status-link" href="/status">● Status</a>
<a class="discord-btn" href="https://discord.gg/JzaPaJWdA7" target="_blank">Discord ↗</a>
</div>
</nav>

<section class="hero" id="home">

<div class="hero-overlay"></div>

<div class="hero-content">

<div class="hero-logo" aria-hidden="true">⛏</div>

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

<a href="/status">Service Status</a> ·
<a href="/admin">Admin</a>

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


STATUS_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#07100c">
<title>Status — MineHosting</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:dark;--bg:#07100c;--panel:#0d1912;--line:#1c3425;--text:#eef7f0;--muted:#91a497;--green:#42e887;--red:#ff6677;--yellow:#f6c85f}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -20%,#163321 0,transparent 58%),var(--bg);color:var(--text);font:15px Inter,system-ui,sans-serif;min-height:100vh}
a{color:inherit;text-decoration:none}.wrap{width:min(920px,calc(100% - 36px));margin:auto}
header{height:76px;border-bottom:1px solid #ffffff0d;display:flex;align-items:center}.nav{display:flex;justify-content:space-between;align-items:center}
.brand{font-weight:800;letter-spacing:-.4px}.brand b{color:var(--green)}.nav-links{display:flex;gap:22px;color:var(--muted);font-size:13px;font-weight:600}.nav-links a:hover{color:var(--green)}
main{padding:74px 0 90px}.eyebrow{color:var(--green);font-size:11px;letter-spacing:2.5px;font-weight:800;text-transform:uppercase}
h1{font-size:clamp(34px,6vw,54px);letter-spacing:-2px;margin:12px 0}.intro{color:var(--muted);line-height:1.75;max-width:620px}
.summary{margin:34px 0 22px;padding:22px 24px;border:1px solid var(--line);border-radius:16px;background:linear-gradient(135deg,#102219,#0b1710);display:flex;align-items:center;gap:15px}
.summary-icon{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;background:#42e8871c;color:var(--green);font-size:19px}
.summary strong{display:block;font-size:15px}.summary small{display:block;color:var(--muted);margin-top:5px}
.summary.down .summary-icon{background:#ff66771a;color:var(--red)}.summary.degraded .summary-icon{background:#f6c85f1a;color:var(--yellow)}
.list{display:grid;gap:12px}.site{padding:19px 21px;border:1px solid var(--line);border-radius:14px;background:#0b1710;display:flex;align-items:center;justify-content:space-between;gap:18px;transition:border-color .2s}
.site:hover{border-color:#42e88766}.site h2{font-size:15px;margin:0 0 7px}.site-url{color:var(--muted);font-size:12px;overflow-wrap:anywhere}
.meta{display:flex;align-items:center;gap:14px;flex-shrink:0}.checked{font-size:11px;color:var(--muted);text-align:right}
.pill{display:inline-flex;align-items:center;gap:7px;border-radius:30px;padding:7px 10px;font-size:11px;font-weight:700;white-space:nowrap;background:#42e88714;color:var(--green)}
.pill:before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}.pill.down{background:#ff667714;color:var(--red)}.pill.unknown{background:#f6c85f14;color:var(--yellow)}
.empty{padding:44px 24px;border:1px dashed #294332;border-radius:15px;text-align:center;color:var(--muted);line-height:1.7}.empty strong{display:block;color:var(--text);margin-bottom:5px}
footer{border-top:1px solid #ffffff0d;padding:22px 0;color:#6e8275;font-size:11px}
@media(max-width:600px){main{padding:52px 0}.nav-links{gap:13px;font-size:12px}.site{align-items:flex-start;padding:17px}.meta{display:block;text-align:right}.checked{margin-top:8px}.pill{font-size:10px}}
</style>
</head>
<body>
<header><div class="wrap nav"><a class="brand" href="/">⛏ MINE<b>HOSTING</b></a><nav class="nav-links"><a href="/">Home</a><a href="/admin">Admin</a></nav></div></header>
<main class="wrap">
<div class="eyebrow">Live service monitoring</div>
<h1>System status</h1>
<p class="intro">A live overview of MineHosting services. Each service is checked automatically and refreshed every minute.</p>
{% if sites %}
  {% set online = sites|selectattr("status", "equalto", "up")|list|length %}
  {% set down = sites|selectattr("status", "equalto", "down")|list|length %}
  {% if down %}
    {% set overall = "down" if online == 0 else "degraded" %}
    {% set overall_text = "Some services are experiencing issues" if online else "Service disruption detected" %}
    {% set overall_icon = "!" %}
  {% else %}
    {% set overall = "" %}
    {% set overall_text = "All systems operational" %}
    {% set overall_icon = "✓" %}
  {% endif %}
  <div class="summary {{ overall }}"><div class="summary-icon">{{ overall_icon }}</div><div><strong>{{ overall_text }}</strong><small>{{ online }} of {{ sites|length }} services operational</small></div></div>
  <div class="list">
  {% for site in sites %}
    <article class="site">
      <div><h2>{{ site.name }}</h2><a class="site-url" href="{{ site.url }}" target="_blank" rel="noopener noreferrer">{{ site.url }}</a></div>
      <div class="meta"><span class="pill {{ 'down' if site.status == 'down' else 'unknown' if site.status == 'unknown' else '' }}">{{ 'Operational' if site.status == 'up' else 'Checking' if site.status == 'unknown' else 'Unavailable' }}</span><span class="checked">{% if site.checked_at %}{{ site.checked_at }} UTC{% else %}Not checked yet{% endif %}{% if site.response_ms is not none %}<br>{{ site.response_ms }} ms{% endif %}</span></div>
    </article>
  {% endfor %}
  </div>
{% else %}
  <div class="summary"><div class="summary-icon">i</div><div><strong>Monitoring is being set up</strong><small>No services have been added yet.</small></div></div>
  <div class="empty"><strong>No monitored services</strong>Come back soon for live updates.</div>
{% endif %}
</main>
<footer><div class="wrap">Status checks run once per minute. &copy; 2026 MineHosting</div></footer>
</body>
</html>
"""

ADMIN_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#07100c">
<title>{{ 'Admin login' if login else 'Manage services' }} — MineHosting</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:dark;--bg:#07100c;--panel:#0d1912;--line:#1c3425;--text:#eef7f0;--muted:#91a497;--green:#42e887;--red:#ff6677}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 50% -20%,#163321 0,transparent 58%),var(--bg);color:var(--text);font:14px Inter,system-ui,sans-serif;min-height:100vh}
a{color:inherit;text-decoration:none}.wrap{width:min(920px,calc(100% - 36px));margin:auto}header{height:76px;border-bottom:1px solid #ffffff0d;display:flex;align-items:center}
.nav{display:flex;align-items:center;justify-content:space-between}.brand{font-weight:800}.brand b{color:var(--green)}.nav-links{display:flex;align-items:center;gap:20px;color:var(--muted);font-size:12px}
main{padding:55px 0 80px}h1{font-size:32px;letter-spacing:-1px;margin:0 0 8px}p.sub{color:var(--muted);margin:0 0 28px}
.panel{background:#0b1710;border:1px solid var(--line);border-radius:16px;padding:24px;margin:18px 0}.panel h2{font-size:16px;margin:0 0 18px}
.grid{display:grid;grid-template-columns:1fr 1.4fr auto;align-items:end;gap:12px}.field label{display:block;color:#b8c8bc;font-size:12px;font-weight:600;margin:0 0 8px}
input{width:100%;height:44px;padding:0 13px;border:1px solid #284231;border-radius:9px;background:#07110b;color:var(--text);font:inherit;outline:none}
input:focus{border-color:var(--green);box-shadow:0 0 0 3px #42e88718}button,.button{border:0;border-radius:9px;background:var(--green);color:#06120a;font:700 12px Inter,system-ui,sans-serif;padding:0 17px;height:44px;cursor:pointer;white-space:nowrap}
button:hover,.button:hover{filter:brightness(1.08)}.button.secondary{height:36px;background:#14251a;color:#c9d7cd;border:1px solid var(--line)}
.flash{padding:12px 14px;border:1px solid #ff667755;border-radius:9px;background:#ff667710;color:#ff9ba6;margin:0 0 15px}
.pill{display:inline-flex;align-items:center;gap:7px;border-radius:30px;padding:7px 10px;font-size:11px;font-weight:700;white-space:nowrap;background:#42e88714;color:#42e887}
.pill:before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}.pill.down{background:#ff667714;color:#ff6677}
.table{display:grid;gap:10px}.row{display:flex;align-items:center;justify-content:space-between;gap:15px;padding:15px;background:#0d1b12;border:1px solid #1a3022;border-radius:11px}.row-info{min-width:0}.row-info strong{display:block;margin-bottom:5px}.row-info a{color:var(--muted);font-size:11px;overflow-wrap:anywhere}
.row-actions{display:flex;align-items:center;gap:10px;flex-shrink:0}.delete{background:#ff667718;color:#ff8793;border:1px solid #ff667733;height:35px;padding:0 12px}
.empty{color:var(--muted);padding:20px;text-align:center;border:1px dashed #294332;border-radius:10px}
.login{max-width:430px;margin:6vh auto}.login .field{margin:15px 0}.login button{width:100%;margin-top:7px}
@media(max-width:650px){.grid{grid-template-columns:1fr}.grid button{width:100%}.panel{padding:18px}.row{align-items:flex-start;flex-direction:column}.row-actions{width:100%;justify-content:space-between}.login{margin-top:2vh}}
</style>
</head>
<body>
<header><div class="wrap nav"><a class="brand" href="/">⛏ MINE<b>HOSTING</b></a><nav class="nav-links"><a href="/">Home</a><a href="/status">Public status</a>{% if not login %}<form method="post" action="/admin/logout"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><button class="button secondary" type="submit">Log out</button></form>{% endif %}</nav></div></header>
<main class="wrap">
{% for message in get_flashed_messages() %}<div class="flash">{{ message }}</div>{% endfor %}
{% if login %}
<section class="panel login"><h1>Admin sign in</h1><p class="sub">Sign in to manage monitored services.</p>
{% if not configured %}<div class="flash">Admin credentials are not configured. Set ADMIN_USERNAME and ADMIN_PASSWORD in the service environment.</div>{% endif %}
<form method="post" action="/admin/login">
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<div class="field"><label for="username">Username</label><input id="username" name="username" autocomplete="username" required maxlength="80"></div>
<div class="field"><label for="password">Password</label><input id="password" name="password" type="password" autocomplete="current-password" required></div>
<button type="submit" {% if not configured %}disabled{% endif %}>Sign in</button>
</form></section>
{% else %}
<h1>Manage monitored services</h1><p class="sub">Add websites to the public MineHosting status page.</p>
<section class="panel"><h2>Add a service</h2>
<form class="grid" method="post" action="/admin/sites/add">
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<div class="field"><label for="name">Site name</label><input id="name" name="name" maxlength="80" placeholder="Main Website" required></div>
<div class="field"><label for="url">Website URL</label><input id="url" name="url" type="url" maxlength="2048" placeholder="https://example.com" required></div>
<button type="submit">Add service</button>
</form></section>
<section class="panel"><h2>Monitored services ({{ sites|length }}/{{ max_sites }})</h2>
{% if sites %}<div class="table">{% for site in sites %}<article class="row"><div class="row-info"><strong>{{ site.name }}</strong><a href="{{ site.url }}" target="_blank" rel="noopener noreferrer">{{ site.url }}</a></div><div class="row-actions"><span class="pill {{ 'down' if site.status == 'down' else '' }}">{{ 'Operational' if site.status == 'up' else 'Unavailable' if site.status == 'down' else 'Waiting for first check' }}</span><form method="post" action="/admin/sites/{{ site.id }}/delete" onsubmit="return confirm('Remove this service from monitoring?')"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><button class="delete" type="submit">Remove</button></form></div></article>{% endfor %}</div>{% else %}<div class="empty">No services added yet.</div>{% endif %}
</section>
{% endif %}
</main>
</body>
</html>
"""


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@contextmanager
def database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """CREATE TABLE IF NOT EXISTS monitored_sites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'unknown',
            http_status INTEGER,
            response_ms INTEGER,
            checked_at REAL
        )"""
    )
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def validate_site_url(value):
    if not value or len(value) > 2048 or any(char.isspace() for char in value):
        raise ValueError("Enter a valid public HTTP or HTTPS website URL.")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Enter a valid public HTTP or HTTPS website URL.") from exc
    if (
        parsed.scheme not in ("http", "https")
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or port not in (None, 80 if parsed.scheme == "http" else 443)
    ):
        raise ValueError("Use a public website URL on standard HTTP or HTTPS.")
    try:
        hostname = hostname.encode("idna").decode("ascii").lower()
        address = ipaddress.ip_address(hostname.strip("[]"))
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("Private and reserved IP addresses cannot be monitored.")
    if hostname in ("localhost",) or hostname.endswith(".localhost"):
        raise ValueError("Local addresses cannot be monitored.")
    netloc = f"[{hostname}]" if ":" in hostname else hostname
    return urlunsplit((parsed.scheme, netloc, parsed.path or "/", parsed.query, ""))


def resolve_public_addresses(hostname, port):
    try:
        records = socket.getaddrinfo(
            hostname, port, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM
        )
    except OSError:
        return []
    addresses = list(dict.fromkeys(record[4][0] for record in records))
    if not addresses or any(
        not ipaddress.ip_address(address.split("%", 1)[0]).is_global
        for address in addresses
    ):
        return []
    return addresses


class PinnedHTTPConnection(http.client.HTTPConnection):
    def __init__(self, hostname, port, address):
        super().__init__(hostname, port, timeout=5)
        self.address = address

    def connect(self):
        self.sock = socket.create_connection((self.address, self.port), self.timeout)


class PinnedHTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, hostname, port, address):
        super().__init__(hostname, port, timeout=5, context=ssl.create_default_context())
        self.address = address

    def connect(self):
        raw_socket = socket.create_connection((self.address, self.port), self.timeout)
        self.sock = self._context.wrap_socket(raw_socket, server_hostname=self.host)


def check_site(url):
    parsed = urlsplit(url)
    hostname = parsed.hostname
    port = 443 if parsed.scheme == "https" else 80
    addresses = resolve_public_addresses(hostname, port)
    if not addresses:
        return "down", None, None
    path = parsed.path or "/"
    if parsed.query:
        path += f"?{parsed.query}"
    connection_type = PinnedHTTPSConnection if parsed.scheme == "https" else PinnedHTTPConnection
    start = time.monotonic()
    connection = connection_type(hostname, port, addresses[0])
    try:
        connection.request(
            "GET",
            path,
            headers={"User-Agent": "MineHosting-Status/1.0", "Connection": "close"},
        )
        response = connection.getresponse()
        response_status = response.status
        response.close()
        elapsed = round((time.monotonic() - start) * 1000)
        return ("up" if response_status < 400 else "down"), response_status, elapsed
    except (OSError, TimeoutError, ssl.SSLError, http.client.HTTPException, ValueError):
        return "down", None, round((time.monotonic() - start) * 1000)
    finally:
        connection.close()


def get_sites(check=False):
    with database() as db:
        sites = [dict(row) for row in db.execute("SELECT * FROM monitored_sites ORDER BY id")]
        if check:
            now = time.time()
            for site in sites:
                if site["checked_at"] is None or now - site["checked_at"] >= CHECK_INTERVAL:
                    status, http_status, response_ms = check_site(site["url"])
                    checked_at = time.time()
                    db.execute(
                        """UPDATE monitored_sites
                           SET status = ?, http_status = ?, response_ms = ?, checked_at = ?
                           WHERE id = ?""",
                        (status, http_status, response_ms, checked_at, site["id"]),
                    )
                    site.update(
                        status=status,
                        http_status=http_status,
                        response_ms=response_ms,
                        checked_at=checked_at,
                    )
    for site in sites:
        site["checked_at"] = (
            time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(site["checked_at"]))
            if site["checked_at"] is not None
            else None
        )
    return sites


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_authenticated"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


def verify_csrf():
    token = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    if not expected or not hmac.compare_digest(token, expected):
        abort(400)


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/status")
def status_page():
    return render_template_string(STATUS_HTML, sites=get_sites(check=True))


@app.route("/admin", methods=["GET"])
@admin_required
def admin_dashboard():
    return render_template_string(ADMIN_HTML, login=False, sites=get_sites(), max_sites=MAX_SITES)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    configured = bool(os.environ.get("ADMIN_USERNAME") and os.environ.get("ADMIN_PASSWORD"))
    if request.method == "POST":
        verify_csrf()
        username = os.environ.get("ADMIN_USERNAME", "")
        password = os.environ.get("ADMIN_PASSWORD", "")
        if (
            configured
            and hmac.compare_digest(request.form.get("username", ""), username)
            and hmac.compare_digest(request.form.get("password", ""), password)
        ):
            session.clear()
            session["admin_authenticated"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Invalid username or password.")
    return render_template_string(ADMIN_HTML, login=True, configured=configured)


@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():
    verify_csrf()
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin/sites/add", methods=["POST"])
@admin_required
def add_site():
    verify_csrf()
    name = request.form.get("name", "").strip()
    if not name or len(name) > 80:
        flash("Site name must be between 1 and 80 characters.")
        return redirect(url_for("admin_dashboard"))
    try:
        site_url = validate_site_url(request.form.get("url", "").strip())
    except ValueError as exc:
        flash(str(exc))
        return redirect(url_for("admin_dashboard"))
    with database() as db:
        count = db.execute("SELECT COUNT(*) FROM monitored_sites").fetchone()[0]
        if count >= MAX_SITES:
            flash(f"You can monitor up to {MAX_SITES} services.")
        else:
            db.execute("INSERT INTO monitored_sites (name, url) VALUES (?, ?)", (name, site_url))
            flash("Service added.")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/sites/<int:site_id>/delete", methods=["POST"])
@admin_required
def delete_site(site_id):
    verify_csrf()
    with database() as db:
        db.execute("DELETE FROM monitored_sites WHERE id = ?", (site_id,))
    flash("Service removed.")
    return redirect(url_for("admin_dashboard"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "2000")),
        debug=False
    )
