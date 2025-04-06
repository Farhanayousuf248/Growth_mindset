import streamlit as st
import pandas as pd
import os
from io import BytesIO



# set_up our App
st.set_page_config(page_title= "Data Sweeper", layout= "wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and Excel formate with built-in data cleaning and visualization!")

uploaded_files = st.file_uploader("upload your (CSV or Excel):", type=["csv","xlsx"],accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"usuppoerted file type:{file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File SIze:** {file.size/1024}")

        # show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Option for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate from {file.name}"):
                    df.drop_duplicate(inplace=True)
            
            with col2:
                if st.button(f"Fill Missing Value for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["numbers"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Value have been Filled!")


        # Choose Specific Columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


    # Creat Some Visualizations
    st.subheader("Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
        st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

    # Convert the file -> CSV to Excel
    st.subheader("Conversion Options")
    conversion_type = st.radio(f"Convert {file.name}to:",["CSV","Excel"],key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer,index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type == "Excel":
            df.to_excel(buffer,index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        # Download Button
        st.download(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            filename=file_name,
            mime=mime_type
        )
    
st.success("All files processed!")
