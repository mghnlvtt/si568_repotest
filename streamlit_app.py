import json
import importlib.util
import streamlit as st

from langchain_pipeline import analyze_tos

spec = importlib.util.spec_from_file_location("pdf_processing_edited", "pdf-processing-edited.py")
pdf_processing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pdf_processing)

extract_chunks = pdf_processing.extract_chunks

def main():
    pdf_path = "sample-tos/google_tos_example.pdf"
    st.title(
            "What are you agreeing to?",
            anchor=False)


    st.subheader(
        "Understanding Terms of Service (ToS)",
        anchor=False,
        divider="blue"
    )
    multi = '''Every day, we're presented with ToS documents that we have to agree to in order to use a service. \
    \nThe language in these documents are confusing and difficult to understand. \
    \nInstead of blindly hitting 'accept', use this tool to understand what exactly you're agreeing to.
    '''
    st.subheader(multi)
    file_upload = st.file_uploader("Upload your file here: ", type="pdf")
    url_variable = st.query_params.get("url", "")
    pasted_url = st.text_input("Or, paste the URL: ", value=url_variable)
    st.query_params["url"] = pasted_url
    print(f"1. Reading PDF ({file_upload}) and extracting chunks...")
    chunks = extract_chunks(input_url=st.query_params["url"], pdf=file_upload)
    
    if not chunks:
        print("Error: Could not extract chunks. Make sure the site allows scraping.")
        return
        
    print(f"Successfully extracted {len(chunks)} chunks!")
    
    print("\n2. Processing chunks through the LangChain pipeline (gpt-4o-mini)...")
    with st.spinner("Wait for it...", show_time=True):
        result = analyze_tos(chunks)
        
        print("\n" + "="*50)
        print("FINISHED ANALYSIS:")
        print("="*50)
        
        # Pretty print the json output
        print(json.dumps(result, indent=2))
    st.success("Done!")
    st.subheader(json.dumps(result, indent=2))
    st.button("Rerun")
    
if __name__ == "__main__":
    main()
