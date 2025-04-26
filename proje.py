import streamlit as st
import pandas as pd
import time

# Başlık
st.title("Patates Ayıklama Takip Sistemi 🥔")
st.write("Bu panelde banttan geçen patateslerin ayıklanma durumlarını takip edebilirsiniz.")

# Saatler listesi
saatler = ['8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']

# DataFrame'i session_state içinde boş başlat
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Saatler", "Toplam Ayıklanan", "Çürük Patates", "Sağlam Patates"])

# Kullanıcı Veri Girişi
with st.form(key='patates_form'):
    st.subheader("Veri Girişi")
    saat = st.selectbox("Saat Seçin", saatler)
    toplam_ayiklanan = st.number_input("Toplam Ayıklanan Patates", min_value=0)
    curuk_patates = st.number_input("Çürük Patates", min_value=0)
    if st.form_submit_button("Verileri Kaydet"):
        saglam_patates = toplam_ayiklanan - curuk_patates
        new_row = pd.DataFrame([{
            "Saatler": saat,
            "Toplam Ayıklanan": toplam_ayiklanan, 
            "Çürük Patates": curuk_patates,
            "Sağlam Patates": saglam_patates
        }])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success(f"{saat} için veriler kaydedildi!")

# Eğer hiç veri yoksa uyarı gösterelim
if st.session_state.df.empty:
    st.info("Henüz veri girilmedi.")
else:
    # Grafik
    st.subheader("Saatlik Ayıklanan Patatesler Grafiği")
    st.line_chart(st.session_state.df.set_index("Saatler")[["Toplam Ayıklanan", "Çürük Patates", "Sağlam Patates"]])

    # Tablo
    st.subheader("Detaylı Saatlik Rapor")
    st.dataframe(st.session_state.df)

    # Rapor Özeti
    st.subheader("Toplam İstatistikler 📊")
    st.metric(label="Toplam Ayıklanan Patates", value=sum(st.session_state.df["Toplam Ayıklanan"]))
    st.metric(label="Toplam Çürük Patates", value=sum(st.session_state.df["Çürük Patates"]))
    st.metric(label="Toplam Sağlam Patates", value=sum(st.session_state.df["Sağlam Patates"]))

    # Zaman Çizelgesi
    st.subheader("Zaman Çizelgesi")
    st.line_chart(st.session_state.df.set_index("Saatler")[["Toplam Ayıklanan"]])

    # Gelişmiş İstatistikler
    st.subheader("Gelişmiş İstatistikler")
    st.write(f"Çürük Patateslerin Oranı: {sum(st.session_state.df['Çürük Patates']) / sum(st.session_state.df['Toplam Ayıklanan']):.2%}")

# İlerleme Çubuğu
if 'progress' not in st.session_state:
    st.session_state.progress = 0

if st.session_state.progress < 100:
    st.session_state.progress += 1
    progress_bar = st.progress(st.session_state.progress)
    time.sleep(0.05)

# Veri Yükleme
st.subheader("Veri Yükle")
uploaded_file = st.file_uploader("Veri Yükle", type=["csv", "xlsx"])
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.success("Yeni veri başarıyla yüklendi!")

# Veriyi CSV Olarak İndirme
st.subheader("Veri İndirme")
st.download_button(
    label="Veriyi CSV Olarak İndir",
    data=st.session_state.df.to_csv(index=False),
    file_name="patates_ayiklama.csv",
    mime="text/csv"
)

# Uyarılar
if not st.session_state.df.empty and sum(st.session_state.df["Çürük Patates"]) > 100:
    st.warning("Çürük patates sayısı yüksek! Dikkatli olmanız gerekebilir.")

