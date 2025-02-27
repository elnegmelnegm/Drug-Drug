import streamlit as st
import google.generativeai as genai

# Configure page settings - MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="ُEDA AI Chat",
    page_icon="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png",
    layout="wide",
)

# **IMPORTANT: Configure the API key - DOUBLE CHECK THIS!**
API_KEY = "AIzaSyDlBv9Br45qcfbzGyr3AlcScyWQo3eSOPU"  # <--- REPLACE WITH YOUR ACTUAL API KEY
if not API_KEY or API_KEY == "AIzaSyDlBv9Br45qcfbzGyr3AlcScyWQo3eSOPU":
    st.error("API key is missing or not configured. Please set your API key in the code.")
    st.stop()
genai.configure(api_key=API_KEY)

# Load the text generation model
@st.cache_resource
def load_text_model() -> genai.GenerativeModel:
    try:
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"Error loading model 'gemini-pro': {e}") # More specific error message
        st.error("Please check:")
        st.error("- Is 'gemini-pro' model available in your region/project?")
        st.error("- Is the Generative AI API enabled in your Google Cloud Project?")
        st.error("- Is your API key correctly configured and valid?")
        st.stop()
        return None

# Define input prompt
input_prompt = """
               As an expert pharmacist specializing in toxicological effects, side effects, and drug-drug interactions... (rest of your prompt)
               """

def generate_gemini_text_response(text_model, user_input):
    if text_model is None:
        return None
    try:
        response = text_model.generate_content([input_prompt, user_input])
        return response.text
    except Exception as e:
        st.error(f"Error generating text response: {e}")
        st.error(f"Detailed Error: {e}") # Show the full error for debugging
        return None

# Display header and logos
st.markdown('''<img src="https://www.edaegypt.gov.eg/media/wc3lsydo/group-287.png" width="250" height="100">''', unsafe_allow_html=True)
st.markdown('''Powered by Google AI <img src="https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png" width="20" height="20"> Streamlit <img src="https://global.discourse-cdn.com/business7/uploads/streamlit/original/2X/f/f0d0d26db1f2d99da8472951c60e5a1b782eb6fe.png" width="22" height="22"> Python <img src="https://i.ibb.co/wwCs096/nn-1-removebg-preview-removebg-preview.png" width="22" height="22">''', unsafe_allow_html=True)

# Load the text model
text_model = load_text_model()

# List available models for debugging
st.subheader("Available Models:")
if text_model: # Only list if model loading was at least attempted (not None initially)
    try:
        available_models = genai.GenerativeModel.list_models()
        if available_models:
            for model_info in available_models:
                st.write(f"- **{model_info.name}**: {model_info.description}")
        else:
            st.warning("No models listed. This is unusual. Check API key and project setup.")
    except Exception as e:
        st.error(f"Error listing models: {e}")
        st.error(f"Detailed Model Listing Error: {e}") # Show error listing models
else:
    st.warning("Model loading failed earlier, cannot list available models.")


# User input
user_input = st.text_area("Enter text describing a drug:")

# Generate response button
if st.button("Generate Response"):
    response = generate_gemini_text_response(text_model, user_input)
    st.text("Generated Response:")
    st.write(response)
