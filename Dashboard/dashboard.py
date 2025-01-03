import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

day_df = pd.read_csv("Dashboard/day.csv")

def convert_to_datetime(df):
    df['dteday'] = pd.to_datetime(df['dteday'])

    df['yr'] = df['dteday'].dt.year
    df['mnth'] = df['dteday'].dt.month


datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

st.header('Sewa Sepeda :sparkles:')

chart_bulan = main_df.groupby(by="mnth").agg({
    "instant": "nunique",
    "cnt": ["mean"]
})

mean_cnt = chart_bulan[('cnt', 'mean')]

plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt.index, y=mean_cnt.values, palette="viridis")
plt.title("Rata-Rata Jumlah Terbanyak Penyewa per Bulan", fontsize=16)
plt.xlabel("Bulan", fontsize=14)
plt.ylabel("Rata-rata", fontsize=14)
plt.xticks(ticks=range(len(mean_cnt.index)), labels=mean_cnt.index)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(plt)

chart_tahun = main_df.groupby(by="yr").agg({
    "instant": "nunique",
    "cnt": ["mean"]
})

mean_cnt = chart_tahun[('cnt', 'mean')]

plt.figure(figsize=(10, 6))
sns.barplot(x=mean_cnt.index, y=mean_cnt.values, palette="viridis")
plt.title("Rata-Rata Jumlah Terbanyak Penyewa per tahun", fontsize=16)
plt.xlabel("Tahun", fontsize=14)
plt.ylabel("Rata-rata", fontsize=14)
plt.xticks(ticks=range(len(mean_cnt.index)), labels=mean_cnt.index)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(plt)
