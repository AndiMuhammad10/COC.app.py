import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# CSS futuristik gradasi
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

# Periodik dan valensi
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

valensi_data = {
    "HCl": 1, "H2SO4": 2, "HNO3": 1, "CH3COOH": 1, "H3PO4": 3, "H2CO3": 2,
    "H2S": 2, "H2C2O4": 2, "HClO3": 1, "H2CrO4": 2,
    "NaOH": 1, "KOH": 1, "Ca(OH)2": 2, "Mg(OH)2": 2, "Ba(OH)2": 2, "LiOH": 1,
    "NH4OH": 1, "Al(OH)3": 3, "Sr(OH)2": 2, "Fe(OH)3": 3,
    "NaCl": 1, "K2SO4": 2, "Na2CO3": 2, "CaCl2": 2, "MgSO4": 2, "NH4Cl": 1,
    "NaHCO3": 1, "KNO3": 1, "AgNO3": 1, "Ca3(PO4)2": 3,
    "KMnO4": 5, "Na2Cr2O7": 6, "H2O2": 1, "Fe2O3": 3, "CuSO4": 2,
    "NH4NO3": 1, "Na2S2O3": 2, "CoCl2": 2, "HClO4": 1, "K2Cr2O7": 6,
    "HClO": 1, "H3BO3": 3, "CH3COOK": 1, "ZnCl2": 2, "Na3PO4": 3, "Li2CO3": 2,
}

def hitung_berat_ekivalen(senyawa, mr):
    valensi = valensi_data.get(senyawa, 1)
    return round(mr / valensi, 3), valensi

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

def hitung_standarisasi(mg_baku_primer, BE_or_BM, volume_mL, Fp=1):
    if BE_or_BM == 0 or volume_mL == 0:
        raise ValueError("BE/BM dan volume mL harus lebih besar dari nol.")
    return mg_baku_primer / (Fp * BE_or_BM * volume_mL)

# Untuk tombol navigasi: pakai session_state
if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

with st.sidebar:
    st.title("Menu COC")

    if st.button("Home"):
        st.session_state['page'] = "Home"
    if st.button("Penimbangan"):
        st.session_state['page'] = "Penimbangan"
    if st.button("Pengenceran"):
        st.session_state['page'] = "Pengenceran"
    if st.button("Standarisasi"):
        st.session_state['page'] = "Standarisasi"
    if st.button("Atom Relatif"):
        st.session_state['page'] = "Atom Relatif"
    if st.button("Tentang Kami"):
        st.session_state['page'] = "Tentang Kami"

page = st.session_state['page']

if page == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        Aplikasi ini dirancang untuk mempermudah pengguna dalam menghitung parameter kimia larutan, seperti:
        - Penimbangan berdasarkan konsentrasi
        - Pengenceran larutan
        - Standarisasi Normalitas dan Molaritas
        - Informasi atom relatif (Mr)

        COC sangat membantu dalam pembelajaran stoikiometri, yaitu perhitungan kuantitatif antar zat dalam reaksi kimia.
        Selamat mencoba!
    """)

elif page == "Penimbangan":
    st.header("Penimbangan Zat")
    rumus = st.text_input("Masukkan rumus senyawa (contoh: H2SO4, NaOH, KMnO4)")
    
    satuan = st.selectbox("Pilih satuan konsentrasi:", [
        "Molaritas (mol/L)", 
        "Normalitas (grek/L)", 
        "PPM", 
        "PPB", 
        "% (b/v)"
    ])
    
    konsentrasi = st.number_input("Masukkan konsentrasi:")
    volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

    with st.expander("📘 Penjelasan Satuan Konsentrasi"):
        st.markdown("""
        - **Molaritas (mol/L)**: jumlah mol zat per liter larutan
        - **Normalitas (grek/L)**: ekivalen zat per liter larutan
        - **PPM**: part per million → setara **mg/L**
        - **PPB**: part per billion → setara **µg/L**
        - **% (b/v)**: gram per 100 mL larutan
        """)

    if st.button("Hitung Penimbangan"): 
        if rumus:
            try:
                mr, detail = hitung_mr(rumus)
                be, valensi = hitung_berat_ekivalen(rumus, mr)
                st.success(f"Mr dari {rumus} = {mr} g/mol")
                st.info(f"Berat Ekivalen (BE) dari {rumus} = {be} g/grek (Valensi = {valensi})")

                volume_l = volume_ml / 1000
                if satuan == "Molaritas (mol/L)":
                    massa = konsentrasi * volume_l * mr
                    st.success(f"Massa = {konsentrasi} mol/L × {volume_l} L × {mr} g/mol = {massa:.4f} g")
                
                elif satuan == "Normalitas (grek/L)":
                    massa = konsentrasi * volume_l * be
                    st.success(f"Massa = {konsentrasi} grek/L × {volume_l} L × {be} g/grek = {massa:.4f} g")
                
                elif satuan == "PPM":
                    massa = konsentrasi * volume_l / 1000
                    st.success(f"Massa = {konsentrasi} mg/L × {volume_l} L ÷ 1000 = {massa:.4f} g")
                    st.info("Catatan: 1 ppm = 1 mg/L, maka massa = ppm × volume (L) ÷ 1000")

                elif satuan == "PPB":
                    massa = konsentrasi * volume_l / 1_000_000
                    st.success(f"Massa = {konsentrasi} µg/L × {volume_l} L ÷ 1.000.000 = {massa:.6f} g")
                    st.info("Catatan: 1 ppb = 1 µg/L, maka massa = ppb × volume (L) ÷ 1.000.000")

                elif satuan == "% (b/v)":
                    massa = konsentrasi * volume_ml / 100
                    st.success(f"Massa = {konsentrasi}% × {volume_ml} mL ÷ 100 = {massa:.4f} g")
                    st.info("Catatan: % b/v = gram per 100 mL, maka massa = % × volume ÷ 100")

            except Exception as e:
                st.error(str(e))

elif page == "Pengenceran":
    st.header("Pengenceran Larutan")
    pilihan = st.radio("Ingin menentukan apa?", ["Volume Awal (V1)", "Konsentrasi Awal (C1)"])

    if pilihan == "Volume Awal (V1)":
        c1 = st.number_input("Masukkan Konsentrasi Awal (C1):")
        c2 = st.number_input("Masukkan Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Masukkan Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung V1"):
            try:
                v1 = (v2 * c2) / c1
                st.success(f"Volume awal (V1) yang dibutuhkan: {v1:.2f} mL")
                st.code(f"V1 = (V2 × C2) / C1 = ({v2} × {c2}) / {c1} = {v1}")
            except ZeroDivisionError:
                st.error("Konsentrasi awal (C1) tidak boleh nol.")
    else:
        v1 = st.number_input("Masukkan Volume Awal (V1) dalam mL:")
        c2 = st.number_input("Masukkan Konsentrasi Yang Diinginkan (C2):")
        v2 = st.number_input("Masukkan Volume Yang Diinginkan (V2) dalam mL:")
        if st.button("Hitung C1"):
            try:
                c1 = (v2 * c2) / v1
                st.success(f"Konsentrasi awal (C1) yang diperlukan: {c1:.4f}")
                st.code(f"C1 = (V2 × C2) / V1 = ({v2} × {c2}) / {v1} = {c1}")
            except ZeroDivisionError:
                st.error("Volume awal (V1) tidak boleh nol.")

elif page == "Standarisasi":
    st.header("Standarisasi Normalitas dan Molaritas")
    mg_baku_primer = st.number_input("Massa baku primer (mg):", min_value=0.0)
    volume_ml = st.number_input("Volume titrasi (mL):", min_value=0.0)
    senyawa = st.selectbox("Pilih senyawa:", list(valensi_data.keys()))
    valensi = valensi_data.get(senyawa, 1)

    mr, _ = hitung_mr(senyawa)
    BE = mr / valensi
    BM = mr

    jenis = st.radio("Jenis perhitungan:", ["Normalitas (N)", "Molaritas (M)"])

    if st.button("Hitung Standarisasi"):
        try:
            if jenis == "Normalitas (N)":
                hasil = hitung_standarisasi(mg_baku_primer, BE, volume_ml)
                st.success(f"Normalitas (N) = {hasil:.6f} grek/L")
                st.info(f"Rumus: N = mg baku primer / (BE × Volume mL) dengan BE = Mr / Valensi = {BE:.3f}")

            else:
                hasil = hitung_standarisasi(mg_baku_primer, BM, volume_ml)
                st.success(f"Molaritas (M) = {hasil:.6f} mol/L")
                st.info(f"Rumus: M = mg baku primer / (BM × Volume mL) dengan BM = Mr = {BM:.3f}")

        except Exception as e:
            st.error(str(e))

elif page == "Atom Relatif":
    st.header("Perhitungan Mr (Berat Molekul Relatif)")
    rumus = st.text_input("Masukkan rumus molekul (contoh: H2SO4, KMnO4, NaCl)")
    if st.button("Hitung Mr"):
        try:
            mr, komposisi = hitung_mr(rumus)
            st.success(f"Mr dari {rumus} adalah {mr} g/mol")
            st.write("Komposisi atom:")
            for el, jml in komposisi.items():
                st.write(f"{el} : {jml}")
        except Exception as e:
            st.error(str(e))

elif page == "Tentang Kami":
    st.header("Tentang Kami")
    st.markdown("""
    **COC - Calculate Of Concentration**  
    Dikembangkan untuk mempermudah perhitungan kimia larutan.  
    Diperuntukkan untuk mahasiswa kimia, laboran, dan praktisi kimia.  
    Dibuat oleh Regant Tegar (AI Assisted)  
    """)
