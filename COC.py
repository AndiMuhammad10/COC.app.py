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

# Valensi diperluas (akan ditambahkan lebih lanjut bila ada permintaan tambahan)
valensi_data = {
    "HCl": 1, "HNO3": 1, "H2SO4": 2, "H3PO4": 3, "CH3COOH": 1, "H2CO3": 2,
    "NaOH": 1, "KOH": 1, "Ca(OH)2": 2, "Ba(OH)2": 2, "Al(OH)3": 3,
    "NaCl": 1, "K2SO4": 2, "FeCl3": 3, "KMnO4": 5, "K2Cr2O7": 6, "Fe2O3": 3,
    "Cl2": 2, "H2O2": 2, "CuO": 2, "HBr": 1, "HI": 1, "HClO4": 1, "LiOH": 1,
    "Mg(OH)2": 2, "Zn(OH)2": 2, "NH3": 1, "HNO2": 1, "H2S": 2, "Na2CO3": 2,
    "MgSO4": 2, "CaCO3": 2, "HClO": 1
}

# Fungsi berat ekivalen

def hitung_berat_ekivalen(senyawa, mr):
    valensi = valensi_data.get(senyawa, 1)
    return round(mr / valensi, 3), valensi

# Konversi satuan dasar

def konversi_satuan(nilai, dari, ke):
    if dari == ke:
        return nilai
    try:
        if dari == "Molaritas (mol/L)" and ke == "Normalitas (grek/L)":
            return nilai * 1  # Anggap 1 grek = 1 mol (default)
        if dari == "Normalitas (grek/L)" and ke == "Molaritas (mol/L)":
            return nilai * 1
        if dari == "% (b/v)" and ke == "PPM":
            return nilai * 10000
        if dari == "PPM" and ke == "% (b/v)":
            return nilai / 10000
        if dari == "PPM" and ke == "PPB":
            return nilai * 1000
        if dari == "PPB" and ke == "PPM":
            return nilai / 1000
        return None
    except:
        return None

# Menu Konversi
if st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Atom Relatif", "Tentang Kami"]) == "Konversi":
    st.header("Konversi Satuan Konsentrasi")
    nilai = st.number_input("Masukkan nilai konsentrasi:")
    satuan_awal = st.selectbox("Satuan Awal", ["Molaritas (mol/L)", "Normalitas (grek/L)", "% (b/v)", "PPM", "PPB"])
    satuan_akhir = st.selectbox("Satuan Akhir", ["Molaritas (mol/L)", "Normalitas (grek/L)", "% (b/v)", "PPM", "PPB"])

    if st.button("Konversi"):
        hasil = konversi_satuan(nilai, satuan_awal, satuan_akhir)
        if hasil is not None:
            st.success(f"Hasil konversi dari {satuan_awal} ke {satuan_akhir} adalah: {hasil}")
        else:
            st.error("Konversi tidak didukung antara satuan yang dipilih.")
