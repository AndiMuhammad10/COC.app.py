import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Custom CSS for background and font
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Orbitron:wght@500;600;700&display=swap');
    
    body {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background-color: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: #BB86FC;
        margin-bottom: 1rem;
    }
    
    .stMarkdown h1 {
        font-size: 2.5rem;
        border-bottom: 2px solid #03DAC6;
        padding-bottom: 0.5rem;
    }
    
    .stMarkdown h2 {
        font-size: 2rem;
        color: #03DAC6;
    }
    
    .stTextInput input, 
    .stNumberInput input, 
    .stSelectbox select {
        background-color: rgba(30, 30, 60, 0.5) !important;
        color: white !important;
        border: 1px solid #BB86FC !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
    }
    
    .stButton button {
        background-color: #7E57C2 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #BB86FC !important;
        transform: translateY(-2px);
    }
    
    .stAlert {
        background-color: rgba(30, 30, 60, 0.7) !important;
        border-left: 4px solid #7E57C2;
        border-radius: 8px;
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
    # ... [all other elements from original code] ...
}

# Common compounds for automatic equivalent weight
common_compounds = {
    # ... [same as original code] ...
}

def parse_formula(rumus):
    # ... [same as original code] ...

def hitung_mr(rumus):
    # ... [same as original code] ...

def hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen=None):
    # ... [same as original code] ...

def hitung_pengenceran(v1=None, c1=None, v2=None, c2=None):
    # ... [same as original code] ...

menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        Aplikasi ini dibuat untuk membantu Anda menghitung berbagai parameter dalam kimia larutan:
        - Penimbangan larutan berdasarkan konsentrasi
        - Pengenceran larutan
        - Konversi satuan konsentrasi
    """)

elif menu == "Penimbangan":
    st.header("Penimbangan Zat")
    
    # ... [same form inputs as original code] ...
    
    if st.button("Kembali ke Beranda", key="penimbangan_home"):
        menu = "Home"  # This will redirect to home page
        st.experimental_rerun()

elif menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    
    # ... [same form inputs as original code] ...
    
    if st.button("Kembali ke Beranda", key="pengenceran_home"):
        menu = "Home"
        st.experimental_rerun()

elif menu == "Konversi":
    st.header("Konversi Satuan")
    
    # Konversi Satuan Form
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Konversi Konsentrasi")
        value = st.number_input("Nilai konsentrasi:")
        from_unit = st.selectbox("Dari satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
        to_unit = st.selectbox("Ke satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
        
        if st.button("Konversi"):
            # ... [same conversion logic as original] ...
    
    with col2:
        st.subheader("Atom Relatif")
        element_input = st.text_input("Simbol unsur:")
        
        if st.button("Cari Massa Atom"):
            if element_input in periodik:
                st.success(f"Massa atom {element_input}: {periodik[element_input]:.4f}")
            else:
                st.error("Unsur tidak dikenali!")
    
    if st.button("Kembali ke Beranda", key="konversi_home"):
        menu = "Home"
        st.experimental_rerun()

elif menu == "Tentang Kami":
    st.header("Tentang Kami")
    st.write("""
    Aplikasi ini dikembangkan oleh tim kimia analisis.
    """)
    
    # ... [rest of about page as original] ...

    if st.button("Kembali ke Beranda"):
        menu = "Home"
        st.experimental_rerun()
