import PyPDF2

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from IPython.display import display, Markdown, clear_output
import time

#initialize the llama model via ollama
model_id = "llama3.1"
model = Ollama(model=model_id)

# function to extract text from PDF
def extract_textPfrom_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
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
    initial_prompt = ChatPromptTemplate.from_template(initial_prompt_text)
    current_summary = model.invoke(initial_prompt.format(text=text))
    
    display(Markdown(f"### Initial Summary (Iteration {iteration})"))
    display(Markdown(current_summary))
    
    #iterative refinment process
    while iteration < max_iterations and questions_generated:
        print("=======================Next iteration=======================")
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
        refinement_prompt = ChatPromptTemplate.from_template(refinement_prompt_text)
        current_summary = model.invoke(refinement_prompt.format(text=text, summary = current_summary))
    
    return current_summary        
    
document_text = extract_textPfrom_pdf("C:/Users/USER/Downloads/Tution clz work/AL/9. Programming/Programming - Python.pdf")
    
final_summary = generate_refined_summary(model, document_text, max_iterations=3)
print("\n\n\n\nFinal Summary:")
display(Markdown(final_summary))