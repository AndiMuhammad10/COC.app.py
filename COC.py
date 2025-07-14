import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# CSS styling modern futuristik
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(-45deg, #000000, #660099);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .kotak-tentang-kami {
        border: 2px solid white;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Tabel Periodik Lengkap
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

# Valensi diperluas
valensi_data = {
    "HCl": 1, "H2SO4": 2, "HNO3": 1, "CH3COOH": 1, "H3PO4": 3, "H2CO3": 2, "H2S": 2,
    "H2C2O4": 2, "HClO3": 1, "H2CrO4": 2, "NaOH": 1, "KOH": 1, "Ca(OH)2": 2,
    "Mg(OH)2": 2, "Ba(OH)2": 2, "LiOH": 1, "NH4OH": 1, "Al(OH)3": 3, "Sr(OH)2": 2,
    "Fe(OH)3": 3, "NaCl": 1, "K2SO4": 2, "Na2CO3": 2, "CaCl2": 2, "MgSO4": 2,
    "NH4Cl": 1, "NaHCO3": 1, "KNO3": 1, "AgNO3": 1, "Ca3(PO4)2": 3, "KMnO4": 5,
    "Na2Cr2O7": 6, "H2O2": 1, "Fe2O3": 3, "CuSO4": 2, "NH4NO3": 1, "Na2S2O3": 2,
    "CoCl2": 2, "HClO4": 1, "K2Cr2O7": 6, "HClO": 1, "H3BO3": 3, "CH3COOK": 1,
    "ZnCl2": 2, "Na3PO4": 3, "Li2CO3": 2
}

# Fungsi tombol lihat hasil perhitungan
if "hasil_terakhir" not in st.session_state:
    st.session_state["hasil_terakhir"] = ""

if st.session_state["hasil_terakhir"]:
    with st.expander("Lihat Perhitungan Terakhir"):
        st.code(st.session_state["hasil_terakhir"])

# Sidebar
st.sidebar.markdown("""
---
**Lihat Hasil Sebelumnya**

- [ ] Penimbangan
- [ ] Pengenceran
- [ ] Konversi
- [ ] Atom Relatif
""")

# Placeholder halaman utama
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Atom Relatif", "Tentang Kami"])

if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        Aplikasi ini dibuat untuk membantu Anda menghitung berbagai parameter dalam kimia larutan seperti:
        - Penimbangan larutan berdasarkan konsentrasi
        - Pengenceran larutan
        - Konversi antar satuan konsentrasi
        - Atom relatif berdasarkan rumus
    """)

elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.markdown("""
    <div class='kotak-tentang-kami'>
        <strong>Pengembang Aplikasi:</strong><br><br>
        - Andi Muhammad Tegar A A 2460322<br>
        - Inezza Azmi Tobri       2460390<br>
        - Muhammad Habibie Rasyha 2460438<br>
        - Saskia Putri Irfani     2460512<br>
        - Zahra Nandya Putri N    2460543<br>
        <br>
        Politeknik AKA Bogor - Kimia Analisis
    </div>
    """, unsafe_allow_html=True)

# TODO: Gabungkan fitur Penimbangan, Pengenceran, Konversi, dan Atom Relatif yang sudah selesai
# dan integrasikan hasil revisi penuh di atas ke dalam setiap mode.

# (Fungsi lengkap akan ditambahkan di bagian selanjutnya sesuai lanjutan implementasi)
