#import libraries
from msilib.schema import TextStyle
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime  # Import datetime module
import warnings
import os
import sys
import base64  # Import base64 module
from io import BytesIO





warnings.filterwarnings('ignore')
st.set_page_config(page_title="المخازن-تمسكو",page_icon=":factory:",layout="wide")
header = st.container()
header.image('logo.png', width=100) 
# Title of the web app
with header:
    st.title(" :bar_chart: TEMSCO Warehouse DashBoard")


st.markdown('<style>div.block-container{padding-top:3rem;}</style>',unsafe_allow_html=True)

f1= st.file_uploader(":file_folder: Upload a file",type=(["csv","xlsx","xls"]))
if f1 is not None:
    filename=f1.name
    st.write(filename)
    df=pd.read_excel(filename)
else:
    st.warning("Please upload a file to start filtering the DataFrame.")
    sys.exit()

st.write('## Dataframe :')
st.write(df)

# Filter DataFrame based on selected date range
col1, col2 = st.columns((2, 2))



st.sidebar.header("Choose Your Filter:")
custname=st.sidebar.multiselect("Pich your Customer Name" , df["Cust-name"].unique())

if not custname:
    df2=df.copy()
else:
    df2=df[df["Cust-name"].isin(custname)]

st.sidebar.header("Choose Your itmname:")
itm_cd_list = df["Itm-CD"].fillna(0).astype(int).unique()  # Get unique values of itm-cd
itm_cd = st.sidebar.selectbox("Select Item Code", itm_cd_list)

# Filter itm-name based on selected itm-cd
if itm_cd:
    itm_names = df[df["Itm-CD"] == itm_cd]["Itm-name"].unique()
    selected_itm_names = st.sidebar.multiselect("Select Item Name", itm_names)
    st.write("Selected Item Names:", selected_itm_names)


custbal=df2.groupby(by=["Cust-name"],as_index=False)["Balance"].sum()

with col1:
    st.subheader("Customer net Balance")
    fig=px.bar(df,x="Cust-name",y="Balance")
    st.plotly_chart(fig,use_container_width=True,height=200)
with col2:
    st.subheader('Iron-Hardness vs Iron-thicknes')
    #fig=px.scatter(custbal, x='Iron-Hardness', y='Iron-thikness', color='Itm-CD', title='Iron-Hardness vs Iron-thickness')
    scatter_fig = px.scatter(df, x='Iron-Hardness', y='Iron-thikness', color='Itm-CD')
    st.plotly_chart(scatter_fig)

with col1:
    
    hist_fig = px.histogram(df, x='Height', title='Itm Name Height')
    st.plotly_chart(hist_fig)
with col2:
    #st.subheader('Box plot of QTY grouped by UOM')
    #box_fig = px.box(df, x='UOM', y='QTY', title='QTY Distribution by UOM')
    #st.plotly_chart(box_fig)
    # Pie chart of 'Cust-name' distribution
    
    Cust_distribution = df['Cust-name'].value_counts()
    pie_fig = px.pie(values=Cust_distribution, names=Cust_distribution.index, title='Customer Name Distribution')
    st.plotly_chart(pie_fig)



if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

    # Getting the min and max dates
    StartDate = pd.to_datetime(df["Date"]).min()
    EndDate = pd.to_datetime(df["Date"]).max()

    with col1:
        date1 = st.date_input("Start Date", None, StartDate, EndDate)

    with col2:
        date2 = st.date_input("End Date", None, StartDate, EndDate)

    if date1 is not None and date2 is not None:
        # Convert datetime.date to datetime.datetime
        date1 = datetime.combine(date1, datetime.min.time())
        date2 = datetime.combine(date2, datetime.min.time())
        
        filtered_df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()
        st.write('## Filtered Dataframe :')
        st.write(filtered_df)
        
       # Add a button to download the filtered DataFrame as an Excel file
        if st.button('Download Filtered Data as Excel'):
            # Writing the DataFrame to BytesIO buffer
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                filtered_df.to_excel(writer, index=False)
            excel_buffer.seek(0)
            
            # Encoding the buffer's contents as base64
            b64 = base64.b64encode(excel_buffer.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="filtered_data.xlsx">Download Excel</a>'
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Please select a date range.")
else:
    st.warning("Please upload a file to start filtering the DataFrame.")