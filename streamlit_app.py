import streamlit as st
from assistant import process_input
 
st.title("UK English Grammar & Spelling Corrector")
 
text = st.text_area("Enter your text:")
mode_choice = st.radio("Mode:", ["grammar and spelling correction", "rephrase"])
 
if st.button("Correct"):
    mode = "grammar and spelling correction" if mode_choice == "grammar and spelling correction" else "rephrase"
    output = process_input(text, mode=mode)
    st.subheader("Corrected Output:")
    st.write(output)