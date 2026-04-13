import streamlit as st
import PyPDF2

from langchain_core.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama

from IPython.display import display, Markdown, clear_output
import time

st.set_page_config(page_title="Document Summarization Refinement", layout="wide")

#initialize the llama model via ollama, let user select model
with st.sidebar:
    st.header("⚙️ Settings")
    model_id = st.selectbox("Choose Model", ["deepseek-r1:1.5b", "phi3:mini", "llama3.2:1b", "llama3.1"])
    model = Ollama(model=model_id)


# function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()
    return text

def generate_refined_summary(model, text, max_iterations=5):
    iteration =0
    current_summary = None
    questions_generated = True
    
    # generate an initial summary
    initial_prompt_text = """
    You are a summarization expert. Your task is to write summaries.
    Here is the original document text:
    
    {text}
    
    Start by creating a summary in your first pass.
    
    Create an initial summary.
    """
    initial_prompt = PromptTemplate.from_template(initial_prompt_text)
    current_summary = model.invoke(initial_prompt.format(text=text))
    
    initial_summary = current_summary
    
    #iterative refinment process
    while iteration < max_iterations and questions_generated:
        iteration += 1
        # ask the LLM to compare the original text and summary and refine it
        refinement_prompt_text = """
        You are a summarizationn expert. Your task is to refine summaries.
        Here is the original document text:
        
        {text}
        
        Refine the below current summary, keep it as it is but ensure it becomes more complete, coherent, clear and accurate.
        Aim to capture the essence of the text with each refinement,
        
        Current summary:
        
        {summary}
        
        Please provide a refined summary below:
        """
        refinement_prompt = PromptTemplate.from_template(refinement_prompt_text)
        current_summary = model.invoke(refinement_prompt.format(text=text, summary = current_summary))
    
    return initial_summary,current_summary        
    
def extract_key_points(model, text):
    prompt = f"""Extract exactly 5 key points as a numbered list from the following document. 
    Be concise. One sentence per point.

    Document:
    {text[:4000]}

    Key Points:"""
    return model.invoke(prompt)


# streamlit UI
st.title('Document Summarization Refinement')

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    document_text = extract_text_from_pdf(uploaded_file)
    st.session_state.doc_name = uploaded_file.name.replace(".pdf", "")
    st.write("Document loaded successfully!")
    
    iterations = st.slider("Select the number of iterations for refinement", min_value=1, max_value=10, value=5)
    
    if st.button("Generate Summary"):
        with st.spinner("Generating summaries..."):
            initial_summary, final_summary = generate_refined_summary(model, document_text, max_iterations=iterations)
            key_points = extract_key_points(model, document_text)
            
            # Save to session state so downloads don't wipe the page
            st.session_state.initial_summary = initial_summary
            st.session_state.final_summary = final_summary
            st.session_state.key_points = key_points
            st.session_state.iterations = iterations
            
    #displaying intial and final summary side by side
    if "initial_summary" in st.session_state:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 Initial Summary")
            st.container(width=500).markdown(st.session_state.initial_summary)

        with col2:
            st.subheader(f"✅ Final Summary after {iterations} iterations")
            st.container(width=500).markdown(st.session_state.final_summary)
            
        st.divider()
        with st.expander("🔑 Key Points", expanded=True):
            st.markdown(st.session_state.key_points)
                    
        st.divider()
        col_d1, col_d2, col_d3 = st.columns(3)
            
        with col_d1:
            st.download_button(
                "⬇️ Download Initial Summary",
                st.session_state.initial_summary,
                file_name=f"{st.session_state.doc_name}_initial_summary.txt",
                mime="text/plain"
            )
        with col_d2:
            st.download_button(
                "⬇️ Download Final Summary",
                st.session_state.final_summary,
                file_name=f"{st.session_state.doc_name}_final_summary.txt",
                mime="text/plain"
            )
        with col_d3:
            st.download_button(
                "⬇️ Download Key Points",
                st.session_state.key_points,
                file_name=f"{st.session_state.doc_name}_key_points.txt",
                mime="text/plain"
            )