import streamlit as st
import re

st.set_page_config(page_title="COC - Calculate Of Concentration", layout="wide")

# Modern stylish purple theme with elegant fonts
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Orbitron:wght@500;600;700&display=swap');
    
    :root {
        --primary: #7E57C2;
        --dark: #1A1A2E;
        --light: #F0F0F5;
        --accent: #BB86FC;
        --secondary: #03DAC6;
    }
    
    body {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: var(--light);
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
        color: var(--accent);
        margin-bottom: 1rem;
    }
    
    .stMarkdown h1 {
        font-size: 2.5rem;
        border-bottom: 2px solid var(--secondary);
        padding-bottom: 0.5rem;
    }
    
    .stMarkdown h2 {
        font-size: 2rem;
        color: var(--secondary);
    }
    
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: rgba(30, 30, 60, 0.5) !important;
        color: white !important;
        border: 1px solid var(--accent) !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton button {
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        background-color: var(--accent) !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(26, 26, 46, 0.8) !important;
        backdrop-filter: blur(8px);
        border-right: 1px solid var(--primary);
    }
    
    .stAlert {
        background-color: rgba(30, 30, 60, 0.7) !important;
        border-left: 4px solid var(--primary);
        border-radius: 8px;
    }
    
    [role="radiogroup"] {
        background-color: rgba(30, 30, 60, 0.5) !important;
        padding: 15px !important;
        border-radius: 8px;
        border: 1px solid var(--accent);
    }
    
    .stExpander {
        background-color: rgba(30, 30, 60, 0.5) !important;
        border-radius: 8px !important;
        margin-bottom: 1rem;
    }
    
    .stExpander label {
        font-weight: 600 !important;
        color: var(--secondary) !important;
    }
    
    .stCodeBlock {
        background-color: rgba(20, 20, 40, 0.8) !important;
        border-radius: 8px;
        padding: 15px !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 40, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary);
        border-radius: 4px;
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

# Common compounds for automatic equivalent weight
common_compounds = {
    "HCl": {"type": "acid", "H+": 1, "be": 1.008},
    "H2SO4": {"type": "acid", "H+": 2, "be": 49.04},
    "HNO3": {"type": "acid", "H+": 1, "be": 63.01},
    "H3PO4": {"type": "acid", "H+": 3, "be": 32.67},
    "CH3COOH": {"type": "acid", "H+": 1, "be": 60.05},
    "NaOH": {"type": "base", "OH-": 1, "be": 40.00},
    "KOH": {"type": "base", "OH-": 1, "be": 56.11},
    "Ca(OH)2": {"type": "base", "OH-": 2, "be": 37.05},
    "Ba(OH)2": {"type": "base", "OH-": 2, "be": 85.68},
    "Na2CO3": {"type": "salt", "n": 2, "charge": 2, "be": 52.99},
    "K2Cr2O7": {"type": "redox", "n": 6, "be": 49.03},
    "KMnO4": {"type": "redox", "n": 5, "be": 31.61},
}

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

    rumus = re.sub(r'\((\w+)\)(\d+)', lambda m: f"{m.group(2)}{m.group(1)}", rumus)
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

menu = st.sidebar.radio("Navigasi", ["Home", "Penimbangan", "Pengenceran", "Konversi", "Tentang Kami"], key='nav')

if menu == "Home":
    st.title("COC - Calculate Of Concentration")
    st.subheader("Selamat datang di aplikasi COC")
    st.write("""
        <div style="font-size:1.1rem; line-height:1.8">
        Aplikasi ini dibuat untuk membantu Anda menghitung berbagai parameter dalam kimia larutan secara modern dan efisien:
        <ul>
            <li>Penimbangan larutan berdasarkan konsentrasi</li>
            <li>Pengenceran larutan dengan presisi</li>
            <li>Konversi antar berbagai satuan konsentrasi</li>
        </ul>
        
        Materi ini berkaitan erat dengan stoikiometri, yaitu jantung dari analisis kimia kuantitatif. Dengan antarmuka yang intuitif dan perhitungan akurat, COC membantu Anda memahami:
        <ul>
            <li>Hubungan stoikiometri dalam reaksi</li>
            <li>Perhitungan konsentrasi yang presisi</li>
            <li>Teknik pengenceran yang tepat</li>
        </ul>
        </div>
    """, unsafe_allow_html=True)
    st.image("https://placehold.co/600x200?text=Chemistry+Calculation+Tool", use_column_width=True)

elif menu == "Penimbangan":
    st.header("Penimbangan Zat")
    with st.expander("Petunjuk Penggunaan", expanded=True):
        st.write("""
        **Masukkan rumus kimia senyawa**, sistem akan secara otomatis:
        - Menghitung massa molekul relatif (Mr)
        - Menentukan berat ekivalen (untuk normalitas)
        - Menampilkan komposisi atom
        """)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        senyawa = st.text_input("Rumus kimia senyawa:", placeholder="Misal: KMnO4, Ca(OH)2, CuSO4.5H2O")
    with col2:
        st.write("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("ℹ️ Petunjuk"):
            st.toast("Masukkan rumus kimia seperti contoh di placeholder")

    try:
        if senyawa:
            mr, detail = hitung_mr(senyawa)
            st.success(f"**Massa Molekul Relatif (Mr):** {mr:.4f} g/mol")
            
            with st.expander(f"Komposisi Atom {senyawa}"):
                for elemen, jumlah in detail.items():
                    st.write(f"- {elemen}: {jumlah} atom × {periodik[elemen]} g/mol = {jumlah * periodik[elemen]:.3f} g")
                    
            # Auto-determine equivalent weight if compound is known
            berat_ekivalen = None
            if senyawa in common_compounds:
                berat_ekivalen = common_compounds[senyawa]["be"]
                st.info(f"**Berat Ekivalen:** {berat_ekivalen:.4f} g/grek (otomatis terdeteksi)")
            else:
                st.warning("Berat ekivalen tidak terdeteksi secara otomatis")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        mr = None
        berat_ekivalen = None

    konsentrasi = st.number_input("Konsentrasi yang diinginkan:", min_value=0.0, value=1.0, step=0.1)
    satuan = st.selectbox("Satuan konsentrasi:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    volume_ml = st.number_input("Volume larutan (mL):", min_value=0.0, value=1000.0, step=1.0)

    if st.button("Hitung Massa", type="primary"):
        if not mr:
            st.error("Masukkan rumus senyawa yang valid terlebih dahulu")
            st.stop()
        
        volume_l = volume_ml / 1000
        
        if satuan == "Normalitas (g/grek)":
            if not berat_ekivalen:
                st.error("Tidak bisa menghitung Normalitas: berat ekivalen tidak diketahui")
                st.stop()
                
        hasil, penjelasan = hitung_gram(mr, konsentrasi, volume_l, satuan, berat_ekivalen)
        
        st.success(f"**Massa yang harus ditimbang:** {hasil:.6f} gram")
        with st.expander("Detail Perhitungan", expanded=True):
            st.code(penjelasan)
    
    if st.button("Kembali ke Beranda"):
        st.experimental_rerun()

elif menu == "Pengenceran":
    st.header("Pengenceran Larutan")
    with st.expander("Rumus Pengenceran", expanded=True):
        st.latex(r"C_1V_1 = C_2V_2")
        st.write("""
        **Dimana:**
        - C₁ = Konsentrasi awal
        - V₁ = Volume awal
        - C₂ = Konsentrasi akhir
        - V₂ = Volume akhir
        """)

    option = st.radio("Pilih perhitungan:", ["Tentukan Volume Awal (V₁)", "Tentukan Konsentrasi Awal (C₁)"], horizontal=True)

    if option == "Tentukan Volume Awal (V₁)":
        c1 = st.number_input("Konsentrasi awal (C₁):", min_value=0.0, value=1.0)
        c2 = st.number_input("Konsentrasi yang diinginkan (C₂):", min_value=0.0, value=0.1)
        v2 = st.number_input("Volume yang diinginkan (V₂ dalam mL):", min_value=0.0, value=100.0)
        
        if st.button("Hitung Volume Awal (V₁)"):
            try:
                v1, penjelasan = hitung_pengenceran(None, c1, v2 / 1000, c2)
                st.success(f"**Volume larutan pekat yang dibutuhkan:** {v1*1000:.4f} mL")
                with st.expander("Detail Perhitungan"):
                    st.code(penjelasan)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        v1 = st.number_input("Volume larutan pekat (V₁ dalam mL):", min_value=0.0, value=10.0)
        c2 = st.number_input("Konsentrasi yang diinginkan (C₂):", min_value=0.0, value=0.1)
        v2 = st.number_input("Volume yang diinginkan (V₂ dalam mL):", min_value=0.0, value=100.0)
        
        if st.button("Hitung Konsentrasi Awal (C₁)"):
            try:
                c1, penjelasan = hitung_pengenceran(v1 / 1000, None, v2 / 1000, c2)
                st.success(f"**Konsentrasi larutan pekat:** {c1:.6f}")
                with st.expander("Detail Perhitungan"):
                    st.code(penjelasan)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    if st.button("Kembali ke Beranda"):
        st.experimental_rerun()

elif menu == "Konversi":
    st.header("Konversi Satuan Konsentrasi")
    with st.expander("Informasi Konversi", expanded=True):
        st.write("""
        **Faktor Konversi Umum:**
        - 1 Molar (M) = 1000 ppm (untuk senyawa dengan Mr ~100 g/mol)
        - 1% (b/v) = 10 g/L = 10,000 ppm
        - 1 ppm = 1000 ppb
        
        **Catatan:** Faktor konversi sebenarnya tergantung pada massa molekul relatif (Mr) senyawa
        """)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        value = st.number_input("Nilai konsentrasi:", min_value=0.0, value=1.0)
    with col2:
        from_unit = st.selectbox("Dari satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    with col3:
        to_unit = st.selectbox("Ke satuan:", ["Molaritas (g/mol)", "Normalitas (g/grek)", "% (b/v)", "PPM (mg/L)", "PPB (µg/L)"])
    
    # Simulasikan konversi (implementasi nyata akan lebih kompleks)
    if st.button("Konversi", type="primary"):
        try:
            if from_unit == to_unit:
                st.warning("Anda memilih satuan yang sama!")
            else:
                # Ini hanya simulasi sederhana - implementasi aktual akan menghitung berdasarkan Mr
                factors = {
                    "Molaritas (g/mol)": 1,
                    "Normalitas (g/grek)": 1,
                    "% (b/v)": 10,
                    "PPM (mg/L)": 1000,
                    "PPB (µg/L)": 1000000
                }
                result = value * factors[to_unit] / factors[from_unit]
                st.success(f"**Hasil konversi:** {value:.4f} {from_unit} = {result:.4f} {to_unit}")
                
                with st.expander("Detail Konversi"):
                    st.write(f"Faktor konversi dari {from_unit} ke {to_unit}:")
                    st.write(f"{factors[to_unit] / factors[from_unit]:.4f}")
        except Exception as e:
            st.error(f"Error dalam konversi: {str(e)}")

    st.divider()
    
    # Tambahkan fitur tambahan untuk menghitung massa atom relatif
    st.subheader("Massa Atom Relatif")
    element_input = st.text_input("Masukkan simbol unsur atau rumus senyawa:")
    
    if element_input:
        try:
            if element_input in periodik:
                st.info(f"Massa atom relatif {element_input}: {periodik[element_input]:.4f}")
            else:
                mr, _ = hitung_mr(element_input)
                st.info(f"Massa molekul relatif {element_input}: {mr:.4f}")
        except Exception as e:
            st.error(f"Tidak dapat menghitung massa untuk '{element_input}': {str(e)}")

    if st.button("Kembali ke Beranda", key="konversi_home"):
        st.experimental_rerun()

elif menu == "Tentang Kami":
    st.header("Tentang COC")
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
    ### Fitur Utama:
    - **Penimbangan Presisi**: Hitung massa zat dengan akurat berdasarkan konsentrasi
    - **Pengenceran Akurat**: Lakukan pengenceran dengan perhitungan tepat
    - **Konversi Satuan**: Ubah antar berbagai satuan konsentrasi
    - **Informasi Stoikiometri**: Dapatkan pemahaman mendalam tentang dasar-dasar perhitungan kimia
    
    Untuk informasi lebih lanjut, silakan hubungi melalui email: coc.chemistry@aka.ac.id
    """)

    st.image("https://placehold.co/600x200?text=Politeknik+AKA+Bogor", caption="Politeknik AKA Bogor", use_column_width=True)
