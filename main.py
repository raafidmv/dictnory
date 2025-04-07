import streamlit as st
import pandas as pd
import re
import os

def highlight_text(text, search_term):
    if pd.isna(text) or search_term == "":
        return text
    
    # Case-insensitive search
    pattern = re.compile(f'({re.escape(search_term)})', re.IGNORECASE)
    highlighted = pattern.sub(r'<span style="background-color: green; font-weight: bold">\1</span>', str(text))
    return highlighted

def search_and_display(df, search_term):
    if search_term:
        # Filter dataframe for rows containing the search term in "English Word" column
        filtered_df = df[df["English Word"].str.contains(search_term, case=False, na=False)]
        
        if not filtered_df.empty:
            st.write(f"Found {len(filtered_df)} results for '{search_term}'")
            
            # Create a copy of the filtered dataframe for display
            display_df = filtered_df.copy()
            
            # Display the results with highlighted text
            for _, row in display_df.iterrows():
                st.markdown("---")
                st.markdown(f"**Source:** {row['column_1']} | **Section:** {row['column_2']} | **Attention Score:** {row['Hypothetical Attention Score']}")
                # st.markdown(f"**Timestamp:** {row['column_3']}")
                
                # Highlight search term in column_4 if it exists
                highlighted_col4 = highlight_text(row['column_4'], search_term)
                st.markdown(f"**English Subtitle:** {highlighted_col4}", unsafe_allow_html=True)
                
                # st.markdown(f"**Timestamp:** {row['column_5']}")
                
                # Highlight search term in column_6 if it exists
                # Also highlight Malayalam Word in column_6 if it exists
                highlighted_col6 = row['column_6']
                if not pd.isna(highlighted_col6):
                    highlighted_col6 = highlight_text(highlighted_col6, search_term)
                    highlighted_col6 = highlight_text(highlighted_col6, row['Malayalam Word'])
                st.markdown(f"**Malayalm Subtitle:** {highlighted_col6}", unsafe_allow_html=True)
                
                # No highlighting for English Word column
                st.markdown(f"**English Word:** {row['English Word']} | **Malayalam Word:** {row['Malayalam Word']}")
                
                # st.markdown(f"**Malayalam Word:** {row['Malayalam Word']}")
                # st.markdown(f"**Base Word:** {row['Base word']}")
                st.markdown(f"<span style='font-size:24px; color:orange'><b>Base Word:</b> {row['Base word']}</span>", unsafe_allow_html=True)
                # st.markdown(f"**Attention Score:** {row['Hypothetical Attention Score']}")
            
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
                
                # Apply highlighting to column_4
                html_df['column_4'] = html_df['column_4'].apply(
                    lambda x: highlight_text(x, search_term) if not pd.isna(x) else x
                )
                
                # Apply highlighting to column_6
                html_df['column_6'] = html_df.apply(
                    lambda row: highlight_text(row['column_6'], search_term) if not pd.isna(row['column_6']) else row['column_6'], 
                    axis=1
                )
                html_df['column_6'] = html_df.apply(
                    lambda row: highlight_text(row['column_6'], row['Malayalam Word']) if not pd.isna(row['column_6']) else row['column_6'], 
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
    st.title("English-Malayalam Translation Search")
    
    # Load the data
    csv_path = os.path.join("", "merged_data_inner_join.csv")
    
    try:
        df = pd.read_csv(csv_path)
        
        # Search interface
        search_term = st.text_input("Enter an English word to search:")
        
        # Display results when search term is provided
        if search_term:
            search_and_display(df, search_term)
        else:
            st.info("Enter a word in the search box to find translations")
            
        # Option to display the full dataset
        if st.checkbox("Show full dataset"):
            st.dataframe(df)
            
    except FileNotFoundError:
        st.error(f"Error: Could not find the file at {csv_path}. Please make sure the file exists in the specified directory.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
