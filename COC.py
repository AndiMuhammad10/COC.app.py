import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# CSS styling untuk tema gradasi hitam-ungu dan font cyberpunk
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
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

berat_ekivalen = {
    "H2SO4": 49,
    "NaOH": 40,
    "KOH": 56.1,
    "HCl": 36.5,
    "HNO3": 63,
    "CH3COOH": 60
}

# Navigasi sementara
menu = st.sidebar.radio("Menu", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.markdown("""
        **Apa itu COC?**
        
        _COC (Calculate Of Concentration)_ adalah aplikasi interaktif untuk membantu menghitung konsentrasi kimia larutan, mulai dari penimbangan, pengenceran, hingga konversi satuan.
        
        **Konsep Dasar:**
        Aplikasi ini berbasis pada prinsip **stoikiometri**, yaitu perbandingan kuantitatif zat dalam reaksi kimia. Dalam laboratorium, stoikiometri sangat penting untuk:
        - Menentukan massa zat yang harus ditimbang
        - Menghitung pengenceran dari larutan induk
        - Konversi antar satuan (mol/L, grek/L, ppm, ppb, %)

        Didesain untuk mahasiswa dan profesional kimia agar lebih efisien dan presisi.
    """)
    st.button("Kembali ke Beranda")

elif menu == "Konversi":
    st.header("Konversi Konsentrasi")
    nilai = st.number_input("Masukkan nilai konsentrasi:")
    satuan_asal = st.selectbox("Dari satuan:", ["mol/L", "grek/L", "%", "ppm", "ppb"])
    satuan_tujuan = st.selectbox("Ke satuan:", ["mol/L", "grek/L", "%", "ppm", "ppb"])

    hasil = None
    if satuan_asal == satuan_tujuan:
        hasil = nilai
    else:
        if satuan_asal == "%":
            nilai = nilai * 10_000  # diasumsikan % b/v (g/100 mL) menjadi mg/L
        elif satuan_asal == "ppm":
            nilai = nilai
        elif satuan_asal == "ppb":
            nilai = nilai / 1_000
        elif satuan_asal == "mol/L":
            nilai = nilai * 1_000  # jadi mmol/L
        elif satuan_asal == "grek/L":
            nilai = nilai * 1_000

        if satuan_tujuan == "%":
            hasil = nilai / 10_000
        elif satuan_tujuan == "ppm":
            hasil = nilai
        elif satuan_tujuan == "ppb":
            hasil = nilai * 1_000
        elif satuan_tujuan == "mol/L":
            hasil = nilai / 1_000
        elif satuan_tujuan == "grek/L":
            hasil = nilai / 1_000

    if hasil is not None:
        st.success(f"Hasil konversi: {hasil:.4f} {satuan_tujuan}")
