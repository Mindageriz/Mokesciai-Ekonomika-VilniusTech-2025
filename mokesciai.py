import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import math

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .main-title {font-size: 2.5em; text-align: center; color: #2c3e50;}
    .sub-title {font-size: 1.5em; color: #34495e;}
    .metric-box {background-color: #f8f9fa; padding: 10px; border-radius: 5px;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Atlyginimo mokesčių skaičiuoklė</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    atlyginimas = st.number_input("Mėnesinis atlyginimas (bruto, €)", min_value=0.0, value=1500.0, step=100.0)
    periodas = st.radio("Rodyti:", ["Mėnesinius", "Metinius"])

MMA = 1038
VDU = 126532.80
if atlyginimas <= 1038:
    npd = 747
elif atlyginimas > 1038 and atlyginimas <= 2387.29:
    npd = math.floor((747 - 0.49 * (atlyginimas - 1038)))    
elif atlyginimas > 2387.29 and atlyginimas < 2865:
    npd = math.floor((400 - 0.18 * (atlyginimas - 642)))
else:
    npd = 0

apmokestinamas = max(0, (atlyginimas - npd))
gpm = apmokestinamas * 0.20
vsd = atlyginimas * 0.1252
psd = atlyginimas * 0.0698
mokesciai_viso = gpm + vsd + psd
grynas = atlyginimas - mokesciai_viso

bvp = 70_000_000_000
gpm_biudzetas = 4_500_000_000
if periodas == "Metinius":
    faktor = 12
    bvp_indelis = ((mokesciai_viso * faktor) / bvp) * 100 
    gpm_indelis = ((gpm * faktor) / gpm_biudzetas) * 100  
else:
    faktor = 1
    bvp_indelis = ((mokesciai_viso * 12) / bvp) * 100 
    gpm_indelis = ((gpm * 12) / gpm_biudzetas) * 100 

st.markdown('<div class="sub-title">Tavo finansai</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    st.metric("Bruto atlyginimas", f"€{(atlyginimas * faktor):.2f}")
with col4:
    st.metric("Grynasis atlyginimas", f"€{(grynas * faktor):.2f}")
with col5:
    st.metric("Visi mokesčiai", f"€{(mokesciai_viso * faktor):.2f}")

if gpm == 0:
    st.warning("Dėl mažo atlyginimo GPM nėra taikomas. Mokesčių paskirstymas ir indėlis į ekonomiką nerodomi.")
else:
    pensijos = mokesciai_viso * 0.37
    sveikata = mokesciai_viso * 0.22
    svietimas = mokesciai_viso * 0.18
    infrastruktura = mokesciai_viso * 0.13
    gynyba = mokesciai_viso * 0.07
    kita = mokesciai_viso * 0.03

    gpm = gpm * faktor
    mokesciai_viso = mokesciai_viso * faktor
    grynas = grynas * faktor
    vsd = vsd * faktor
    psd = psd * faktor
    pensijos = pensijos * faktor
    sveikata = sveikata * faktor
    svietimas = svietimas * faktor
    infrastruktura = infrastruktura * faktor
    gynyba = gynyba * faktor
    kita = kita * faktor

    st.markdown('<div class="sub-title">Mokesčių detalės</div>', unsafe_allow_html=True)
    col6, col7 = st.columns([2, 4])
    with col6:
        st.write("**Mokesčių paskirstymas**")
        df = pd.DataFrame({
            "Kategorija": ["GPM", "VSD", "PSD"],
            "Suma (€)": [gpm, vsd, psd]
        })
        st.dataframe(df.style.format({"Suma (€)": "{:.2f}"}))
    with col7:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(df["Kategorija"], df["Suma (€)"], color="#4b7bec")
        ax.set_title("Mokesčių struktūra")
        st.pyplot(fig)

    st.markdown('<div class="sub-title">Kur keliauja tavo mokesčiai?</div>', unsafe_allow_html=True)
    col8, col9 = st.columns([2, 1])
    with col8:
        kategorijos = ["Pensijos", "Sveikata", "Švietimas", "Infrastruktūra", "Gynyba", "Kita"]
        sumos = [pensijos, sveikata, svietimas, infrastruktura, gynyba, kita]
        procentai = [37, 22, 18, 13, 7, 3]
        labels = [f"{kat}\n€{suma:.2f} ({proc}%)" for kat, suma, proc in zip(kategorijos, sumos, procentai)]
        colors = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f"]
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(procentai, labels=labels, colors=colors)
        ax.set_title("Mokesčių paskirstymas")
        st.pyplot(fig)
    with col9:
        st.write("**Paskirstymo detalės**")
        for kat, suma, proc in zip(kategorijos, sumos, procentai):
            st.write(f"{kat}: €{suma:.2f} ({proc}%)")

    st.markdown('<div class="sub-title">Kur keliauja tavo VSD įmokos?</div>', unsafe_allow_html=True)
    col_vsd1, col_vsd2 = st.columns([2, 1])
    vsd_viso = vsd
    vsd_kategorijos = ["Pensijos", "Ligos/Motinystė", "Nedarbas", "Nelaimingi atsitikimai", "Administravimas"]
    vsd_procentai = [65, 17, 7, 2, 2]
    vsd_sumos = [vsd_viso * (proc / 100) for proc in vsd_procentai]
    vsd_labels = [f"{kat}\n€{suma:.2f} ({proc}%)" for kat, suma, proc in zip(vsd_kategorijos, vsd_sumos, vsd_procentai)]
    vsd_colors = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e"]

    with col_vsd1:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(vsd_procentai, labels=vsd_labels, colors=vsd_colors)
        ax.set_title("VSD įmokų paskirstymas")
        st.pyplot(fig)
    with col_vsd2:
        st.write("**VSD paskirstymo detalės**")
        for kat, suma, proc in zip(vsd_kategorijos, vsd_sumos, vsd_procentai):
            st.write(f"{kat}: €{suma:.2f} ({proc}%)")

    st.markdown('<div class="sub-title">Tavo indėlis į Lietuvą</div>', unsafe_allow_html=True)
    col10, col11 = st.columns(2)
    with col10:
        st.metric("Prie BVP (€70 mlrd.)", f"{bvp_indelis:.6f}%")
    with col11:
        st.metric("Prie GPM (€4,5 mlrd.)", f"{gpm_indelis:.6f}%")

with st.expander("Daugiau informacijos"):
    st.write("Skaičiavimai pagrįsti 2025 m. tarifais.")