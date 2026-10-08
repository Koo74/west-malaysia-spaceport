"""
Advanced GeoAI Agent - West Malaysia Spaceport Site Selection
===============================================================
CYBERPUNK EDITION: Futuristic UI + OSM Up-to-Date + INSTANT Results
FOCUSED ON: SPACEPORT SITE SELECTION IN PENINSULAR (WEST) MALAYSIA
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MiniMap, MousePosition
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import requests
from pathlib import Path
import sqlite3
import pickle
import math

# ============================================================================
# CYBERPUNK STYLING
# ============================================================================

CYBERPUNK_CSS = """
<style>
    :root {
        --neon-cyan: #00f0ff;
        --neon-pink: #ff2d95;
        --neon-purple: #b026ff;
        --neon-green: #39ff14;
        --neon-yellow: #ffe84d;
    }
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a1f 100%); }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 3.2rem; font-weight: 900;
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(0, 240, 255, 0.3);
        letter-spacing: 4px; animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 40px rgba(0, 240, 255, 0.3); }
        50% { text-shadow: 0 0 60px rgba(0, 240, 255, 0.6), 0 0 80px rgba(176, 38, 255, 0.3); }
    }
    .subtitle {
        font-family: 'Courier New', monospace; color: #00f0ff;
        font-size: 1.1rem; letter-spacing: 8px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .css-1d391kg, .css-1633s9g {
        background: rgba(10, 10, 20, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    .css-1d391kg p, .css-1633s9g p,
    .css-1d391kg label, .css-1633s9g label,
    .css-1d391kg div, .css-1633s9g div,
    .css-1d391kg span, .css-1633s9g span {
        color: #ffffff !important; font-weight: 400 !important;
    }
    .recommendation-container {
        background: rgba(15, 15, 35, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px; padding: 20px; margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
    }
    .recommendation-container:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }
    .recommendation-title {
        color: #00f0ff; font-family: 'Courier New', monospace;
        font-size: 1.2rem; font-weight: bold; letter-spacing: 2px;
        margin-bottom: 10px; text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    .recommendation-item {
        color: #ffffff; font-family: 'Courier New', monospace;
        font-size: 0.9rem; padding: 6px 0;
        border-bottom: 1px solid rgba(0, 240, 255, 0.05);
        line-height: 1.6;
    }
    .recommendation-item:last-child { border-bottom: none; }
    .recommendation-item .icon { margin-right: 8px; }
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(176, 38, 255, 0.15)) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important; text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px);
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.3), rgba(176, 38, 255, 0.3)) !important;
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3) !important;
        transform: scale(1.02); color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(176, 38, 255, 0.25)) !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
    }
    [data-testid="metric-container"] {
        background: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 10px; padding: 15px; backdrop-filter: blur(5px);
    }
    [data-testid="metric-container"] label {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px; font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] div {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    .dataframe {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    .dataframe th {
        color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.1) !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px; font-weight: bold !important; font-size: 0.9rem !important;
    }
    .dataframe td {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderHeader {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important; color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 1px; font-weight: bold !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.1) !important;
        border-top: none !important;
    }
    .streamlit-expanderContent p, .streamlit-expanderContent div,
    .streamlit-expanderContent li, .streamlit-expanderContent span {
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #00f0ff !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important; color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }
    .stAlert {
        background: rgba(15, 15, 35, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    .stAlert p, .stAlert div, .stAlert li, .stAlert span { color: #ffffff !important; }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px; text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00f0ff !important;
        border-bottom: 2px solid #00f0ff !important;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        font-weight: bold !important;
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(10, 10, 20, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f0ff, #b026ff);
        border-radius: 3px;
    }
    .folium-map {
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.05);
    }
    .cyber-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00f0ff, #b026ff, #ff2d95, transparent);
        margin: 20px 0; opacity: 0.5;
    }
    .stMarkdown p, .stMarkdown li {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        line-height: 1.6 !important;
    }
    .stMarkdown h1 { color: #00f0ff !important; }
    .stMarkdown h2 { color: #b026ff !important; }
    .stMarkdown h3 { color: #ff2d95 !important; }
    .stMarkdown h4 { color: #39ff14 !important; }
    .stCaption {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
    }
    .stRadio label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }
    .stRadio [role="radiogroup"] { gap: 8px; }
</style>
"""

# ============================================================================
# RECOMMENDATION ENGINE (with weather actions)
# ============================================================================

def generate_recommendation_strategy(result_data: Dict) -> Dict:
    """Generate recommendation strategy. Feasibility consistent with actions."""
    score = result_data.get('suitability_percentage', 0)
    details = result_data.get('details', {})
    elevation_m = result_data.get('elevation_m', 0)
    flood_risk = result_data.get('flood_risk', 'Unknown')
    population_density = result_data.get('population_density', 0)
    coastal_distance = result_data.get('coastal_distance_km', 0)
    wind_speed = result_data.get('wind_speed_ms', None)
    wind_gust = result_data.get('wind_gust_ms', None)

    recommendations = {
        'immediate_actions': [],
        'short_term_actions': [],
        'long_term_actions': [],
        'investment_required': 'Low',
        'overall_feasibility': 'High',
        'risk_level': 'Low',
    }

    def add_action(bucket, text, priority, cost):
        recommendations[bucket].append({
            'text': text, 'priority': priority, 'cost': cost
        })

    # 1. ELEVATION
    if elevation_m < 20:
        add_action('immediate_actions',
            '🚨 CRITICAL: Elevation is very low (<20m). Build massive flood defenses and elevated launch pads immediately.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif elevation_m < 50:
        add_action('short_term_actions',
            '🌊 Build flood defenses and drainage systems. Elevation is moderate.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'
    elif elevation_m < 200:
        add_action('immediate_actions',
            '✅ Excellent elevation (50-200m). No flood defenses needed. Proceed with standard launch pad design.',
            'Low', '💸')
    elif elevation_m < 500:
        add_action('short_term_actions',
            '⛰️ Good elevation (200-500m). Plan for stable foundations and wind protection.',
            'Medium', '💸💸')
    else:
        add_action('short_term_actions',
            '🏔️ Very high elevation (500m+). Consider construction challenges and weather protection.',
            'Medium', '💸💸💸')

    # 2. POPULATION
    if population_density > 5:
        add_action('immediate_actions',
            '🏙️ HIGH POPULATION DENSITY. Need extensive evacuation plans and safety buffer zones.',
            'Critical', '💸💸💸💸')
    elif population_density > 2:
        add_action('short_term_actions',
            '🏘️ MODERATE POPULATION. Develop evacuation procedures and community engagement.',
            'High', '💸💸💸')
    else:
        add_action('immediate_actions',
            '✅ VERY LOW POPULATION. Ideal for spaceport - minimal evacuation required.',
            'Low', '💸')

    # 3. COASTAL
    if coastal_distance < 5:
        add_action('immediate_actions',
            '🌊 PERFECT COASTAL ACCESS. Leverage sea transport for heavy equipment.',
            'Low', '💸')
    elif coastal_distance < 30:
        add_action('short_term_actions',
            '🚢 GOOD COASTAL ACCESS. Build access roads to the coast. Consider sea transport hub.',
            'Medium', '💸💸')
    else:
        add_action('long_term_actions',
            '🚛 INLAND LOCATION. Significant transport infrastructure needed.',
            'High', '💸💸💸💸')

    # 4. INFRASTRUCTURE
    infra_details = details.get('infrastructure_access', {}).get('value', {})
    if isinstance(infra_details, dict):
        if infra_details.get('airports', 0) == 0:
            add_action('short_term_actions',
                '✈️ No airport nearby. Build airstrip for personnel transport.',
                'High', '💸💸💸')
        if infra_details.get('major_roads', 0) == 0:
            add_action('short_term_actions',
                '🛣️ No major roads. Build access roads for equipment transport.',
                'High', '💸💸💸')
        if infra_details.get('ports', 0) == 0:
            add_action('long_term_actions',
                '🚢 No port. Consider building a small port for heavy equipment delivery.',
                'Medium', '💸💸💸💸')
        if infra_details.get('power_facilities', 0) == 0:
            add_action('long_term_actions',
                '⚡ No power infrastructure. Build power plant or connect to grid.',
                'High', '💸💸💸💸')

    # 5. LAND
    land_details = details.get('land_availability', {}).get('value', {})
    if isinstance(land_details, dict):
        forest = land_details.get('forest_areas', 0)
        developed = land_details.get('developed_areas', 0)
        if forest > 20 and developed < 5:
            add_action('immediate_actions',
                '🌳 ABUNDANT LAND. Excellent for expansion. Ready for development.',
                'Low', '💸')
        elif forest > 10 and developed < 10:
            add_action('short_term_actions',
                '🌿 GOOD LAND AVAILABILITY. Plan for expansion and buffer zones.',
                'Medium', '💸💸')
        else:
            add_action('immediate_actions',
                '🏗️ LIMITED LAND. Need to acquire additional land for launch pads and safety zones.',
                'Critical', '💸💸💸💸')

    # 6. FLOOD
    if flood_risk == 'High':
        add_action('immediate_actions',
            '🌊 HIGH FLOOD RISK! Emergency flood defenses needed. Consider elevating all structures.',
            'Critical', '💸💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif flood_risk == 'Moderate':
        add_action('short_term_actions',
            '🌊 MODERATE FLOOD RISK. Build standard flood defenses and drainage systems.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'

    # 7. LATITUDE
    lat_deg = result_data.get('lat_deg', 0)
    if lat_deg < 3:
        add_action('immediate_actions',
            f'🌐 EXCELLENT LATITUDE ({lat_deg:.1f}°). Near equator - maximum fuel efficiency! ✅',
            'Low', '💸')
    elif lat_deg < 5:
        add_action('immediate_actions',
            f'🌐 GOOD LATITUDE ({lat_deg:.1f}°). Good launch efficiency.',
            'Low', '💸')
    else:
        add_action('short_term_actions',
            f'🌐 MODERATE LATITUDE ({lat_deg:.1f}°). Optimize launch trajectories for fuel efficiency.',
            'Medium', '💸💸')

    # ============ 8. WIND / WEATHER ============
    if wind_speed is not None:
        if wind_speed > 12:
            add_action('immediate_actions',
                f'🌬️ HIGH WIND SPEED ({wind_speed:.1f} m/s). Need robust wind shear protection and launch-window scheduling. High operational cost.',
                'Critical', '💸💸💸💸')
        elif wind_speed > 8:
            add_action('short_term_actions',
                f'🌬️ MODERATE WIND ({wind_speed:.1f} m/s). Plan wind-monitoring systems and flexible launch windows.',
                'High', '💸💸💸')
        elif wind_speed < 4:
            add_action('immediate_actions',
                f'✅ EXCELLENT WIND CONDITIONS ({wind_speed:.1f} m/s). Calm, stable air — ideal for launches.',
                'Low', '💸')
        else:
            add_action('short_term_actions',
                f'🌬️ GOOD WIND ({wind_speed:.1f} m/s). Normal launch conditions. Standard weather monitoring recommended.',
                'Low', '💸')

        if wind_gust is not None and wind_gust > 15:
            add_action('short_term_actions',
                f'💨 STRONG GUSTS ({wind_gust:.1f} m/s). Design structures for high wind-load. Consider reinforced launch pad and hangar.',
                'High', '💸💸💸')

    # ================= FEASIBILITY LOGIC =================
    critical_count = sum(
        1 for a in recommendations['immediate_actions']
        if a['priority'] == 'Critical'
    )
    high_count = sum(
        1 for a in recommendations['short_term_actions']
        if a['priority'] == 'High'
    )
    total_actions = (
        len(recommendations['immediate_actions'])
        + len(recommendations['short_term_actions'])
        + len(recommendations['long_term_actions'])
    )

    if score >= 80:
        score_band, score_emoji = 'Excellent', '✅'
    elif score >= 65:
        score_band, score_emoji = 'Good', '👍'
    elif score >= 50:
        score_band, score_emoji = 'Moderate', '👌'
    elif score >= 35:
        score_band, score_emoji = 'Limited', '⚠️'
    else:
        score_band, score_emoji = 'Poor', '❌'

    if critical_count >= 3:
        feasibility = '❌ Poor - Major critical issues must be resolved before development'
        risk_level = 'Very High'
    elif critical_count == 2:
        feasibility = '⚠️ Limited - Multiple critical issues require resolution'
        risk_level = 'High'
    elif critical_count == 1:
        feasibility = '👌 Moderate - One critical issue requires resolution'
        risk_level = 'High'
    elif high_count >= 2:
        feasibility = '👌 Moderate - Several high-priority preparations required'
        risk_level = 'Medium'
    else:
        feasibility = f'{score_emoji} {score_band} - ' + {
            'Excellent': 'High potential for immediate development',
            'Good': 'Suitable with minor site preparation',
            'Moderate': 'Significant investment required',
            'Limited': 'Major investment required',
            'Poor': 'Not recommended for spaceport development',
        }[score_band]
        risk_level = {
            'Excellent': 'Low', 'Good': 'Low',
            'Moderate': 'Medium', 'Limited': 'High', 'Poor': 'Very High',
        }[score_band]

    recommendations['overall_feasibility'] = feasibility
    recommendations['risk_level'] = risk_level
    recommendations['critical_action_count'] = critical_count
    recommendations['high_action_count'] = high_count
    recommendations['total_action_count'] = total_actions

    recommendations['timeline_summary'] = {
        'immediate': f"{len(recommendations['immediate_actions'])} actions (0-6 months)",
        'short_term': f"{len(recommendations['short_term_actions'])} actions (6-18 months)",
        'long_term': f"{len(recommendations['long_term_actions'])} actions (18-36 months)"
    }
    return recommendations

# ============================================================================
# CACHE
# ============================================================================

class APICache:
    def __init__(self, cache_dir: str = "west_malaysia_api_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, url: str, params: Dict) -> str:
        key_str = url + json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, url: str, params: Dict) -> Optional[Dict]:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            modified_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - modified_time < self.ttl:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception:
                    return None
        return None

    def set(self, url: str, params: Dict, data: Dict) -> None:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def get_stats(self) -> Dict:
        files = list(self.cache_dir.glob("*.json"))
        return {'total_cached': len(files), 'cache_dir': str(self.cache_dir)}

api_cache = APICache()

# ============================================================================
# WEST MALAYSIA LOCATIONS
# ============================================================================

WEST_MALAYSIA_LOCATIONS = {
    # PERLIS
    'Kangar (Perlis)': (6.4414, 100.1986),
    'Arau (Perlis)': (6.4297, 100.2703),
    'Padang Besar (Perlis)': (6.6601, 100.3244),
    'Kuala Perlis': (6.4000, 100.1300),
    'Chuping (Perlis)': (6.5000, 100.2600),
    'Wang Kelian (Perlis)': (6.6800, 100.1700),
    # KEDAH
    'Alor Setar (Kedah)': (6.1248, 100.3678),
    'Sungai Petani (Kedah)': (5.6470, 100.4877),
    'Kulim (Kedah)': (5.3649, 100.5600),
    'Langkawi (Kedah)': (6.3500, 99.8000),
    'Kuah (Langkawi)': (6.3265, 99.8430),
    'Pantai Cenang (Langkawi)': (6.2930, 99.7250),
    'Padang Matsirat (Langkawi)': (6.3400, 99.7600),
    'Tanjung Rhu (Langkawi)': (6.4400, 99.8500),
    'Teluk Ewa (Langkawi)': (6.4000, 99.9000),
    'Datai Bay (Langkawi)': (6.4700, 99.6800),
    'Baling (Kedah)': (5.6800, 100.9200),
    'Sik (Kedah)': (5.8200, 100.7400),
    'Pendang (Kedah)': (6.0000, 100.4700),
    'Jitra (Kedah)': (6.2683, 100.4225),
    'Yan (Kedah)': (5.8000, 100.3700),
    'Gurun (Kedah)': (5.8200, 100.4700),
    # PENANG
    'George Town (Penang)': (5.4141, 100.3288),
    'Bayan Lepas (Penang)': (5.2950, 100.2700),
    'Batu Ferringhi (Penang)': (5.4750, 100.2400),
    'Balik Pulau (Penang)': (5.3500, 100.2300),
    'Butterworth (Penang)': (5.3990, 100.3630),
    'Bukit Mertajam (Penang)': (5.3630, 100.4670),
    'Nibong Tebal (Penang)': (5.1700, 100.4800),
    'Teluk Bahang (Penang)': (5.4600, 100.2100),
    'Gertak Sanggul (Penang)': (5.2700, 100.2000),
    'Batu Maung (Penang)': (5.2800, 100.2900),
    # PERAK
    'Ipoh (Perak)': (4.5975, 101.0901),
    'Taiping (Perak)': (4.8500, 100.7333),
    'Teluk Intan (Perak)': (4.0259, 101.0214),
    'Kuala Kangsar (Perak)': (4.7700, 100.9400),
    'Lumut (Perak)': (4.2300, 100.6300),
    'Pangkor Island (Perak)': (4.2200, 100.5600),
    'Sitiawan (Perak)': (4.2200, 100.7000),
    'Batu Gajah (Perak)': (4.4700, 101.0400),
    'Kampar (Perak)': (4.3100, 101.1500),
    'Tapah (Perak)': (4.2000, 101.2600),
    'Tanjung Malim (Perak)': (3.6800, 101.5200),
    'Gerik (Perak)': (5.4300, 101.1300),
    'Segari (Perak)': (4.2800, 100.6000),
    'Pantai Remis (Perak)': (4.4500, 100.6300),
    # SELANGOR / KL / PUTRAJAYA
    'Shah Alam (Selangor)': (3.0733, 101.5185),
    'Petaling Jaya (Selangor)': (3.1073, 101.6067),
    'Subang Jaya (Selangor)': (3.0567, 101.5850),
    'Klang (Selangor)': (3.0333, 101.4500),
    'Port Klang (Selangor)': (3.0000, 101.4000),
    'Kuala Selangor (Selangor)': (3.3500, 101.2500),
    'Kuala Kubu Bharu (Selangor)': (3.5600, 101.6400),
    'Rawang (Selangor)': (3.3200, 101.5800),
    'Sepang (Selangor)': (2.7000, 101.7500),
    'Banting (Selangor)': (2.8100, 101.5000),
    'Morib (Selangor)': (2.7500, 101.4400),
    'Tanjung Sepat (Selangor)': (2.6600, 101.5600),
    'Sekinchan (Selangor)': (3.5100, 101.1000),
    'Sabak Bernam (Selangor)': (3.7700, 100.9800),
    'Kajang (Selangor)': (2.9900, 101.7900),
    'Bangi (Selangor)': (2.9500, 101.7800),
    'Putrajaya (FT)': (2.9264, 101.6964),
    'Cyberjaya (Selangor)': (2.9200, 101.6500),
    'Puchong (Selangor)': (3.0000, 101.6200),
    'Batang Kali (Selangor)': (3.4700, 101.6500),
    'Carey Island (Selangor)': (2.8700, 101.3800),
    'Pulau Ketam (Selangor)': (3.0200, 101.2500),
    'Pulau Carey (Selangor)': (2.8800, 101.3500),
    'Pulau Indah (Selangor)': (2.9800, 101.3200),
    'Kuala Langat (Selangor)': (2.8500, 101.4500),
    'Kuala Lumpur City Centre': (3.1390, 101.6869),
    'KLCC (KL)': (3.1578, 101.7120),
    'Bukit Bintang (KL)': (3.1450, 101.7100),
    'Cheras (KL)': (3.0800, 101.7300),
    'Kepong (KL)': (3.2100, 101.6400),
    'Sungai Besi (KL)': (3.0600, 101.7000),
    'Batu Caves (Selangor)': (3.2379, 101.6840),
    # NEGERI SEMBILAN
    'Seremban (N. Sembilan)': (2.7297, 101.9381),
    'Port Dickson (N. Sembilan)': (2.5228, 101.7967),
    'Nilai (N. Sembilan)': (2.8200, 101.8000),
    'Bahau (N. Sembilan)': (2.8000, 102.4000),
    'Tampin (N. Sembilan)': (2.4700, 102.2300),
    'Kuala Pilah (N. Sembilan)': (2.7400, 102.2500),
    'Rembau (N. Sembilan)': (2.5900, 102.0900),
    'Gemas (N. Sembilan)': (2.5800, 102.6100),
    'Lukut (N. Sembilan)': (2.5800, 101.8300),
    'Tanjung Tuan (N. Sembilan)': (2.4000, 101.8500),
    'Blue Lagoon (N. Sembilan)': (2.4800, 101.8300),
    'Linggi (N. Sembilan)': (2.4800, 102.0000),
    # MELAKA
    'Melaka City (Melaka)': (2.1896, 102.2501),
    'Ayer Keroh (Melaka)': (2.2700, 102.2900),
    'Alor Gajah (Melaka)': (2.3800, 102.2100),
    'Jasin (Melaka)': (2.3100, 102.4300),
    'Masjid Tanah (Melaka)': (2.3500, 102.1100),
    'Merlimau (Melaka)': (2.1400, 102.4300),
    'Tanjung Kling (Melaka)': (2.2200, 102.1600),
    'Tanjung Bidara (Melaka)': (2.2800, 102.0900),
    'Pengkalan Balak (Melaka)': (2.3200, 102.0800),
    'Kuala Sungai Baru (Melaka)': (2.3500, 102.0400),
    # JOHOR
    'Johor Bahru (Johor)': (1.4927, 103.7414),
    'Iskandar Puteri (Johor)': (1.4300, 103.6300),
    'Kulai (Johor)': (1.6600, 103.6000),
    'Skudai (Johor)': (1.5400, 103.6700),
    'Senai (Johor)': (1.6200, 103.6600),
    'Pasir Gudang (Johor)': (1.4700, 103.9000),
    'Pengerang (Johor)': (1.3600, 104.1700),
    'Kota Tinggi (Johor)': (1.7300, 103.9000),
    'Mersing (Johor)': (2.4300, 103.8300),
    'Batu Pahat (Johor)': (1.8500, 102.9300),
    'Muar (Johor)': (2.0500, 102.5700),
    'Segamat (Johor)': (2.5100, 102.8100),
    'Kluang (Johor)': (2.0300, 103.3200),
    'Pontian (Johor)': (1.4800, 103.3800),
    'Desaru (Johor)': (1.5500, 104.2600),
    'Endau (Johor)': (2.6500, 103.6200),
    'Pulau Aur (Johor)': (2.4500, 104.5200),
    'Pulau Pemanggil (Johor)': (2.5800, 104.3300),
    'Pulau Sibu (Johor)': (2.2000, 104.1000),
    'Pulau Tinggi (Johor)': (2.3000, 104.1200),
    'Pulau Rawa (Johor)': (2.5300, 103.9700),
    'Pulau Kukup (Johor)': (1.3100, 103.4200),
    'Tanjung Piai (Johor)': (1.2700, 103.5100),
    'Gelang Patah (Johor)': (1.4500, 103.5900),
    'Kukup (Johor)': (1.3200, 103.4300),
    'Labis (Johor)': (2.3800, 103.0200),
    'Yong Peng (Johor)': (2.0100, 103.0600),
    'Ayer Hitam (Johor)': (1.9200, 103.1800),
    # KELANTAN
    'Kota Bharu (Kelantan)': (6.1256, 102.2386),
    'Kubang Kerian (Kelantan)': (6.1000, 102.2800),
    'Pasir Puteh (Kelantan)': (5.8300, 102.4000),
    'Pasir Mas (Kelantan)': (6.0500, 102.1400),
    'Tumpat (Kelantan)': (6.2000, 102.1700),
    'Bachok (Kelantan)': (6.0700, 102.4000),
    'Tanah Merah (Kelantan)': (5.8000, 102.1500),
    'Machang (Kelantan)': (5.7700, 102.2100),
    'Kuala Krai (Kelantan)': (5.5300, 102.2000),
    'Gua Musang (Kelantan)': (4.8800, 101.9600),
    'Jeli (Kelantan)': (5.7000, 101.8400),
    'Tok Bali (Kelantan)': (5.8200, 102.4500),
    'Pantai Cahaya Bulan (Kelantan)': (6.1300, 102.2900),
    # TERENGGANU
    'Kuala Terengganu (Terengganu)': (5.3303, 103.1408),
    'Kuala Nerus (Terengganu)': (5.3800, 103.0800),
    'Kemaman (Terengganu)': (4.2300, 103.4200),
    'Chukai (Terengganu)': (4.2200, 103.4200),
    'Kerteh (Terengganu)': (4.5200, 103.4500),
    'Paka (Terengganu)': (4.6400, 103.4400),
    'Dungun (Terengganu)': (4.7700, 103.4200),
    'Marang (Terengganu)': (5.2000, 103.2100),
    'Kuala Berang (Terengganu)': (5.0700, 102.9500),
    'Jerteh (Terengganu)': (5.7400, 102.5100),
    'Besut (Terengganu)': (5.7300, 102.5600),
    'Setiu (Terengganu)': (5.5800, 102.8000),
    'Kuala Besut (Terengganu)': (5.8300, 102.5600),
    'Pulau Perhentian (Terengganu)': (5.9100, 102.7400),
    'Pulau Redang (Terengganu)': (5.7800, 103.0000),
    'Pulau Kapas (Terengganu)': (5.2200, 103.2600),
    'Pulau Tenggol (Terengganu)': (4.8000, 103.6800),
    'Pulau Lang Tengah (Terengganu)': (5.7800, 102.8900),
    'Kijal (Terengganu)': (4.3600, 103.5000),
    # PAHANG
    'Kuantan (Pahang)': (3.8077, 103.3260),
    'Pekan (Pahang)': (3.4900, 103.3900),
    'Temerloh (Pahang)': (3.4500, 102.4200),
    'Bentong (Pahang)': (3.5200, 101.9100),
    'Raub (Pahang)': (3.7900, 101.8600),
    'Kuala Lipis (Pahang)': (4.1800, 102.0500),
    'Jerantut (Pahang)': (3.9400, 102.3600),
    'Mentakab (Pahang)': (3.4900, 102.3500),
    'Cameron Highlands (Pahang)': (4.4700, 101.3800),
    'Genting Highlands (Pahang)': (3.4200, 101.7900),
    'Fraser\'s Hill (Pahang)': (3.7100, 101.7400),
    'Tioman Island (Pahang)': (2.7900, 104.1700),
    'Cherating (Pahang)': (4.1300, 103.3900),
    'Balok (Pahang)': (3.9500, 103.3700),
    'Beserah (Pahang)': (3.8800, 103.3600),
    'Sungai Lembing (Pahang)': (3.9200, 103.0300),
    'Gambang (Pahang)': (3.7100, 103.0900),
    'Maran (Pahang)': (3.5800, 102.7700),
    'Kuala Rompin (Pahang)': (2.8200, 103.4800),
    'Nenasi (Pahang)': (2.9900, 103.4900),
    'Gebeng (Pahang)': (3.9600, 103.3700),
    'Bukit Ibam (Pahang)': (3.3000, 102.8500),
    'Lanchang (Pahang)': (3.5000, 102.2000),
    'Janda Baik (Pahang)': (3.3200, 101.8800),
}

# ============================================================================
# SPACEPORT CANDIDATES
# ============================================================================

WEST_MALAYSIA_SPACEPORT_CANDIDATES = {
    'Pengerang, Johor': (1.3600, 104.1700),
    'Desaru Coast, Johor': (1.5500, 104.2600),
    'Kota Tinggi, Johor': (1.7300, 103.9000),
    'Mersing, Johor': (2.4300, 103.8300),
    'Endau, Johor': (2.6500, 103.6200),
    'Pulau Aur, Johor': (2.4500, 104.5200),
    'Pulau Pemanggil, Johor': (2.5800, 104.3300),
    'Pulau Sibu, Johor': (2.2000, 104.1000),
    'Pulau Tinggi, Johor': (2.3000, 104.1200),
    'Pulau Rawa, Johor': (2.5300, 103.9700),
    'Tanjung Piai, Johor': (1.2700, 103.5100),
    'Pulau Kukup, Johor': (1.3100, 103.4200),
    'Kukup, Johor': (1.3200, 103.4300),
    'Pontian Coast, Johor': (1.4800, 103.3800),
    'Labis, Johor': (2.3800, 103.0200),
    'Ayer Hitam, Johor': (1.9200, 103.1800),
    'Pulau Tioman, Pahang': (2.7900, 104.1700),
    'Kuala Rompin, Pahang': (2.8200, 103.4800),
    'Nenasi, Pahang': (2.9900, 103.4900),
    'Pekan, Pahang': (3.4900, 103.3900),
    'Cherating, Pahang': (4.1300, 103.3900),
    'Balok, Pahang': (3.9500, 103.3700),
    'Beserah, Pahang': (3.8800, 103.3600),
    'Gebeng, Pahang': (3.9600, 103.3700),
    'Bukit Ibam, Pahang': (3.3000, 102.8500),
    'Lanchang, Pahang': (3.5000, 102.2000),
    'Kerteh, Terengganu': (4.5200, 103.4500),
    'Paka, Terengganu': (4.6400, 103.4400),
    'Kijal, Terengganu': (4.3600, 103.5000),
    'Kuala Kemaman, Terengganu': (4.2300, 103.4200),
    'Pulau Tenggol, Terengganu': (4.8000, 103.6800),
    'Pulau Redang, Terengganu': (5.7800, 103.0000),
    'Pulau Perhentian, Terengganu': (5.9100, 102.7400),
    'Pulau Kapas, Terengganu': (5.2200, 103.2600),
    'Pulau Lang Tengah, Terengganu': (5.7800, 102.8900),
    'Setiu, Terengganu': (5.5800, 102.8000),
    'Kuala Besut, Terengganu': (5.8300, 102.5600),
    'Besut, Terengganu': (5.7300, 102.5600),
    'Kuala Berang, Terengganu': (5.0700, 102.9500),
    'Dungun, Terengganu': (4.7700, 103.4200),
    'Marang, Terengganu': (5.2000, 103.2100),
    'Tok Bali, Kelantan': (5.8200, 102.4500),
    'Bachok, Kelantan': (6.0700, 102.4000),
    'Pasir Puteh, Kelantan': (5.8300, 102.4000),
    'Gua Musang, Kelantan': (4.8800, 101.9600),
    'Dabong, Kelantan': (5.3800, 102.0100),
    'Kuala Krai, Kelantan': (5.5300, 102.2000),
    'Langkawi (Kedah)': (6.3500, 99.8000),
    'Teluk Ewa, Langkawi': (6.4000, 99.9000),
    'Pantai Cenang, Langkawi': (6.2930, 99.7250),
    'Padang Matsirat, Langkawi': (6.3400, 99.7600),
    'Datai Bay, Langkawi': (6.4700, 99.6800),
    'Kuala Perlis': (6.4000, 100.1300),
    'Padang Besar (Perlis)': (6.6601, 100.3244),
    'Chuping (Perlis)': (6.5000, 100.2600),
    'Pangkor Island (Perak)': (4.2200, 100.5600),
    'Pulau Pangkor (Perak)': (4.2200, 100.5600),
    'Pulau Sembilan (Perak)': (4.0800, 100.5300),
    'Pulau Jarak (Perak)': (4.0800, 100.2800),
    'Segari (Perak)': (4.2800, 100.6000),
    'Pantai Remis (Perak)': (4.4500, 100.6300),
    'Pulau Ketam (Selangor)': (3.0200, 101.2500),
    'Pulau Carey (Selangor)': (2.8800, 101.3500),
    'Pulau Indah (Selangor)': (2.9800, 101.3200),
    'Morib (Selangor)': (2.7500, 101.4400),
    'Tanjung Sepat (Selangor)': (2.6600, 101.5600),
    'Sekinchan Coast (Selangor)': (3.5000, 101.0800),
    'Sungai Besar (Selangor)': (3.6700, 100.9800),
    'Sabak Bernam (Selangor)': (3.7700, 100.9800),
    'Banting (Selangor)': (2.8100, 101.5000),
    'Kuala Langat (Selangor)': (2.8500, 101.4500),
    'Carey Island (Selangor)': (2.8700, 101.3800),
    'Tanjung Bidara (Melaka)': (2.2800, 102.0900),
    'Pengkalan Balak (Melaka)': (2.3200, 102.0800),
    'Kuala Sungai Baru (Melaka)': (2.3500, 102.0400),
    'Port Dickson (N. Sembilan)': (2.5228, 101.7967),
    'Tanjung Tuan (N. Sembilan)': (2.4000, 101.8500),
    'Blue Lagoon (N. Sembilan)': (2.4800, 101.8300),
    'Linggi (N. Sembilan)': (2.4800, 102.0000),
    'Gemas (N. Sembilan)': (2.5800, 102.6100),
    'Teluk Bahang (Penang)': (5.4600, 100.2100),
    'Gertak Sanggul (Penang)': (5.2700, 100.2000),
    'Batu Maung (Penang)': (5.2800, 100.2900),
    'Balik Pulau (Penang)': (5.3500, 100.2300),
    'Pulau Betong (Penang)': (5.3300, 100.2000),
}

# ============================================================================
# STATIC AIRPORTS & SETTLEMENTS
# ============================================================================

STATIC_AIRPORTS = {
    'Langkawi International': (6.3297, 99.7287),
    'Sultan Abdul Halim (Alor Setar)': (6.1897, 100.3982),
    'Kangar Airport': (6.4500, 100.2000),
    'Penang International': (5.2972, 100.2768),
    'Butterworth Air Base': (5.4000, 100.3700),
    'Sultan Azlan Shah (Ipoh)': (4.5679, 101.0920),
    'Taiping Airport': (4.8667, 100.7167),
    'Pulau Pangkor Airstrip': (4.2200, 100.5500),
    'Lumut RMAF Base': (4.2300, 100.6200),
    'Sultan Abdul Aziz Shah (Subang)': (3.1306, 101.5493),
    'KLIA (Sepang)': (2.7456, 101.7099),
    'KLIA2 (Sepang)': (2.7430, 101.6860),
    'Melaka International': (2.2633, 102.2517),
    'Senai International (JB)': (1.6411, 103.6696),
    'Batu Pahat Airport': (1.8500, 102.9300),
    'Mersing Airport': (2.4300, 103.8300),
    'Sultan Ahmad Shah (Kuantan)': (3.7753, 103.2090),
    'Tioman Airport': (2.8183, 104.1600),
    'Sultan Mahmud (K. Terengganu)': (5.3825, 103.1033),
    'Kerteh Airport': (4.5200, 103.4500),
    'Sultan Ismail Petra (Kota Bharu)': (6.1664, 102.2924),
    'Tok Bali Airstrip': (5.8200, 102.4500),
    'Gua Musang Airstrip': (4.8800, 101.9600),
}

STATIC_SETTLEMENTS = {
    'Kangar': {'coords': (6.4414, 100.1986), 'population': 50000},
    'Arau': {'coords': (6.4297, 100.2703), 'population': 30000},
    'Alor Setar': {'coords': (6.1248, 100.3678), 'population': 400000},
    'Sungai Petani': {'coords': (5.6470, 100.4877), 'population': 300000},
    'Kulim': {'coords': (5.3649, 100.5600), 'population': 150000},
    'Langkawi': {'coords': (6.3500, 99.8000), 'population': 90000},
    'Baling': {'coords': (5.6800, 100.9200), 'population': 30000},
    'George Town': {'coords': (5.4141, 100.3288), 'population': 700000},
    'Butterworth': {'coords': (5.3990, 100.3630), 'population': 200000},
    'Bukit Mertajam': {'coords': (5.3630, 100.4670), 'population': 200000},
    'Bayan Lepas': {'coords': (5.2950, 100.2700), 'population': 150000},
    'Ipoh': {'coords': (4.5975, 101.0901), 'population': 750000},
    'Taiping': {'coords': (4.8500, 100.7333), 'population': 200000},
    'Teluk Intan': {'coords': (4.0259, 101.0214), 'population': 100000},
    'Kuala Kangsar': {'coords': (4.7700, 100.9400), 'population': 50000},
    'Lumut': {'coords': (4.2300, 100.6300), 'population': 40000},
    'Sitiawan': {'coords': (4.2200, 100.7000), 'population': 150000},
    'Shah Alam': {'coords': (3.0733, 101.5185), 'population': 700000},
    'Petaling Jaya': {'coords': (3.1073, 101.6067), 'population': 800000},
    'Subang Jaya': {'coords': (3.0567, 101.5850), 'population': 700000},
    'Klang': {'coords': (3.0333, 101.4500), 'population': 900000},
    'Kuala Lumpur': {'coords': (3.1390, 101.6869), 'population': 1800000},
    'Putrajaya': {'coords': (2.9264, 101.6964), 'population': 100000},
    'Cyberjaya': {'coords': (2.9200, 101.6500), 'population': 100000},
    'Sepang': {'coords': (2.7000, 101.7500), 'population': 90000},
    'Kajang': {'coords': (2.9900, 101.7900), 'population': 300000},
    'Bangi': {'coords': (2.9500, 101.7800), 'population': 200000},
    'Kuala Selangor': {'coords': (3.3500, 101.2500), 'population': 40000},
    'Kuala Kubu Bharu': {'coords': (3.5600, 101.6400), 'population': 30000},
    'Rawang': {'coords': (3.3200, 101.5800), 'population': 200000},
    'Banting': {'coords': (2.8100, 101.5000), 'population': 40000},
    'Sekinchan': {'coords': (3.5100, 101.1000), 'population': 15000},
    'Sabak Bernam': {'coords': (3.7700, 100.9800), 'population': 30000},
    'Seremban': {'coords': (2.7297, 101.9381), 'population': 500000},
    'Port Dickson': {'coords': (2.5228, 101.7967), 'population': 100000},
    'Nilai': {'coords': (2.8200, 101.8000), 'population': 100000},
    'Bahau': {'coords': (2.8000, 102.4000), 'population': 30000},
    'Tampin': {'coords': (2.4700, 102.2300), 'population': 30000},
    'Kuala Pilah': {'coords': (2.7400, 102.2500), 'population': 20000},
    'Melaka City': {'coords': (2.1896, 102.2501), 'population': 500000},
    'Ayer Keroh': {'coords': (2.2700, 102.2900), 'population': 60000},
    'Alor Gajah': {'coords': (2.3800, 102.2100), 'population': 40000},
    'Jasin': {'coords': (2.3100, 102.4300), 'population': 30000},
    'Johor Bahru': {'coords': (1.4927, 103.7414), 'population': 1500000},
    'Iskandar Puteri': {'coords': (1.4300, 103.6300), 'population': 500000},
    'Kulai': {'coords': (1.6600, 103.6000), 'population': 200000},
    'Pasir Gudang': {'coords': (1.4700, 103.9000), 'population': 200000},
    'Pengerang': {'coords': (1.3600, 104.1700), 'population': 30000},
    'Kota Tinggi': {'coords': (1.7300, 103.9000), 'population': 50000},
    'Mersing': {'coords': (2.4300, 103.8300), 'population': 30000},
    'Batu Pahat': {'coords': (1.8500, 102.9300), 'population': 300000},
    'Muar': {'coords': (2.0500, 102.5700), 'population': 200000},
    'Segamat': {'coords': (2.5100, 102.8100), 'population': 80000},
    'Kluang': {'coords': (2.0300, 103.3200), 'population': 150000},
    'Pontian': {'coords': (1.4800, 103.3800), 'population': 50000},
    'Desaru': {'coords': (1.5500, 104.2600), 'population': 15000},
    'Kota Bharu': {'coords': (6.1256, 102.2386), 'population': 500000},
    'Kubang Kerian': {'coords': (6.1000, 102.2800), 'population': 50000},
    'Pasir Puteh': {'coords': (5.8300, 102.4000), 'population': 30000},
    'Pasir Mas': {'coords': (6.0500, 102.1400), 'population': 40000},
    'Tumpat': {'coords': (6.2000, 102.1700), 'population': 30000},
    'Bachok': {'coords': (6.0700, 102.4000), 'population': 20000},
    'Kuala Krai': {'coords': (5.5300, 102.2000), 'population': 20000},
    'Gua Musang': {'coords': (4.8800, 101.9600), 'population': 15000},
    'Kuala Terengganu': {'coords': (5.3303, 103.1408), 'population': 400000},
    'Kemaman': {'coords': (4.2300, 103.4200), 'population': 60000},
    'Chukai': {'coords': (4.2200, 103.4200), 'population': 40000},
    'Kerteh': {'coords': (4.5200, 103.4500), 'population': 20000},
    'Paka': {'coords': (4.6400, 103.4400), 'population': 15000},
    'Dungun': {'coords': (4.7700, 103.4200), 'population': 40000},
    'Marang': {'coords': (5.2000, 103.2100), 'population': 20000},
    'Kuala Berang': {'coords': (5.0700, 102.9500), 'population': 15000},
    'Jerteh': {'coords': (5.7400, 102.5100), 'population': 30000},
    'Besut': {'coords': (5.7300, 102.5600), 'population': 25000},
    'Setiu': {'coords': (5.5800, 102.8000), 'population': 15000},
    'Kuantan': {'coords': (3.8077, 103.3260), 'population': 600000},
    'Pekan': {'coords': (3.4900, 103.3900), 'population': 50000},
    'Temerloh': {'coords': (3.4500, 102.4200), 'population': 100000},
    'Bentong': {'coords': (3.5200, 101.9100), 'population': 60000},
    'Raub': {'coords': (3.7900, 101.8600), 'population': 50000},
    'Kuala Lipis': {'coords': (4.1800, 102.0500), 'population': 20000},
    'Jerantut': {'coords': (3.9400, 102.3600), 'population': 30000},
    'Mentakab': {'coords': (3.4900, 102.3500), 'population': 40000},
    'Cameron Highlands': {'coords': (4.4700, 101.3800), 'population': 40000},
    'Genting Highlands': {'coords': (3.4200, 101.7900), 'population': 30000},
    'Kuala Rompin': {'coords': (2.8200, 103.4800), 'population': 20000},
    'Cherating': {'coords': (4.1300, 103.3900), 'population': 10000},
    'Balok': {'coords': (3.9500, 103.3700), 'population': 15000},
    'Gambang': {'coords': (3.7100, 103.0900), 'population': 20000},
    'Maran': {'coords': (3.5800, 102.7700), 'population': 15000},
}

SPACEPORT_FACILITY_TAGS = {
    'hospital': [('amenity', 'hospital'), ('amenity', 'clinic')],
    'airport': [('aeroway', 'aerodrome'), ('aeroway', 'airport'), ('aeroway', 'heliport')],
    'port': [('harbour', 'yes'), ('amenity', 'ferry_terminal'), ('waterway', 'port')],
    'power_plant': [('power', 'plant'), ('power', 'substation'), ('power', 'generator')],
    'road': [('highway', 'motorway'), ('highway', 'trunk'), ('highway', 'primary')],
    'railway': [('railway', 'rail'), ('railway', 'station')],
    'telecom': [('telecom', 'tower'), ('telecom', 'exchange'), ('man_made', 'tower')],
    'population_center': [('place', 'city'), ('place', 'town'), ('place', 'village')],
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Location:
    lat: float
    lon: float
    name: str = ""
    properties: Dict = field(default_factory=dict)

@dataclass
class AnalysisStep:
    step_number: int
    name: str
    description: str
    status: str = "pending"
    result: Any = None
    execution_time: float = 0.0
    reasoning: str = ""

@dataclass
class AnalysisResult:
    query: str
    steps: List[AnalysisStep] = field(default_factory=list)
    final_result: Any = None
    total_time: float = 0.0
    timestamp: str = ""
    success: bool = False

@dataclass
class MemoryEntry:
    query: str
    query_embedding: List[float] = field(default_factory=list)
    result_summary: str = ""
    success: bool = False
    execution_time: float = 0.0
    timestamp: str = ""
    parameters_used: Dict = field(default_factory=dict)

# ============================================================================
# MEMORY REPOSITORY
# ============================================================================

class MemoryRepository:
    def __init__(self, db_path: str = "west_malaysia_spaceport_memory.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL, query_hash TEXT NOT NULL,
                result_summary TEXT, success INTEGER, execution_time REAL,
                parameters TEXT, timestamp TEXT, embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL, parameter_name TEXT NOT NULL,
                optimal_value TEXT, success_rate REAL,
                usage_count INTEGER DEFAULT 1, last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_analysis(self, entry: MemoryEntry):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query_hash = hashlib.md5(entry.query.lower().encode()).hexdigest()
        cursor.execute("""
            INSERT INTO analysis_memory
            (query, query_hash, result_summary, success, execution_time, parameters, timestamp, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (entry.query, query_hash, entry.result_summary,
              1 if entry.success else 0, entry.execution_time,
              json.dumps(entry.parameters_used), entry.timestamp,
              pickle.dumps(entry.query_embedding)))
        conn.commit()
        conn.close()

    def get_all_analyses(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        results = [{
            'query': row[1], 'result_summary': row[3],
            'success': bool(row[4]), 'execution_time': row[5],
            'parameters': json.loads(row[6]) if row[6] else {},
            'timestamp': row[7]
        } for row in rows]
        conn.close()
        return results

    def find_similar_analyses(self, query: str, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        if not query or not query.strip():
            conn.close()
            return []
        keywords = query.lower().split()
        results = []
        for row in rows:
            stored_query = row[1].lower()
            match_score = sum(1 for kw in keywords if kw in stored_query)
            if match_score > 0:
                results.append({
                    'query': row[1], 'result_summary': row[3],
                    'success': bool(row[4]), 'execution_time': row[5],
                    'parameters': json.loads(row[6]) if row[6] else {},
                    'timestamp': row[7], 'match_score': match_score
                })
        conn.close()
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:limit]

    def get_learned_parameter(self, analysis_type: str, parameter_name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT optimal_value FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ?
            ORDER BY success_rate DESC LIMIT 1
        """, (analysis_type, parameter_name))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def update_learned_parameter(self, analysis_type: str, parameter_name: str,
                                  value: str, success: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, success_rate, usage_count FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ? AND optimal_value = ?
        """, (analysis_type, parameter_name, value))
        row = cursor.fetchone()
        if row:
            new_count = row[2] + 1
            new_rate = ((row[1] * row[2]) + (1 if success else 0)) / new_count
            cursor.execute("""
                UPDATE learned_parameters
                SET success_rate = ?, usage_count = ?, last_updated = ?
                WHERE id = ?
            """, (new_rate, new_count, datetime.now().isoformat(), row[0]))
        else:
            cursor.execute("""
                INSERT INTO learned_parameters
                (analysis_type, parameter_name, optimal_value, success_rate, usage_count, last_updated)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (analysis_type, parameter_name, value,
                  1.0 if success else 0.0, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_analysis_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_memory")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM analysis_memory WHERE success = 1")
        successful = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(execution_time) FROM analysis_memory")
        avg_time = cursor.fetchone()[0] or 0
        conn.close()
        return {
            'total_analyses': total, 'successful_analyses': successful,
            'success_rate': successful / total if total > 0 else 0,
            'avg_execution_time': avg_time
        }

# ============================================================================
# ANALYSIS STRATEGY
# ============================================================================

class AnalysisStrategy(ABC):
    @abstractmethod
    def analyse(self, location: Location, params: Dict) -> Dict: pass
    @abstractmethod
    def get_name(self) -> str: pass


class SpaceportSuitabilityStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Spaceport Suitability Analysis (HYBRID)"

    def _get_elevation_quick(self, location: Location) -> tuple:
        try:
            url = f"https://api.open-elevation.com/api/v1/lookup?locations={location.lat},{location.lon}"
            r = requests.get(url, timeout=3)
            elev = r.json()['results'][0]['elevation']
            if 50 <= elev <= 200: return 5.0, elev, 'Live Elevation API'
            elif 200 < elev <= 500: return 4.5, elev, 'Live Elevation API'
            elif 20 <= elev < 50: return 4.0, elev, 'Live Elevation API'
            elif 0 <= elev < 20: return 2.0, elev, 'Live Elevation API'
            else: return 3.0, elev, 'Live Elevation API'
        except Exception:
            lat, lon = location.lat, location.lon
            if 3.3 < lat < 4.6 and 101.3 < lon < 101.9:
                return 4.5, 1200, 'Fallback: Titiwangsa highlands'
            elif lat > 4.5 and 101.5 < lon < 102.5:
                return 3.5, 250, 'Fallback: Kelantan interior'
            elif 3.5 < lat < 4.6 and 101.9 < lon < 102.8:
                return 3.5, 300, 'Fallback: Pahang interior'
            elif lat < 2.5 and 102.5 < lon < 103.8:
                return 3.0, 80, 'Fallback: Johor interior'
            else:
                return 3.0, 30, 'Fallback: Coastal lowland'

    # ============ NEW: WEATHER (Open-Meteo, no API key) ============
    def _get_weather(self, location: Location) -> Optional[Dict]:
        """Fetch current wind & weather from Open-Meteo (free, no API key)."""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": location.lat,
                "longitude": location.lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,"
                           "wind_direction_10m,wind_gusts_10m",
                "wind_speed_unit": "ms",
                "timezone": "auto",
            }
            r = requests.get(url, params=params, timeout=4)
            data = r.json()
            cur = data.get("current", {})
            return {
                "temperature_c": cur.get("temperature_2m"),
                "humidity_pct": cur.get("relative_humidity_2m"),
                "wind_speed_ms": cur.get("wind_speed_10m"),
                "wind_direction_deg": cur.get("wind_direction_10m"),
                "wind_gust_ms": cur.get("wind_gusts_10m"),
                "source": "Open-Meteo (Live)",
                "time": cur.get("time"),
            }
        except Exception:
            return None

    def _score_wind(self, wind_speed_ms: Optional[float],
                    wind_gust_ms: Optional[float]) -> tuple:
        """Score wind conditions 0-5 and return explanation."""
        if wind_speed_ms is None:
            return 3.0, "Unknown", "Weather unavailable — neutral score"
        if wind_speed_ms < 4:
            return 5.0, "Excellent", f"Calm ({wind_speed_ms:.1f} m/s) — ideal for launches"
        elif wind_speed_ms < 6:
            return 4.5, "Good", f"Light breeze ({wind_speed_ms:.1f} m/s) — very suitable"
        elif wind_speed_ms < 8:
            return 4.0, "Good", f"Moderate wind ({wind_speed_ms:.1f} m/s) — manageable"
        elif wind_speed_ms < 12:
            return 3.0, "Moderate", f"Fairly windy ({wind_speed_ms:.1f} m/s) — schedule around it"
        else:
            return 2.0, "Poor", f"High wind ({wind_speed_ms:.1f} m/s) — challenging launches"

    def _geographic_score_coastal(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        if lon > 103.0: return 5.0, 0, 'Geographic: East coast (South China Sea)'
        elif lon > 102.5: return 4.5, 5, 'Geographic: Near east coast'
        elif lon > 101.5: return 3.5, 15, 'Geographic: Central'
        elif lon > 100.5: return 3.0, 25, 'Geographic: Near west coast'
        else: return 2.5, 5, 'Geographic: West coast (Strait of Malacca)'

    def _geographic_score_population(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        closest_pop = 0
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            dist = self._haversine(lat, lon, s_lat, s_lon)
            if dist < min_dist:
                min_dist = dist
                closest_pop = data['population']

        if min_dist > 60: return 5.0, 0.2, 'Geographic: Remote'
        elif min_dist > 35: return 4.0, 1.0, 'Geographic: Rural'
        elif min_dist > 20: return 3.0, 2.5, 'Geographic: Semi-rural'
        elif min_dist > 10: return 2.0, 5.0, 'Geographic: Near town'
        else: return 1.0, 12.0, 'Geographic: Near city'

    def _geographic_score_infrastructure(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, coords in STATIC_AIRPORTS.items():
            d = self._haversine(lat, lon, coords[0], coords[1])
            min_dist = min(min_dist, d)
        details = {
            'airports': 1 if min_dist < 60 else 0,
            'major_roads': 2 if min_dist < 30 else 0,
            'ports': 0, 'power_facilities': 0
        }
        if min_dist < 30: return 4.5, details, 'Geographic: Near airport'
        elif min_dist < 60: return 3.5, details, 'Geographic: Airport nearby'
        elif min_dist < 100: return 2.5, details, 'Geographic: Some access'
        else: return 1.5, details, 'Geographic: Remote'

    def _geographic_score_land(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            d = self._haversine(lat, lon, data['coords'][0], data['coords'][1])
            min_dist = min(min_dist, d)
        details = {
            'forest_areas': 30 if min_dist > 40 else 10,
            'developed_areas': 2 if min_dist > 40 else 10,
            'agriculture': 5
        }
        if min_dist > 60: return 5.0, details, 'Geographic: Abundant land'
        elif min_dist > 35: return 4.0, details, 'Geographic: Good land'
        elif min_dist > 20: return 3.0, details, 'Geographic: Moderate land'
        elif min_dist > 10: return 2.0, details, 'Geographic: Limited land'
        else: return 1.0, details, 'Geographic: Scarce land'

    def _geographic_score_flood(self, elevation_m: float) -> tuple:
        if elevation_m > 100: return 5.0, 'Low'
        elif elevation_m > 50: return 4.0, 'Low'
        elif elevation_m > 20: return 3.0, 'Moderate'
        else: return 1.5, 'High'

    def _score_latitudinal_advantage(self, lat: float) -> float:
        a = abs(lat)
        if a <= 1.5: return 5.0
        elif a <= 3: return 4.5
        elif a <= 5: return 4.0
        elif a <= 7: return 3.0
        else: return 2.0

    def _haversine(self, lat1, lon1, lat2, lon2) -> float:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(min(1, math.sqrt(a)))

    def _try_osm_in_background(self, location: Location, radius: int) -> Optional[Dict]:
        try:
            url = "https://overpass-api.de/api/interpreter"
            results = {}
            q = f'[out:json][timeout:5];(node["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon});way["aeroway"="aerodrome"](around:{radius},{location.lat},{location.lon}););out count;'
            results['airport_count'] = len(requests.post(url, data={'data': q}, timeout=5).json().get('elements', []))
            q = f'[out:json][timeout:5];(node["place"~"city|town|village"](around:{radius},{location.lat},{location.lon}););out count;'
            results['settlement_count'] = len(requests.post(url, data={'data': q}, timeout=5).json().get('elements', []))
            q = f'[out:json][timeout:5];(way["highway"~"motorway|trunk|primary"](around:{radius},{location.lat},{location.lon}););out count;'
            results['road_count'] = len(requests.post(url, data={'data': q}, timeout=5).json().get('elements', []))
            q = f'[out:json][timeout:5];(way["natural"="coastline"](around:{radius},{location.lat},{location.lon}););out count;'
            results['coastline_count'] = len(requests.post(url, data={'data': q}, timeout=5).json().get('elements', []))
            return results
        except Exception:
            return None

    def analyse(self, location: Location, params: Dict) -> Dict:
        radius = params.get('radius', 10000)
        weights = params.get('weights', {
            'elevation': 0.15,
            'population_density': 0.18,
            'coastal_proximity': 0.13,
            'infrastructure_access': 0.13,
            'land_availability': 0.13,
            'flood_risk': 0.10,
            'latitudinal_advantage': 0.08,
            'wind_conditions': 0.10,
        })

        scores, details = {}, {}
        data_source_details = []

        elevation_score, elevation_m, elev_source = self._get_elevation_quick(location)
        scores['elevation'] = elevation_score
        details['elevation'] = {'score': elevation_score, 'value': f"{elevation_m:.0f}m",
                                'weight': weights['elevation'], 'source': elev_source}
        data_source_details.append(f"Elevation: {elev_source}")

        pop_score, pop_density, pop_source = self._geographic_score_population(location)
        scores['population_density'] = pop_score
        details['population_density'] = {'score': pop_score,
                                         'value': f"{pop_density:.1f} people/km²",
                                         'weight': weights['population_density'], 'source': pop_source}
        data_source_details.append(f"Population: {pop_source}")

        coastal_score, dist_coast, coastal_source = self._geographic_score_coastal(location)
        scores['coastal_proximity'] = coastal_score
        details['coastal_proximity'] = {'score': coastal_score, 'value': f"{dist_coast:.1f}km",
                                        'weight': weights['coastal_proximity'], 'source': coastal_source}
        data_source_details.append(f"Coastal: {coastal_source}")

        infra_score, infra_details, infra_source = self._geographic_score_infrastructure(location)
        scores['infrastructure_access'] = infra_score
        details['infrastructure_access'] = {'score': infra_score, 'value': infra_details,
                                            'weight': weights['infrastructure_access'], 'source': infra_source}
        data_source_details.append(f"Infrastructure: {infra_source}")

        land_score, land_details, land_source = self._geographic_score_land(location)
        scores['land_availability'] = land_score
        details['land_availability'] = {'score': land_score, 'value': land_details,
                                        'weight': weights['land_availability'], 'source': land_source}
        data_source_details.append(f"Land: {land_source}")

        flood_score, flood_risk = self._geographic_score_flood(elevation_m)
        scores['flood_risk'] = flood_score
        details['flood_risk'] = {'score': flood_score, 'value': flood_risk,
                                 'weight': weights['flood_risk'], 'source': 'From elevation'}

        lat_score = self._score_latitudinal_advantage(location.lat)
        scores['latitudinal_advantage'] = lat_score
        details['latitudinal_advantage'] = {'score': lat_score,
                                            'value': f"{abs(location.lat):.1f}°N",
                                            'weight': weights['latitudinal_advantage'],
                                            'source': 'Geographic'}

        # ============ WIND / WEATHER ============
        weather_data = self._get_weather(location)
        if weather_data:
            ws = weather_data.get('wind_speed_ms')
            wg = weather_data.get('wind_gust_ms')
            wind_score, wind_rating, wind_explanation = self._score_wind(ws, wg)
            data_source_details.append(f"Wind: {wind_explanation}")
            weather_data['wind_rating'] = wind_rating
            weather_data['wind_explanation'] = wind_explanation
        else:
            wind_score, wind_rating, wind_explanation = 3.0, "Unknown", "Weather unavailable"
            data_source_details.append("Wind: Weather API unavailable — neutral score")

        scores['wind_conditions'] = wind_score
        details['wind_conditions'] = {
            'score': wind_score,
            'value': weather_data.get('wind_speed_ms') and f"{weather_data['wind_speed_ms']:.1f} m/s" or "N/A",
            'weight': weights['wind_conditions'],
            'source': weather_data.get('source', 'Unavailable') if weather_data else 'Unavailable'
        }

        # ============ BASE SCORE (0-100) ============
        total_score = sum(scores[k] * weights.get(k, 0) for k in scores if k in weights)
        max_possible = sum(weights.values()) * 5.0
        percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0

        # ============ CRITICAL PENALTIES ============
        penalty = 0.0
        penalty_reasons = []

        if elevation_m < 20:
            penalty += 15.0
            penalty_reasons.append(f"Very low elevation ({elevation_m:.0f}m): -15%")
        if flood_risk == 'High':
            penalty += 10.0
            penalty_reasons.append("High flood risk: -10%")
        if pop_density > 5:
            penalty += 10.0
            penalty_reasons.append(f"High population density: -10%")

        if isinstance(land_details, dict) and land_details.get('developed_areas', 0) >= 10:
            penalty += 8.0
            penalty_reasons.append("Scarce land availability: -8%")

        if weather_data and weather_data.get('wind_speed_ms'):
            if weather_data['wind_speed_ms'] > 12:
                penalty += 8.0
                penalty_reasons.append(f"Very high wind ({weather_data['wind_speed_ms']:.1f} m/s): -8%")

        percentage = max(0.0, min(100.0, percentage - penalty))

        if percentage >= 80:
            rating, emoji, rec = 'Excellent', '🚀', 'Highly recommended for spaceport development'
        elif percentage >= 65:
            rating, emoji, rec = 'Good', '👍', 'Suitable with minor site preparation'
        elif percentage >= 50:
            rating, emoji, rec = 'Moderate', '👌', 'Suitable with significant site preparation'
        elif percentage >= 35:
            rating, emoji, rec = 'Limited', '⚠️', 'Marginal - requires major investment'
        else:
            rating, emoji, rec = 'Poor', '❌', 'Not recommended for spaceport development'

        osm_data = None
        osm_available = False
        try:
            osm_data = self._try_osm_in_background(location, radius)
            if osm_data and any(v > 0 for v in osm_data.values()):
                osm_available = True
                data_source_details.append(
                    f"🌐 OSM Background: Found {osm_data.get('airport_count', 0)} airports, "
                    f"{osm_data.get('settlement_count', 0)} settlements")
        except Exception:
            pass

        return {
            'success': True, 'scores': scores, 'details': details,
            'weighted_score': total_score, 'max_possible_score': max_possible,
            'suitability_percentage': round(percentage, 1),
            'base_percentage': round((total_score / max_possible * 100) if max_possible > 0 else 0, 1),
            'penalty_applied': round(penalty, 1),
            'penalty_reasons': penalty_reasons,
            'rating': rating, 'rating_emoji': emoji, 'recommendation': rec,
            'radius_used': radius,
            'location': f"{location.name or 'West Malaysia location'} ({location.lat:.4f}, {location.lon:.4f})",
            'elevation_m': elevation_m, 'population_density': pop_density,
            'coastal_distance_km': dist_coast, 'flood_risk': flood_risk,
            'lat_deg': abs(location.lat),
            'data_source_details': data_source_details,
            'used_osm': osm_available, 'osm_data': osm_data if osm_available else None,
            'weather': weather_data,
            'wind_speed_ms': weather_data.get('wind_speed_ms') if weather_data else None,
            'wind_gust_ms': weather_data.get('wind_gust_ms') if weather_data else None,
            'wind_direction_deg': weather_data.get('wind_direction_deg') if weather_data else None,
            'temperature_c': weather_data.get('temperature_c') if weather_data else None,
            'humidity_pct': weather_data.get('humidity_pct') if weather_data else None,
            'used_fallback': True, 'from_cache': False,
            'analysis_method': 'HYBRID: Geographic Rules + OSM + Weather'
        }


class ProximityAnalysisStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Proximity Analysis"

    def analyse(self, location: Location, params: Dict) -> Dict:
        amenity_type = params.get('amenity_type', 'hospital')
        radius = params.get('radius', 5000)
        tags = SPACEPORT_FACILITY_TAGS.get(amenity_type, [('amenity', amenity_type)])
        parts = []
        for k, v in tags:
            parts.append(f'node["{k}"="{v}"](around:{radius},{location.lat},{location.lon});')
            parts.append(f'way["{k}"="{v}"](around:{radius},{location.lat},{location.lon});')
        query = f"[out:json][timeout:45];({chr(10).join(parts)});out center;"
        try:
            r = requests.post("https://overpass-api.de/api/interpreter",
                              data={'data': query},
                              headers={'User-Agent': 'WMSpaceport/1.0'}, timeout=45)
            r.raise_for_status()
            results, seen = [], set()
            for elem in r.json().get('elements', []):
                lat = elem.get('lat') or elem.get('center', {}).get('lat')
                lon = elem.get('lon') or elem.get('center', {}).get('lon')
                if lat and lon:
                    key = f"{round(lat,5)}_{round(lon,5)}"
                    if key not in seen:
                        seen.add(key)
                        tags_d = elem.get('tags', {})
                        results.append({
                            'name': tags_d.get('name', tags_d.get('brand', 'Unknown')),
                            'lat': lat, 'lon': lon, 'type': amenity_type, 'tags': tags_d
                        })
            return {'success': True, 'count': len(results), 'amenities': results,
                    'radius': radius, 'amenity_type': amenity_type,
                    'location': f"West Malaysia ({location.lat:.4f}, {location.lon:.4f})"}
        except Exception as e:
            return {'success': False, 'error': str(e), 'amenities': [],
                    'count': 0, 'radius': radius, 'amenity_type': amenity_type}


class StrategySelector:
    _strategies = {'spaceport': SpaceportSuitabilityStrategy,
                   'proximity': ProximityAnalysisStrategy}

    @classmethod
    def get_strategy(cls, t: str) -> AnalysisStrategy:
        c = cls._strategies.get(t)
        if not c: raise ValueError(f"Unknown strategy: {t}")
        return c()

# ============================================================================
# PIPELINE + RATE LIMITER
# ============================================================================

class PipelineStep:
    def __init__(self, name, processor, description=""):
        self.name = name; self.processor = processor
        self.description = description; self.execution_time = 0.0; self.result = None

class Pipeline:
    def __init__(self, name):
        self.name = name; self.steps = []; self.results = {}
        self.execution_log = []
    def add_step(self, s): self.steps.append(s); return self
    def execute(self, initial_data, progress_callback=None):
        current = initial_data.copy()
        total = len(self.steps)
        for i, step in enumerate(self.steps):
            a = AnalysisStep(step_number=i+1, name=step.name,
                             description=step.description, status="running")
            if progress_callback: progress_callback(i/total, f"Running: {step.name}")
            t0 = time.time()
            try:
                step.result = step.processor(current)
                current.update(step.result)
                self.results[step.name] = step.result
                step.execution_time = time.time() - t0
                a.status = "completed"; a.result = step.result
                a.execution_time = step.execution_time
                a.reasoning = f"Successfully processed {step.name}"
            except Exception as e:
                step.execution_time = time.time() - t0
                a.status = "failed"; a.reasoning = f"Error: {e}"
                self.execution_log.append(a); raise
            self.execution_log.append(a)
        if progress_callback: progress_callback(1.0, "Complete")
        return current

class RateLimiter:
    def __init__(self, calls_per_second=0.5):
        self.calls_per_second = calls_per_second; self.last_call = 0
    def wait(self):
        now = time.time()
        delta = now - self.last_call
        min_i = 1.0 / self.calls_per_second
        if delta < min_i: time.sleep(min_i - delta)
        self.last_call = time.time()

# ============================================================================
# AGENT
# ============================================================================

class WestMalaysiaSpaceportGeoAIAgent:
    def __init__(self):
        self.memory_repo = MemoryRepository()
        self.rate_limiter = RateLimiter(0.5)
        self.short_term_memory = {}
        self.current_analysis = None

    def reason_about_query(self, query: str) -> tuple:
        ql = query.lower()
        steps = [{'step': 'Understanding Query',
                  'reasoning': f"Analysing spaceport site selection request: '{query}'",
                  'action': 'parse_intent'}]
        similar = self.memory_repo.find_similar_analyses(query, 3)
        if similar:
            steps.append({'step': 'Memory Recall',
                          'reasoning': f"Found {len(similar)} similar past analyses.",
                          'action': 'apply_learned_parameters'})
        analysis_type = 'spaceport'
        steps.append({'step': 'Strategy Selection',
                      'reasoning': 'Using Spaceport Suitability strategy.',
                      'action': 'use_spaceport_strategy'})
        lr = self.memory_repo.get_learned_parameter(analysis_type, 'radius')
        if lr:
            steps.append({'step': 'Parameter Optimisation',
                          'reasoning': f"Using learned radius {lr}m.",
                          'action': 'apply_learned_radius', 'value': lr})
        else:
            steps.append({'step': 'Parameter Selection',
                          'reasoning': 'Using default radius 10000m.',
                          'action': 'use_default_radius', 'value': '10000'})
        steps.append({'step': 'Execution Planning',
                      'reasoning': f'Will execute {analysis_type} analysis.',
                      'action': 'prepare_execution'})
        return steps, analysis_type

    def execute_analysis(self, location, query, params, progress_callback=None):
        t0 = time.time()
        result = AnalysisResult(query=query, timestamp=datetime.now().isoformat())
        reasoning, atype = self.reason_about_query(query)
        for i, si in enumerate(reasoning):
            result.steps.append(AnalysisStep(step_number=i+1, name=si['step'],
                                             description=si['reasoning'],
                                             status='completed', reasoning=si['reasoning']))
        if progress_callback: progress_callback(0.3, "Executing analysis...")
        try:
            strategy = StrategySelector.get_strategy(atype)
            self.rate_limiter.wait()
            ar = strategy.analyse(location, params)
            ar['from_cache'] = False
            if ar.get('success'):
                used_osm = ar.get('used_osm', False)
                result.steps.append(AnalysisStep(
                    step_number=len(result.steps)+1, name="Data Source Validation",
                    description=f"Method: {ar.get('analysis_method','HYBRID')}",
                    status='completed',
                    reasoning=f"Used {'OSM + Geographic' if used_osm else 'Geographic'} rules"))
            result.steps.append(AnalysisStep(
                step_number=len(result.steps)+1,
                name=f"Execute {strategy.get_name()}",
                description=f"Running {atype} on {location.name or 'location'}",
                status='completed' if ar.get('success') else 'failed',
                result=ar, reasoning=f"Returned {len(str(ar))} bytes"))
            result.final_result = ar
            result.success = ar.get('success', False)
        except Exception as e:
            result.steps.append(AnalysisStep(
                step_number=len(result.steps)+1, name="Analysis Execution",
                description="Executing spatial analysis", status='failed',
                reasoning=f"Error: {e}"))
            result.success = False
        if progress_callback: progress_callback(0.8, "Storing in memory...")
        result.total_time = time.time() - t0
        self.memory_repo.store_analysis(MemoryEntry(
            query=query,
            result_summary=str(result.final_result)[:500] if result.final_result else "",
            success=result.success, execution_time=result.total_time,
            timestamp=result.timestamp, parameters_used=params))
        if result.success:
            self.memory_repo.update_learned_parameter(
                atype, 'radius', str(params.get('radius', 10000)), True)
        self.short_term_memory['last_analysis'] = result
        self.short_term_memory['last_location'] = location
        if progress_callback: progress_callback(1.0, "Complete")
        return result

# ============================================================================
# UI HELPERS
# ============================================================================

def render_region_selector():
    regions = {
        '🌏 All West Malaysia': 'all',
        '🏝️ Northern (Perlis, Kedah, Penang, Perak)': 'north',
        '🏙️ Central (Selangor, KL, Putrajaya, N. Sembilan)': 'central',
        '🌴 Southern (Melaka, Johor)': 'south',
        '🌊 East Coast (Kelantan, Terengganu, Pahang)': 'east',
        '🚀 Spaceport Candidates': 'candidates'
    }
    sel = st.selectbox("Select Region", options=list(regions.keys()), index=0)
    rk = regions[sel]
    north = ['Perlis', 'Kedah', 'Penang', 'Perak']
    central = ['Selangor', 'Kuala Lumpur', 'Putrajaya', 'Negeri Sembilan']
    south = ['Melaka', 'Johor']
    east = ['Kelantan', 'Terengganu', 'Pahang']
    if rk == 'all':
        locs = WEST_MALAYSIA_LOCATIONS
        st.info(f"🌏 Showing {len(locs)} locations across West Malaysia")
    elif rk == 'candidates':
        locs = WEST_MALAYSIA_SPACEPORT_CANDIDATES
        st.info(f"🚀 Showing {len(locs)} spaceport candidate sites")
    else:
        sl = {'north': north, 'central': central, 'south': south, 'east': east}[rk]
        locs = {k: v for k, v in WEST_MALAYSIA_LOCATIONS.items()
                if any(f"({s})" in k for s in sl)}
        st.info(f"📍 Showing {len(locs)} locations in {sel}")
    return locs, rk


def init_session_state():
    if 'agent' not in st.session_state:
        st.session_state.agent = WestMalaysiaSpaceportGeoAIAgent()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = Location(
            lat=1.3600, lon=104.1700, name="Pengerang, Johor")
    if 'reasoning_log' not in st.session_state:
        st.session_state.reasoning_log = []
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    if 'basemap_choice' not in st.session_state:
        st.session_state.basemap_choice = "OpenStreetMap"
    if 'show_radius_circle' not in st.session_state:
        st.session_state.show_radius_circle = True
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'candidate_scores' not in st.session_state:
        st.session_state.candidate_scores = {}


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.2rem; font-family: 'Courier New', monospace;
                 background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 font-weight: 900; letter-spacing: 3px;">SPACEPORT</div>
            <div style="color: #00f0ff; font-size: 0.75rem; font-family: 'Courier New', monospace;
                 letter-spacing: 5px;">WEST MALAYSIA</div>
            <div class="cyber-divider"></div>
        </div>
        """, unsafe_allow_html=True)

        cache_stats = api_cache.get_stats()
        st.markdown(f"""
        <div style="color: #a0a0c0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             letter-spacing: 1px; text-align: center; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; padding: 4px 8px; margin-bottom: 10px;">
            ⚡ CACHE: {cache_stats['total_cached']} RESPONSES
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚡ LOCATION SELECTOR</div>""", unsafe_allow_html=True)

        locations, region = render_region_selector()
        quick = st.selectbox("Select Location", list(locations.keys()), index=0)
        if st.button("⚡ GO TO LOCATION", use_container_width=True):
            coords = locations[quick]
            st.session_state.selected_location = Location(
                lat=coords[0], lon=coords[1], name=quick)
            st.rerun()
        st.caption("Or click on the map to select any location")
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🗺️ MAP SETTINGS</div>""", unsafe_allow_html=True)
        basemap_choice = st.radio(
            "Map Style",
            options=["🗺️ OpenStreetMap", "🛰️ Satellite"],
            index=0 if st.session_state.basemap_choice == "OpenStreetMap" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        if "Satellite" in basemap_choice:
            st.session_state.basemap_choice = "Satellite"
        else:
            st.session_state.basemap_choice = "OpenStreetMap"
        st.session_state.show_radius_circle = st.checkbox("Show Search Radius", value=True)
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            ⚙️ ANALYSIS PARAMETERS</div>""", unsafe_allow_html=True)
        radius = st.slider("Assessment Radius (m)", 2000, 20000, 10000, 1000)
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            📊 SITE RANKING</div>""", unsafe_allow_html=True)

        if st.session_state.current_results:
            rd = st.session_state.current_results
            if 'suitability_percentage' in rd:
                pct = rd['suitability_percentage']; rating = rd['rating']
                color = ("#39ff14" if pct >= 80 else "#00f0ff" if pct >= 65
                         else "#ff2d95" if pct >= 50 else "#ff6600")
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(0, 240, 255, 0.2);
                     border-radius: 8px; background: rgba(0, 240, 255, 0.05);">
                    <div style="font-size: 2.5rem; font-weight: 900; color: {color};
                         font-family: 'Courier New', monospace;">{pct}%</div>
                    <div style="color: #d0d0e8; font-family: 'Courier New', monospace;
                         letter-spacing: 2px; font-size: 0.8rem;">{rating}</div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; margin-top: 5px;">
                        {rd['recommendation'][:50]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if rd.get('used_osm'):
                    tag, tcol = "🌐 OSM + 🌤️ WEATHER LIVE", "#39ff14"
                else:
                    tag, tcol = "📍 GEOGRAPHIC RULES", "#00f0ff"
                st.markdown(f"""
                <div style="color: {tcol}; font-family: 'Courier New', monospace;
                     font-size: 0.7rem; letter-spacing: 1px; text-align: center;
                     border: 1px solid {tcol}; border-radius: 4px; padding: 2px 8px;
                     margin-top: 8px;">{tag}</div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run an analysis to see site ranking")

        if st.button("🔄 COMPARE ALL", use_container_width=True):
            st.session_state.comparison_mode = True; st.rerun()
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("Results cleared!"); st.rerun()
        if st.button("🗑️ CLEAR CACHE", use_container_width=True):
            api_cache.clear(); st.success("Cache cleared!"); st.rerun()
        st.divider()

        st.markdown("""<div style="color: #00f0ff; font-family: 'Courier New', monospace;
             letter-spacing: 2px; font-size: 0.9rem; margin-bottom: 10px;">
            🧠 AGENT MEMORY</div>""", unsafe_allow_html=True)
        stats = st.session_state.agent.memory_repo.get_analysis_stats()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div style="text-align:center;padding:8px;
                 border:1px solid rgba(0,240,255,0.1);border-radius:4px;">
                <div style="color:#8080a0;font-family:'Courier New',monospace;font-size:0.6rem;">
                     ANALYSES</div>
                <div style="color:#00f0ff;font-family:'Courier New',monospace;
                     font-size:1.2rem;font-weight:bold;">{stats['total_analyses']}</div></div>""",
                unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div style="text-align:center;padding:8px;
                 border:1px solid rgba(0,240,255,0.1);border-radius:4px;">
                <div style="color:#8080a0;font-family:'Courier New',monospace;font-size:0.6rem;">
                     SUCCESS RATE</div>
                <div style="color:#39ff14;font-family:'Courier New',monospace;
                     font-size:1.2rem;font-weight:bold;">{stats['success_rate']*100:.0f}%</div></div>""",
                unsafe_allow_html=True)
        st.markdown(f"""<div style="text-align:center;padding:8px;
             border:1px solid rgba(0,240,255,0.1);border-radius:4px;margin-top:8px;">
            <div style="color:#8080a0;font-family:'Courier New',monospace;font-size:0.6rem;">
                 AVG EXECUTION</div>
            <div style="color:#b026ff;font-family:'Courier New',monospace;
                 font-size:1.2rem;font-weight:bold;">{stats['avg_execution_time']:.2f}s</div></div>""",
            unsafe_allow_html=True)
        if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
            Path("west_malaysia_spaceport_memory.db").unlink(missing_ok=True)
            st.session_state.agent = WestMalaysiaSpaceportGeoAIAgent()
            st.session_state.analysis_history = []
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.success("All memory cleared!"); st.rerun()
        return {'radius': radius}


def get_tiles_for_basemap(basemap_choice: str) -> str:
    if basemap_choice == "Satellite":
        return "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    return "OpenStreetMap"


def render_map(params):
    st.subheader("🗺️ West Malaysia Spaceport Site Map")
    center = [4.2, 102.0]
    name = "West Malaysia"
    if st.session_state.selected_location:
        center = [st.session_state.selected_location.lat, st.session_state.selected_location.lon]
        name = st.session_state.selected_location.name or "West Malaysia Location"

    basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
    tiles_url = get_tiles_for_basemap(basemap_choice)

    try:
        if basemap_choice == "Satellite":
            m = folium.Map(location=center, zoom_start=7,
                           tiles=tiles_url, attr='Esri World Imagery')
        else:
            m = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    except Exception:
        m = folium.Map(location=center, zoom_start=7)

    if st.session_state.selected_location:
        mc = 'red'
        rd = st.session_state.get('current_results', None)
        if rd and 'suitability_percentage' in rd:
            pct = rd['suitability_percentage']
            mc = ('green' if pct >= 80 else 'lightgreen' if pct >= 65
                  else 'orange' if pct >= 50 else 'lightred' if pct >= 35 else 'red')
        folium.Marker(center, popup=f"<b>🚀 {name}</b><br>Lat: {center[0]:.6f}<br>Lon: {center[1]:.6f}<br>🇲🇾 West Malaysia",
                      tooltip="🚀 Candidate Site",
                      icon=folium.Icon(color=mc, icon='rocket', prefix='fa')).add_to(m)
        if st.session_state.get('show_radius_circle', True):
            folium.Circle(center, radius=params.get('radius', 10000),
                          color='#2ecc71', fill=True, fillColor='#2ecc71',
                          fillOpacity=0.1, weight=2,
                          tooltip=f"Assessment radius: {params.get('radius',10000)}m").add_to(m)

    rd = st.session_state.get('current_results', None)
    if rd and 'suitability_percentage' in rd:
        pct = rd['suitability_percentage']; rating = rd.get('rating', 'Unknown')
        rec = rd.get('recommendation', '')
        color = ('green' if pct >= 80 else 'lightgreen' if pct >= 65
                 else 'orange' if pct >= 50 else 'lightred' if pct >= 35 else 'red')
        folium.Circle(center, radius=params.get('radius', 10000), color=color,
                      fill=True, fillColor=color, fillOpacity=0.15, weight=3,
                      tooltip=f"🚀 {rating} ({pct}%)\n{rec}").add_to(m)
    try: Fullscreen(position='topleft').add_to(m)
    except Exception: pass
    try: MiniMap(toggle_display=True, position='bottomright').add_to(m)
    except Exception: pass
    try: MousePosition(position='bottomleft', prefix='West MY Coords: ').add_to(m)
    except Exception: pass

    md = st_folium(m, width=None, height=500, use_container_width=True)
    if md and md.get('last_clicked'):
        clat = md['last_clicked']['lat']; clon = md['last_clicked']['lng']
        if (st.session_state.selected_location is None or
                abs(st.session_state.selected_location.lat - clat) > 0.0001 or
                abs(st.session_state.selected_location.lon - clon) > 0.0001):
            st.session_state.selected_location = Location(lat=clat, lon=clon, name="West Malaysia Location")
            st.rerun()
    if rd and 'suitability_percentage' in rd:
        tag = "🌐 OSM + 🌤️ Weather" if rd.get('used_osm') else "📍 Geographic Rules"
        st.success(f"🚀 {rd['rating']} Suitability: {rd['suitability_percentage']}% ({tag})")
        st.info(f"💡 {rd['recommendation']}")


def render_query_interface(params):
    st.subheader("💬 Natural Language Query")
    with st.expander("💡 Example Spaceport Queries", expanded=False):
        st.markdown("""
        **🚀 Spaceport Site Selection:**
        - "Find the best location for a spaceport in West Malaysia"
        - "Which site has the best launch characteristics?"
        - "Compare all candidate sites for spaceport development"
        - "What are the advantages of Pengerang for a spaceport?"
        - "How windy is this site?"
        """)
    query = st.text_area("Describe what you want to analyse for spaceport site selection:",
                         placeholder="e.g., Find the best location for a spaceport in West Malaysia",
                         height=100)
    c1, c2, _ = st.columns([1, 1, 2])
    with c1: analyse_btn = st.button("🚀 ANALYSE SITE", type="primary", use_container_width=True)
    with c2: clear_btn = st.button("🧹 CLEAR", use_container_width=True)
    if clear_btn:
        st.session_state.current_results = None
        st.session_state.reasoning_log = []
        st.rerun()
    if analyse_btn and st.session_state.selected_location:
        with st.spinner("🧠 HYBRID: INSTANT results + OSM + weather..."):
            pb = st.progress(0); stx = st.empty()
            def upd(p, s): pb.progress(p); stx.text(s)
            result = st.session_state.agent.execute_analysis(
                st.session_state.selected_location,
                query if query else "Evaluate this site for spaceport development",
                params, progress_callback=upd)
            st.session_state.analysis_history.append(result)
            st.session_state.reasoning_log = result.steps
            st.session_state.current_results = result.final_result
            pb.empty(); stx.empty()
            if result.success:
                st.success(f"✅ Analysis complete in {result.total_time:.2f}s"); st.rerun()
            else:
                st.error("❌ Analysis failed. Check reasoning log.")
    elif analyse_btn and not st.session_state.selected_location:
        st.warning("Please select a location in West Malaysia first!")


def render_reasoning_log():
    st.subheader("🧠 Agent Reasoning (Chain of Thought)")
    if not st.session_state.reasoning_log:
        st.info("Run a spaceport site analysis to see the agent's reasoning.")
        return
    for step in st.session_state.reasoning_log:
        icon = "✅" if step.status == "completed" else "❌" if step.status == "failed" else "⏳"
        with st.expander(f"{icon} Step {step.step_number}: {step.name}", expanded=True):
            st.write(f"**Reasoning:** {step.reasoning}")
            if step.execution_time > 0:
                st.write(f"**Execution Time:** {step.execution_time:.3f}s")
            if step.result and step.name.startswith("Execute"):
                st.json(step.result)


def render_results():
    st.subheader("🚀 Spaceport Site Analysis Results")
    if not st.session_state.analysis_history:
        st.info("No analysis results yet.")
        return
    lr = st.session_state.analysis_history[-1]
    if not lr.final_result:
        st.warning("No results available."); return
    rd = lr.final_result
    if not rd.get('success', False):
        st.error(f"Analysis failed: {rd.get('error', 'Unknown error')}"); return

    if 'suitability_percentage' in rd:
        if rd.get('used_osm', False):
            st.success("🌐 **HYBRID: OSM + Weather + Geographic Rules**")
        else:
            st.success("📍 **Geographic Rules (INSTANT)** - OSM unavailable")

        if rd.get('penalty_applied', 0) > 0:
            with st.expander(f"⚠️ Score Penalty Applied: -{rd['penalty_applied']}%"):
                st.write(f"**Base score:** {rd.get('base_percentage', 0)}%")
                st.write(f"**Penalty:** -{rd['penalty_applied']}%")
                st.write("**Reasons:**")
                for r in rd.get('penalty_reasons', []):
                    st.warning(r)
                st.write(f"**Final score:** {rd['suitability_percentage']}%")

        if 'data_source_details' in rd:
            with st.expander("📊 Data Sources Used"):
                for d in rd['data_source_details']:
                    if '🌐' in d: st.success(f"🌐 {d}")
                    elif 'Wind' in d: st.info(f"🌬️ {d}")
                    elif 'Geographic' in d: st.info(f"📍 {d}")
                    elif 'Fallback' in d: st.warning(f"⚠️ {d}")
                    else: st.success(f"✅ {d}")

        # Weather expander
        weather = rd.get('weather')
        if weather:
            with st.expander("🌤️ Live Weather Data (Open-Meteo)", expanded=False):
                wc1, wc2, wc3 = st.columns(3)
                with wc1:
                    if weather.get('wind_speed_ms') is not None:
                        st.metric("💨 Wind Speed", f"{weather['wind_speed_ms']:.1f} m/s",
                                  delta=weather.get('wind_rating', ''))
                    if weather.get('temperature_c') is not None:
                        st.metric("🌡️ Temperature", f"{weather['temperature_c']:.1f}°C")
                with wc2:
                    if weather.get('wind_gust_ms') is not None:
                        st.metric("🌪️ Wind Gust", f"{weather['wind_gust_ms']:.1f} m/s")
                    if weather.get('humidity_pct') is not None:
                        st.metric("💧 Humidity", f"{weather['humidity_pct']:.0f}%")
                with wc3:
                    if weather.get('wind_direction_deg') is not None:
                        dirs = ['N','NE','E','SE','S','SW','W','NW']
                        deg = weather['wind_direction_deg']
                        compass = dirs[int((deg + 22.5) % 360 // 45)]
                        st.metric("🧭 Wind Direction", f"{compass} ({deg:.0f}°)")
                if weather.get('wind_explanation'):
                    st.caption(f"**Assessment:** {weather['wind_explanation']}")

        if rd.get('used_osm', False) and rd.get('osm_data'):
            with st.expander("🌐 OSM Data Found (Up-to-Date)"):
                st.json(rd['osm_data'])

        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.metric("🚀 Spaceport Suitability", f"{rd['suitability_percentage']}%",
                      delta=f"{rd['rating']} {rd['rating_emoji']}")
            st.caption(rd['recommendation'])
        with c2:
            st.metric("Elevation", f"{rd.get('elevation_m', 0):.0f}m")
        with c3:
            st.metric("Latitude", f"{rd.get('lat_deg', 0):.1f}°N")
        with c4:
            ws = rd.get('wind_speed_ms')
            st.metric("💨 Wind", f"{ws:.1f} m/s" if ws is not None else "N/A")

        st.write("---")
        st.write("**Detailed Scoring Breakdown:**")
        details = rd.get('details', {}); scores = rd.get('scores', {})
        score_data = []
        for k, d in details.items():
            w = d.get('weight', 0); sc = scores.get(k, 0)
            src = d.get('source', 'Unknown')
            emoji = ('📍' if 'Geographic' in src else '✅' if 'Live' in src
                     else '🌤️' if 'Open-Meteo' in src
                     else '⚠️' if 'Fallback' in src else 'ℹ️')
            score_data.append({
                'Criteria': k.replace('_', ' ').title(),
                'Score': f"{sc:.1f}/5", 'Value': d.get('value', 'N/A'),
                'Weight': f"{w*100:.0f}%", 'Weighted': f"{sc*w:.2f}",
                'Source': f"{emoji} {src[:35]}{'...' if len(src) > 35 else ''}"
            })
        st.dataframe(pd.DataFrame(score_data), use_container_width=True, hide_index=True)
        chart = pd.DataFrame([{'Criteria': r['Criteria'], 'Score': float(r['Score'].split('/')[0])}
                              for r in score_data])
        st.bar_chart(chart.set_index('Criteria'))

        st.write("---")
        st.write("**📋 Detailed Recommendation Strategy**")
        recs = generate_recommendation_strategy(rd)

        risk = recs.get('risk_level', 'Unknown')
        risk_color = ('#ff2d95' if risk in ('High', 'Very High')
                      else '#39ff14' if risk == 'Low' else '#ffe84d')

        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">🎯 Overall Feasibility</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace;
                 font-size: 1.1rem; padding: 10px;">
                {recs.get('overall_feasibility', 'Assessment not available')}
            </div>
            <div style="display: flex; gap: 20px; margin-top: 12px; flex-wrap: wrap;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1);
                     padding: 8px 15px; border-radius: 8px;">
                    💰 Investment: <span style="color: #00f0ff; font-weight: bold;">
                    {recs.get('investment_required', 'Unknown')}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3);
                     padding: 8px 15px; border-radius: 8px;">
                    ⚠️ Risk Level: <span style="color: {risk_color}; font-weight: bold;">
                    {risk}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3);
                     padding: 8px 15px; border-radius: 8px;">
                    🚨 Critical Actions: <span style="color: #ff2d95; font-weight: bold;">
                    {recs.get('critical_action_count', 0)}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1);
                     padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Immediate: <span style="color: #39ff14; font-weight: bold;">
                    {recs['timeline_summary']['immediate']}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1);
                     padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Short-term: <span style="color: #ffe84d; font-weight: bold;">
                    {recs['timeline_summary']['short_term']}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1);
                     padding: 8px 15px; border-radius: 8px;">
                    ⏱️ Long-term: <span style="color: #b026ff; font-weight: bold;">
                    {recs['timeline_summary']['long_term']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for bucket, title in [
            ('immediate_actions', '🔴 IMMEDIATE ACTIONS (0-6 Months)'),
            ('short_term_actions', '🟡 SHORT-TERM ACTIONS (6-18 Months)'),
            ('long_term_actions', '🟢 LONG-TERM ACTIONS (18-36 Months)')
        ]:
            if recs[bucket]:
                st.markdown(f"""<div class="recommendation-container">
                    <div class="recommendation-title">{title}</div>""", unsafe_allow_html=True)
                for a in recs[bucket]:
                    st.markdown(f"""
                    <div class="recommendation-item">
                        <span class="icon">{a.get('priority', '')}</span>
                        {a['text']}
                        <span style="float: right; color: #8080a0; font-size: 0.8rem;">
                            {a.get('cost', '')}</span>
                    </div>""", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">💰 Investment Summary</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; padding: 10px;">
                <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 150px;">
                        <div style="color: #8080a0; font-size: 0.7rem;">TOTAL INVESTMENT</div>
                        <div style="font-size: 1.2rem; font-weight: bold;
                             color: {'#ff2d95' if recs.get('investment_required') == 'Very High'
                                     else '#ffe84d' if recs.get('investment_required') == 'Moderate'
                                     else '#39ff14'}">
                            {recs.get('investment_required', 'Unknown')}
                        </div>
                    </div>
                    <div style="flex: 2; min-width: 200px;">
                        <div style="color: #8080a0; font-size: 0.7rem;">ACTION ITEMS</div>
                        <div style="font-size: 1rem;">
                            {len(recs['immediate_actions'])} Immediate •
                            {len(recs['short_term_actions'])} Short-term •
                            {len(recs['long_term_actions'])} Long-term
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        st.write("**📋 Summary**")
        rating = rd.get('rating', 'Unknown'); emoji = rd.get('rating_emoji', '')
        rec = rd.get('recommendation', '')
        if rating in ['Excellent', 'Good']:
            st.success(f"{emoji} **{rating}** - {rec}")
            st.write("This site has strong potential for spaceport development.")
        elif rating == 'Moderate':
            st.warning(f"{emoji} **{rating}** - {rec}")
            st.write("This site requires significant investment and site preparation.")
        else:
            st.error(f"{emoji} **{rating}** - {rec}")
            st.write("This site may not be suitable for spaceport development.")


def render_comparison_mode():
    st.subheader("🔄 Site Comparison Dashboard")
    with st.spinner("Analysing all candidate sites (HYBRID + Weather)..."):
        results = []
        pb = st.progress(0); stx = st.empty()
        for i, (name, coords) in enumerate(WEST_MALAYSIA_SPACEPORT_CANDIDATES.items()):
            stx.text(f"Analysing: {name}")
            pb.progress((i + 1) / len(WEST_MALAYSIA_SPACEPORT_CANDIDATES))
            loc = Location(lat=coords[0], lon=coords[1], name=name)
            try:
                strategy = StrategySelector.get_strategy('spaceport')
                r = strategy.analyse(loc, {'radius': 10000})
                if r.get('success'):
                    results.append({
                        'Site': name, 'Suitability %': r['suitability_percentage'],
                        'Rating': r['rating'], 'Elevation (m)': r.get('elevation_m', 0),
                        'Wind (m/s)': r.get('wind_speed_ms') if r.get('wind_speed_ms') is not None else 'N/A',
                        'Flood Risk': r.get('flood_risk', 'Unknown'),
                        'Latitude (°)': r.get('lat_deg', 0),
                        'Method': '🌐 OSM + 🌤️' if r.get('used_osm', False) else '📍 Geographic',
                        'Recommendation': r['recommendation'][:50] + '...',
                        'Data': r
                    })
            except Exception as e:
                results.append({
                    'Site': name, 'Suitability %': 0, 'Rating': 'Error',
                    'Elevation (m)': 0, 'Wind (m/s)': 'N/A', 'Flood Risk': 'Unknown',
                    'Latitude (°)': abs(coords[0]), 'Method': 'Error',
                    'Recommendation': f"Error: {str(e)[:50]}", 'Data': None
                })
        pb.empty(); stx.empty()
        if results:
            df = pd.DataFrame(results)
            df_sorted = df.sort_values('Suitability %', ascending=False)
            st.write(f"**📊 Comparison of {len(results)} Candidate Sites**")
            top = df_sorted.iloc[0]
            st.success(f"🚀 **Top Recommended: {top['Site']}** ({top['Suitability %']:.1f}%)")
            st.caption(top['Recommendation'])
            cols = ['Site', 'Suitability %', 'Rating', 'Elevation (m)', 'Wind (m/s)',
                    'Flood Risk', 'Latitude (°)', 'Method']
            st.dataframe(df_sorted[cols], use_container_width=True, hide_index=True)
            st.bar_chart(df_sorted[['Site', 'Suitability %']].set_index('Site'))
            st.session_state.candidate_scores = {
                row['Site']: row['Suitability %'] for _, row in df.iterrows()
            }
            st.write("---")
            st.write("**🗺️ Site Map with Suitability Scores**")
            basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
            tiles_url = get_tiles_for_basemap(basemap_choice)
            if basemap_choice == "Satellite":
                m = folium.Map(location=[4.2, 102.0], zoom_start=6,
                               tiles=tiles_url, attr='Esri World Imagery')
            else:
                m = folium.Map(location=[4.2, 102.0], zoom_start=6, tiles="OpenStreetMap")
            for _, row in df.iterrows():
                sc = row['Suitability %']
                color = ('green' if sc >= 80 else 'lightgreen' if sc >= 65
                         else 'orange' if sc >= 50 else 'lightred' if sc >= 35 else 'red')
                coords = WEST_MALAYSIA_SPACEPORT_CANDIDATES.get(row['Site'], (0, 0))
                folium.Marker(coords, popup=f"<b>{row['Site']}</b><br>Suitability: {sc:.1f}%<br>Rating: {row['Rating']}<br>Wind: {row['Wind (m/s)']} m/s<br>Method: {row['Method']}",
                              tooltip=f"{row['Site']}: {sc:.1f}%",
                              icon=folium.Icon(color=color, icon='rocket', prefix='fa')).add_to(m)
            try: Fullscreen(position='topleft').add_to(m)
            except Exception: pass
            st_folium(m, width=None, height=400, use_container_width=True)
            sel = st.selectbox("Select a site for detailed analysis:",
                               df_sorted['Site'].tolist())
            if sel:
                coords = WEST_MALAYSIA_SPACEPORT_CANDIDATES[sel]
                st.session_state.selected_location = Location(lat=coords[0], lon=coords[1], name=sel)
                st.session_state.comparison_mode = False
                st.rerun()


def render_memory_explorer():
    st.subheader("💾 Memory Explorer")
    t1, t2 = st.tabs(["Past Analyses", "Learned Parameters"])
    with t1:
        analyses = st.session_state.agent.memory_repo.get_all_analyses(20)
        if analyses:
            st.write(f"**{len(analyses)} past analyses stored**")
            for e in analyses:
                preview = e['query'][:50] + ("..." if len(e['query']) > 50 else "")
                with st.expander(f"{'✅' if e['success'] else '❌'} {preview}"):
                    st.write(f"**Query:** {e['query']}")
                    st.write(f"**Success:** {'✅ Yes' if e['success'] else '❌ No'}")
                    st.write(f"**Time:** {e['execution_time']:.2f}s")
                    st.write(f"**Timestamp:** {e['timestamp']}")
        else:
            st.info("No past analyses yet.")
    with t2:
        try:
            conn = sqlite3.connect("west_malaysia_spaceport_memory.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM learned_parameters ORDER BY success_rate DESC")
            rows = cur.fetchall(); conn.close()
            if rows:
                df = pd.DataFrame(rows, columns=['ID', 'Analysis Type', 'Parameter',
                                                 'Value', 'Success Rate', 'Usage Count',
                                                 'Last Updated'])
                st.dataframe(df[['Analysis Type', 'Parameter', 'Value',
                                 'Success Rate', 'Usage Count']],
                             use_container_width=True)
            else:
                st.info("No learned parameters yet.")
        except Exception:
            st.info("No learned parameters yet.")


def main():
    st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div class="main-title">🚀 WEST MALAYSIA SPACEPORT</div>
        <div class="subtitle">PENINSULAR MALAYSIA · SITE SELECTOR</div>
        <div class="cyber-divider"></div>
        <div style="color: #8080a0; font-family: 'Courier New', monospace;
             font-size: 0.7rem; letter-spacing: 4px; margin-top: 5px;">
            ⚡ HYBRID · OSM LIVE · 🌤️ WEATHER LIVE · INSTANT RESULTS ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)

    init_session_state()
    total_locs = len(WEST_MALAYSIA_LOCATIONS)
    total_cands = len(WEST_MALAYSIA_SPACEPORT_CANDIDATES)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 8px 15px;
         border: 1px solid rgba(0, 240, 255, 0.1); border-radius: 8px;
         background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
        <span style="color: #8080a0; font-family: 'Courier New', monospace;
             font-size: 0.7rem; letter-spacing: 1px;">📍 LOCATIONS LOADED</span>
        <span style="color: #00f0ff; font-family: 'Courier New', monospace;
             font-size: 0.8rem; font-weight: bold; letter-spacing: 1px;">
            {total_locs} (+ {total_cands} candidates)</span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace;
             font-size: 0.6rem; letter-spacing: 1px;">PENINSULAR MALAYSIA</span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('comparison_mode', False):
        render_comparison_mode()
        if st.button("← BACK TO SINGLE SITE"):
            st.session_state.comparison_mode = False; st.rerun()
        st.divider(); return

    params = render_sidebar()
    c1, c2 = st.columns([1.5, 1])
    with c1:
        render_map(params)
        render_query_interface(params)
    with c2:
        if st.session_state.selected_location:
            name = st.session_state.selected_location.name or "West Malaysia Location"
            st.markdown(f"""
            <div style="padding: 10px 15px; border: 1px solid rgba(0, 240, 255, 0.15);
                 border-radius: 8px; background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.6rem; letter-spacing: 1px;">SELECTED LOCATION</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace;
                     font-size: 0.9rem;">{name}</div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace;
                     font-size: 0.6rem; letter-spacing: 1px;">
                    {st.session_state.selected_location.lat:.4f},
                    {st.session_state.selected_location.lon:.4f}
                </div>
            </div>
            """, unsafe_allow_html=True)
        render_reasoning_log()
    st.divider()
    c1, c2 = st.columns(2)
    with c1: render_results()
    with c2: render_memory_explorer()
    st.markdown("""
    <div class="cyber-divider"></div>
    <div style="text-align: center; padding: 15px 0; color: #333;
         font-family: 'Courier New', monospace; font-size: 0.6rem; letter-spacing: 2px;">
        <span style="color: #00f0ff;">[</span>
        WEST MALAYSIA SPACEPORT SELECTOR v2.0 · CYBERPUNK EDITION
        <span style="color: #00f0ff;">]</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
