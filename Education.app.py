import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Educational Infrastructure and Access Dashboard",
    page_icon="📚",
    layout="wide"
)
@st.cache_data
def load_data():
    df=pd.read_csv("education_cleaned.csv")
    
    return df
df=load_data()

def main():
    st.sidebar.title("🏫📚Educational Infrastructure and Access")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Options")
    
    School_type_filter=st.sidebar.selectbox(
         "Select School type:",
         options=["All School type"] + sorted(df['School_type'].unique().tolist())
    )

    Management_type_filter=st.sidebar.selectbox(
         "Select Management type:",
         options=["All Management type"] + sorted(df['Management_type'].unique().tolist())
    )

    Lga_filter=st.sidebar.multiselect( 
         "Select LGA",
         options=df['Unique_lga'].unique().tolist(),
         default=df['Unique_lga'].unique().tolist()
    )

    filtered_data=df.copy()
    if School_type_filter != "All School type":
         filtered_data=filtered_data[filtered_data['School_type'] == School_type_filter]
    if Management_type_filter != "All Management type":
         filtered_data=filtered_data[filtered_data['Management_type'] == Management_type_filter]
    if Lga_filter:
        filtered_data=filtered_data[filtered_data['Unique_lga'].isin (Lga_filter)]

    st.title("🏫📚Educational Infrastructure and Access Dashboard")
    st.markdown("---")
    def format_number(num):
        if num >= 1_000_000_000:
            return f"{num/1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num/1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{round(num/1_000)}K"
        else:
            return str(num)
    
    col1, col2, col3 = st.columns(3)
    with col1:
         Total_schools = len(filtered_data)
         st.metric("🏫Total Schools", format_number(Total_schools))
    with col2:
         Total_students = filtered_data['Total_students'].sum()
         st.metric("👨‍🎓👩‍🎓Total Students", format_number(Total_students))
    with col3:
         Average_student=filtered_data['Total_students'].mean()
         st.metric("📊Average Student per Schoool", f"{Average_student:.2f}")
    col4, col5= st.columns(2)
    with col4:
         Electricity_access=filtered_data['Electricity_access'].mean()*100
         st.metric("⚡Percentage of Schools with Electricity Access", f"{Electricity_access:.2f}%")
    with col5:
         Improved_water_supply=filtered_data['Improved_water_supply'].mean()*100
         st.metric("🚰Percentage of schools with Improved Water Supply", f"{Improved_water_supply:.2f}%")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
         st.subheader("Distribution of School Types")
         school_type= filtered_data['School_type'].value_counts().reset_index()
         school_type.columns= ['School_type', 'counts']
         fig_school_type=px.bar(
              school_type,
              x='School_type',
              y='counts',
              color='School_type',
              color_continuous_scale=["#1f77b4"] 

         )
         fig_school_type.update_layout(width=1000, height=500)
         st.plotly_chart(fig_school_type, use_container_width=True)


if __name__ == "__main__":
        main()
