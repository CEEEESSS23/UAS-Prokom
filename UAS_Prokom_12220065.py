import json
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

#Mochamad Ricki Andriansyah
#12220065
#UAS PROKOM 2021

# Open JSON
f = open("kode_negara_lengkap.json")
data = json.load(f)
# Open Excel
df = pd.read_csv(
    "produksi_minyak_mentah.csv")

st.set_page_config(page_title='Data Produksi Minyak', layout='wide', page_icon=':fire:')
st.markdown('<p style="font-family: sans-serif; font-size: 40px;"><b>Data Produksi Minyak</b></p>', unsafe_allow_html = True)
st.markdown('<p style="font-family: sans-serif; font-size: 20px;">Mochamad Ricki Andriansyah/12220065</p>', unsafe_allow_html = True)
#A
listnama_negara = []
for i in list(df['kode_negara']):
    for j in data:
        if i == str(j["alpha-3"]):
            if str(j["name"]) not in listnama_negara:
                listnama_negara.append(str(j["name"]))
    
n_negara = st.selectbox(
    "Negara apa yang ingin anda ketahui produksinya: ", listnama_negara)

x = dict()
for i in data:
    nama_negara = str(i["name"])
    kode_negara = str(i["alpha-3"])
    listnama_negara.append(nama_negara)

    x[nama_negara] = kode_negara

kodenegara = x[n_negara]
data_new = df.loc[df["kode_negara"] == kodenegara]
data_new.plot(kind="bar", x="tahun", y="produksi", grid=True)
fig1 = plt.show()

st.pyplot(fig1)

#B
# Notes : n --> jumlah negara ,  t --> timeframe yang diinginkan
n = st.number_input(
    "Masukkan jumlah negara yang ingin anda periksa: ", min_value=1)
t = st.number_input("Pada tahun berapaa nih pengen diliatnya: ", min_value=1)

# ide nya : sorting berdasarkan tahun dulu nanti baru berdasarkan jumlah
# x --> total produksi
x = dict()

for i in data:
    kode = str(i["alpha-3"])
    # pengen dapet tahun aja dari excel
    datax = df.loc[df["tahun"] == int(t)]
    # check di json karena ada beberapa negara yang gada di excel
    data_new = datax.loc[datax["kode_negara"] == kode]
    # Untuk kode negara yang sama itu di sum, ditambahin semua jadi kumulatif
    # total
    x[kode] = data_new.sum()["produksi"]
    # print(x[kode]) --> check

# nyimpen semua dict dengan key dan val nya, kalo problem ini kode sama
# total produksi
data_items = x.items()
lst = list(data_items)
# print(lst) --> check

# Membuat data frame dari list baru
dfakhir = pd.DataFrame(data=lst, columns=['kode_negara', 'produksi'])
# sorting value
data_new2 = dfakhir.sort_values(["produksi"], ascending=[0])
data_new3 = data_new2[1:int(n) + 1]

fig2, ax = plt.subplots()
data_new3.plot.bar(x='kode_negara', y='produksi', rot=15, title="Grafik " + str(n) +
                   " negara dengan produksi terbesar pada tahun " + str(t), figsize=(15, 10), color="red")

fig2 = plt.show()
st.pyplot(fig2)

st.set_option('deprecation.showPyplotGlobalUse', False)

#C
Jumlah_Negara = st.slider(
    "Masukkan jumlah negara yang ingin anda periksa: ", min_value=1, max_value=100)

x = dict()
for i in data:
    kode = str(i["alpha-3"])
    # check di json karena ada beberapa negara yang gada di excel
    data_new = df.loc[df["kode_negara"] == kode]
    # Untuk kode negara yang sama itu di sum, ditambahin semua jadi kumulatif
    # total
    x[kode] = data_new.sum()["produksi"]
    # print(x[kode])

    # nyimpen semua dict dengan key dan val nya, kalo problem ini kode sama
    # total produksi
    data_items = x.items()
    lst = list(data_items)
    # print(lst)

    # Membuat data frame dari list baru
    df_new = pd.DataFrame(data=lst, columns=['kode_negara', 'produksi'])

    # sorting value
data_new2 = df_new.sort_values(["produksi"], ascending=[0])
data_new3 = data_new2[1:int(Jumlah_Negara) + 1]

data_new3.plot(x='kode_negara', y='produksi', title="Grafik negara dengan produksi terbesar secara kumulatif ",
               grid=True, xlabel=" kode negara ", ylabel=" Total Produksi ", kind="bar")
fig3 = plt.show()
st.pyplot(fig3)

# D
bahan_dfnew = []
for i in data:
    nama_negara = i.get('name')
    kode_negara = i.get('alpha-3')
    reg_negara = i.get('region')
    subreg_negara = i.get('sub-region')
    kode_negara1 = i.get('country-code')
    bahan_dfnew.append([nama_negara, kode_negara,
                         reg_negara, subreg_negara, kode_negara1])

# Prdoduuksi Terbesar Kumulatif
st.info("Negara Penghasil Minyak Terbesar Kumulatif")
terbesar_kumulatif = df.groupby('kode_negara', as_index=False).sum()
terbesar_kumulatif = terbesar_kumulatif.sort_values(by='produksi', ascending=False)
terbesar_kumulatif = terbesar_kumulatif[:1]
terbesar_kumulatif = terbesar_kumulatif[['kode_negara', 'produksi']]
pilih = terbesar_kumulatif.iloc[0, 0]

for i in bahan_dfnew:
    if i[1] == pilih:
        st.write("Negara      : " + i[0])
        st.write("Kode Negara : " + i[4])
        st.write("Region      : " + i[2])
        st.write("Sub-Region  : " + i[3])
st.write('Total produksi :' + str(terbesar_kumulatif.iloc[0, 1]))

# Produksi Terbesar Spasial
B3 = st.number_input("Tahun produksi yang ingin dicari", 2000, key="biga")
st.info("Negara produksi Minyak Terbesar pada tahun " + str(B3))
terbesar_spasial = df.loc[df["tahun"] == B3]
terbesar_spasial = terbesar_spasial.loc[terbesar_spasial["produksi"] > 0]
terbesar_spasial = terbesar_spasial.sort_values(by='produksi', ascending=False)
terbesar_spasial = terbesar_spasial[:1]
terbesar_spasial = terbesar_spasial[['kode_negara', 'produksi']]
pilih = terbesar_spasial.iloc[0, 0]

for i in bahan_dfnew:
    if i[1] == pilih:
        st.write("Negara      : " + i[0])
        st.write("Kode Negara : " + i[4])
        st.write("Region      : " + i[2])
        st.write("Sub-Region  : " + i[3])
st.write('Total produksi :' + str(terbesar_spasial.iloc[0, 1]))

# Produksi Terkecil Kumulatif
st.info("Negara Penghasil Produsen Minyak Terkecil Kumulatif")
terkecil_kumulatif = df.groupby('kode_negara', as_index=False).sum()
terkecil_kumulatif = terkecil_kumulatif.loc[terkecil_kumulatif["produksi"] > 0]
terkecil_kumulatif = terkecil_kumulatif.sort_values(by='produksi', ascending=True)
terkecil_kumulatif = terkecil_kumulatif[:1]
terkecil_kumulatif = terkecil_kumulatif[['kode_negara', 'produksi']]
pilih = terkecil_kumulatif.iloc[0, 0]

for i in bahan_dfnew:
    if i[1] == pilih:
        st.write("Negara      : " + i[0])
        st.write("Kode Negara : " + i[4])
        st.write("Region      : " + i[2])
        st.write("Sub-Region  : " + i[3])
st.write('Total produksi :' + str(terkecil_kumulatif.iloc[0, 1]))

# Produksi Terkecil Spasial
st.info("Negara Produksi Minyak Terkecil pada tahun " + str(B3))
terkecil_spasial = df.loc[df["produksi"] > 0]
terkecil_spasial = terkecil_spasial.loc[df["tahun"] == B3]
terkecil_spasial = terkecil_spasial.sort_values(by='produksi', ascending=True)
terkecil_spasial = terkecil_spasial[:1]
terkecil_spasial = terkecil_spasial[['kode_negara', 'produksi']]
pilih = terkecil_spasial.iloc[0, 0]

for i in bahan_dfnew:
    if i[1] == pilih:
        st.write("Negara      : " + i[0])
        st.write("Kode Negara : " + i[4])
        st.write("Region      : " + i[2])
        st.write("Sub-Region  : " + i[3])
st.write('Total produksi :' + str(terkecil_spasial.iloc[0, 1]))

# Tidak ada produksi kumulatif
st.info(" Negara yang Tidak Memproduksi Minyak ")
nol_kumulatif = df.groupby('kode_negara', as_index=False).sum()
nol_kumulatif = nol_kumulatif.loc[nol_kumulatif["produksi"] == 0]
list_n = nol_kumulatif['kode_negara'].tolist()
kumpulan = []
for c in list_n:
    for i in bahan_dfnew:
        if i[1] == c:
            kumpulan.append(
                [i[0], i[4], i[2], i[3]])
nol_kumulatif1 = pd.DataFrame(kumpulan, columns=[
                   'Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.table(nol_kumulatif1)

# Tidak ada produksi per tahun input
st.info(" Negara yang Tidak Memproduksi Minyak Pada Tahun " + str(B3))
nol_spasial = df.loc[df["produksi"] == 0]
nol_spasial = nol_spasial.loc[nol_spasial["tahun"] == B3]
list_n = nol_spasial['kode_negara'].tolist()
kumpulan = []
for c in list_n:
    for i in bahan_dfnew:
        if i[1] == c:
            kumpulan.append(
                [i[0], i[4], i[2], i[3]])
nol_spasial1 = pd.DataFrame(kumpulan, columns=[
                    'Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.table(nol_spasial)
