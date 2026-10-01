#!/usr/bin/env python3
"""
generate_featured_cards.py
Generates the live & animated featured project cards and 3D fanned showcase
matching the EXACT design language of the VISUAL.MAP:
- Pure black monochrome aesthetic (no red, no cyan, no purple - all black & silver/white)
- 1-bit dithered dotwork graphics (Serpentine Floyd-Steinberg dot styling)
- Terminal HUD telemetry, corner reticles (┌ ┐ └ ┘), and mono typography
- Live 3D fanned deck layout with out-of-phase levitation physics
"""

import math
import numpy as np
import xml.etree.ElementTree as ET
from pathlib import Path

def esc(s: str) -> str:
    """Safely escape text for XML / SVG."""
    return (str(s).replace("&", "&amp;")
                  .replace("<", "&lt;")
                  .replace(">", "&gt;")
                  .replace('"', "&quot;"))

def generate_eye_dither_points(center=(140, 110), rng=None):
    """Generate 1-bit dithered points for the cyber-optic vision eye."""
    if rng is None:
        rng = np.random.default_rng(42)
    cx, cy = center
    pts = []
    
    # Outer dithered eye contour
    for t in np.linspace(-math.pi, math.pi, 280):
        # Parametric eye shape
        r = 42 * (1 - 0.25 * math.sin(t)**2)
        px = cx + r * math.cos(t)
        py = cy + r * math.sin(t) * 0.55
        if rng.random() > 0.15:
            pts.append((px + rng.normal(0, 0.7), py + rng.normal(0, 0.7)))
            
    # Iris ring
    for r in np.linspace(6, 18, 5):
        n_dots = int(r * 5)
        for t in np.linspace(0, 2*math.pi, n_dots):
            if rng.random() > 0.2:
                pts.append((cx + r * math.cos(t) + rng.normal(0, 0.5), 
                            cy + r * math.sin(t) + rng.normal(0, 0.5)))
                
    # Center pupil core (dense)
    for _ in range(65):
        r = rng.uniform(0, 5)
        a = rng.uniform(0, 2*math.pi)
        pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
        
    # Scanning crosshair dots
    for x in np.linspace(cx - 52, cx + 52, 28):
        if abs(x - cx) > 18 and rng.random() > 0.25:
            pts.append((x, cy + rng.normal(0, 0.4)))
    for y in np.linspace(cy - 28, cy + 28, 16):
        if abs(y - cy) > 14 and rng.random() > 0.25:
            pts.append((cx + rng.normal(0, 0.4), y))
            
    return np.array(pts)

def generate_portal_dither_points(center=(140, 110), rng=None):
    """Generate 1-bit dithered points for the SIH AI intelligence portal."""
    if rng is None:
        rng = np.random.default_rng(101)
    cx, cy = center
    pts = []
    
    # Concentric orbital rings with dither diffusion
    radii = [10, 22, 34, 46, 56]
    for r in radii:
        n_dots = int(r * 6.5)
        for t in np.linspace(0, 2*math.pi, n_dots):
            if rng.random() > 0.25:
                pts.append((cx + r * math.cos(t) + rng.normal(0, 0.7),
                            cy + r * math.sin(t) + rng.normal(0, 0.7)))
                
    # Orbiting tilted electron ring
    for t in np.linspace(0, 2*math.pi, 140):
        if rng.random() > 0.2:
            x_raw = 48 * math.cos(t)
            y_raw = 16 * math.sin(t)
            # rotate -25 deg
            a = -0.45
            px = cx + x_raw * math.cos(a) - y_raw * math.sin(a)
            py = cy + x_raw * math.sin(a) + y_raw * math.cos(a)
            pts.append((px + rng.normal(0, 0.5), py + rng.normal(0, 0.5)))
            
    # Dense central singularity
    for _ in range(70):
        r = rng.uniform(0, 6)
        t = rng.uniform(0, 2*math.pi)
        pts.append((cx + r*math.cos(t), cy + r*math.sin(t)))
        
    return np.array(pts)

def generate_grid_dither_points(center=(140, 110), rng=None):
    """Generate 1-bit dithered points for the MicroGrid energy orchestration."""
    if rng is None:
        rng = np.random.default_rng(202)
    cx, cy = center
    pts = []
    
    # Outer square matrix
    for x in np.linspace(cx - 44, cx + 44, 28):
        for y in [cy - 44, cy + 44]:
            if rng.random() > 0.2:
                pts.append((x + rng.normal(0, 0.5), y + rng.normal(0, 0.5)))
    for y in np.linspace(cy - 44, cy + 44, 28):
        for x in [cx - 44, cx + 44]:
            if rng.random() > 0.2:
                pts.append((x + rng.normal(0, 0.5), y + rng.normal(0, 0.5)))
                
    # Diagonal circuit traces
    for t in np.linspace(-35, 35, 36):
        if abs(t) > 16 and rng.random() > 0.25:
            pts.append((cx + t, cy + t + rng.normal(0, 0.5)))
            pts.append((cx + t, cy - t + rng.normal(0, 0.5)))
            
    # Energy node clusters at corners and cardinal points
    nodes = [
        (cx - 32, cy - 32), (cx + 32, cy - 32),
        (cx - 32, cy + 32), (cx + 32, cy + 32),
        (cx, cy - 44), (cx, cy + 44),
        (cx - 44, cy), (cx + 44, cy)
    ]
    for nx, ny in nodes:
        for _ in range(16):
            r = rng.uniform(0, 4)
            a = rng.uniform(0, 2*math.pi)
            pts.append((nx + r*math.cos(a), ny + r*math.sin(a)))
            
    return np.array(pts)

def points_to_svg_path(pts):
    """Convert points to horizontal 1px dither segments M x y h 1 (exact visual map styling)."""
    return "".join(f"M{x:.1f} {y:.1f}h1" for x, y in pts)

PROJECTS = [
    {
        "id": "sih-inthack",
        "index": "01",
        "total": "03",
        "title": "SIH InThack",
        "spec": "300×340 / 1-BIT",
        "pts_label": "PTS 04820 · FS/SERPENTINE",
        "subtitle": "HACKATHON AI INTELLIGENCE PLATFORM",
        "description": "National platform built for Smart India Hackathon '25: automated judging, team tracking & AI categorization.",
        "tech": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Gemini AI"],
        "repo_url": "https://github.com/kaaviyavarshini/sih-inthack",
        "repo_display": "github.com/kaaviyavarshini/sih-inthack",
        "badge": "SIH '25 WINNER",
        "dither_fn": generate_portal_dither_points
    },
    {
        "id": "microplastics",
        "index": "02",
        "total": "03",
        "title": "Microplastic Detection",
        "spec": "300×340 / 1-BIT",
        "pts_label": "PTS 05190 · FS/SERPENTINE",
        "subtitle": "COMPUTER VISION & WATER SAFETY",
        "description": "Real-time water contaminant vision: 97.4% CNN confidence, microscope profiling & WQI environmental alerts.",
        "tech": ["Python", "TensorFlow", "OpenCV", "Keras", "NumPy", "Streamlit"],
        "repo_url": "https://github.com/kaaviyavarshini/Microplastics-Detection-in-Water-System",
        "repo_display": "github.com/kaaviyavarshini/Microplastics-Detection...",
        "badge": "97.4% ACCURACY",
        "dither_fn": generate_eye_dither_points
    },
    {
        "id": "microgrid",
        "index": "03",
        "total": "03",
        "title": "MicroGrid Simulation",
        "spec": "300×340 / 1-BIT",
        "pts_label": "PTS 04640 · FS/SERPENTINE",
        "subtitle": "HOSPITAL ENERGY ORCHESTRATION",
        "description": "Deterministic zero-blackout controller orchestrating Solar PV, BESS & Grid using PuLP linear programming.",
        "tech": ["Python", "PuLP LP", "NumPy", "Pandas", "Matplotlib", "Streamlit"],
        "repo_url": "https://github.com/kaaviyavarshini/microgrid_simulation",
        "repo_display": "github.com/kaaviyavarshini/microgrid_simulation",
        "badge": "ZERO-BLACKOUT",
        "dither_fn": generate_grid_dither_points
    }
]

def make_showcase_svg():
    """
    Renders the pure black / monochrome stealth visual map featured projects showcase.
    Zero colors: pure black, charcoal, silver, and crisp monochrome 1-bit dotwork.
    """
    # Pure black monochrome palette (matching VISUAL.MAP)
    bg_main = "#070A12"
    panel_bg = "#0B101E"
    panel_inner = "#0E1528"
    card_surface = "#0A0F1D"
    line_border = "#25344C"
    line_subtle = "#192438"
    text_white = "#F0F6FC"
    text_silver = "#DDE7F5"
    text_muted = "#8291A8"
    text_dim = "#54657E"
    dot_color = "#DDE7F5"

    # Pre-generate 1-bit dither paths
    p1_path = points_to_svg_path(PROJECTS[0]["dither_fn"]())
    p2_path = points_to_svg_path(PROJECTS[1]["dither_fn"]())
    p3_path = points_to_svg_path(PROJECTS[2]["dither_fn"]())

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="680" viewBox="0 0 1180 680" role="img" aria-label="Featured Projects Visual Map Showcase">
  <defs>
    <!-- Deep stealth drop shadow (pure black) -->
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="170%">
      <feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#000000" flood-opacity="0.9" />
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.75" />
    </filter>

    <filter id="card-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Clip path for card face -->
    <clipPath id="card-clip">
      <rect width="280" height="420" rx="14" ry="14" />
    </clipPath>

    <!-- Monochrome Sheen Layer -->
    <linearGradient id="sheen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="45%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.12" />
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0" />
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
    </linearGradient>

    <style>
      @keyframes floatLeft {{
        0%, 100% {{ transform: translate(160px, 175px) rotate(-18deg) scale(0.96); }}
        50% {{ transform: translate(150px, 155px) rotate(-20deg) scale(0.98); }}
      }}

      @keyframes floatCenter {{
        0%, 100% {{ transform: translate(450px, 130px) rotate(0deg) scale(1.04); }}
        50% {{ transform: translate(450px, 110px) rotate(0.6deg) scale(1.06); }}
      }}

      @keyframes floatRight {{
        0%, 100% {{ transform: translate(740px, 175px) rotate(18deg) scale(0.96); }}
        50% {{ transform: translate(750px, 155px) rotate(20deg) scale(0.98); }}
      }}

      @keyframes sweepSheen {{
        0% {{ transform: translateX(-150%) translateY(-150%); }}
        40%, 100% {{ transform: translateX(150%) translateY(150%); }}
      }}

      @keyframes ditherPulse {{
        0%, 100% {{ opacity: 0.94; }}
        50% {{ opacity: 0.70; }}
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

      .dither-dots {{
        animation: ditherPulse 3s ease-in-out infinite;
      }}

      text {{
        font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
        user-select: none;
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
        stroke: {line_border};
        stroke-width: 2px;
      }}

      .hover-lift {{
        transition: transform 0.3s ease, filter 0.3s ease;
      }}
      .hover-lift:hover {{
        filter: brightness(1.2);
      }}
    </style>
  </defs>

  <!-- Canvas Background (Pure Deep Black) -->
  <rect width="1180" height="680" rx="18" fill="{bg_main}" />
  <rect x="13" y="13" width="1154" height="654" rx="13" fill="{panel_bg}" stroke="{line_border}" filter="url(#shadow)" />
  <path d="M13 62H1167" stroke="{line_border}" />

  <!-- Terminal Window Controls (Monochrome) -->
  <circle cx="38" cy="38" r="5" fill="{text_dim}" />
  <circle cx="56" cy="38" r="5" fill="{text_dim}" />
  <circle cx="74" cy="38" r="5" fill="{text_dim}" />

  <!-- Terminal Header Title -->
  <text x="590" y="43" text-anchor="middle" fill="{text_muted}" font-size="13" letter-spacing=".6">projects.sh --visual-map --1bit</text>
  <text x="1135" y="43" text-anchor="end" fill="{text_muted}" font-size="11">MONOCHROME HUD</text>

  <!-- Technical Background Grid Marks (+) matching Visual Map -->
  <g stroke="{line_border}" stroke-width="1.2">
    <path d="M 60 90 L 70 90 M 65 85 L 65 95" />
    <path d="M 400 90 L 410 90 M 405 85 L 405 95" />
    <path d="M 780 90 L 790 90 M 785 85 L 785 95" />
    <path d="M 1120 90 L 1130 90 M 1125 85 L 1125 95" />

    <path d="M 65 340 L 75 340 M 70 335 L 70 345" />
    <path d="M 1115 340 L 1125 340 M 1120 335 L 1120 345" />

    <path d="M 65 625 L 75 625 M 70 620 L 70 630" />
    <path d="M 1115 625 L 1125 625 M 1120 620 L 1120 630" />
  </g>

  <!-- ===================================================================== -->
  <!-- HEADER SECTION (VISUAL.MAP STYLE)                                     -->
  <!-- ===================================================================== -->
  <text x="65" y="98" font-size="12" font-weight="700" letter-spacing="3" fill="{text_silver}">// 03 FEATURED REPOSITORIES</text>
  <text x="65" y="118" font-size="11" font-weight="700" letter-spacing="3" fill="{text_muted}">VISUAL.MAP ARCHITECTURE</text>

  <!-- Stealth Black Structural Bar slicing behind PORTFOLIO -->
  <rect x="375" y="80" width="85" height="110" fill="#04060B" stroke="{line_border}" stroke-width="1.5" rx="2" />

  <!-- Brutalist Monochrome Display Title -->
  <text x="65" y="152" font-size="76" class="brutalist-outline">PORTFOLIO</text>
  <text x="65" y="168" font-size="76" fill="{text_white}" class="brutalist-title">PORTFOLIO</text>

  <!-- Architect Metadata Tags -->
  <text x="65" y="194" font-size="11" font-weight="700" letter-spacing="2" fill="{text_muted}">KAAVIYA VARSHINI</text>
  <text x="590" y="194" font-size="11" font-weight="700" letter-spacing="2" fill="{text_muted}">AI &amp; SYSTEMS ENGINEER</text>
  <text x="1115" y="194" font-size="11" font-weight="700" letter-spacing="2" text-anchor="end" fill="{text_silver}">300×340 / 1-BIT</text>

  <line x1="65" y1="206" x2="1115" y2="206" stroke="{line_border}" stroke-width="1" />

  <!-- ===================================================================== -->
  <!-- ROTATING TURNTABLE PEDESTAL (Monochrome Wireframe Orbit)              -->
  <!-- ===================================================================== -->
  <g transform="translate(0, 40)">
    <ellipse cx="590" cy="580" rx="420" ry="105" fill="none" stroke="{line_border}" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.65" />
    <ellipse cx="590" cy="580" rx="460" ry="115" fill="none" stroke="{line_subtle}" stroke-width="1" opacity="0.4" />
    <circle cx="590" cy="580" r="10" fill="{line_border}" opacity="0.5" />
    <circle cx="590" cy="580" r="3" fill="{text_silver}" />
  </g>

  <!-- ===================================================================== -->
  <!-- 3D FANNED DECK: PURE BLACK VISUAL.MAP CARDS                           -->
  <!-- ===================================================================== -->

  <!-- CARD 1 (LEFT): SIH InThack -->
  <g class="card-left">
    <a xlink:href="{esc(PROJECTS[0]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="14" fill="#000000" filter="url(#shadow)" opacity="0.9" />
      
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="14" fill="{card_surface}" stroke="{line_border}" stroke-width="2" />
        <rect x="8" y="8" width="264" height="404" rx="10" fill="none" stroke="{line_subtle}" stroke-width="1" />

        <!-- VISUAL.MAP Header & 1-BIT Spec -->
        <text x="20" y="30" font-size="11" font-weight="700" fill="{text_silver}">VISUAL.MAP</text>
        <text x="260" y="30" font-size="10" font-weight="700" text-anchor="end" fill="{text_muted}">[ 01 // 03 ]</text>
        <line x1="20" y1="38" x2="260" y2="38" stroke="{line_border}" stroke-width="1" />

        <!-- Corner Reticle Target Brackets (Exact Visual Map Signature) -->
        <path d="M 22 48 h 10 M 22 48 v 10 M 258 48 h -10 M 258 48 v 10 M 22 170 h 10 M 22 170 v -10 M 258 170 h -10 M 258 170 v -10" fill="none" stroke="{text_silver}" opacity="0.5" stroke-width="1.2" />

        <!-- 1-BIT Serpentine Dither Portal (Pure Monochrome Dots) -->
        <g class="dither-dots" shape-rendering="crispEdges">
          <path d="{p1_path}" fill="none" stroke="{dot_color}" stroke-width="1" opacity="0.95" />
        </g>

        <!-- Point Count Telemetry -->
        <text x="22" y="180" font-size="9.5" fill="{text_muted}">{PROJECTS[0]['pts_label']}</text>

        <!-- Project Title and Subtitle -->
        <text x="20" y="208" font-size="18" font-weight="900" fill="{text_white}" letter-spacing="-0.5">SIH InThack</text>
        <text x="20" y="224" font-size="10" font-weight="700" fill="{text_silver}">{esc(PROJECTS[0]['subtitle'])}</text>

        <!-- Description -->
        <text x="20" y="246" font-size="11" fill="{text_muted}">
          <tspan x="20" dy="0">National platform built for Smart India</tspan>
          <tspan x="20" dy="16">Hackathon '25: automated judging,</tspan>
          <tspan x="20" dy="16">team tracking &amp; AI categorization.</tspan>
        </text>

        <!-- Monochrome Tech Pills -->
        <g transform="translate(20, 296)">
          <rect x="0" y="0" width="56" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="28" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Python</text>

          <rect x="62" y="0" width="58" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="91" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">FastAPI</text>

          <rect x="126" y="0" width="48" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="150" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">React</text>

          <rect x="180" y="0" width="56" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="208" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Docker</text>

          <rect x="0" y="24" width="76" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="38" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">PostgreSQL</text>

          <rect x="82" y="24" width="68" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="116" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Gemini AI</text>
        </g>

        <!-- Terminal Prompt Repo Link Button -->
        <g transform="translate(20, 360)">
          <rect x="0" y="0" width="240" height="34" rx="6" fill="#04070E" stroke="{text_silver}" stroke-width="1.2" />
          <text x="120" y="22" font-size="11" font-weight="800" text-anchor="middle" fill="{text_white}">&gt; RUN REPO ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- CARD 2 (CENTER): Microplastic Detection (Pure Black Visual Map) -->
  <g class="card-center">
    <a xlink:href="{esc(PROJECTS[1]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="14" fill="#000000" filter="url(#shadow)" opacity="0.95" />
      
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="14" fill="{card_surface}" stroke="{text_silver}" stroke-width="2" />
        <rect x="8" y="8" width="264" height="404" rx="10" fill="none" stroke="{line_border}" stroke-width="1" />

        <!-- VISUAL.MAP Header & 1-BIT Spec -->
        <text x="20" y="30" font-size="11" font-weight="700" fill="{text_white}">VISUAL.MAP</text>
        <text x="260" y="30" font-size="10" font-weight="700" text-anchor="end" fill="{text_silver}">[ 02 // 03 ]</text>
        <line x1="20" y1="38" x2="260" y2="38" stroke="{line_border}" stroke-width="1" />

        <!-- Corner Reticle Target Brackets -->
        <path d="M 22 48 h 10 M 22 48 v 10 M 258 48 h -10 M 258 48 v 10 M 22 170 h 10 M 22 170 v -10 M 258 170 h -10 M 258 170 v -10" fill="none" stroke="{text_white}" opacity="0.75" stroke-width="1.2" />

        <!-- 1-BIT Serpentine Dither Eye Scanner (Monochrome White Dots) -->
        <g class="dither-dots" shape-rendering="crispEdges">
          <path d="{p2_path}" fill="none" stroke="{text_white}" stroke-width="1" opacity="0.98" />
        </g>

        <!-- Point Count Telemetry -->
        <text x="22" y="180" font-size="9.5" fill="{text_silver}">{PROJECTS[1]['pts_label']}</text>

        <!-- Project Title and Subtitle -->
        <text x="20" y="208" font-size="18" font-weight="900" fill="{text_white}" letter-spacing="-0.5">Microplastic Detection</text>
        <text x="20" y="224" font-size="10" font-weight="700" fill="{text_silver}">{esc(PROJECTS[1]['subtitle'])}</text>

        <!-- Description -->
        <text x="20" y="246" font-size="11" fill="{text_silver}">
          <tspan x="20" dy="0">Real-time water contaminant vision:</tspan>
          <tspan x="20" dy="16">97.4% CNN confidence, microscope</tspan>
          <tspan x="20" dy="16">profiling &amp; WQI environmental alerts.</tspan>
        </text>

        <!-- Monochrome Tech Pills -->
        <g transform="translate(20, 296)">
          <rect x="0" y="0" width="76" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="38" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">TensorFlow</text>

          <rect x="82" y="0" width="58" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="111" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">OpenCV</text>

          <rect x="146" y="0" width="48" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="170" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">Keras</text>

          <rect x="200" y="0" width="38" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="219" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">CNN</text>

          <rect x="0" y="24" width="54" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="27" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">NumPy</text>

          <rect x="60" y="24" width="48" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="84" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">Flask</text>

          <rect x="114" y="24" width="66" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="147" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_white}">Streamlit</text>
        </g>

        <!-- Terminal Prompt Repo Link Button -->
        <g transform="translate(20, 360)">
          <rect x="0" y="0" width="240" height="34" rx="6" fill="#04070E" stroke="{text_white}" stroke-width="1.4" />
          <text x="120" y="22" font-size="11" font-weight="800" text-anchor="middle" fill="{text_white}">&gt; RUN REPO ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- CARD 3 (RIGHT): MicroGrid Simulation (Pure Black Visual Map) -->
  <g class="card-right">
    <a xlink:href="{esc(PROJECTS[2]['repo_url'])}" target="_blank" class="hover-lift">
      <rect width="280" height="420" rx="14" fill="#000000" filter="url(#shadow)" opacity="0.9" />
      
      <g clip-path="url(#card-clip)">
        <rect width="280" height="420" rx="14" fill="{card_surface}" stroke="{line_border}" stroke-width="2" />
        <rect x="8" y="8" width="264" height="404" rx="10" fill="none" stroke="{line_subtle}" stroke-width="1" />

        <!-- VISUAL.MAP Header & 1-BIT Spec -->
        <text x="20" y="30" font-size="11" font-weight="700" fill="{text_silver}">VISUAL.MAP</text>
        <text x="260" y="30" font-size="10" font-weight="700" text-anchor="end" fill="{text_muted}">[ 03 // 03 ]</text>
        <line x1="20" y1="38" x2="260" y2="38" stroke="{line_border}" stroke-width="1" />

        <!-- Corner Reticle Target Brackets -->
        <path d="M 22 48 h 10 M 22 48 v 10 M 258 48 h -10 M 258 48 v 10 M 22 170 h 10 M 22 170 v -10 M 258 170 h -10 M 258 170 v -10" fill="none" stroke="{text_silver}" opacity="0.5" stroke-width="1.2" />

        <!-- 1-BIT Serpentine Dither Energy Matrix (Monochrome Silver Dots) -->
        <g class="dither-dots" shape-rendering="crispEdges">
          <path d="{p3_path}" fill="none" stroke="{dot_color}" stroke-width="1" opacity="0.95" />
          <!-- 1:1 Center Typography -->
          <text x="140" y="115" font-size="18" font-weight="900" text-anchor="middle" fill="{text_white}">1 : 1</text>
        </g>

        <!-- Point Count Telemetry -->
        <text x="22" y="180" font-size="9.5" fill="{text_muted}">{PROJECTS[2]['pts_label']}</text>

        <!-- Project Title and Subtitle -->
        <text x="20" y="208" font-size="18" font-weight="900" fill="{text_white}" letter-spacing="-0.5">MicroGrid Simulation</text>
        <text x="20" y="224" font-size="10" font-weight="700" fill="{text_silver}">{esc(PROJECTS[2]['subtitle'])}</text>

        <!-- Description -->
        <text x="20" y="246" font-size="11" fill="{text_muted}">
          <tspan x="20" dy="0">Deterministic zero-blackout controller</tspan>
          <tspan x="20" dy="16">orchestrating Solar PV, BESS &amp; Grid</tspan>
          <tspan x="20" dy="16">using PuLP linear programming.</tspan>
        </text>

        <!-- Monochrome Tech Pills -->
        <g transform="translate(20, 296)">
          <rect x="0" y="0" width="56" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="28" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Python</text>

          <rect x="62" y="0" width="58" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="91" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">PuLP LP</text>

          <rect x="126" y="0" width="52" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="152" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">NumPy</text>

          <rect x="184" y="0" width="52" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="210" y="13" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Pandas</text>

          <rect x="0" y="24" width="68" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="34" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Matplotlib</text>

          <rect x="74" y="24" width="66" height="18" rx="4" fill="#04060C" stroke="{line_border}" stroke-width="1" />
          <text x="107" y="37" font-size="9" font-weight="700" text-anchor="middle" fill="{text_silver}">Streamlit</text>
        </g>

        <!-- Terminal Prompt Repo Link Button -->
        <g transform="translate(20, 360)">
          <rect x="0" y="0" width="240" height="34" rx="6" fill="#04070E" stroke="{text_silver}" stroke-width="1.2" />
          <text x="120" y="22" font-size="11" font-weight="800" text-anchor="middle" fill="{text_white}">&gt; RUN REPO ↗</text>
        </g>

        <!-- Sheen -->
        <rect width="280" height="420" fill="url(#sheen)" class="sheen-layer" pointer-events="none" />
      </g>
    </a>
  </g>

  <!-- Bottom System Telemetry Bar (Monochrome) -->
  <g transform="translate(65, 650)">
    <text x="0" y="0" font-size="11" font-weight="700" fill="{text_silver}">● 3 REPOSITORIES ACTIVE · 1-BIT HUD</text>
    <text x="1050" y="0" font-size="11" font-weight="700" text-anchor="end" fill="{text_muted}">SELECT ANY CARD TO DISPATCH SOURCE</text>
  </g>
</svg>"""
    return svg

def main():
    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate pure black / monochrome stealth visual map showcase
    content = make_showcase_svg()

    # Save to both dark and light files so it is always 100% black as requested
    for name in ["featured-deck-dark.svg", "featured-deck-light.svg"]:
        target = out_dir / name
        target.write_text(content, encoding="utf-8")
        ET.fromstring(content)
        print(f"Validated and wrote {target}")

if __name__ == "__main__":
    main()
