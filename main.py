import streamlit as st
import pandas as pd
import re
import os

def highlight_text(text, search_term):
    if pd.isna(text) or search_term == "":
        return text
    
    # Ensure text is a string
    text = str(text)
    search_term = str(search_term)
    
    # Case-insensitive search for whole word
    pattern = re.compile(f'\\b({re.escape(search_term)})\\b', re.IGNORECASE)
    highlighted = pattern.sub(r'<span style="background-color: green; font-weight: bold">\1</span>', text)
    return highlighted

def search_and_display(df, search_term):
    if search_term:
        # Filter dataframe for rows containing the exact search term in "English Word" column
        # Using word boundaries \b to match exact words
        pattern = f'\\b{re.escape(search_term)}\\b'
        
        # Make sure we're only applying regex filtering to string columns
        mask = df["English Word"].astype(str).str.contains(pattern, case=False, na=False, regex=True)
        filtered_df = df[mask]
        
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} results for '{search_term}'")
            
            # Create a copy of the filtered dataframe for display
            display_df = filtered_df.copy()
            
            # Display the results with highlighted text
            for _, row in display_df.iterrows():
                st.markdown("---")
                st.markdown(f"<span style='font-size:22px; color:white'><b>Source: {str(row['column_1'])} | **Author:** </b>{str(row['column_2'])}</span> | <span style='font-size:18px; color:violet'><b>Probability:</b> {str(row['Hypothetical Attention Score'])}</span>", unsafe_allow_html=True)
                
                # Highlight search term in column_4 if it exists
                highlighted_col4 = highlight_text(row['column_4'], search_term)
                st.markdown(f"**English Subtitle:** {highlighted_col4}", unsafe_allow_html=True)
                
                # Highlight search term in column_6 if it exists
                # Also highlight Malayalam Word in column_6 if it exists
                highlighted_col6 = str(row['column_6']) if not pd.isna(row['column_6']) else ""
                if highlighted_col6:
                    highlighted_col6 = highlight_text(highlighted_col6, search_term)
                    highlighted_col6 = highlight_text(highlighted_col6, str(row['Malayalam Word']))
                st.markdown(f"**Malayalm Subtitle:** {highlighted_col6}", unsafe_allow_html=True)
                
                # No highlighting for English Word column
                st.markdown(f"**Malayalam Word:** {str(row['Malayalam Word'])}")
                
                st.markdown(f"<span style='font-size:24px; color:orange'><b>Base Word:</b> {str(row['Base word'])}</span>", unsafe_allow_html=True)
            
            # Display tabular results
            st.subheader("Results in Tabular Format")
            
            # Select columns to display
            display_columns = ['column_1', 'column_2', 'column_3', 'column_4', 'column_5', 'column_6', 
                              'English Word', 'Malayalam Word', 'Base word', 'Hypothetical Attention Score']
            
            # Create a new dataframe for display
            table_df = filtered_df[display_columns].copy()
            
            # Apply highlighting only to specific keywords in column_4 and column_6
            # Convert to HTML for display
            def format_df_with_highlights():
                # Create a copy of the dataframe for HTML formatting
                html_df = table_df.copy()
                
                # Convert all columns to string to prevent type errors
                for col in html_df.columns:
                    html_df[col] = html_df[col].astype(str)
                
                # Apply highlighting to column_4
                html_df['column_4'] = html_df['column_4'].apply(
                    lambda x: highlight_text(x, search_term)
                )
                
                # Apply highlighting to column_6
                html_df['column_6'] = html_df.apply(
                    lambda row: highlight_text(row['column_6'], search_term), 
                    axis=1
                )
                html_df['column_6'] = html_df.apply(
                    lambda row: highlight_text(row['column_6'], row['Malayalam Word']), 
                    axis=1
                )
                
                # Convert to HTML
                html = html_df.to_html(escape=False)
                return html
            
            # Display the HTML table
            st.markdown(format_df_with_highlights(), unsafe_allow_html=True)
            
        else:
            st.warning(f"No results found for '{search_term}'")

def main():
    st.title("Msone Dictionary")
    
    # Load the data
    csv_path = os.path.join("/Users/raafid_mv/Downloads", "merged_data_inner_join.csv")
    
    try:
        df = pd.read_csv(csv_path)
        
        # Search interface
        search_term = st.text_input("Enter an English word to search:")
        
        # Display results when search term is provided
        if search_term:
            search_and_display(df, search_term)
        
    except FileNotFoundError:
        st.error(f"Error: Could not find the file at {csv_path}. Please make sure the file exists in the specified directory.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
