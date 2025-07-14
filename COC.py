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

# Tabel Periodik Lengkap dan Berat Ekivalen
periodik = {
    "H": 1.008, "O": 15.999, "Na": 22.990, "Cl": 35.45, "K": 39.098, "Cr": 51.996,
    "Fe": 55.845, "Cu": 63.546, "S": 32.06, "C": 12.011, "N": 14.007, "P": 30.974,
    "Mg": 24.305, "Ca": 40.078, "Mn": 54.938, "Zn": 65.38, "Al": 26.982
}

berat_ekivalen = {
    "H2SO4": 49, "NaOH": 40, "KOH": 56.1, "HCl": 36.5, "HNO3": 63, "CH3COOH": 60
}

# Fungsi Penimbangan
menu = st.sidebar.radio("Menu", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

if menu == "Penimbangan":
    st.header("Penimbangan Zat")
    senyawa = st.text_input("Masukkan rumus kimia (Contoh: H2SO4, NaOH, FeCl3)")
    konsentrasi = st.number_input("Masukkan konsentrasi:")
    satuan = st.selectbox("Satuan konsentrasi:", ["Molaritas (mol/L)", "Normalitas (grek/L)"])
    volume_ml = st.number_input("Masukkan volume (mL):")
    volume_l = volume_ml / 1000

    if st.button("Hitung Massa"):
        if satuan == "Normalitas (grek/L)" and senyawa in berat_ekivalen:
            be = berat_ekivalen[senyawa]
            massa = be * volume_l * konsentrasi
            st.success(f"Berat yang ditimbang: {massa:.4f} g")
            st.code(f"Massa = {be} g/grek × {volume_l} L × {konsentrasi} grek/L = {massa:.4f} g")
        elif satuan == "Molaritas (mol/L)" and all(el in periodik for el in re.findall(r'[A-Z][a-z]?', senyawa)):
            tokens = re.findall(r'([A-Z][a-z]*)(\d*)', senyawa)
            mr = sum(periodik[el] * int(cnt or 1) for el, cnt in tokens)
            massa = mr * volume_l * konsentrasi
            st.success(f"Berat yang ditimbang: {massa:.4f} g")
            st.code(f"Massa = {mr:.2f} g/mol × {volume_l} L × {konsentrasi} mol/L = {massa:.4f} g")
        else:
            st.error("Senyawa tidak dikenali atau belum didukung untuk satuan ini.")

if menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    mode = st.radio("Ingin menghitung:", ["Volume Awal (V1)", "Konsentrasi Awal (C1)"])

    if mode == "Volume Awal (V1)":
        c1 = st.number_input("Masukkan C1:")
        c2 = st.number_input("Masukkan C2:")
        v2 = st.number_input("Masukkan V2 (mL):")
        if st.button("Hitung V1"):
            v1 = (v2 * c2) / c1
            st.success(f"Volume awal: {v1:.2f} mL")
            st.code(f"V1 = (V2 × C2) / C1 = ({v2} × {c2}) / {c1} = {v1:.2f} mL")
    else:
        v1 = st.number_input("Masukkan V1 (mL):")
        c2 = st.number_input("Masukkan C2:")
        v2 = st.number_input("Masukkan V2 (mL):")
        if st.button("Hitung C1"):
            c1 = (v2 * c2) / v1
            st.success(f"Konsentrasi awal: {c1:.4f}")
            st.code(f"C1 = (V2 × C2) / V1 = ({v2} × {c2}) / {v1} = {c1:.4f}")

# Halaman Konversi tetap ada seperti sebelumnya
if menu == "Konversi":
    st.header("Konversi Konsentrasi")
    nilai = st.number_input("Masukkan nilai konsentrasi:")
    satuan_asal = st.selectbox("Dari satuan:", ["mol/L", "grek/L", "%", "ppm", "ppb"])
    satuan_tujuan = st.selectbox("Ke satuan:", ["mol/L", "grek/L", "%", "ppm", "ppb"])

    hasil = None
    if satuan_asal == satuan_tujuan:
        hasil = nilai
    else:
        if satuan_asal == "%":
            nilai = nilai * 10_000
        elif satuan_asal == "ppm":
            nilai = nilai
        elif satuan_asal == "ppb":
            nilai = nilai / 1_000
        elif satuan_asal == "mol/L":
            nilai = nilai * 1_000
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

if menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.markdown("""
    Aplikasi ini dikembangkan oleh:

    - Andi Muhammad Tegar A A 2460322
    - Inezza Azmi Tobri       2460390
    - Muhammad Habibie Rasyha 2460438
    - Saskia Putri Irfani     2460512
    - Zahra Nandya Putri N    2460543

    Politeknik AKA Bogor - Kimia Analisis
    """)
