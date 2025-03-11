from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader

def load_extract_cv_data(cv):

    chroma_db_path = './chroma_db_nccn'
    print('Start processing')
    try:
        cv_data_loader = [PyPDFLoader(cv)]
        applicant_data_collection = []

        for applicant_data in cv_data_loader:
            applicant_data_collection.extend(applicant_data.load())

        embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )

        vectorstore = Chroma.from_documents(applicant_data_collection, embedding_function, persist_directory= chroma_db_path)
    except Exception as e:
        print(f"Something went wrong in data embedding processs... {e}")
