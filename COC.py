import streamlit as st

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Sidebar navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Tentang Kami"])

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
    senyawa = st.text_input("Masukkan nama senyawa (contoh: NaOH, KMnO4)")
    mr = st.number_input("Masukkan Mr senyawa tersebut:", min_value=1.0)
    konsentrasi = st.number_input("Masukkan konsentrasi yang diinginkan:")
    satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)"])
    volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

    if st.button("Hitung Massa"):
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
