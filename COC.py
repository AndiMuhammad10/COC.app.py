import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Custom CSS for background and font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #5C4B8A, #8A2BE2);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
        font-family: 'Orbitron', sans-serif;
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

# Fungsi parsing rumus dengan tanda kurung dan hidrasi
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

    # Replace hydrated compounds
    rumus = re.sub(r'\((\w+)\)(\d+)', lambda m: f"{m.group(2)}{m.group(1)}", rumus)
    tokens = re.findall(r'[A-Z][a-z]?|\d+|\(|\)', rumus)
    elements = extract(tokens)
    hasil = {}
    for el in elements:
        if el not in periodik:
            raise ValueError(f"Elemen tidak dikenali: {el}")
        hasil[el] = hasil.get(el, 0) + 1
    return hasil

# Hitung Mr dari hasil parsing
def hitung_mr(rumus):
    komposisi = parse_formula(rumus)
    total = sum(periodik[el] * jumlah for el, jumlah in komposisi.items())
    return round(total, 3), komposisi

# Fungsi menghitung massa dari konsentrasi
def hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen=None):
    if satuan == "Molaritas (g/mol)":
        mol = konsentrasi * volume_l
        return mol * mr, f"mol = {konsentrasi} mol/L × {volume_l} L = {mol:.4f} mol\nMassa = {mol:.4f} mol × {mr} g/mol = {mol * mr:.4f} g"
    elif satuan == "Normalitas (g/grek)":
        if berat_ekivalen is None:
            raise ValueError("Berat ekivalen harus diberikan untuk Normalitas.")
        grek = konsentrasi * volume_l
        return grek * berat_ekivalen, f"grek = {konsentrasi} grek/L × {volume_l} L = {grek:.4f} grek\nMassa = {grek:.4f} grek × {berat_ekivalen} g/grek = {grek * berat_ekivalen:.4f} g"
    elif satuan == "% (b/v)":
        return konsentrasi * volume_l * 10, f"Massa = {konsentrasi}% × {volume_l} L × 10 = {konsentrasi * volume_l * 10:.4f} g"
    elif satuan == "PPM (mg/L)":
        mg = konsentrasi * volume_l
        return mg / 1000, f"Massa = {konsentrasi} mg/L × {volume_l} L = {mg} mg = {mg / 1000:.4f} g"
    elif satuan == "PPB (µg/L)":
        µg = konsentrasi * volume_l
        return µg / 1e6, f"Massa = {konsentrasi} µg/L × {volume_l} L = {µg} µg = {µg / 1e6:.8f} g"

# Fungsi pengenceran
def hitung_pengenceran(v1=None, c1=None, v2=None, c2=None):
    if v1 is None:
        return (v2 * c2) / c1, f"V1 = (V2 × C2) / C1 = ({v2} × {c2}) / {c1} = {(v2 * c2) / c1:.6f}"
    elif c1 is None:
        return (v2 * c2) / v1, f"C1 = (V2 × C2) / V1 = ({v2} × {c2}) / {v1} = {(v2 * c2) / v1:.6f}"

# Sidebar navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

# Tampilan halaman
if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        Aplikasi ini dibuat untuk membantu Anda menghitung berbagai parameter dalam kimia larutan seperti:
        - Penimbangan larutan berdasarkan konsentrasi
        - Pengenceran larutan

        Materi ini berkaitan erat dengan stoikiometri, yaitu ilmu yang mempelajari perbandingan kuantitatif antara reaktan dan produk dalam reaksi kimia. 
        Stoikiometri sangat penting dalam kimia analisis karena membantu kita memahami bagaimana zat-zat berinteraksi dan berapa banyak yang diperlukan untuk mencapai reaksi yang diinginkan.

        Aplikasi ini juga memungkinkan Anda untuk melakukan konversi antara berbagai satuan konsentrasi, sehingga memudahkan dalam perhitungan laboratorium.
    """)

elif menu == "Penimbangan":
    st.header("Penimbangan Zat")
    senyawa = st.text_input("Masukkan rumus kimia senyawa (contoh: K2Cr2O7, Fe(OH)3, CuSO4.(H2O)5")
    
    try:
        if senyawa:
            mr, detail = hitung_mr(senyawa)
            st.success(f"Mr dari {senyawa} adalah {mr} g/mol")
            with st.expander("Detail Atom"):
                for elemen, jumlah in detail.items():
                    st.write(f"{elemen}: {jumlah} atom × {periodik[elemen]} g/mol = {jumlah * periodik[elemen]:.3f} g")
    except Exception as e:
        st.error(str(e))
        mr = None

    konsentrasi = st.number_input("Masukkan konsentrasi yang diinginkan:")
    satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

    if st.button("Hitung Massa") and mr is not None:
        volume_l = volume_ml / 1000
        if satuan == "Normalitas (g/grek)":
            # Automatically calculate equivalent weight based on the compound type
            if senyawa in common_compounds:
                berat_ekivalen = common_compounds[senyawa]["H+"]  # Example for acids
            else:
                st.error("Berat ekivalen tidak ditemukan untuk senyawa ini.")
                berat_ekivalen = None
        else:
            berat_ekivalen = None

        hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen)
        st.success(f"Massa {senyawa} yang harus ditimbang: {hasil:.4f} g")
        with st.expander("Lihat Perhitungan"):
            st.code(penjelasan)

    if st.button("Beranda"):
        st.experimental_rerun()

elif menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    pilihan = st.radio("Ingin menentukan apa?", ["Volume Awal (V1)", "Konsentrasi Awal (C1)"])

    if pilihan == "Volume Awal (V1)":
        c1 = st.number_input("Masukkan Konsentrasi Awal (C1):")
        c2 = st.number_input("Masukkan Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Masukkan Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung V1"):
            v1, penjelasan = hitung_pengenceran(None, c1, v2 / 1000, c2)
            st.success(f"Volume awal (V1) yang dibutuhkan: {v1*1000:.2f} mL")
            with st.expander("Lihat Perhitungan"):
                st.code(penjelasan)
    else:
        v1 = st.number_input("Masukkan Volume Awal (V1) dalam mL:")
        c2 = st.number_input("Masukkan Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Masukkan Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung C1"):
            c1, penjelasan = hitung_pengenceran(v1 / 1000, None, v2 / 1000, c2)
            st.success(f"Konsentrasi awal (C1) yang dibutuhkan: {c1:.4f}")
            with st.expander("Lihat Perhitungan"):
                st.code(penjelasan)

    if st.button("Beranda"):
        st.experimental_rerun()

elif menu == "Konversi":
    st.header("Konversi Satuan")
    st.write("""
    Aplikasi ini memungkinkan Anda untuk mengkonversi antara berbagai satuan konsentrasi:
    - Molaritas (g/mol)
    - Normalitas (g/grek)
    - PPM (mg/L)
    - PPB (µg/L)
    - % (b/v)
    """)
    
    value = st.number_input("Masukkan nilai konsentrasi:")
    from_unit = st.selectbox("Dari satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    to_unit = st.selectbox("Ke satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])

    if st.button("Konversi"):
        # Implement conversion logic here
        st.success("Konversi berhasil!")  # Placeholder for actual conversion result

    if st.button("Beranda"):
        st.experimental_rerun()

elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.write("""
    Aplikasi ini dikembangkan oleh:

    - Andi Muhammad Tegar A A 2460322
    - Inezza Azmi Tobri       2460390
    - Muhammad Habibie Rasyha 2460438
    - Saskia Putri Irfani     2460512
    - Zahra Nandya Putri N    2460543

    Politkenik  AKA Bogor - Kimia Analisis

    Proyek ini bertujuan untuk memberikan alat bantu yang efisien dalam perhitungan konsentrasi dan pengenceran larutan, serta memberikan pemahaman yang lebih baik tentang stoikiometri dalam kimia.
    """)

