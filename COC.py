import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

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

# Fungsi parsing rumus

def parse_formula(rumus):
    rumus = rumus.upper()
    rumus = re.sub(r'(\d+)([A-Z])', r'\1 \2', rumus)
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

def konversi_volume(angka, satuan):
    return angka / 1000 if satuan == "mL" else angka

menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Tentang Kami"])

if menu == "Home":
    st.title("Selamat Datang di COC")
    st.write("Website ini dirancang untuk membantu menghitung konsentrasi larutan kimia secara mudah dan akurat.")
    st.subheader("Tentang COC")
    st.write("COC (Calculate of Concentration) adalah alat bantu interaktif berbasis web untuk perhitungan stoikiometri dan konsentrasi.")

elif menu == "Penimbangan":
    st.title("Penimbangan Zat Kimia")
    senyawa = st.text_input("Masukkan rumus senyawa (misal: NaOH, CuSO4.5H2O, Fe(OH)3)")
    try:
        if senyawa:
            mr = 0
            komposisi = parse_formula(senyawa)
            for el, jumlah in komposisi.items():
                mr += periodik[el] * jumlah
            mr = round(mr, 3)
            st.success(f"Mr dari {senyawa.upper()} adalah {mr} g/mol")
            with st.expander("Detail Atom"):
                for el, jumlah in komposisi.items():
                    st.write(f"{el}: {jumlah} × {periodik[el]} = {jumlah * periodik[el]:.3f}")
    except Exception as e:
        st.error(str(e))
        mr = None

    konsentrasi = st.number_input("Masukkan konsentrasi:")
    satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)"])
    volume_val = st.number_input("Masukkan volume larutan:")
    volume_unit = st.selectbox("Pilih satuan volume:", ["mL", "L"])

    def hitung_gram(mr, konsentrasi, volume_l, satuan):
        if satuan == "Molaritas (g/mol)":
            mol = konsentrasi * volume_l
            return mol * mr, f"mol = {konsentrasi} × {volume_l} = {mol}\nMassa = {mol} × {mr} = {mol * mr} g"
        elif satuan == "Normalitas (g/grek)":
            grek = konsentrasi * volume_l
            return grek * mr, f"grek = {konsentrasi} × {volume_l} = {grek}\nMassa = {grek} × {mr} = {grek * mr} g"
        elif satuan == "% (b/v)":
            return konsentrasi * volume_l * 10, f"Massa = {konsentrasi}% × {volume_l} L × 10 = {konsentrasi * volume_l * 10} g"
        elif satuan == "PPM (mg/L)":
            mg = konsentrasi * volume_l
            return mg / 1000, f"Massa = {konsentrasi} mg/L × {volume_l} L = {mg} mg = {mg / 1000} g"

    if st.button("Hitung Massa") and mr is not None:
        volume_l = konversi_volume(volume_val, volume_unit)
        hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan)
        st.success(f"Massa {senyawa.upper()} yang harus ditimbang: {hasil:.4f} g")
        with st.expander("Lihat Perhitungan"):
            st.code(penjelasan)

elif menu == "Pengenceran":
    st.title("Pengenceran Larutan")
    metode = st.radio("Tentukan yang ingin dihitung:", ["Volume akhir", "Konsentrasi akhir"])
    if metode == "Volume akhir":
        c1 = st.number_input("Konsentrasi awal (C1)")
        c2 = st.number_input("Konsentrasi yang diinginkan (C2)")
        v1 = st.number_input("Volume awal (V1) dalam L")
        if st.button("Hitung Volume Akhir"):
            v2 = (c1 * v1) / c2 if c2 != 0 else 0
            st.success(f"Volume akhir (V2) = {v2:.4f} L")
    else:
        v1 = st.number_input("Volume awal (V1) dalam L")
        v2 = st.number_input("Volume akhir (V2) dalam L")
        c1 = st.number_input("Konsentrasi awal (C1)")
        if st.button("Hitung Konsentrasi Akhir"):
            c2 = (c1 * v1) / v2 if v2 != 0 else 0
            st.success(f"Konsentrasi akhir (C2) = {c2:.4f}")

elif menu == "Tentang Kami":
    st.title("Tentang Kami")
    st.markdown("""
    **Nama-nama Anggota Tim:**
    
    - Regant Tegar (NIM: 123456)
    - Teman 1 (NIM: 123457)
    - Teman 2 (NIM: 123458)
    - Teman 3 (NIM: 123459)
    """)
