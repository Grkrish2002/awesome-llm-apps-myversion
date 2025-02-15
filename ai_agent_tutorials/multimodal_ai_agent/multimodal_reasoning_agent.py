import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.model.together import Together
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import upload_file, get_file
import time
import os
from pathlib import Path
import tempfile

load_dotenv()
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def main():
    # Set up the reasoning agent
    agent = Agent(
        # model=Gemini(id="gemini-2.0-flash-thinking-exp-1219"), 
        # model=Gemini(id="gemini-2.0-flash-thinking-exp"),
        # model=Gemini(id="gemini-2.0-flash"),
        model=Gemini(id="gemini-2.0-flash-001"),
        # model=Gemini(id="gemini-2.0-pro-exp-02-05"),
        markdown=True
    )

    # Streamlit app title
    st.title("Multimodal Reasoning AI Agent 🧠")

    # Instruction
    st.write(
        "Upload an image and provide a reasoning-based task for the AI Agent. "
        "The AI Agent will analyze the image and respond based on your input."
    )

    # File uploader for image
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Save uploaded file to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_path = tmp_file.name

            # Display the uploaded image
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

            # Input for dynamic task
            task_input = st.text_area(
                "Enter your task/question for the AI Agent:"
            )

            # Button to process the image and task
            if st.button("Analyze Image") and task_input:
                with st.spinner("AI is thinking... 🤖"):
                    try:
                        # Call the agent with the dynamic task and image path
                        response = agent.run(task_input, images=[temp_path])
                        
                        # Display the response from the model
                        st.markdown("### AI Response:")
                        st.markdown(response.content)
                    except Exception as e:
                        st.error(f"An error occurred during analysis: {str(e)}")
                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)

        except Exception as e:
            st.error(f"An error occurred while processing the image: {str(e)}")

if __name__ == "__main__":
    main()