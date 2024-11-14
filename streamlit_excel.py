import streamlit as st
import pandas as pd
import google.generativeai as genai
import time

# Configure the Google Generative AI API key
genai.configure(api_key="AIzaSyDUKuFJ49VVqgPIfVJAzwcw2Q6NCKiDRtI")  # Replace with your actual API key

# Function to load and preview Excel data
def load_excel_data(file):
    # Load the Excel file into a DataFrame
    data = pd.read_excel(file)
    return data

# Function to interact with the model
def ask_model_with_excel(data_context, question):
    try:
        # Start a chat with the model
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        chat = model.start_chat()

        # Send the request with the data context and question
        prompt = f"Here is the data:\n\n{data_context}\n\nQuestion: {question}"
        response = chat.send_message(prompt)
        
        if response:
            # Extract the answer from the model's response
            answer = response.candidates[0].content.parts[0].text
            return answer
        else:
            return "No response received from the model."
    except Exception as e:
        return f"Error occurred: {e}"

# Streamlit App
st.title("Excel Data Analysis with Google Generative AI")
st.write("Upload an Excel file, preview the data, and ask questions about it.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Load and display Excel data
    data = load_excel_data(uploaded_file)
    st.write("### Preview of Excel Data")
    st.dataframe(data)  # Show the DataFrame in a scrollable table
    
    # Convert the entire DataFrame to a readable string format for the prompt
    data_context = data.to_string(index=False)
    
    # Input for user question
    question = st.text_input("Enter your question about the data")
    
    if question:
        # Send the request with the data context and question
        answer = ask_model_with_excel(data_context, question)
        
        # Display the answer
        st.write("### Answer")
        st.write(answer)
