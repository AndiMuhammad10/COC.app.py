import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Tabel Periodik Sederhana
periodik = {
    "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.81, "C": 12.01,
    "N": 14.01, "O": 16.00, "F": 19.00, "Ne": 20.18, "Na": 22.99, "Mg": 24.31,
    "Al": 26.98, "Si": 28.09, "P": 30.97, "S": 32.07, "Cl": 35.45, "Ar": 39.95,
    "K": 39.10, "Ca": 40.08, "Mn": 54.94, "Fe": 55.85, "Cu": 63.55, "Zn": 65.38,
    "Br": 79.90, "Ag": 107.87, "I": 126.90, "Ba": 137.33, "Hg": 200.59, "Pb": 207.2
}

# Fungsi untuk parsing rumus kimia
def hitung_mr(senyawa):
    pattern = r"([A-Z][a-z]?)(\d*)"
    matches = re.findall(pattern, senyawa)
    mr = 0
    for elemen, jumlah in matches:
        if elemen not in periodik:
            raise ValueError(f"Elemen tidak dikenali: {elemen}")
        jumlah = int(jumlah) if jumlah else 1
        mr += periodik[elemen] * jumlah
    return round(mr, 3)

# Fungsi menghitung massa dari konsentrasi

def hitung_gram(mr, konsentrasi, volume_l, satuan):
    if satuan == "Molaritas (g/mol)":
        mol = konsentrasi * volume_l
        return mol * mr, f"mol = {konsentrasi} mol/L × {volume_l} L = {mol} mol\nMassa = {mol} mol × {mr} g/mol = {mol * mr} g"
    elif satuan == "Normalitas (g/grek)":
        grek = konsentrasi * volume_l
        return grek * mr, f"grek = {konsentrasi} grek/L × {volume_l} L = {grek} grek\nMassa = {grek} grek × {mr} g/grek = {grek * mr} g"
    elif satuan == "% (b/v)":
        return konsentrasi * volume_l * 10, f"Massa = {konsentrasi}% × {volume_l} L × 10 = {konsentrasi * volume_l * 10} g"
    elif satuan == "PPM (mg/L)":
        mg = konsentrasi * volume_l
        return mg / 1000, f"Massa = {konsentrasi} mg/L × {volume_l} L = {mg} mg = {mg / 1000} g"

# Fungsi pengenceran

def hitung_pengenceran(v1=None, c1=None, v2=None, c2=None):
    if v1 is None:
        return (v2 * c2) / c1, f"V1 = (V2 × C2) / C1 = ({v2} × {c2}) / {c1} = {(v2 * c2) / c1}"
    elif c1 is None:
        return (v2 * c2) / v1, f"C1 = (V2 × C2) / V1 = ({v2} × {c2}) / {v1} = {(v2 * c2) / v1}"

# Sidebar navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Tentang Kami"])

# Tampilan halaman
if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        Aplikasi ini dibuat untuk membantu Anda menghitung berbagai parameter dalam kimia larutan seperti:
        - Penimbangan larutan berdasarkan konsentrasi
        - Pengenceran larutan

        Materi ini berkaitan erat dengan stoikiometri, yaitu ilmu yang mempelajari perbandingan kuantitatif antara reaktan dan produk dalam reaksi kimia.
    """)

elif menu == "Penimbangan":
    st.header("Penimbangan Zat")
    senyawa = st.text_input("Masukkan rumus kimia senyawa (contoh: NaOH, KMnO4, CuSO45H2O)")
    try:
        if senyawa:
            mr = hitung_mr(senyawa)
            st.success(f"Mr dari {senyawa} adalah {mr} g/mol")
    except Exception as e:
        st.error(str(e))
        mr = None

    konsentrasi = st.number_input("Masukkan konsentrasi yang diinginkan:")
    satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)"])
    volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

    if st.button("Hitung Massa") and mr is not None:
        volume_l = volume_ml / 1000
        hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan)
        st.success(f"Massa {senyawa} yang harus ditimbang: {hasil:.4f} g")
        with st.expander("Lihat Perhitungan"):
            st.code(penjelasan)

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

elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.write("""
    Aplikasi ini dikembangkan oleh:

    - Regant Tegar (NIM: 12345678)
    - Teman 1 (NIM: 23456789)
    - Teman 2 (NIM: 34567890)
    - Teman 3 (NIM: 45678901)

    Mahasiswa AKA Bogor - Kimia Analisis
    """)
