import streamlit as st
import google.generativeai as genai

# Configure page settings - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# **IMPORTANT: Configure the API key - DOUBLE CHECK THIS!**
API_KEY = "AIzaSyDlBv9Br45qcfbzGyr3AlcScyWQo3eSOPU"  # <--- REPLACE WITH YOUR ACTUAL API KEY HERE
if not API_KEY or API_KEY == "YOUR_API_KEY":
    st.error("API key is missing or not configured. Please set your API key in the code.")
    st.stop()
genai.configure(api_key=API_KEY)

# First, list available models for debugging and selection
st.subheader("Available Models")
try:
    available_models = genai.list_models()
    model_names = []
    
    if available_models:
        for model_info in available_models:
            st.write(f"- **{model_info.name}**: {model_info.description}")
            model_names.append(model_info.name)
        
        # Create a model selector if models are available
        if model_names:
            selected_model_name = st.selectbox("Select a model to use:", model_names)
        else:
            st.error("No models available with your API key/project.")
            st.stop()
    else:
        st.warning("No models listed. Check API key and project setup.")
        st.stop()
except Exception as e:
    st.error(f"Error listing models: {e}")
    st.error("Please check your API key and Google Cloud project configuration.")
    st.stop()

# Load the text generation model
@st.cache_resource
def load_text_model(model_name):
    try:
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"Error loading model '{model_name}': {e}")
        st.error("Please check:")
        st.error(f"- Is '{model_name}' model available in your region/project?")
        st.error("- Is the Generative AI API enabled in your Google Cloud Project?")
        st.error("- Is your API key correctly configured and valid?")
        return None

# Define input prompt
input_prompt = """
               As an expert pharmacist specializing in toxicological effects, side effects, and drug-drug interactions, your task involves analyzing input text describing various drugs. Provide information on the potential toxicological effects, side effects, and interactions between the mentioned drugs. Consider the context of individuals with specific health conditions. If there are notable interactions, specify the recommendations or precautions to be taken. Use Arabic languages for the response.
               """

def generate_gemini_text_response(text_model, user_input):
    if text_model is None:
        return None
    try:
        response = text_model.generate_content([input_prompt, user_input])
        return response.text
    except Exception as e:
        st.error(f"Error generating text response: {e}")
        st.error(f"Detailed Error: {e}")
        return None

# Display header and logos
st.markdown('''<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)
st.markdown('''Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Load the selected model
text_model = load_text_model(selected_model_name)

# User input
user_input = st.text_area("Enter text describing a drug:")

# Generate response button
if st.button("Generate Response"):
    if text_model is None:
        st.error("Model failed to load. Check the errors above.")
    else:
        with st.spinner("Generating response..."):
            response = generate_gemini_text_response(text_model, user_input)
            if response:
                st.subheader("Generated Response:")
                st.write(response)
            else:
                st.error("Failed to generate a response. Check the errors above.")
