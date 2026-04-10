import streamlit as st
import streamlit.components.v1 as components

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Intelli-Credit | Credit Decision Intelligence",
    page_icon="image-removebg-preview (3).png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit branding and default menu
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove default padding and margins */
    .main > div {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Fix for Streamlit's default padding */
    .css-18e3th9 {
        padding: 0 !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #0b1220;
    }
    
    /* Font Awesome for sidebar */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
</style>
""", unsafe_allow_html=True)

# Landing page — enterprise-grade presentation
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Critical Libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <!-- Google Fonts — IBM Plex Sans (enterprise UI) -->
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg: #0b1220;
            --bg-elevated: #111827;
            --surface: rgba(255, 255, 255, 0.04);
            --accent: #0ea5e9;
            --accent-2: #4f46e5;
            --accent-soft: rgba(14, 165, 233, 0.14);
            --border: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(14, 165, 233, 0.35);
            --text: #f1f5f9;
            --text-muted: #94a3b8;
            --radius-lg: 14px;
            --radius-pill: 999px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'IBM Plex Sans', system-ui, -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        /* ===== LOADER ===== */
        .loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            transition: opacity 0.6s ease, visibility 0.6s ease;
        }

        .loader-content {
            text-align: center;
        }

        .loader-text {
            font-size: 1.25rem;
            font-weight: 600;
            letter-spacing: 0.04em;
            color: var(--text);
            margin-bottom: 1rem;
        }

        .loader-bar {
            width: 200px;
            height: 2px;
            background: var(--border);
            border-radius: 2px;
            overflow: hidden;
        }

        .loader-progress {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            animation: load 1.1s ease forwards;
        }

        @keyframes load {
            0% { width: 0%; }
            100% { width: 100%; }
        }

        /* ===== NAVIGATION ===== */
        .navbar {
            position: fixed;
            top: 16px;
            left: 50%;
            transform: translateX(-50%);
            width: min(1120px, 92%);
            padding: 14px 28px;
            background: rgba(11, 18, 32, 0.88);
            backdrop-filter: blur(10px);
            border-radius: var(--radius-lg);
            border: 1px solid var(--border);
            z-index: 1000;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.25s ease;
        }

        .navbar.scrolled {
            top: 10px;
            background: rgba(11, 18, 32, 0.96);
            border-color: var(--border-accent);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
        }

        .logo {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text);
        }

        .nav-menu {
            display: flex;
            gap: 40px;
            list-style: none;
        }

        .nav-menu li a {
            color: #FFFFFF;
            text-decoration: none;
            font-weight: 500;
            font-size: 16px;
            position: relative;
            padding: 5px 0;
        }

        .nav-menu li a::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--accent);
            transition: width 0.25s ease;
        }

        .nav-menu li a:hover::after {
            width: 100%;
        }

        .nav-menu li a:hover {
            color: var(--accent);
        }

        .nav-button {
            background: var(--accent);
            color: #0b1220;
            border: none;
            padding: 10px 22px;
            border-radius: var(--radius-pill);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
        }

        .nav-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.35);
            background: #38bdf8;
        }

        /* ===== PROGRESS BAR ===== */
        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 0%;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            z-index: 1001;
            transition: width 0.1s;
        }

        /* ===== HERO SECTION ===== */
        .hero {
            min-height: 85vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
            padding: 0 5%;
        }

        .hero-background {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .hero-gradient {
            position: absolute;
            top: -50%;
            right: -20%;
            width: 80%;
            height: 80%;
            background: radial-gradient(circle, rgba(14, 165, 233, 0.08) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(60px);
            animation: float 10s ease-in-out infinite;
        }

        .hero-gradient-2 {
            position: absolute;
            bottom: -30%;
            left: -10%;
            width: 60%;
            height: 60%;
            background: radial-gradient(circle, rgba(79, 70, 229, 0.07) 0%, transparent 70%);
            border-radius: 50%;
            filter: blur(60px);
            animation: float 15s ease-in-out infinite reverse;
        }

        .hero-content {
            max-width: 800px;
            z-index: 2;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--accent-soft);
            border: 1px solid var(--border-accent);
            color: var(--accent);
            padding: 0.5rem 1rem;
            border-radius: var(--radius-pill);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 1.5rem;
        }

        .hero-title {
            font-size: clamp(2.25rem, 5vw, 3.5rem);
            font-weight: 600;
            letter-spacing: -0.03em;
            line-height: 1.12;
            margin-bottom: 1.5rem;
            color: var(--text);
        }

        .hero-title span {
            color: var(--accent);
            display: inline;
        }

        .hero-description {
            font-size: 1.0625rem;
            color: var(--text-muted);
            line-height: 1.65;
            margin-bottom: 2rem;
            max-width: 36rem;
        }

        .hero-stats {
            display: flex;
            gap: 60px;
            margin-bottom: 50px;
        }

        .stat-item {
            text-align: left;
        }

        .stat-number {
            font-size: 2rem;
            font-weight: 600;
            color: var(--text);
            line-height: 1;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.35rem;
        }

        .hero-cta {
            display: flex;
            gap: 20px;
        }

        .btn-primary {
            background: var(--accent);
            color: #0b1220;
            padding: 0.875rem 1.75rem;
            border-radius: var(--radius-pill);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9375rem;
            transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
            border: none;
            cursor: pointer;
        }

        .btn-primary:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 28px rgba(14, 165, 233, 0.35);
            background: #38bdf8;
        }

        .btn-secondary {
            background: transparent;
            color: var(--text);
            padding: 0.875rem 1.75rem;
            border-radius: var(--radius-pill);
            text-decoration: none;
            font-weight: 600;
            border: 1px solid var(--border-accent);
            transition: all 0.2s;
            cursor: pointer;
            font-size: 0.9375rem;
        }

        .btn-secondary:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
            transform: translateY(-1px);
        }

        /* ===== 3D CARD ===== */
        .hero-visual {
            position: absolute;
            right: 5%;
            top: 50%;
            transform: translateY(-50%);
            width: 500px;
            height: 500px;
            perspective: 1000px;
        }

        .floating-card {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: float 6s ease-in-out infinite;
            transition: transform 0.6s;
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            background: linear-gradient(145deg, var(--surface), rgba(14, 165, 233, 0.06));
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-lg);
            backdrop-filter: blur(10px);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 20px;
            backface-visibility: hidden;
            box-shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
        }

        .card-face i {
            font-size: 3rem;
            color: var(--accent);
        }

        .card-face h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text);
        }

        .card-face p {
            color: var(--text-muted);
        }

        .card-front {
            transform: translateZ(20px);
        }

        .card-back {
            transform: rotateY(180deg) translateZ(20px);
        }

        .floating-card:hover {
            transform: rotateY(180deg);
        }

        /* ===== FEATURES SECTION ===== */
        .features {
            padding: 100px 5%;
            background: var(--bg-elevated);
            position: relative;
            overflow: hidden;
        }

        .section-header {
            text-align: center;
            margin-bottom: 80px;
        }

        .section-badge {
            display: inline-block;
            background: var(--accent-soft);
            border: 1px solid var(--border-accent);
            color: var(--accent);
            padding: 0.5rem 1rem;
            border-radius: var(--radius-pill);
            font-size: 0.6875rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .section-title {
            font-size: clamp(1.75rem, 3vw, 2.25rem);
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 0.75rem;
            color: var(--text);
        }

        .section-subtitle {
            font-size: 1rem;
            color: var(--text-muted);
            max-width: 36rem;
            margin: 0 auto;
            line-height: 1.6;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }

        .feature-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.75rem 1.5rem;
            transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
            position: relative;
            overflow: hidden;
        }

        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), var(--accent-2));
            transform: translateX(-100%);
            transition: transform 0.35s ease;
        }

        .feature-card:hover::before {
            transform: translateX(0);
        }

        .feature-card:hover {
            transform: translateY(-4px);
            border-color: var(--border-accent);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
        }

        .feature-icon {
            width: 48px;
            height: 48px;
            background: var(--accent-soft);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.25rem;
            font-size: 1.25rem;
            color: var(--accent);
        }

        .feature-title {
            font-size: 1.0625rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text);
        }

        .feature-desc {
            color: var(--text-muted);
            line-height: 1.55;
            font-size: 0.875rem;
        }

        /* ===== HOW IT WORKS ===== */
        .how-it-works {
            padding: 100px 5%;
            background: var(--bg);
        }

        .steps-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .step-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 2rem 1.75rem;
            text-align: center;
            position: relative;
        }

        .step-number {
            width: 48px;
            height: 48px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.125rem;
            font-weight: 600;
            margin: 0 auto 1.25rem;
            color: #0b1220;
        }

        .step-title {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text);
        }

        .step-desc {
            color: var(--text-muted);
            line-height: 1.6;
            font-size: 0.9375rem;
        }

        .step-connector {
            position: absolute;
            top: 50%;
            right: -20px;
            transform: translateY(-50%);
            font-size: 1rem;
            color: var(--text-muted);
        }

        /* ===== DEMO SECTION ===== */
        .demo-section {
            padding: 100px 5%;
            background: linear-gradient(180deg, var(--bg) 0%, var(--bg-elevated) 100%);
            position: relative;
            overflow: hidden;
        }

        .demo-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 60px;
            max-width: 1200px;
            margin: 0 auto;
            align-items: center;
        }

        .demo-content h2 {
            font-size: clamp(1.75rem, 3vw, 2.25rem);
            font-weight: 600;
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
            color: var(--text);
        }

        .demo-content p {
            font-size: 1rem;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 1.75rem;
        }

        .demo-features {
            list-style: none;
        }

        .demo-features li {
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--text);
            font-size: 0.9375rem;
        }

        .demo-features i {
            color: var(--accent);
            font-size: 1rem;
        }

        .demo-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 2rem 1.75rem;
            backdrop-filter: blur(10px);
        }

        .demo-card h3 {
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
            color: var(--text);
        }

        .demo-upload {
            border: 1px dashed var(--border-accent);
            border-radius: var(--radius-lg);
            padding: 2.5rem 1.5rem;
            text-align: center;
            transition: border-color 0.2s, background 0.2s;
            cursor: pointer;
        }

        .demo-upload-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .demo-upload-option h4 {
            color: var(--text);
            font-size: 0.9375rem;
            font-weight: 600;
            margin-bottom: 0.375rem;
        }

        .demo-upload:hover {
            border-color: var(--accent);
            background: var(--accent-soft);
        }

        .demo-upload i {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 1rem;
        }

        .demo-upload p {
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }

        .demo-upload-btn {
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 0.625rem 1.5rem;
            border-radius: var(--radius-pill);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .demo-upload-btn:hover {
            background: var(--accent);
            color: #0b1220;
        }

        /* ===== TEAM SECTION ===== */
        .team-section {
            padding: 100px 5%;
            background: var(--bg-elevated);
        }

        .team-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .team-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 1.75rem 1.25rem;
            text-align: center;
            transition: border-color 0.2s, transform 0.2s;
        }

        .team-card:hover {
            transform: translateY(-3px);
            border-color: var(--border-accent);
        }

        .team-image {
            width: 88px;
            height: 88px;
            background: var(--accent-soft);
            border: 1px solid var(--border-accent);
            border-radius: 50%;
            margin: 0 auto 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.75rem;
            color: var(--accent);
        }

        .team-name {
            font-size: 1.0625rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            color: var(--text);
        }

        .team-role {
            color: var(--text-muted);
            font-size: 0.8125rem;
            margin-bottom: 1rem;
        }

        .team-social {
            display: flex;
            gap: 15px;
            justify-content: center;
        }

        .team-social a {
            color: var(--text-muted);
            transition: color 0.2s;
        }

        .team-social a:hover {
            color: var(--accent);
        }

        /* ===== FOOTER ===== */
        .footer {
            background: var(--bg);
            padding: 80px 5% 30px;
            border-top: 1px solid var(--border);
        }

        .footer-content {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 60px;
            max-width: 1200px;
            margin: 0 auto 60px;
        }

        .footer-logo {
            font-size: 1.125rem;
            font-weight: 600;
            letter-spacing: -0.02em;
            color: var(--text);
            margin-bottom: 1rem;
        }

        .footer-about {
            color: var(--text-muted);
            line-height: 1.6;
            font-size: 0.9375rem;
            margin-bottom: 1.25rem;
        }

        .footer-social {
            display: flex;
            gap: 20px;
        }

        .footer-social a {
            color: var(--text-muted);
            font-size: 1.125rem;
            transition: color 0.2s;
        }

        .footer-social a:hover {
            color: var(--accent);
        }

        .footer-links h4 {
            margin-bottom: 20px;
            font-size: 0.9375rem;
            font-weight: 600;
            color: var(--text);
        }

        .footer-links ul {
            list-style: none;
        }

        .footer-links ul li {
            margin-bottom: 10px;
        }

        .footer-links ul li a {
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.2s;
            font-size: 0.9375rem;
        }

        .footer-links ul li a:hover {
            color: var(--accent);
        }

        .footer-bottom {
            text-align: center;
            padding-top: 1.75rem;
            border-top: 1px solid var(--border);
            color: var(--text-muted);
            font-size: 0.8125rem;
        }

        /* ===== TOAST (replaces alert) ===== */
        .toast {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%) translateY(120%);
            max-width: 26rem;
            padding: 1rem 1.25rem;
            background: var(--bg-elevated);
            border: 1px solid var(--border-accent);
            border-radius: var(--radius-lg);
            color: var(--text);
            font-size: 0.875rem;
            line-height: 1.5;
            z-index: 20000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.35s ease, transform 0.35s ease;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45);
        }

        .toast.show {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }

        .toast strong {
            display: block;
            font-weight: 600;
            margin-bottom: 0.35rem;
            color: var(--text);
        }

        .toast .toast-sub {
            display: block;
            margin-top: 0.35rem;
            color: var(--text-muted);
            font-size: 0.8125rem;
            font-weight: 400;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1200px) {
            .hero-title { font-size: 56px; }
            .hero-visual { width: 400px; height: 400px; }
            .features-grid { grid-template-columns: repeat(2, 1fr); }
            .team-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 768px) {
            .navbar { padding: 15px 20px; }
            .nav-menu { display: none; }
            .hero-title { font-size: 42px; }
            .hero-visual { display: none; }
            .features-grid { grid-template-columns: 1fr; }
            .steps-container { grid-template-columns: 1fr; }
            .team-grid { grid-template-columns: 1fr; }
            .demo-container { grid-template-columns: 1fr; }
            .demo-upload-grid { grid-template-columns: 1fr; }
            .footer-content { grid-template-columns: 1fr; }
            .hero-stats { flex-direction: column; gap: 30px; }
        }
    </style>
</head>
<body>
    <!-- Loader -->
    <div class="loader" id="loader">
        <div class="loader-content">
            <div class="loader-text">Intelli-Credit</div>
            <div class="loader-bar">
                <div class="loader-progress"></div>
            </div>
        </div>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar" id="progressBar"></div>

    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="logo">Intelli-Credit</div>
        <ul class="nav-menu">
            <li><a href="#home">Home</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#how-it-works">Process</a></li>
            <li><a href="#demo">Demo</a></li>
            <li><a href="#team">Team</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
        <button class="nav-button" onclick="document.querySelector('#demo').scrollIntoView({behavior: 'smooth'})">
            Book demo
        </button>
    </nav>

    <!-- Hero Section -->
    <section class="hero" id="home">
        <div class="hero-background">
            <div class="hero-gradient"></div>
            <div class="hero-gradient-2"></div>
        </div>
        
        <div class="hero-content">
            <div class="hero-badge"><i class="fas fa-shield-alt" style="font-size:0.7rem;"></i> Enterprise credit intelligence</div>
            <h1 class="hero-title">
                Bridge the <span>intelligence gap</span> in corporate lending
            </h1>
            <p class="hero-description">
                AI-powered platform that automates end-to-end credit assessment, ingesting multi-source data and delivering explainable recommendations in minutes.
            </p>
            
            <div class="hero-stats">
                <div class="stat-item">
                    <div class="stat-number">10x</div>
                    <div class="stat-label">Faster Processing</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">99.9%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">Availability</div>
                </div>
            </div>
            
            <div class="hero-cta">
                <button class="btn-primary" onclick="document.querySelector('#demo').scrollIntoView({behavior: 'smooth'})">
                    View live demo
                </button>
                <button class="btn-secondary" onclick="document.querySelector('#features').scrollIntoView({behavior: 'smooth'})">
                    Explore capabilities
                </button>
            </div>
        </div>
        
        <div class="hero-visual">
            <div class="floating-card">
                <div class="card-face card-front">
                    <i class="fas fa-chart-line"></i>
                    <h3>AI-Powered</h3>
                    <p>Real-time Analysis</p>
                </div>
                <div class="card-face card-back">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Secure</h3>
                    <p>Bank-Grade Security</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features" id="features">
        <div class="section-header">
            <div class="section-badge">Platform capabilities</div>
            <h2 class="section-title">Everything you need in one workflow</h2>
            <p class="section-subtitle">Purpose-built tools for faster, more consistent credit assessment</p>
        </div>
        
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-file-invoice"></i></div>
                <h3 class="feature-title">Multi-format parsing</h3>
                <p class="feature-desc">Extract data from PDFs, scanned docs, Excel, GST returns, and bank statements automatically</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-search"></i></div>
                <h3 class="feature-title">Research agent</h3>
                <p class="feature-desc">Scans news, MCA filings, e-Courts, and sector trends for early warning signals</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-brain"></i></div>
                <h3 class="feature-title">Explainable AI</h3>
                <p class="feature-desc">Every decision comes with a clear reason - no black boxes, complete transparency</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-landmark"></i></div>
                <h3 class="feature-title">India-first</h3>
                <p class="feature-desc">Built for GST, MCA, CIBIL, and Indian accounting standards</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-project-diagram"></i></div>
                <h3 class="feature-title">Circular trading detection</h3>
                <p class="feature-desc">Identifies revenue inflation and round-tripping between vendors</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-file-signature"></i></div>
                <h3 class="feature-title">CAM generator</h3>
                <p class="feature-desc">Professional Credit Appraisal Memo with Five Cs of Credit analysis</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-balance-scale"></i></div>
                <h3 class="feature-title">Legal risk detection</h3>
                <p class="feature-desc">Scans e-Courts and MCA for litigation, defaults, and director disqualifications</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon"><i class="fas fa-chart-line"></i></div>
                <h3 class="feature-title">Sentiment analysis</h3>
                <p class="feature-desc">Analyzes news and social media for promoter and sector sentiment</p>
            </div>
        </div>
    </section>

    <!-- How It Works -->
    <section class="how-it-works" id="how-it-works">
        <div class="section-header">
            <div class="section-badge">How it works</div>
            <h2 class="section-title">From documents to decision-ready output</h2>
            <p class="section-subtitle">A clear, repeatable process your credit team can trust</p>
        </div>
        
        <div class="steps-container">
            <div class="step-card">
                <div class="step-number">1</div>
                <h3 class="step-title">Ingest Data</h3>
                <p class="step-desc">Upload annual reports, GST filings, bank statements, and legal notices. Our AI parses everything automatically.</p>
                <div class="step-connector">→</div>
            </div>
            
            <div class="step-card">
                <div class="step-number">2</div>
                <h3 class="step-title">Analyze & Research</h3>
                <p class="step-desc">AI cross-references data, scans web for news, and detects early warning signals in minutes.</p>
                <div class="step-connector">→</div>
            </div>
            
            <div class="step-card">
                <div class="step-number">3</div>
                <h3 class="step-title">Get Recommendation</h3>
                <p class="step-desc">Receive explainable risk score, loan limit, interest rate, and complete Credit Appraisal Memo.</p>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section class="demo-section" id="demo">
        <div class="demo-container">
            <div class="demo-content">
                <div class="section-badge">Interactive demo</div>
                <h2>Evaluate the workflow</h2>
                <p>Upload sample documents to simulate parsing, risk signals, and structured credit outputs.</p>
                
                <ul class="demo-features">
                    <li><i class="fas fa-check-circle"></i> Real-time analysis</li>
                    <li><i class="fas fa-check-circle"></i> Risk score calculation</li>
                    <li><i class="fas fa-check-circle"></i> Circular trading detection</li>
                    <li><i class="fas fa-check-circle"></i> Complete CAM generation</li>
                </ul>
            </div>
            
            <div class="demo-card">
                <h3>Upload Documents</h3>
                <div class="demo-upload-grid">
                    <div class="demo-upload demo-upload-option" onclick="document.getElementById('gstInput').click()">
                        <i class="fas fa-file-invoice"></i>
                        <h4>GST Returns</h4>
                        <p>Upload GSTR files and sales summaries</p>
                        <p style="font-size: 12px;">Supports: PDF, Excel</p>
                        <input type="file" id="gstInput" style="display: none;" multiple accept=".pdf,.xls,.xlsx,.csv">
                    </div>
                    <div class="demo-upload demo-upload-option" onclick="document.getElementById('bankInput').click()">
                        <i class="fas fa-university"></i>
                        <h4>Bank Statements</h4>
                        <p>Upload account statements for cash-flow checks</p>
                        <p style="font-size: 12px;">Supports: PDF, Excel, CSV</p>
                        <input type="file" id="bankInput" style="display: none;" multiple accept=".pdf,.xls,.xlsx,.csv">
                    </div>
                </div>
                <div style="margin-top: 1rem; text-align: center;">
                    <button class="demo-upload-btn" onclick="simulateAnalysis()">
                        Analyze Documents
                    </button>
                </div>
            </div>
        </div>
    </section>

    <!-- Team Section -->
    <section class="team-section" id="team">
        <div class="section-header">
            <div class="section-badge">Leadership</div>
            <h2 class="section-title">Built by credit and technology specialists</h2>
            <p class="section-subtitle">Experience across AI, risk, and Indian corporate lending</p>
        </div>
        
        <div class="team-grid">
            <div class="team-card">
                <div class="team-image"><i class="fas fa-user-tie"></i></div>
                <h3 class="team-name">Urmila</h3>
                <p class="team-role">AI Lead, Full Stack Developer, Data Scientist</p>
                <div class="team-social">
                    <a href="#"><i class="fab fa-linkedin"></i></a>
                    <a href="#"><i class="fab fa-twitter"></i></a>
                    <a href="#"><i class="fab fa-github"></i></a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer Section -->
    <footer class="footer" id="contact">
        <div class="footer-content">
            <div class="footer-links">
                <h4>Product</h4>
                <ul>
                    <li><a href="#features">Features</a></li>
                    <li><a href="#how-it-works">How it Works</a></li>
                    <li><a href="#demo">Demo</a></li>
                    <li><a href="#">Pricing</a></li>
                </ul>
            </div>
            
            <div class="footer-links">
                <h4>Company</h4>
                <ul>
                    <li><a href="#team">About Us</a></li>
                    <li><a href="#">Blog</a></li>
                    <li><a href="#">Careers</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div>
            
            <div class="footer-links">
                <h4>Contact</h4>
                <ul>
                    <li><i class="fas fa-envelope"></i> hello@intelli-credit.ai</li>

                </ul>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p>© 2025 Intelli-Credit. All rights reserved.</p>
        </div>
    </footer>

    <div id="toast" class="toast" role="status" aria-live="polite"></div>

    <!-- JavaScript -->
    <script>
        // Wait for DOM to be fully loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Hide loader after page load
            setTimeout(function() {
                const loader = document.getElementById('loader');
                if (loader) {
                    loader.style.opacity = '0';
                    loader.style.visibility = 'hidden';
                }
            }, 1100);

            // Navbar scroll effect
            window.addEventListener('scroll', function() {
                const navbar = document.getElementById('navbar');
                if (navbar) {
                    if (window.scrollY > 100) {
                        navbar.classList.add('scrolled');
                    } else {
                        navbar.classList.remove('scrolled');
                    }
                }
                
                // Progress bar
                const progressBar = document.getElementById('progressBar');
                if (progressBar) {
                    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                    const scrolled = (winScroll / height) * 100;
                    progressBar.style.width = scrolled + '%';
                }
            });

            // GSAP Animations - only if GSAP is loaded
            if (typeof gsap !== 'undefined') {
                gsap.registerPlugin(ScrollTrigger);

                // Hero animations
                gsap.from('.hero-content', {
                    scrollTrigger: {
                        trigger: '.hero',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    y: 100,
                    duration: 1.5,
                    ease: 'power3.out'
                });

                gsap.from('.hero-visual', {
                    scrollTrigger: {
                        trigger: '.hero',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    x: 100,
                    duration: 1.5,
                    delay: 0.5,
                    ease: 'power3.out'
                });

                // Feature cards stagger animation
                gsap.from('.feature-card', {
                    scrollTrigger: {
                        trigger: '#features',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    y: 50,
                    duration: 0.8,
                    stagger: 0.2,
                    ease: 'back.out(1.2)'
                });

                // Step cards animation
                gsap.from('.step-card', {
                    scrollTrigger: {
                        trigger: '#how-it-works',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    y: 50,
                    duration: 0.8,
                    stagger: 0.3,
                    ease: 'power3.out'
                });

                // Team cards animation
                gsap.from('.team-card', {
                    scrollTrigger: {
                        trigger: '#team',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    scale: 0.8,
                    duration: 0.8,
                    stagger: 0.2,
                    ease: 'back.out(1.2)'
                });

                // Demo section animation
                gsap.from('.demo-content', {
                    scrollTrigger: {
                        trigger: '#demo',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    x: -100,
                    duration: 1,
                    ease: 'power3.out'
                });

                gsap.from('.demo-card', {
                    scrollTrigger: {
                        trigger: '#demo',
                        start: 'top center',
                        toggleActions: 'play none none reverse'
                    },
                    opacity: 0,
                    x: 100,
                    duration: 1,
                    delay: 0.3,
                    ease: 'power3.out'
                });
            }

            // Smooth scroll for navigation
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });

            // Parallax effect on hero gradient
            window.addEventListener('scroll', () => {
                const scrolled = window.scrollY;
                const gradient1 = document.querySelector('.hero-gradient');
                const gradient2 = document.querySelector('.hero-gradient-2');
                
                if (gradient1 && gradient2) {
                    gradient1.style.transform = `translateY(${scrolled * 0.2}px)`;
                    gradient2.style.transform = `translateY(${-scrolled * 0.1}px)`;
                }
            });
        });

        function simulateAnalysis() {
            const t = document.getElementById('toast');
            if (!t) return;
            t.innerHTML = '<strong>Analysis complete</strong><span class="toast-sub">GST and bank data were parsed; circular-trade checks and risk scoring ran successfully. For full CAM output, use the main application.</span>';
            t.classList.add('show');
            window.clearTimeout(window.__demoToastTimer);
            window.__demoToastTimer = window.setTimeout(function() {
                t.classList.remove('show');
            }, 5000);
        }
    </script>
</body>
</html>
"""

# Render the HTML in Streamlit with appropriate height
components.html(html_code, height=1200, scrolling=True)

# Floating action button for quick demo
st.markdown("""
<div style="position: fixed; bottom: 24px; right: 24px; z-index: 10000;">
    <button onclick="window.scrollTo({top: document.querySelector('#demo').offsetTop, behavior: 'smooth'});" 
            style="background: #0ea5e9; 
                   color: #0b1220; 
                   border: none; 
                   padding: 12px 22px; 
                   border-radius: 999px; 
                   font-weight: 600;
                   font-size: 14px;
                   cursor: pointer;
                   box-shadow: 0 8px 24px rgba(14, 165, 233, 0.35);
                   transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
                   font-family: system-ui, sans-serif;"
                   onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 32px rgba(14, 165, 233, 0.45)'; this.style.background='#38bdf8';"
                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 24px rgba(14, 165, 233, 0.35)'; this.style.background='#0ea5e9';">
        Go to demo
    </button>
</div>

<script>
    // Function to scroll to demo section
    function scrollToDemo() {
        const demoSection = document.querySelector('#demo');
        if (demoSection) {
            demoSection.scrollIntoView({behavior: 'smooth'});
        }
    }
</script>
""", unsafe_allow_html=True)

# Sidebar with hackathon info
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #0A0F1E, #0F1526); border-radius: 20px; border: 1px solid #00E5FF20;">
        <h2 style="color: #00E5FF; margin-bottom: 10px;">🏆 HACKATHON</h2>
        <p style="color: #A0AEC0; font-size: 12px;">Intelli-Credit v2.0</p>
        <div style="margin: 20px 0;">
            <div style="background: rgba(0,229,255,0.1); border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                <p style="color: #00E5FF; font-size: 14px;"><i class="fas fa-clock"></i> Round 1 Submission</p>
            </div>
            <div style="background: rgba(124,58,237,0.1); border-radius: 10px; padding: 10px;">
                <p style="color: #7C3AED; font-size: 14px;"><i class="fas fa-calendar"></i> Due: March 10, 2024</p>
            </div>
        </div>
        <hr style="border-color: #00E5FF20; margin: 20px 0;">
        <p style="color: #A0AEC0; font-size: 12px;">Made with ❤️ for the Hackathon</p>
        <p style="color: #00E5FF; font-size: 10px;">© 2024 Intelli-Credit Team</p>
    </div>
    """, unsafe_allow_html=True)