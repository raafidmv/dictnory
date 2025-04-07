import streamlit as st
import pandas as pd
import numpy as np

# Set page title and configuration
st.set_page_config(
    page_title="Msone Dictionary",
    # layout="wide"
)

# App title
st.markdown("<h1 class='main-header'>English-Malayalam Dictionary</h1>", unsafe_allow_html=True)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/raafid_mv/Downloads/merged_data_inner_join.csv')
    
    # Convert Hypothetical Attention Score to numeric
    df['Hypothetical Attention Score'] = pd.to_numeric(df['Hypothetical Attention Score'], errors='coerce')
    
    # Fill NaN values with 0
    df['Hypothetical Attention Score'] = df['Hypothetical Attention Score'].fillna(0)
    
    return df

try:
    df = load_data()
    
    # Search functionality
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    search_term = st.text_input("Enter an English word:", "")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if search_term:
        # Filter dataframe for matching English words
        filtered_df = df[df['English Word'].str.lower() == search_term.lower()]
        
        if not filtered_df.empty:
            # Further filter to only include rows with attention score >= 0.5
            high_attention_df = filtered_df[filtered_df['Hypothetical Attention Score'] >= 0.5]
            
            if not high_attention_df.empty:
                # Get unique translations (to avoid duplicates)
                unique_translations = high_attention_df['Base word'].drop_duplicates().tolist()
                
                st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                # st.markdown(f"<h2><div class='word-header'>{search_term}</div></h2>", unsafe_allow_html=True)
                
                # Display each translation
                for translation in unique_translations:
                    st.markdown(f"<span style='font-size:22px; color:white'><b>{translation}<b></span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning(f"No translations with sufficient attention score found for '{search_term}'")
        else:
            st.warning(f"No translation found for '{search_term}'")
    
except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.info("Please make sure 'merged_data_inner_join.csv' exists and contains the required columns")
