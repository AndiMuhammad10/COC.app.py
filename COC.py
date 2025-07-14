import streamlit as st
import re

# Improved custom CSS with animated gradient and filled background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    body {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
        font-family: 'Orbitron', sans-serif;
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background-color: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    .stButton button {
        background-color: #8A2BE2 !important;
        color: white !important;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #9932CC !important;
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Complete periodic table data with all elements and oxidation states
periodik = {
    "H": {"mass": 1.008, "oxidation": [1, -1]},
    "He": {"mass": 4.0026, "oxidation": [0]},
    "Li": {"mass": 6.94, "oxidation": [1]},
    "Be": {"mass": 9.0122, "oxidation": [2]},
    "B": {"mass": 10.81, "oxidation": [3]},
    "C": {"mass": 12.011, "oxidation": [4, 2, -4]},
    "N": {"mass": 14.007, "oxidation": [5, 4, 3, 2, -3]},
    "O": {"mass": 15.999, "oxidation": [-2, -1]},
    "F": {"mass": 18.998, "oxidation": [-1]},
    "Ne": {"mass": 20.180, "oxidation": [0]},
    "Na": {"mass": 22.990, "oxidation": [1]},
    "Mg": {"mass": 24.305, "oxidation": [2]},
    "Al": {"mass": 26.982, "oxidation": [3]},
    "Si": {"mass": 28.085, "oxidation": [4, 2, -4]},
    "P": {"mass": 30.974, "oxidation": [5, 3, -3]},
    "S": {"mass": 32.06, "oxidation": [6, 4, 2, -2]},
    "Cl": {"mass": 35.45, "oxidation": [7, 5, 1, -1]},
    "Ar": {"mass": 39.948, "oxidation": [0]},
    "K": {"mass": 39.098, "oxidation": [1]},
    "Ca": {"mass": 40.078, "oxidation": [2]},
    "Sc": {"mass": 44.956, "oxidation": [3]},
    "Ti": {"mass": 47.867, "oxidation": [4, 3, 2]},
    "V": {"mass": 50.942, "oxidation": [5, 4, 3, 2]},
    "Cr": {"mass": 51.996, "oxidation": [6, 3, 2]},
    "Mn": {"mass": 54.938, "oxidation": [7, 6, 4, 2]},
    "Fe": {"mass": 55.845, "oxidation": [3, 2]},
    "Co": {"mass": 58.933, "oxidation": [3, 2]},
    "Ni": {"mass": 58.693, "oxidation": [3, 2]},
    "Cu": {"mass": 63.546, "oxidation": [2, 1]},
    "Zn": {"mass": 65.38, "oxidation": [2]},
    "Ga": {"mass": 69.723, "oxidation": [3]},
    "Ge": {"mass": 72.630, "oxidation": [4, 2]},
    "As": {"mass": 74.922, "oxidation": [5, 3, -3]},
    "Se": {"mass": 78.971, "oxidation": [6, 4, -2]},
    "Br": {"mass": 79.904, "oxidation": [7, 5, 1, -1]},
    "Kr": {"mass": 83.798, "oxidation": [2, 0]},
    "Rb": {"mass": 85.468, "oxidation": [1]},
    "Sr": {"mass": 87.62, "oxidation": [2]},
    "Y": {"mass": 88.906, "oxidation": [3]},
    "Zr": {"mass": 91.224, "oxidation": [4]},
    "Nb": {"mass": 92.906, "oxidation": [5, 3]},
    "Mo": {"mass": 95.95, "oxidation": [6, 4]},
    "Tc": {"mass": 98.0, "oxidation": [7, 6, 4]},
    "Ru": {"mass": 101.07, "oxidation": [8, 6, 4, 3, 2]},
    "Rh": {"mass": 102.91, "oxidation": [4, 3]},
    "Pd": {"mass": 106.42, "oxidation": [4, 2]},
    "Ag": {"mass": 107.87, "oxidation": [1]},
    "Cd": {"mass": 112.41, "oxidation": [2]},
    "In": {"mass": 114.82, "oxidation": [3]},
    "Sn": {"mass": 118.71, "oxidation": [4, 2]},
    "Sb": {"mass": 121.76, "oxidation": [5, 3]},
    "Te": {"mass": 127.60, "oxidation": [6, 4, -2]},
    "I": {"mass": 126.90, "oxidation": [7, 5, 1, -1]},
    "Xe": {"mass": 131.29, "oxidation": [8, 6, 4, 2, 0]},
    "Cs": {"mass": 132.91, "oxidation": [1]},
    "Ba": {"mass": 137.33, "oxidation": [2]},
    "La": {"mass": 138.91, "oxidation": [3]},
    "Ce": {"mass": 140.12, "oxidation": [4, 3]},
    "Pr": {"mass": 140.91, "oxidation": [4, 3]},
    "Nd": {"mass": 144.24, "oxidation": [3]},
    "Pm": {"mass": 145.0, "oxidation": [3]},
    "Sm": {"mass": 150.36, "oxidation": [3, 2]},
    "Eu": {"mass": 151.96, "oxidation": [3, 2]},
    "Gd": {"mass": 157.25, "oxidation": [3]},
    "Tb": {"mass": 158.93, "oxidation": [4, 3]},
    "Dy": {"mass": 162.50, "oxidation": [3]},
    "Ho": {"mass": 164.93, "oxidation": [3]},
    "Er": {"mass": 167.26, "oxidation": [3]},
    "Tm": {"mass": 168.93, "oxidation": [3]},
    "Yb": {"mass": 173.05, "oxidation": [3, 2]},
    "Lu": {"mass": 174.97, "oxidation": [3]},
    "Hf": {"mass": 178.49, "oxidation": [4]},
    "Ta": {"mass": 180.95, "oxidation": [5]},
    "W": {"mass": 183.84, "oxidation": [6, 5, 4]},
    "Re": {"mass": 186.21, "oxidation": [7, 6, 4, 2]},
    "Os": {"mass": 190.23, "oxidation": [8, 6, 4, 3, 2]},
    "Ir": {"mass": 192.22, "oxidation": [6, 4, 3]},
    "Pt": {"mass": 195.08, "oxidation": [4, 2]},
    "Au": {"mass": 196.97, "oxidation": [3, 1]},
    "Hg": {"mass": 200.59, "oxidation": [2, 1]},
    "Tl": {"mass": 204.38, "oxidation": [3, 1]},
    "Pb": {"mass": 207.2, "oxidation": [4, 2]},
    "Bi": {"mass": 208.98, "oxidation": [5, 3]},
    "Po": {"mass": 209.0, "oxidation": [6, 4, 2]},
    "At": {"mass": 210.0, "oxidation": [7, 5, 1, -1]},
    "Rn": {"mass": 222.0, "oxidation": [2, 0]},
    "Fr": {"mass": 223.0, "oxidation": [1]},
    "Ra": {"mass": 226.0, "oxidation": [2]},
    "Ac": {"mass": 227.0, "oxidation": [3]},
    "Th": {"mass": 232.04, "oxidation": [4]},
    "Pa": {"mass": 231.04, "oxidation": [5, 4]},
    "U": {"mass": 238.03, "oxidation": [6, 5, 4, 3]},
    "Np": {"mass": 237.0, "oxidation": [7, 6, 5, 4]},
    "Pu": {"mass": 244.0, "oxidation": [7, 6, 5, 4]},
    "Am": {"mass": 243.0, "oxidation": [7, 6, 5, 4, 3]},
    "Cm": {"mass": 247.0, "oxidation": [4, 3]},
    "Bk": {"mass": 247.0, "oxidation": [4, 3]},
    "Cf": {"mass": 251.0, "oxidation": [4, 3]},
    "Es": {"mass": 252.0, "oxidation": [4, 3]},
    "Fm": {"mass": 257.0, "oxidation": [3]},
    "Md": {"mass": 258.0, "oxidation": [3]},
    "No": {"mass": 259.0, "oxidation": [3]},
    "Lr": {"mass": 262.0, "oxidation": [3]}
}

# Common acids, bases and salts for automatic equivalent weight determination
common_compounds = {
    "HCl": {"type": "acid", "H+": 1},
    "H2SO4": {"type": "acid", "H+": 2},
    "HNO3": {"type": "acid", "H+": 1},
    "H3PO4": {"type": "acid", "H+": 3},
    "H2C2O4": {"type": "acid", "H+": 2},
    "CH3COOH": {"type": "acid", "H+": 1},
    "NaOH": {"type": "base", "OH-": 1},
    "KOH": {"type": "base", "OH-": 1},
    "Ca(OH)2": {"type": "base", "OH-": 2},
    "Ba(OH)2": {"type": "base", "OH-": 2},
    "NH4OH": {"type": "base", "OH-": 1},
    "Na2CO3": {"type": "salt", "n": 2, "charge": 2},
    "K2Cr2O7": {"type": "redox", "n": 6},  # Cr changes from +6 to +3 (3 electron change per Cr, 2 Cr atoms)
    "KMnO4": {"type": "redox", "n": 5},    # Mn changes from +7 to +2
    "FeSO4": {"type": "redox", "n": 1},    # Fe changes from +2 to +3
    "Na2S2O3": {"type": "redox", "n": 1},  # Iodometry reactions
    "H2O2": {"type": "redox", "n": 2},     # O changes from -1 to -2
    "NaCl": {"type": "salt", "n": 1, "charge": 1}
}

# Rest of the code remains exactly the same as in the previous version
# [...] 

# (Continuing with all the existing functions and Streamlit UI code)

