import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sb
 
df = pd.read_csv('dashboard/main_data.csv')

st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")
st.title('Bike Sharing Analysis')
st.write('by Adrian Reynold Ga  adrian.reynold.ga@gmail.com')

if 'page_number' not in st.session_state:
    st.session_state['page_number'] = 1  

total_rows = len(df)
total_pages = math.ceil(total_rows / 10)
page_number = st.session_state['page_number']
start_idx = (page_number - 1) * 10
end_idx = start_idx + 10

st.write(f"### Page {page_number} of {total_pages}")
st.dataframe(df.iloc[start_idx:end_idx])

button_col = st.columns([1, 1])  

with button_col[0]:
    if st.button("Previous"):
        if st.session_state['page_number'] > 1:
            st.session_state['page_number'] -= 1

with button_col[1]:
    if st.button("Next"):
        if st.session_state['page_number'] < math.ceil(len(df) / 10):
            st.session_state['page_number'] += 1


df['datetime'] = pd.to_datetime(df['datetime'])
df['year_month'] = df['datetime'].dt.to_period('M')

st.write('')
st.write('')
st.write('')
st.write('')

st.write("## Select Monthly Range for Graph")

year_months = df['year_month'].astype(str).unique()

start_month = st.selectbox("Start Month", options=year_months, index=0)
end_month = st.selectbox("End Month", options=year_months, index=len(year_months)-1)

if start_month > end_month:
    st.warning("Start month cannot be greater than end month. Please adjust your selection.")
else:

    filtered_data = df[(df['year_month'] >= start_month) & (df['year_month'] <= end_month)]
    monthly_data = filtered_data.groupby('year_month')['count'].sum().reset_index()

    monthly_data['year_month'] = monthly_data['year_month'].astype(str)
    
    plt.figure(figsize=(10, 6))
    sb.lineplot(data=monthly_data, x='year_month', y='count', marker='o', color='blue')
    plt.gca().set_facecolor('#0e1117')  
    plt.gcf().set_facecolor('#0e1117')  

    st.write('')
    st.write('')
    st.write('')

    plt.title(f'Bike Sharing Count from {start_month} to {end_month}', color='white')
    plt.xlabel('Month', color='white')
    plt.ylabel('Count', color='white')

    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    
    plt.xticks(rotation=45)
    plt.title(f'Bike Sharing Count from {start_month} to {end_month}')
    plt.xlabel('Month', color='white')
    plt.ylabel('Count', color='white')
    
    st.pyplot(plt)

monthly_data = df.groupby(['year', 'month'])['count'].sum().reset_index()

monthly_pivot = monthly_data.pivot(index='month', columns='year', values='count')
monthly_pivot.columns = ['2011', '2012']
monthly_pivot = monthly_pivot.sort_index()
monthly_pivot['growth (%)'] = ((monthly_pivot['2012'] - monthly_pivot['2011']) / monthly_pivot['2011']) * 100

st.write(monthly_pivot)

st.write('Graph ini menunjukkan performa penyewaan sepeda dari waktu ke waktu dalam rentang per bulan. Dapat dilihat jika terjadi pertumbuhan permintaan pada tahun 2012 jika dibandingkan dengan tahun sebelumnya, terjadi pertumbuhan yang signifikan dimana pertumbuhan terendah berada pada angka +41%, dan tertinggi pada angka +157%')

st.write('')
st.write('')
st.write('')
st.write('')

df['hour'] = df['datetime'].dt.hour

st.write("## Select Day Type for Graph")

filter_option = st.radio("Select Workday or Holiday:", ('Workday', 'Holiday'))

if filter_option.lower() == 'workday':
    filtered_data = df[df['workday'] == 'Workday']
else:
    filtered_data = df[df['workday'] == 'Holiday']

if filtered_data.empty:
    st.write("No data available for this filter.")
else:
    hourly_sum_filtered = filtered_data.groupby('hour')['count'].sum().reset_index()
    
    plt.figure(figsize=(20, 10))
    sb.barplot(x='hour', y='count', data=hourly_sum_filtered, color='blue')  
    plt.title(f'Total Bike Count for Each Hour on {filter_option}s', color='white')
    plt.xticks(rotation=45, color='white')
    plt.yticks(color='white')
    plt.tight_layout()
    plt.grid(True)
    plt.xlabel('Hour', color='white')
    plt.ylabel('Count', color='white')
    plt.gca().set_facecolor('#0e1117')  
    plt.gcf().set_facecolor('#0e1117')

    st.pyplot(plt)

st.write('Dari graf untuk hari kerja, menunjukkan aktifitas sekolah dan kantor yang sangat mempengaruhi meningkatnya jumlah penyewaan sepeda, sedangkan graf hari libur menunjukkan fluktuasi yang cukup normal dalam jumlah penyewaan sepeda, yang disebabkan kurangnya urgensi bepergian pada jam tertentu')

st.write('')
st.write('')
st.write('')
st.write('')

st.write("### Correlation Matrix")
numerical_columns = ['temperature', 'humidity', 'windspeed', 'count']
correlation_matrix = df[numerical_columns].corr()

plt.figure(figsize=(12, 8))
sb.heatmap(correlation_matrix, annot=True, cmap='RdBu', vmin=-1, vmax=1, color='white')
plt.title('Correlation Between Weather Variables and Bike Rental Count', color='white')
plt.gca().set_facecolor('#0e1117')
plt.gcf().set_facecolor('#0e1117')
plt.xticks(color='white') 
plt.yticks(color='white')

st.pyplot(plt)

weather_per_season = df.groupby(['season', 'weather']).size().reset_index(name='count')

plt.figure(figsize=(10, 6))
sb.barplot(x='season', y='count', hue='weather', data=weather_per_season, color='blue')

plt.xlabel('Musim', color='white')
plt.ylabel('Tingkat Kemunculan', color='white')
plt.gca().set_facecolor('#0e1117') 
plt.gcf().set_facecolor('#0e1117')
plt.xticks(rotation=45, color='white')
plt.yticks(color='white')
plt.title('Kondisi Cuaca per Musim', color='white')

st.pyplot(plt)
plt.clf()

st.write('Dari graf ini menunjukkan musim sangat mempengaruhi performa penyewaan sepeda, seperti summer dan fall yang mayoritas memiliki cuaca cerah menyebabkan jumlah sewa yang meningkat. Lalu berkaca dari tabel korelasi, temperatur cukup mempengaruhi pilihan untuk menyewa sepeda. Temperatur yang dingin cenderung membuat orang untuk menggunakan mobil atau tranportasi umum lainnya, sedangkan kelembapan dan kecepatan angin kurang berpengaruh pada performa penyewaan sepeda. Hal ini mungkin disebabkan oleh kurangnya kondisi ekstrim yang tercatat pada dataframe ini.')


