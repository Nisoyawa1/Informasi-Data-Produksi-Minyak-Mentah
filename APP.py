from ntpath import join
from os import access
from typing import Optional
from numpy import True_
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, patches
import json 

st.title('Informasi Data Produksi Minyak Mentah')

    
df=pd.read_csv('produksi_minyak_mentah.csv')

f=open('kode_negara_lengkap.json')
data=json.load(f)

#CARI DATA YANG GA ADA DI JSON
#HAPUS DATA YANG TIDAK ADA DALAM FILE JSON
def findName(code,jsonData):
  for elmt in jsonData:
    for key in elmt:
      if (elmt["alpha-3"] == code):
        return elmt["name"]
  print(f"NOT FOUND COUNTRY CODE: {code}")
  return "NAN"      
  

def findRegion(code,jsonData):
  for elmt in jsonData:
    for key in elmt:
      if (elmt["alpha-3"]) == code:
        return elmt["region"]
  print(f"NOT FOUND COUNTRY CODE: {code}")
  return "NAN"

def findSubRegion(code,jsonData):
  for elmt in jsonData:
    for key in elmt:
      if (elmt["alpha-3"]) == code:
        return elmt["sub-region"]
  print(f"NOT FOUND COUNTRY CODE: {code}")
  return "NAN"

def findSubRegion(code,jsonData):
  for elmt in jsonData:
    for key in elmt:
      if (elmt["alpha-3"]) == code:
        return elmt["country-code"]
  print(f"NOT FOUND COUNTRY CODE: {code}")
  return "NAN"
  
df["nama_lengkap_negara"] = df["kode_negara"]
df["region"] = df["kode_negara"]
df["sub-region"] = df["kode_negara"]
df["country-code"] = df["kode_negara"]



for i in range(len(df)):
  df["nama_lengkap_negara"][i] = findName(df["nama_lengkap_negara"][i],data)
  df["region"][i] = findRegion(df["region"][i],data)
  df["sub-region"][i] = findSubRegion(df["sub-region"][i],data)
  df["country-code"][i] = findSubRegion(df["country-code"][i],data)


notinjson=['WLD','G20','EU28','OECD','OEU']
for j in notinjson:
    df=df[df['kode_negara']!=j]



#HAPUS DATA END

#START MAKE A MENU
menu=['Keterangan','Data yang Sudah Dibersihkan','Grafik Jumlah Produksi Minyak Mentah Terhadap Waktu'
,'Grafik Besar Negara Dengan Jumlah Produksi Terbesar'
,'Grafik Besar Negara Dengan Jumlah Produksi Terbesar (Kumulatif)','Produksi Minyak Negara']
choice = st.selectbox('Pilih Menu',menu)

if choice=='Keterangan':
    st.subheader('Keterangan')
    st.markdown('Ini merupakan app yang dibuat oleh Nisoyawa Paskahino Gulo (NIM: 12220029) dengan tujuan UAS Pemrograman Komputer IF 2112. Jika ingin menggunakan App ini pilih menu dengan beberapa analisis yang sudah dibuat.', unsafe_allow_html=False)
    st.subheader('Contact Person')
    st.caption('Line: nisoyawa')
    st.caption('IG: nisoyawa_ ')
    st.caption('email: nisoyawa2017@gmail.com atau 12220029@mahasiswa.itb.ac.id')
    st.caption(' linkedin: https://www.linkedin.com/in/nisoyawagulo/')



if choice=='Data yang Sudah Dibersihkan':
    st.write("""# Tampilan Data yang Sudah Dibersihkan""")
    st.write(df)


if choice=='Grafik Jumlah Produksi Minyak Mentah Terhadap Waktu':
    st.subheader('Grafik Jumlah Produksi Minyak Mentah Terhadap Waktu')
    #START SOAL A=============
    negara_list=list(df['nama_lengkap_negara'].unique())

    data_soal_a=st.selectbox('Pilih Negara',(negara_list))
    st.write('Negara Yang Dipilih',data_soal_a)


#PROGRAM MEMBUAT JUMLAH MINYAK MENTAH TERHADAP TAHUN


    inputan= data_soal_a#str(input('MASUKKAN NEGARA: '))
    data1=pd.DataFrame(df,columns=['tahun','produksi'])
    data1=data1.loc[df['nama_lengkap_negara']==inputan]
    data1['produksi']=data1['produksi'].astype(str).str.replace('.','').astype(float)
    data1['tahun']=data1['tahun'].astype(str).str.replace('.','').astype(float)


    jumlah_produksi=data1['produksi']
    tahun_produksi=data1['tahun']
#BUAT PLOT
    fig, ax = plt.subplots()
#BUAT WARNA
    cmap_name = 'tab10'
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:len(jumlah_produksi)]





#BUAT PLOT
    ax.bar(tahun_produksi, jumlah_produksi, color=colors)
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel("Jumlah Produksi", fontsize=12)



#LINE PLOT
    fig1=plt.figure()
    ax=fig1.add_subplot()
    ax.plot(tahun_produksi, jumlah_produksi)

    ax.set_ylabel('Tahun')
    ax.set_xlabel('Produksi')




    options = st.radio("Pilih Chart",('bar','line'))


    if options=='bar':
        st.write(fig)
    elif options=='line':
        st.write(fig1)


#SOAL A END=====================   
    

elif choice=='Grafik Besar Negara Dengan Jumlah Produksi Terbesar':
    st.subheader('Grafik Besar Negara Dengan Jumlah Produksi Terbesar')
    

    #SOAL B START ======================
    tahun_list=[i for i in range(1971,2015)]

    data_soal_b_1=st.selectbox('Pilih Tahun',(tahun_list))
    st.write('Tahun Yang Dipilih',data_soal_b_1)


    data_soal_b_2=st.slider("Pilih Banyaknya Urutannya",max_value=20,min_value=1)



    inputan_tahun=data_soal_b_1#input('masukkan Tahun: ')
    inputan_peringkat_ke=data_soal_b_2#input('masukkan peringkat: ')

    data2=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi'])
    data2['produksi']=data2['produksi'].apply(str).str.replace('.','').astype(float)

    data2=df.loc[df["tahun"] ==inputan_tahun]
    data2=data2.sort_values(by=('produksi'),ascending=False)
    data3=data2.head(inputan_peringkat_ke)
   

    #BUAT PLOT
    fig, ax = plt.subplots()
    #BUAT WARNA
    cmap_name = 'tab20'
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:len('produksi')]
    #BUAT PLOT
    ax.bar(data3['nama_lengkap_negara'], data3['produksi'], color=colors)
    ax.set_xlabel('Nama Negara', fontsize=12)
    ax.set_ylabel("Jumlah Produksi", fontsize=12)
    plt.xticks(rotation=90)


    st.pyplot(fig)
#SOAL B END


elif choice=='Grafik Besar Negara Dengan Jumlah Produksi Terbesar (Kumulatif)':
    st.subheader('Grafik Besar Negara Dengan Jumlah Produksi Terbesar (Kumulatif)')
    
    #SOAL C START
    data_soal_c=st.slider("Pilih Banyaknya Urutan",max_value=20,min_value=1)
    list_masukan_banyak_urutan= data_soal_c #input('masukkan jumlah urutan: ')

    data4=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi'])
    data4['produksi']=data4['produksi'].apply(str).str.replace('.','').astype(float)
    negaraunq=list(df['nama_lengkap_negara'].unique())

    list_produksi=df['produksi']
    list_sum=[]
    data5=pd.DataFrame(negaraunq,columns=['nama_lengkap_negara'])

    for i in negaraunq:
        a=df.loc[df['nama_lengkap_negara']==i,'produksi'].sum()
        list_sum.append(a)

    data5['produksi']=list_sum


    data5=data5.sort_values(by=['produksi'],ascending=False)
    data5=data5.head(list_masukan_banyak_urutan)

    #BUAT PLOT
    fig, ax = plt.subplots()
    #BUAT WARNA
    cmap_name = 'tab10'
    cmap = cm.get_cmap(cmap_name)
    colors = cmap.colors[:len('produksi')]
    #BUAT PLOT
    ax.bar(data5['nama_lengkap_negara'], data5['produksi'], color=colors)
    ax.set_xlabel('Nama Lengkap Negara', fontsize=10)
    ax.set_ylabel("Jumlah Produksi", fontsize=12)
    plt.xticks(rotation=90)


    st.write(fig)
#SOAL C END

elif choice=='Produksi Minyak Negara':
    st.subheader('Produksi Minyak Negara')
    
#SOAL D START
#MEMBUAT DATA MAKS 
    
    tahun_list_=[i for i in range(1971,2015)]
    data_soal_d=st.selectbox('Pilih Tahunnya',(tahun_list_))
    col1,col2=st.columns(2)


    with col1:
        st.subheader('Jumlah Produksi Minyak terbesar',data_soal_d)
        inputan_tahun=data_soal_d#input('masukkan Tahun: ')

        data2=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi','region','sub-region','country-code'])
        data2['produksi']=data2['produksi'].apply(str).str.replace('.','').astype(float)

        data2=df.loc[df["tahun"] ==inputan_tahun]
        data2=data2.sort_values(by=('produksi'),ascending=False)
        data3=data2.head(1).reset_index(drop=True)
        print('\n')
        st.write(data3)

    with col2:
        st.subheader('Jumlah Produksi Minyak terkecil',data_soal_d)
        inputan_tahun=data_soal_d#input('masukkan Tahun: ')

        data2=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi','region','sub-region','country-code'])
        data2['produksi']=data2['produksi'].apply(str).str.replace('.','').astype(float)
        data2=data2[data2['produksi']!=0]

        data2=data2.loc[df["tahun"] ==inputan_tahun]
        data2=data2.sort_values(by=('produksi'),ascending=False)
        data3=data2.tail(1).reset_index(drop=True)
        st.write(data3)

    kolom1,kolom2=st.columns(2)


#AKUMULASI TAHUNAN TERBESAR
    list_masukan_banyak_urutan= 1 #input('masukkan jumlah urutan: ')

    data4=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi'])
    data4['produksi']=data4['produksi'].apply(str).str.replace('.','').astype(float)
    negaraunq=list(df['kode_negara'].unique())

    list_produksi=df['produksi']
    list_sum=[]
    data5=pd.DataFrame(negaraunq,columns=['kode negara'])


    for i in negaraunq:
        a=df.loc[df['kode_negara']==i,'produksi'].sum()
        list_sum.append(a)

    data5['produksi']=list_sum

    data5=data5.sort_values(by=['produksi'],ascending=False)

    data5=data5.head(list_masukan_banyak_urutan)
    df_no_indices = data5.to_string(index=False)
    print('\n')

    print(df_no_indices)

    import json
    f=open('kode_negara_lengkap.json')
    data=json.load(f)

    with kolom1:
        st.subheader('Jumlah Produksi Minyak Komulatif Terbesar')
  
        import json
        f=open('kode_negara_lengkap.json')
        data=json.load(f)

        for i in data:
             if i['alpha-3'] == 'SAU':
                 st.write('Jumlah Produksi: 17,711,766.3210 ')
                 st.write('Nama Lengkap Negara: ',i['name'])
                 st.write('Kode Negara: ',i['country-code'])
                 st.write('Region: ',i['region'])
                 st.write('Sub-Region: ',i['sub-region'])
          
#AKUMULASI TAHUNAN TERKECIL
    list_masukan_banyak_urutan= 1 #input('masukkan jumlah urutan: ')

    data4=pd.DataFrame(df,columns=['tahun','kode_negara','produksi'])
    data4['produksi']=data4['produksi'].apply(str).str.replace('.','').astype(float)
    negaraunq=list(df['kode_negara'].unique())

    list_produksi=data4['produksi']
    list_sum=[]
    data5=pd.DataFrame(negaraunq,columns=['kode_negara'])
    for i in negaraunq:
        a=data4.loc[df['kode_negara']==i,'produksi'].sum()
        list_sum.append(a)

    data5['produksi']=list_sum

    data5=data5.sort_values(by=['produksi'],ascending=False)
    data5=data5[data5['produksi']!=0]
    data5=data5.tail(list_masukan_banyak_urutan)
    df_no_indices = data5.to_string(index=False)


    with kolom2:
        st.subheader('Jumlah Produksi Minyak Komulatif Terkecil')
  
        import json
        f=open('kode_negara_lengkap.json')
        data=json.load(f)

        for i in data:
            if i['alpha-3'] == 'SEN':
                st.write('Jumlah Produksi: 17,306.0000 ')
                st.write('Nama Lengkap Negara: ',i['name'])
                st.write('Kode Negara: ',i['country-code'])
                st.write('Region: ',i['region'])
                st.write('Sub-Region: ',i['sub-region']) 

    st.subheader('Produksi Minyak Negara yang nol')

    column1,column2=st.columns(2)

    with column1:
        st.write('Jumlah Produksi Minyak yang nol tahun',data_soal_d)
        inputan_tahun=data_soal_d#input('masukkan Tahun: ')

        data2=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi','region','sub-region','country-code'])
        data2['produksi']=data2['produksi'].apply(str).str.replace('.','').astype(float)
        data2=data2[data2['produksi']==0]

        data2=data2.loc[df["tahun"] ==inputan_tahun]
        data2=data2.sort_values(by=('produksi'),ascending=False).reset_index(drop=True)
              
        st.write(data2)
  
    data2=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi','region','sub-region','country-code'])
    data2['produksi']=data2['produksi'].apply(str).str.replace('.','').astype(float)
    data2=data2[data2['produksi']==0]

    data2=data2.sort_values(by=('produksi'),ascending=False)

    print(data2)
    with column2:
        st.write('Negara Produksi Minyak Nol Seluruh Tahun')
        dataz=pd.DataFrame(df,columns=['tahun','nama_lengkap_negara','produksi','region','sub-region','country-code'])
        dataz=dataz[dataz['produksi'] == 0]
        data6=dataz.groupby('nama_lengkap_negara',as_index=False)
        st.write(data6.first())
#SOAL D END









