import streamlit as st
import re

# Improved custom CSS with animated gradient and filled background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    body {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
        font-family: 'Orbitron', sans-serif;
        min-height: 100vh;
        margin: 0;
        padding: 0;
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

# Periodic table data with oxidation states for equivalent weight calculation
periodik = {
    "H": {"mass": 1.008, "oxidation": [1, -1]},
    "He": {"mass": 4.0026, "oxidation": [0]},
    "Li": {"mass": 6.94, "oxidation": [1]},
    "Be": {"mass": 9.0122, "oxidation": [2]},
    "B": {"mass": 10.81, "oxidation": [3]},
    "C": {"mass": 12.011, "oxidation": [4, 2, -4]},
    "N": {"mass": 14.007, "oxidation": [5, 4, 3, 2, -3]},
    "O": {"mass": 15.999, "oxidation": [-2]},
    "F": {"mass": 18.998, "oxidation": [-1]},
    "Ne": {"mass": 20.180, "oxidation": [0]},
    "Na": {"mass": 22.990, "oxidation": [1]},
    "Mg": {"mass": 24.305, "oxidation": [2]},
    "Al": {"mass": 26.982, "oxidation": [3]},
    "Si": {"mass": 28.085, "oxidation": [4, 2, -4]},
    "P": {"mass": 30.974, "oxidation": [5, 3, -3]},
    "S": {"mass": 32.06, "oxidation": [6, 4, 2, -2]},
    "Cl": {"mass": 35.45, "oxidation": [7, 5, 1, -1]},
    "Ar": {"mass": 39.948, "oxidation": [0]},
}

# Common acids, bases and salts for automatic equivalent weight determination
common_compounds = {
    "HCl": {"type": "acid", "H+": 1},
    "H2SO4": {"type": "acid", "H+": 2},
    "HNO3": {"type": "acid", "H+": 1},
    "H3PO4": {"type": "acid", "H+": 3},
    "CH3COOH": {"type": "acid", "H+": 1},
    "NaOH": {"type": "base", "OH-": 1},
    "KOH": {"type": "base", "OH-": 1},
    "Ca(OH)2": {"type": "base", "OH-": 2},
    "Ba(OH)2": {"type": "base", "OH-": 2},
    "Na2CO3": {"type": "salt", "n": 2, "charge": 2},
    "K2Cr2O7": {"type": "redox", "n": 6},  # Cr changes from +6 to +3 (3 electron change per Cr)
    "KMnO4": {"type": "redox", "n": 5},    # Mn changes from +7 to +2
}

def parse_formula(rumus):
    """Parse chemical formula including hydrates, returns element counts"""
    # Replace hydrated compounds like CuSO4.5H2O into CuSO4(H2O)5
    rumus = re.sub(r'\.(\d*H2O)', r'(\1)', rumus)
    
    # Handle hydrates by expanding them into individual elements
    def expand_hydrate(match):
        if match.group(3):
            return f"{match.group(2)}{match.group(1)}" * int(match.group(3))
        return match.group(2)
    
    rumus = re.sub(r'(\((\d*)(H2O)\))(\d+)', expand_hydrate, rumus)
    rumus = re.sub(r'(\((\d*)(H2O)\))', expand_hydrate, rumus)
    
    # Parse the formula
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
    result = {}
    for el in elements:
        if el not in periodik:
            raise ValueError(f"Unrecognized element: {el}")
        result[el] = result.get(el, 0) + 1
    return result

def calculate_equivalent_weight(formula, comp_type=None):
    """Calculate equivalent weight based on compound type"""
    elements = parse_formula(formula)
    mr = sum(periodik[el]["mass"] * count for el, count in elements.items())
    
    # Check if compound is in our common compounds database
    formula_no_hydrate = re.sub(r'\.?\d*H2O', '', formula)
    if formula_no_hydrate in common_compounds:
        comp_data = common_compounds[formula_no_hydrate]
        if comp_data["type"] == "acid":
            return mr / comp_data["H+"]
        elif comp_data["type"] == "base":
            return mr / comp_data["OH-"]
        elif comp_data["type"] == "salt":
            return mr / comp_data["charge"]
        elif comp_data["type"] == "redox":
            return mr / comp_data["n"]
    
    # If not in database, use general rules
    if comp_type == "acid":
        # Count number of H+ ions (H not in OH groups)
        # This is simplified - proper analysis would need structural formula
        h_count = elements.get("H", 0)
        return mr / h_count if h_count > 0 else mr
    elif comp_type == "base":
        # Count number of OH- groups
        # Simple estimate based on OH in formula
        oh_count = elements.get("O", 0)  # Very rough estimate
        return mr / oh_count if oh_count > 0 else mr
    elif comp_type == "salt":
        # For salts, equivalent weight is molecular weight divided by total charge
        # This is a simplification
        return mr / 2  # Default assumption of 2+ charge
    else:
        # For redox reactions, we'd need to know the electron change
        # Without specific info, we'll return None
        return None

def hitung_mr(rumus):
    komposisi = parse_formula(rumus)
    total = sum(periodik[el]["mass"] * jumlah for el, jumlah in komposisi.items())
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
    elif satuan == "% (b/v)":
        return konsentrasi * volume_l * 10, f"Massa = {konsentrasi}% × {volume_l} L × 10 = {konsentrasi * volume_l * 10:.4f} g"
    elif satuan == "PPM (mg/L)":
        mg = konsentrasi * volume_l
        return mg / 1000, f"Massa = {konsentrasi} mg/L × {volume_l} L = {mg} mg = {mg / 1000:.4f} g"
    elif satuan == "PPB (µg/L)":
        µg = konsentrasi * volume_l
        return µg / 1e6, f"Massa = {konsentrasi} µg/L × {volume_l} L = {µg} µg = {µg / 1e6:.8f} g"

def hitung_pengenceran(v1=None, c1=None, v2=None, c2=None):
    if v1 is None:
        return (v2 * c2) / c1, f"V1 = (V2 × C2) / C1 = ({v2} × {c2}) / {c1} = {(v2 * c2) / c1:.6f}"
    elif c1 is None:
        return (v2 * c2) / v1, f"C1 = (V2 × C2) / V1 = ({v2} × {c2}) / {v1} = {(v2 * c2) / v1:.6f}"

def convert_concentration(value, from_unit, to_unit):
    """Convert between concentration units"""
    conversions = {
        "Molaritas (g/mol)": {
            "Normalitas (g/grek)": lambda x, be: x * be,
            "% (b/v)": lambda x, _: x * 100,
            "PPM (mg/L)": lambda x, _: x * 1000,
            "PPB (µg/L)": lambda x, _: x * 1e6
        },
        "Normalitas (g/grek)": {
            "Molaritas (g/mol)": lambda x, be: x / be,
            "% (b/v)": lambda x, _: x * 100,
            "PPM (mg/L)": lambda x, _: x * 1000,
            "PPB (µg/L)": lambda x, _: x * 1e6
        },
        "% (b/v)": {
            "Molaritas (g/mol)": lambda x, _: x / 100,
            "Normalitas (g/grek)": lambda x, _: x / 100,
            "PPM (mg/L)": lambda x, _: x * 10000,
            "PPB (µg/L)": lambda x, _: x * 1e7
        },
        "PPM (mg/L)": {
            "Molaritas (g/mol)": lambda x, _: x / 1000,
            "Normalitas (g/grek)": lambda x, _: x / 1000,
            "% (b/v)": lambda x, _: x / 10000,
            "PPB (µg/L)": lambda x, _: x * 1000
        },
        "PPB (µg/L)": {
            "Molaritas (g/mol)": lambda x, _: x / 1e6,
            "Normalitas (g/grek)": lambda x, _: x / 1e6,
            "% (b/v)": lambda x, _: x / 1e7,
            "PPM (mg/L)": lambda x, _: x / 1000
        }
    }
    
    try:
        return conversions[from_unit][to_unit](value, 1)  # Passing 1 as default BE for non-molar conversions
    except KeyError:
        return value  # If conversion not defined, return original value

# Sidebar navigation
menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"])

# Main content
st.title("COC - Calculate Of Concentration")
st.write("Aplikasi untuk perhitungan kimia analisis")

if menu == "Home":
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
    COC (Calculate of Concentration) adalah aplikasi yang dirancang untuk membantu praktisi kimia dalam melakukan berbagai perhitungan penting dalam analisis kimia:

    ### Fitur Utama:
    - **Penimbangan Zat**: Menghitung massa zat yang dibutuhkan untuk membuat larutan dengan konsentrasi tertentu dalam berbagai satuan (Molaritas, Normalitas, %, PPM, PPB)
    - **Pengenceran Larutan**: Menghitung konsentrasi atau volume yang dibutuhkan saat melakukan pengenceran larutan
    - **Konversi Satuan**: Mengubah antar berbagai satuan konsentrasi dengan mudah

    ### Konsep Dasar Stoikiometri:
    Stoikiometri adalah bidang ilmu kimia yang mempelajari hubungan kuantitatif antara pereaksi dan produk dalam reaksi kimia. Aplikasi ini mengimplementasikan konsep:
    - Hukum Kekekalan Massa
    - Perbandingan stoikiometri dalam reaksi
    - Konsep mol dan hubungannya dengan massa
    - Konsentrasi larutan dalam berbagai satuan

    Aplikasi ini sangat berguna untuk:
    - Persiapan larutan standar
    - Perhitungan pengenceran
    - Konversi antara berbagai satuan konsentrasi
    - Praktikum kimia analisis
    """)

elif menu == "Penimbangan":
    st.subheader("Penimbangan Zat")
    with st.expander("Petunjuk Penggunaan"):
        st.write("""
        1. Masukkan rumus kimia senyawa (contoh: H2SO4, NaOH, K2Cr2O7, CuSO4.5H2O)
        2. Pilih jenis senyawa (asam, basa, garam) untuk menentukan berat ekivalen otomatis
        3. Masukkan parameter yang dibutuhkan (konsentrasi, volume)
        4. Klik tombol hitung untuk melihat hasil
        """)
        
    col1, col2 = st.columns(2)
    with col1:
        senyawa = st.text_input("Rumus kimia senyawa:")
    with col2:
        comp_type = st.selectbox("Jenis senyawa (untuk Normalitas):", 
                                ["Autodeteksi", "Asam", "Basa", "Garam", "Redoks"])
    
    try:
        if senyawa:
            mr, detail = hitung_mr(senyawa)
            st.success(f"Mr senyawa {senyawa} = {mr:.4f} g/mol")
            
            # Determine equivalent weight
            if comp_type == "Asam":
                be = calculate_equivalent_weight(senyawa, "acid")
            elif comp_type == "Basa":
                be = calculate_equivalent_weight(senyawa, "base")
            elif comp_type == "Garam":
                be = calculate_equivalent_weight(senyawa, "salt")
            elif comp_type == "Redoks":
                be = calculate_equivalent_weight(senyawa, "redox")
            else:
                be = calculate_equivalent_weight(senyawa)
                
            st.info(f"Berat ekivalen: {be:.4f} g/grek" if be is not None else "Tidak dapat menentukan berat ekivalen (perlu info reaksi redoks)")
            
            with st.expander(f"Komposisi atom {senyawa}"):
                for elemen, jumlah in detail.items():
                    st.write(f"{elemen}: {jumlah} atom × {periodik[elemen]['mass']} g/mol = {jumlah * periodik[elemen]['mass']:.3f} g")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        mr = None
        be = None

    konsentrasi = st.number_input("Konsentrasi yang diinginkan:", min_value=0.0, value=1.0)
    satuan = st.selectbox("Satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    volume_ml = st.number_input("Volume larutan (mL):", min_value=0.0, value=1000.0)

    if st.button("Hitung Massa"):
        try:
            volume_l = volume_ml / 1000
            if satuan == "Normalitas (g/grek)" and be is None:
                st.error("Harap tentukan jenis senyawa untuk menghitung Normalitas")
            else:
                hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan, be if satuan == "Normalitas (g/grek)" else None)
                st.success(f"**Massa yang harus ditimbang:** {hasil:.6f} g")
                with st.expander("Detail Perhitungan"):
                    st.code(penjelasan)
        except Exception as e:
            st.error(f"Error dalam perhitungan: {str(e)}")

    if st.button("Kembali ke Beranda"):
        st.experimental_rerun()

elif menu == "Pengenceran":
    st.subheader("Pengenceran Larutan")
    with st.expander("Rumus Pengenceran"):
        st.latex(r"C_1V_1 = C_2V_2")
        st.write("Dimana:")
        st.write("- C₁ = Konsentrasi larutan pekat")
        st.write("- V₁ = Volume larutan pekat yang dibutuhkan")
        st.write("- C₂ = Konsentrasi larutan encer yang diinginkan")
        st.write("- V₂ = Volume larutan encer yang akan dibuat")

    option = st.radio("Pilih perhitungan:", ["Tentukan V1", "Tentukan C1"], horizontal=True)

    if option == "Tentukan V1":
        c1 = st.number_input("Konsentrasi larutan pekat (C1):", min_value=0.0, value=1.0)
        c2 = st.number_input("Konsentrasi larutan encer (C2):", min_value=0.0, value=0.1)
        v2 = st.number_input("Volume larutan encer yang diinginkan (V2 dalam mL):", min_value=0.0, value=100.0)
        
        if st.button("Hitung Volume Awal (V1)"):
            try:
                v1, penjelasan = hitung_pengenceran(None, c1, v2 / 1000, c2)
                st.success(f"**Volume larutan pekat yang dibutuhkan:** {v1*1000:.4f} mL")
                with st.expander("Detail Perhitungan"):
                    st.code(penjelasan)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        v1 = st.number_input("Volume larutan pekat yang diambil (V1 dalam mL):", min_value=0.0, value=10.0)
        c2 = st.number_input("Konsentrasi larutan encer (C2):", min_value=0.0, value=0.1)
        v2 = st.number_input("Volume larutan encer yang diinginkan (V2 dalam mL):", min_value=0.0, value=100.0)
        
        if st.button("Hitung Konsentrasi Awal (C1)"):
            try:
                c1, penjelasan = hitung_pengenceran(v1 / 1000, None, v2 / 1000, c2)
                st.success(f"**Konsentrasi larutan pekat:** {c1:.6f}")
                with st.expander("Detail Perhitungan"):
                    st.code(penjelasan)
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif menu == "Konversi":
    st.subheader("Konversi Satuan Konsentrasi")
    with st.expander("Informasi Konversi"):
        st.write("""
        Konversi antar berbagai satuan konsentrasi:
        - **Molaritas (M)**: mol zat terlarut per liter larutan
        - **Normalitas (N)**: grek zat terlarut per liter larutan
        - **% b/v**: gram zat terlarut per 100 mL larutan
        - **PPM (mg/L)**: miligram zat terlarut per liter larutan
        - **PPB (µg/L)**: mikrogram zat terlarut per liter larutan
        """)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        value = st.number_input("Nilai konsentrasi:", min_value=0.0, value=1.0)
    with col2:
        from_unit = st.selectbox("Dari satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    with col3:
        to_unit = st.selectbox("Ke satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    
    if st.button("Konversi"):
        try:
            if from_unit == to_unit:
                st.warning("Anda memilih satuan yang sama!")
            else:
                # For molarity <-> normality conversions, we need equivalent weight
                if ("Molaritas" in from_unit and "Normalitas" in to_unit) or ("Normalitas" in from_unit and "Molaritas" in to_unit):
                    st.warning("Konversi Molaritas ↔ Normalitas membutuhkan Berat Ekivalen senyawa")
                    be = st.number_input("Masukkan Berat Ekivalen (g/grek):", min_value=0.0)
                    result = convert_concentration(value, from_unit, to_unit) * (be if "Normalitas" in to_unit else 1/be)
                else:
                    result = convert_concentration(value, from_unit, to_unit)
                
                st.success(f"Hasil konversi: {value} {from_unit} = {result:.8f} {to_unit}")
        except Exception as e:
            st.error(f"Error dalam konversi: {str(e)}")

elif menu == "Tentang Kami":
    st.subheader("Tentang COC")
    st.write("""
    **Calculate of Concentration** (COC) adalah aplikasi yang dikembangkan untuk mempermudah perhitungan dalam kimia analisis. 
    Dibuat oleh mahasiswa Program Studi Kimia Analisis, Politeknik AKA Bogor:
    """)
    
    st.write("""
    | Nama | NIM |
    |------|-----|
    | Andi Muhammad Tegar A A | 2460322 |
    | Inezza Azmi Tobri | 2460390 |
    | Muhammad Habibie Rasyha | 2460438 |
    | Saskia Putri Irfani | 2460512 |
    | Zahra Nandya Putri N | 2460543 |
    """)
    
    st.write("""
    ### Keunggulan Aplikasi:
    - **Otomatisasi Perhitungan**: Menghilangkan kesalahan manual dalam perhitungan konsentrasi
    - **Multi-satuan**: Mendukung berbagai satuan konsentrasi yang digunakan di laboratorium
    - **User Friendly**: Antarmuka yang mudah digunakan untuk praktisi kimia
    - **Edukatif**: Dilengkapi penjelasan konsep untuk membantu pemahaman
    
    Untuk informasi lebih lanjut, silakan hubungi kami di alamat@email.com
    """)

    st.image("https://placehold.co/600x200?text=Politeknik+AKA+Bogor", 
             caption="Politeknik AKA Bogor", use_column_width=True)
