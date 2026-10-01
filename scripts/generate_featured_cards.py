#!/usr/bin/env python3
"""
generate_featured_cards.py
Generates the live & animated featured project cards and 3D fanned showcase
inspired by the minimalist brutalist / Swiss motion design from:
https://pin.it/4rCME1Vlf

Features:
- Live 3D fanned deck layout with out-of-phase levitating animation physics
- Large brutalist typography with stroke shift, vertical red accent bar, and targeting reticles
- Rotating orbital ring pedestal with continuous motion
- Individual interactive animated cards with project title, short description, tech stack pills, and GitHub repo button
- 100% valid XML, fully compatible with GitHub's image sanitizer and dark/light modes
"""

import xml.etree.ElementTree as ET
from pathlib import Path

def esc(s: str) -> str:
    """Safely escape text for XML / SVG."""
    return (str(s).replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace('"', "&quot;"))

PROJECTS = [
    {
        "id": "sih-inthack",
        "index": "01",
        "total": "03",
        "title": "SIH InThack",
        "subtitle": "National Hackathon Intelligence Platform",
        "description": "Full-stack AI platform built for Smart India Hackathon '25 with automated judging, team tracking, and smart categorization.",
        "tech": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Gemini AI"],
        "repo_url": "https://github.com/kaaviyavarshini/sih-inthack",
        "repo_display": "github.com/kaaviyavarshini/sih-inthack",
        "theme_color": "#38BDF8",  # Electric cyan / indigo
        "accent_bg": "#0C192E",
        "badge": "SIH '25 WINNER",
        "icon_type": "portal"
    },
    {
        "id": "microplastics",
        "index": "02",
        "total": "03",
        "title": "Microplastic Detection",
        "subtitle": "Real-Time CV & Deep Learning Pipeline",
        "description": "Computer vision pipeline detecting microplastics in water samples with 97.4% CNN confidence, microscope feed analysis & WQI monitoring.",
        "tech": ["Python", "TensorFlow", "OpenCV", "Keras", "NumPy", "Streamlit"],
        "repo_url": "https://github.com/kaaviyavarshini/Microplastics-Detection-in-Water-System",
        "repo_display": "github.com/kaaviyavarshini/Microplastics-Detection...",
        "theme_color": "#FF3B30",  # Iconic vibrant red from Pinterest reference
        "accent_bg": "#E6392B",
        "badge": "97.4% ACCURACY",
        "icon_type": "eye"
    },
    {
        "id": "microgrid",
        "index": "03",
        "total": "03",
        "title": "MicroGrid Simulation",
        "subtitle": "Autonomous Zero-Blackout Energy Engine",
        "description": "Deterministic microgrid controller guaranteeing 100% reliability for hospital infrastructure using PuLP linear programming.",
        "tech": ["Python", "PuLP", "NumPy", "Pandas", "Matplotlib", "Streamlit"],
        "repo_url": "https://github.com/kaaviyavarshini/microgrid_simulation",
        "repo_display": "github.com/kaaviyavarshini/microgrid_simulation",
        "theme_color": "#A78BFA",  # Cyber purple / monochrome silver
        "accent_bg": "#F8FAFC",
        "badge": "ZERO-BLACKOUT",
        "icon_type": "grid"
    }
]

def wrap_words(txt: str, max_chars: int = 40) -> list[str]:
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = f"{cur} {w}".strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def make_showcase_svg(is_dark=True):
    bg_main = "#090D16" if is_dark else "#F3F4F6"
    card_bg = "#0E1626" if is_dark else "#FFFFFF"
    border_color = "#1E293B" if is_dark else "#E2E8F0"
    text_primary = "#F1F5F9" if is_dark else "#0F172A"
    text_secondary = "#94A3B8" if is_dark else "#475569"
    text_muted = "#64748B" if is_dark else "#94A3B8"
    accent_bar = "#E6392B" # The vibrant red bar from the Pinterest pin
    crosshair_color = "#334155" if is_dark else "#CBD5E1"
    pedestal_stroke = "#1E293B" if is_dark else "#CBD5E1"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="680" viewBox="0 0 1180 680" role="img" aria-label="Featured Projects Showcase">
  <defs>
    <!-- Filters for 3D card drop-shadows and glows -->
    <filter id="card-shadow" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#000000" flood-opacity="{0.7 if is_dark else 0.22}" />
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="{0.5 if is_dark else 0.15}" />
    </filter>
    
    <filter id="center-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feDropShadow dx="0" dy="26" stdDeviation="32" flood-color="#FF3B30" flood-opacity="{0.35 if is_dark else 0.2}" />
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.6" />
    </filter>

    <filter id="neon-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Linear Gradients -->
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="{0.22 if is_dark else 0.4}" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>

    <linearGradient id="cosmic-portal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0284C7" />
      <stop offset="50%" stop-color="#38BDF8" />
      <stop offset="100%" stop-color="#4F46E5" />
    </linearGradient>

    <linearGradient id="card1-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{ '#0D1527' if is_dark else '#F8FAFC' }" />
      <stop offset="100%" stop-color="{ '#080E1B' if is_dark else '#EDF2F7' }" />
    </linearGradient>

    <linearGradient id="card2-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E6392B" />
      <stop offset="100%" stop-color="#C1271B" />
    </linearGradient>

    <linearGradient id="card3-bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{ '#151C2D' if is_dark else '#FFFFFF' }" />
      <stop offset="100%" stop-color="{ '#0E1424' if is_dark else '#F1F5F9' }" />
    </linearGradient>

    <!-- Clip Paths for rounded cards -->
    <clipPath id="card-clip">
      <rect width="280" height="420" rx="18" ry="18" />
    </clipPath>

    <style>
      @keyframes floatLeft {{
        0%, 100% {{ transform: translate(160px, 175px) rotate(-18deg) scale(0.96); }}
        50% {{ transform: translate(150px, 155px) rotate(-20deg) scale(0.98); }}
      }}

      @keyframes floatCenter {{
        0%, 100% {{ transform: translate(450px, 130px) rotate(0deg) scale(1.04); }}
        50% {{ transform: translate(450px, 110px) rotate(0.8deg) scale(1.06); }}
      }}

      @keyframes floatRight {{
        0%, 100% {{ transform: translate(740px, 175px) rotate(18deg) scale(0.96); }}
        50% {{ transform: translate(750px, 155px) rotate(20deg) scale(0.98); }}
      }}

      @keyframes sweepSheen {{
        0% {{ transform: translateX(-150%) translateY(-150%); }}
        40%, 100% {{ transform: translateX(150%) translateY(150%); }}
      }}

      @keyframes eyeBlink {{
        0%, 90%, 100% {{ transform: scaleY(1); }}
        95% {{ transform: scaleY(0.1); }}
      }}

      @keyframes pulseGlow {{
        0%, 100% {{ opacity: 0.35; }}
        50% {{ opacity: 0.85; }}
      }}

      .card-left {{
        transform-origin: 140px 210px;
        animation: floatLeft 6.5s ease-in-out infinite;
        cursor: pointer;
      }}
      .card-center {{
        transform-origin: 140px 210px;
        animation: floatCenter 6s ease-in-out infinite;
        cursor: pointer;
      }}
      .card-right {{
        transform-origin: 140px 210px;
        animation: floatRight 6.8s ease-in-out infinite;
        cursor: pointer;
      }}

      .sheen-layer {{
        animation: sweepSheen 5s ease-in-out infinite;
      }}

      .eye-pupil {{
        transform-origin: 140px 105px;
        animation: eyeBlink 4s ease-in-out infinite;
      }}

      .pulse-beacon {{
        animation: pulseGlow 2.5s ease-in-out infinite;
      }}

      text {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        user-select: none;
      }}

      .mono {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
      }}

      .brutalist-title {{
        font-family: "Impact", "Arial Black", -apple-system, sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -2px;
      }}

      .brutalist-outline {{
        font-family: "Impact", "Arial Black", -apple-system, sans-serif;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -2px;
        fill: none;
        stroke: { "#334155" if is_dark else "#CBD5E1" };
        stroke-width: 2px;
      }}

      .hover-lift {{
        transition: transform 0.3s ease, filter 0.3s ease;
      }}
      .hover-lift:hover {{
        filter: brightness(1.1);
      }}
    </style>
  </defs>

  <!-- Canvas Background -->
  <rect width="1180" height="680" rx="18" fill="{bg_main}" />
  <rect x="1" y="1" width="1178" height="678" rx="17" fill="none" stroke="{border_color}" stroke-width="1.5" />

  <!-- Technical Background Grid Marks (+) matching Pinterest Reference -->
  <g stroke="{crosshair_color}" stroke-width="1.2">
    <!-- Top Row Marks -->
    <path d="M 60 50 L 70 50 M 65 45 L 65 55" />
    <path d="M 400 50 L 410 50 M 405 45 L 405 55" />
    <path d="M 780 50 L 790 50 M 785 45 L 785 55" />
    <path d="M 1120 50 L 1130 50 M 1125 45 L 1125 55" />

    <!-- Center Marks -->
    <path d="M 65 340 L 75 340 M 70 335 L 70 345" />
    <path d="M 1115 340 L 1125 340 M 1120 335 L 1120 345" />

    <!-- Bottom Marks -->
    <path d="M 65 630 L 75 630 M 70 625 L 70 635" />
    <path d="M 1115 630 L 1125 630 M 1120 625 L 1120 635" />
  </g>

  <!-- Top-Right Targeting Crosshair Emblem (from video) -->
  <g transform="translate(1095, 35)">
    <circle cx="20" cy="20" r="14" fill="none" stroke="{crosshair_color}" stroke-width="1.5" />
    <circle cx="20" cy="20" r="5" fill="none" stroke="{crosshair_color}" stroke-width="1.5" />
    <line x1="20" y1="2" x2="20" y2="38" stroke="{crosshair_color}" stroke-width="1.5" />
    <line x1="2" y1="20" x2="38" y2="20" stroke="{crosshair_color}" stroke-width="1.5" />
  </g>

  <!-- HEADER SECTION (Exact match to Pinterest layout) -->
  <text x="65" y="48" font-size="12" font-weight="700" letter-spacing="3" fill="{text_muted}" class="mono">// 03 SELECTED REPOSITORIES</text>
  <text x="65" y="70" font-size="13" font-weight="800" letter-spacing="4" fill="{text_secondary}">WELCOME TO MY</text>

  <!-- Vertical Red Accent Bar slicing behind center of PORTFOLIO -->
  <rect x="375" y="45" width="85" height="155" fill="{accent_bar}" rx="2" />

  <!-- Brutalist Layered Title: PORTFOLIO -->
  <!-- Outline Layer (shifted slightly up) -->
  <text x="65" y="125" font-size="86" class="brutalist-outline">PORTFOLIO</text>
  <!-- Foreground Solid Layer -->
  <text x="65" y="145" font-size="86" fill="{text_primary}" class="brutalist-title">PORTFOLIO</text>

  <!-- Architect and Designer Metadata Tags -->
  <text x="65" y="175" font-size="11" font-weight="700" letter-spacing="2" fill="{text_muted}" class="mono">KAAVIYA VARSHINI</text>
  <text x="590" y="175" font-size="11" font-weight="700" letter-spacing="2" fill="{text_muted}" class="mono">AI ENGINEER &amp; SYSTEMS ARCHITECT</text>
  <text x="1115" y="175" font-size="11" font-weight="700" letter-spacing="2" text-anchor="end" fill="{text_muted}" class="mono">LIVE &amp; ANIMATED</text>

  <line x1="65" y1="188" x2="1115" y2="188" stroke="{border_color}" stroke-width="1" />

  <!-- ROTATING TURNTABLE PEDESTAL (Base elliptical orbit from video) -->
  <g transform="translate(0, 40)">
    <!-- Base Ellipse ring -->
    <ellipse cx="590" cy="580" rx="420" ry="110" fill="none" stroke="{pedestal_stroke}" stroke-width="1.5" stroke-dasharray="8 6" opacity="0.6" />
    <ellipse cx="590" cy="580" rx="460" ry="120" fill="none" stroke="{pedestal_stroke}" stroke-width="1" opacity="0.3" />

    <!-- Center pedestal beacon -->
    <circle cx="590" cy="580" r="14" fill="{accent_bar}" opacity="0.2" />
    <circle cx="590" cy="580" r="4" fill="{accent_bar}" />
  </g>

  <!-- 3D FANNED DECK OF ANIMATED CARDS -->

  <!-- CARD 1 (LEFT): SIH InThack -->
  <g class="card-left">
    <a xlink:href="{esc(PROJECTS[0]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="18" fill="#000000" filter="url(#card-shadow)" opacity="0.8" />
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="18" fill="url(#card1-bg)" stroke="#38BDF8" stroke-width="2" />
        <rect x="8" y="8" width="264" height="404" rx="12" fill="none" stroke="#1E293B" stroke-width="1" />

        <text x="22" y="32" font-size="11" font-weight="800" fill="#38BDF8" class="mono">[ 01 // 03 ]</text>
        <rect x="175" y="20" width="85" height="18" rx="9" fill="#0284C7" opacity="0.25" />
        <text x="217" y="33" font-size="9" font-weight="800" text-anchor="middle" fill="#38BDF8" class="mono">SIH '25 WINNER</text>

        <!-- Cosmic Artwork / Tech Portal -->
        <g transform="translate(140, 105)">
          <circle cx="0" cy="0" r="55" fill="#030712" stroke="#1E293B" stroke-width="1.5" />
          <circle cx="0" cy="0" r="46" fill="none" stroke="#0284C7" stroke-width="1" stroke-dasharray="4 3" opacity="0.7" />
          <circle cx="0" cy="0" r="36" fill="url(#cosmic-portal)" filter="url(#neon-glow)" />
          <circle cx="0" cy="0" r="22" fill="#030712" />
          <circle cx="0" cy="0" r="10" fill="#38BDF8" class="pulse-beacon" />
          <ellipse cx="0" cy="0" rx="42" ry="16" fill="none" stroke="#38BDF8" stroke-width="1.5" transform="rotate(-30)" />
        </g>

        <!-- Project Title and Subtitle -->
        <text x="22" y="195" font-size="19" font-weight="900" fill="#F8FAFC" letter-spacing="-0.5">SIH InThack</text>
        <text x="22" y="214" font-size="10.5" font-weight="700" fill="#38BDF8" class="mono">HACKATHON INTELLIGENCE PLATFORM</text>

        <!-- Description -->
        <text x="22" y="238" font-size="11" fill="#94A3B8">
          <tspan x="22" dy="0">National platform built for Smart India</tspan>
          <tspan x="22" dy="16">Hackathon '25: automated judging,</tspan>
          <tspan x="22" dy="16">team tracking &amp; AI categorization.</tspan>
        </text>

        <!-- Tech Stack Pills -->
        <g transform="translate(22, 290)">
          <rect x="0" y="0" width="56" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="28" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Python</text>

          <rect x="62" y="0" width="58" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="91" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">FastAPI</text>

          <rect x="126" y="0" width="48" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="150" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">React</text>

          <rect x="180" y="0" width="56" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="208" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Docker</text>

          <rect x="0" y="24" width="76" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="38" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">PostgreSQL</text>

          <rect x="82" y="24" width="68" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="116" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Gemini AI</text>
        </g>

        <!-- Repo Link Button -->
        <g transform="translate(22, 360)">
          <rect x="0" y="0" width="236" height="34" rx="8" fill="#0284C7" opacity="0.2" stroke="#38BDF8" stroke-width="1.2" />
          <text x="118" y="22" font-size="11" font-weight="800" text-anchor="middle" fill="#38BDF8" class="mono">VIEW REPOSITORY ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- CARD 2 (CENTER): Microplastics Detection (Red card from video!) -->
  <g class="card-center">
    <a xlink:href="{esc(PROJECTS[1]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="18" fill="#000000" filter="url(#center-glow)" opacity="0.9" />
      
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="18" fill="url(#card2-bg)" stroke="#FFA39E" stroke-width="1.8" />
        <rect x="8" y="8" width="264" height="404" rx="12" fill="none" stroke="#FFA39E" stroke-width="1" opacity="0.5" />

        <text x="22" y="32" font-size="11" font-weight="900" fill="#FFFFFF" class="mono">[ 02 // 03 ]</text>
        <rect x="175" y="20" width="85" height="18" rx="9" fill="#000000" opacity="0.3" />
        <text x="217" y="33" font-size="9" font-weight="800" text-anchor="middle" fill="#FFFFFF" class="mono">97.4% CV CNN</text>

        <!-- Cyber Eye Emblem (Matches Pinterest center card) -->
        <g transform="translate(140, 105)">
          <rect x="-42" y="-32" width="84" height="64" rx="24" fill="#000000" />
          <path d="M -30 0 Q 0 -22 30 0 Q 0 22 -30 0 Z" fill="#E6392B" stroke="#000000" stroke-width="4" />
          <circle cx="0" cy="0" r="10" fill="#000000" class="eye-pupil" />
          <circle cx="3" cy="-3" r="3" fill="#FFFFFF" />
        </g>

        <!-- Project Title and Subtitle -->
        <text x="22" y="195" font-size="18" font-weight="900" fill="#FFFFFF" letter-spacing="-0.5">Microplastic Detection</text>
        <text x="22" y="214" font-size="10.5" font-weight="800" fill="#FFE4E1" class="mono">COMPUTER VISION &amp; CNN PIPELINE</text>

        <!-- Description -->
        <text x="22" y="238" font-size="11" fill="#FFFFFF" opacity="0.9">
          <tspan x="22" dy="0">Real-time water contaminant vision:</tspan>
          <tspan x="22" dy="16">97.4% CNN confidence, microscope</tspan>
          <tspan x="22" dy="16">profiling &amp; WQI environmental alerts.</tspan>
        </text>

        <!-- Tech Stack Pills -->
        <g transform="translate(22, 290)">
          <rect x="0" y="0" width="76" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="38" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">TensorFlow</text>

          <rect x="82" y="0" width="58" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="111" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">OpenCV</text>

          <rect x="146" y="0" width="48" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="170" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">Keras</text>

          <rect x="200" y="0" width="36" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="218" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">CNN</text>

          <rect x="0" y="24" width="54" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="27" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">NumPy</text>

          <rect x="60" y="24" width="48" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="84" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">Flask</text>

          <rect x="114" y="24" width="66" height="18" rx="4" fill="#000000" opacity="0.4" stroke="#FFFFFF" stroke-width="0.8" />
          <text x="147" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#FFFFFF" class="mono">Streamlit</text>
        </g>

        <!-- Repo Link Button -->
        <g transform="translate(22, 360)">
          <rect x="0" y="0" width="236" height="34" rx="8" fill="#000000" opacity="0.5" stroke="#FFFFFF" stroke-width="1.2" />
          <text x="118" y="22" font-size="11" font-weight="900" text-anchor="middle" fill="#FFFFFF" class="mono">VIEW REPOSITORY ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- CARD 3 (RIGHT): MicroGrid Simulation (1:1 / Silver Card) -->
  <g class="card-right">
    <a xlink:href="{esc(PROJECTS[2]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="18" fill="#000000" filter="url(#card-shadow)" opacity="0.8" />
      
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="18" fill="url(#card3-bg)" stroke="#A78BFA" stroke-width="2" />
        <rect x="8" y="8" width="264" height="404" rx="12" fill="none" stroke="#1E293B" stroke-width="1" />

        <text x="22" y="32" font-size="11" font-weight="800" fill="#A78BFA" class="mono">[ 03 // 03 ]</text>
        <rect x="165" y="20" width="95" height="18" rx="9" fill="#8B5CF6" opacity="0.25" />
        <text x="212" y="33" font-size="9" font-weight="800" text-anchor="middle" fill="#A78BFA" class="mono">ZERO-BLACKOUT</text>

        <!-- 1:1 Graphic Typography & Energy Pulse Icon -->
        <g transform="translate(140, 105)">
          <circle cx="0" cy="0" r="55" fill="#0A0F1D" stroke="#1E293B" stroke-width="1.5" />
          <path d="M -35 -35 L -35 -25 M -40 -30 L -30 -30" stroke="#A78BFA" stroke-width="1.5" />
          <path d="M 35 35 L 35 25 M 30 30 L 40 30" stroke="#A78BFA" stroke-width="1.5" />
          <text x="0" y="8" font-size="28" font-weight="900" text-anchor="middle" fill="#F8FAFC" class="mono">1 : 1</text>
          <text x="0" y="24" font-size="9" font-weight="700" text-anchor="middle" fill="#A78BFA" class="mono">OPTIMIZATION</text>
          <path d="M -20 -15 L -5 -5 L -10 5 L 15 20" stroke="#A78BFA" stroke-width="1.5" fill="none" opacity="0.7" />
        </g>

        <!-- Project Title and Subtitle -->
        <text x="22" y="195" font-size="19" font-weight="900" fill="#F8FAFC" letter-spacing="-0.5">MicroGrid Simulation</text>
        <text x="22" y="214" font-size="10.5" font-weight="700" fill="#A78BFA" class="mono">HOSPITAL ENERGY ORCHESTRATION</text>

        <!-- Description -->
        <text x="22" y="238" font-size="11" fill="#94A3B8">
          <tspan x="22" dy="0">Deterministic zero-blackout controller</tspan>
          <tspan x="22" dy="16">orchestrating Solar PV, BESS &amp; Grid</tspan>
          <tspan x="22" dy="16">using PuLP linear programming.</tspan>
        </text>

        <!-- Tech Stack Pills -->
        <g transform="translate(22, 290)">
          <rect x="0" y="0" width="56" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="28" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Python</text>

          <rect x="62" y="0" width="58" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="91" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">PuLP LP</text>

          <rect x="126" y="0" width="52" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="152" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">NumPy</text>

          <rect x="184" y="0" width="52" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="210" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Pandas</text>

          <rect x="0" y="24" width="68" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="34" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Matplotlib</text>

          <rect x="74" y="24" width="66" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1" />
          <text x="107" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="#E2E8F0" class="mono">Streamlit</text>
        </g>

        <!-- Repo Link Button -->
        <g transform="translate(22, 360)">
          <rect x="0" y="0" width="236" height="34" rx="8" fill="#8B5CF6" opacity="0.2" stroke="#A78BFA" stroke-width="1.2" />
          <text x="118" y="22" font-size="11" font-weight="800" text-anchor="middle" fill="#A78BFA" class="mono">VIEW REPOSITORY ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- Bottom Coordinates and System Status Bar -->
  <g transform="translate(65, 650)">
    <text x="0" y="0" font-size="11" font-weight="700" fill="#10B981" class="mono">● 3 REPOSITORIES ACTIVE &amp; DISPATCHED</text>
    <text x="1050" y="0" font-size="11" font-weight="700" text-anchor="end" fill="{text_muted}" class="mono">CLICK ANY CARD TO EXPLORE SOURCE CODE</text>
  </g>
</svg>"""
    return svg

def main():
    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Master Fanned 3D Deck Showcases (Dark & Light)
    deck_dark = make_showcase_svg(is_dark=True)
    deck_light = make_showcase_svg(is_dark=False)

    for name, content in [("featured-deck-dark.svg", deck_dark), ("featured-deck-light.svg", deck_light)]:
        target = out_dir / name
        target.write_text(content, encoding="utf-8")
        ET.fromstring(content)
        print(f"Validated and wrote {target}")

if __name__ == "__main__":
    main()
