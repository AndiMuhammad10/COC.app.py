import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Custom CSS for background and font (sama seperti sebelumnya)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
    }
    
    .stButton button {
        background-color: #7E57C2;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Tabel Periodik Lengkap (sama seperti sebelumnya)
periodik = {
    "H": 1.008, "He": 4.0026, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
    # ... [seluruh elemen lainnya] ...
}

# Database senyawa umum dengan berat ekivalen
common_compounds = {
    "HCl": {"type": "acid", "H+": 1, "be": 36.46},
    "H2SO4": {"type": "acid", "H+": 2, "be": 49.04},
    "NaOH": {"type": "base", "OH-": 1, "be": 40.00},
    # ... [senyawa lainnya] ...
}

def parse_formula(rumus):
    # ... [fungsi parsing yang sama] ...

def hitung_mr(rumus):
    komposisi = parse_formula(rumus)
    total = sum(periodik[el] * jumlah for el, jumlah in komposisi.items())
    return round(total, 3), komposisi

def hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen=None):
    if satuan == "Molaritas (g/mol)":
        mol = konsentrasi * volume_l
        return mol * mr, f"mol = {konsentrasi} mol/L × {volume_l} L = {mol:.4f} mol\nMassa = {mol:.4f} mol × {mr} g/mol = {mol * mr:.4f} g"
    elif satuan == "Normalitas (g/grek)":
        if berat_ekivalen is None:
            raise ValueError("Berat ekivalen harus diberikan untuk Normalitas.")
        grek = konsentrasi * volume_l
        return grek * berat_ekivalen, f"grek = {konsentrasi} grek/L × {volume_l} L = {grek:.4f} grek\nMassa = {grek:.4f} grek × {berat_ekivalen} g/grek = {grek * berat_ekivalen:.4f} g"
    # ... [satuan lainnya] ...

# Sidebar navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

# Tampilan halaman
if menu == "Penimbangan":
    st.header("Penimbangan Zat")
    senyawa = st.text_input("Masukkan rumus kimia senyawa")
    
    try:
        if senyawa:
            mr, detail = hitung_mr(senyawa)
            st.success(f"Mr dari {senyawa} adalah {mr} g/mol")
            
            # Bagian yang Anda mau - deteksi otomatis berat ekivalen
            berat_ekivalen = None
            if senyawa in common_compounds:
                berat_ekivalen = common_compounds[senyawa]["be"] 
                st.info(f"Berat Ekivalen: {berat_ekivalen:.4f} g/grek (otomatis terdeteksi)")
            else:
                st.warning("Berat ekivalen tidak terdeteksi otomatis")
            
            with st.expander("Detail Atom"):
                for elemen, jumlah in detail.items():
                    st.write(f"{elemen}: {jumlah} atom × {periodik[elemen]} g/mol = {jumlah * periodik[elemen]:.3f} g")
    
    except Exception as e:
        st.error(str(e))
        mr = None

    konsentrasi = st.number_input("Masukkan konsentrasi yang diinginkan:")
    satuan = st.selectbox("Pilih satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)"])
    volume_ml = st.number_input("Masukkan volume larutan (dalam mL):")

    if st.button("Hitung Massa") and mr is not None:
        volume_l = volume_ml / 1000
        
        # Gunakan berat ekivalen jika tersedia untuk Normalitas
        if satuan == "Normalitas (g/grek)":
            if senyawa in common_compounds:
                hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan, common_compounds[senyawa]["be"])
            else:
                st.error("Tidak dapat menghitung Normalitas: berat ekivalen tidak diketahui")
                st.stop()
        else:
            hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan)
        
        st.success(f"Massa {senyawa} yang harus ditimbang: {hasil:.4f} g")
        with st.expander("Lihat Perhitungan"):
            st.code(penjelasan)

    if st.button("Kembali ke Beranda"):
        st.experimental_rerun()

elif menu == "Konversi":
    st.header("Konversi Satuan")
    
    # Tab terpisah seperti yang Anda mau
    tab1, tab2 = st.tabs(["Konversi Konsentrasi", "Massa Atom Relatif"])
    
    with tab1:
        # ... [kode konversi] ...
    
    with tab2:
        element_input = st.text_input("Masukkan simbol unsur:")
        if st.button("Cari Massa Atom"):
            if element_input in periodik:
                st.success(f"Massa atom {element_input}: {periodik[element_input]:.4f}")
            else:
                st.error("Unsur tidak dikenali!")
    
    if st.button("Kembali ke Beranda"):
        st.experimental_rerun()

# ... [halaman lainnya tetap sama] ...
