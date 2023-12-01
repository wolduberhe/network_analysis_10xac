import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Slack Messages')
st.text('Channel Members Analysis')

upload_file = st.file_uploader("Upload your file")

if upload_file:
    df = pd.read_csv(upload_file)
    st.header('Data Header')
    st.write(df.head())

    st.header('Data Statistics')    
    st.write(df.describe())  

    df = df[:3]
    fig, ax = plt.subplots(1, 1)
    ax.bar(df['Channel'], df['ReplyCount'])
    ax.set_xlabel('channel')
    ax.set_ylabel('replycount')

    st.pyplot(fig)


