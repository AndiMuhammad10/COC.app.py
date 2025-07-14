import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton button {
        background-color: #7E57C2;
        color: white;
        border-radius: 8px;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Periodic Table Data
periodik = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180, "Na": 22.990, "Mg": 24.305,
    "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45, "Ar": 39.948,
    "K": 39.098, "Ca": 40.078, "Sc": 44.956, "Ti": 47.867, "V": 50.942, "Cr": 51.996,
    "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38,
    "Ga": 69.723, "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904, "Kr": 83.798,
    "Rb": 85.468, "Sr": 87.62, "Y": 88.906, "Zr": 91.224, "Nb": 92.906, "Mo": 95.95,
    "Tc": 98.0, "Ru": 101.07, "Rh": 102.91, "Pd": 106.42, "Ag": 107.87, "Cd": 112.41,
    "In": 114.82, "Sn": 118.71, "Sb": 121.76, "Te": 127.60, "I": 126.90, "Xe": 131.29,
    "Cs": 132.91, "Ba": 137.33, "La": 138.91, "Ce": 140.12, "Pr": 140.91, "Nd": 144.24,
    "Sm": 150.36, "Eu": 151.96, "Gd": 157.25, "Tb": 158.93, "Dy": 162.50, "Ho": 164.93,
    "Er": 167.26, "Tm": 168.93, "Yb": 173.05, "Lu": 174.97, "Hf": 178.49, "Ta": 180.95,
    "W": 183.84, "Re": 186.21, "Os": 190.23, "Ir": 192.22, "Pt": 195.08, "Au": 196.97,
    "Hg": 200.59, "Tl": 204.38, "Pb": 207.2, "Bi": 208.98, "Th": 232.04, "U": 238.03
}

common_compounds = {
    "HCl": {"type": "acid", "H+": 1, "be": 36.46},
    "H2SO4": {"type": "acid", "H+": 2, "be": 49.04},
    "NaOH": {"type": "base", "OH-": 1, "be": 40.00}
}

def parse_formula(rumus):
    # ... [same parsing function as before] ...
    pass

def hitung_mr(rumus):
    # ... [same molecular weight calculation as before] ...
    pass

def hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen=None):
    # ... [same mass calculation as before] ...
    pass

def hitung_pengenceran(v1=None, c1=None, v2=None, c2=None):
    # ... [same dilution calculation as before] ...
    pass

# Navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

# Home Page
if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    
# Mass Calculation Page
elif menu == "Penimbangan":
    st.header("Penimbangan Zat")
    
    # Your original mass calculation form here
    # ...
    
    if st.button("Kembali ke Beranda"):
        st.session_state.menu = "Home"
        st.experimental_rerun()

# Dilution Page
elif menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    
    # Your original dilution form here
    # ...
    
    if st.button("Kembali ke Beranda"):
        st.session_state.menu = "Home"
        st.experimental_rerun()

# Conversion Page
elif menu == "Konversi":
    st.header("Konversi Satuan")
    
    # Conversion Form
    st.subheader("Konversi Konsentrasi")
    # ... your conversion form here ...
    
    # Separate Atomic Mass Section
    st.subheader("Massa Atom Relatif")
    element = st.text_input("Masukkan simbol unsur:")
    if st.button("Cari Massa Atom"):
        if element in periodik:
            st.success(f"Massa atom {element}: {periodik[element]}")
        else:
            st.error("Unsur tidak dikenali!")
    
    if st.button("Kembali ke Beranda"):
        st.session_state.menu = "Home"
        st.experimental_rerun()

# About Page
elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    
    if st.button("Kembali ke Beranda"):
        st.session_state.menu = "Home"
        st.experimental_rerun()
