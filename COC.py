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

# Fungsi menghitung berat ekivalen otomatis berdasarkan valensi
valensi_asam_basa = {
    "H2SO4": 2,
    "NaOH": 1,
    "KOH": 1,
    "HCl": 1,
    "HNO3": 1,
    "CH3COOH": 1,
    "Ca(OH)2": 2,
    "Ba(OH)2": 2,
    "H3PO4": 3
}

def hitung_berat_ekivalen(senyawa, mr):
    valensi = valensi_asam_basa.get(senyawa, 1)  # default 1 jika tidak ditemukan
    return round(mr / valensi, 3)

# Fungsi parsing rumus

def parse_formula(rumus):
    def extract(tokens):
        stack = [[]]
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '(':
                stack.append([])
            elif token == ')':
                group = stack.pop()
                i += 1
                multiplier = int(tokens[i]) if i < len(tokens) and tokens[i].isdigit() else 1
                stack[-1].extend(group * multiplier)
            elif re.match(r'[A-Z][a-z]?$', token):
                count = 1
                if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                    i += 1
                    count = int(tokens[i])
                stack[-1].extend([token] * count)
            i += 1
        return stack[0]

    tokens = re.findall(r'[A-Z][a-z]?|\d+|\(|\)', rumus)
    elements = extract(tokens)
    hasil = {}
    for el in elements:
        if el not in periodik:
            raise ValueError(f"Elemen tidak dikenali: {el}")
        hasil[el] = hasil.get(el, 0) + 1
    return hasil

def hitung_mr(rumus):
    komposisi = parse_formula(rumus)
    total = sum(periodik[el] * jumlah for el, jumlah in komposisi.items())
    return round(total, 3), komposisi

# Navigasi
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Atom Relatif", "Tentang Kami"])

if menu == "Penimbangan":
    st.header("Penimbangan Zat")
    senyawa = st.text_input("Masukkan rumus kimia senyawa (contoh: K2Cr2O7, Fe(OH)3, CuSO4.(H2O)5)")
    if senyawa:
        try:
            mr, detail = hitung_mr(senyawa)
            st.success(f"Mr dari {senyawa} adalah {mr} g/mol")
            with st.expander("Detail Atom"):
                for elemen, jumlah in detail.items():
                    st.write(f"{elemen}: {jumlah} atom × {periodik[elemen]} g/mol = {jumlah * periodik[elemen]:.3f} g")
        except Exception as e:
            st.error(str(e))
            mr = None

        konsentrasi = st.number_input("Masukkan konsentrasi yang diinginkan:")
        satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)"])
        volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

        if st.button("Hitung Massa") and mr:
            volume_l = volume_ml / 1000
            if satuan == "Molaritas (g/mol)":
                mol = konsentrasi * volume_l
                massa = mol * mr
                st.success(f"Massa {senyawa}: {massa:.4f} g")
                st.code(f"mol = {konsentrasi} mol/L × {volume_l} L = {mol} mol\nMassa = {mol} mol × {mr} g/mol = {massa} g")
            elif satuan == "Normalitas (g/grek)":
                be = hitung_berat_ekivalen(senyawa, mr)
                grek = konsentrasi * volume_l
                massa = grek * be
                st.success(f"Massa {senyawa}: {massa:.4f} g")
                st.code(f"grek = {konsentrasi} grek/L × {volume_l} L = {grek} grek\nBerat Ekivalen = {mr} / valensi = {be} g/grek\nMassa = {grek} grek × {be} g/grek = {massa} g")

elif menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    pilihan = st.radio("Ingin menentukan apa?", ["Volume Awal (V1)", "Konsentrasi Awal (C1)"])
    if pilihan == "Volume Awal (V1)":
        c1 = st.number_input("Konsentrasi Awal (C1):")
        c2 = st.number_input("Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung V1"):
            v1 = (v2 * c2) / c1
            st.success(f"Volume awal (V1): {v1:.2f} mL")
    else:
        v1 = st.number_input("Volume Awal (V1) dalam mL:")
        c2 = st.number_input("Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung C1"):
            c1 = (v2 * c2) / v1
            st.success(f"Konsentrasi awal (C1): {c1:.4f}")
    st.button("Kembali ke Home")

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
            nilai *= 10000
        elif satuan_asal == "ppb":
            nilai /= 1000
        elif satuan_asal in ["mol/L", "grek/L"]:
            nilai *= 1000

        if satuan_tujuan == "%":
            hasil = nilai / 10000
        elif satuan_tujuan == "ppb":
            hasil = nilai * 1000
        else:
            hasil = nilai / 1000
    if hasil is not None:
        st.success(f"Hasil konversi: {hasil:.4f} {satuan_tujuan}")
    st.button("Kembali ke Home")

elif menu == "Atom Relatif":
    st.header("Cek Massa Atom Relatif (Mr)")
    senyawa = st.text_input("Masukkan rumus senyawa:")
    if senyawa:
        try:
            mr, detail = hitung_mr(senyawa)
            st.success(f"Mr dari {senyawa} adalah {mr} g/mol")
            with st.expander("Detail Atom"):
                for elemen, jumlah in detail.items():
                    st.write(f"{elemen}: {jumlah} atom × {periodik[elemen]} g/mol = {jumlah * periodik[elemen]:.3f} g")
        except Exception as e:
            st.error(str(e))

elif menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.markdown("""
    **Apa itu COC?**
    _Calculate of Concentration (COC)_ adalah aplikasi interaktif untuk membantu mahasiswa dan analis kimia dalam menghitung konsentrasi larutan.

    Aplikasi ini mengintegrasikan:
    - Penimbangan zat berdasarkan konsentrasi
    - Pengenceran larutan
    - Konversi antar satuan konsentrasi
    - Perhitungan massa atom relatif

    Dilengkapi dengan database Tabel Periodik untuk menghitung Mr dan atom senyawa secara otomatis.
    """)

elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.write("""
    Aplikasi ini dikembangkan oleh:

    - Andi Muhammad Tegar A A 2460322
    - Inezza Azmi Tobri       2460390
    - Muhammad Habibie Rasyha 2460438
    - Saskia Putri Irfani     2460512
    - Zahra Nandya Putri N    2460543

    Politeknik AKA Bogor - Kimia Analisis
    """)
