from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import google.generativeai as genai
import json
import re

GEMINI_API_KEY="AIzaSyDfv9usD4XN39tIYsY6zBwLl0bGfASW6lg"

#  get relevance contents
def get_relevance_content(query) :
    context = ""
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'})
    
    vector_db = Chroma(persist_directory='./chroma_db_nccn', embedding_function= embedding_function)
    search_result = vector_db.similarity_search(query)

    for result in search_result:
        context += f"\n{result}"

    return context


# create propper prompt
def create_prompt(query,context):
    shaped_text = query.replace("'", "").replace('"',"").replace("\n"," ")
    prompt = ("""
                you need to act as cv auditor. You need to get data about applicant name, contact, mail, qualification, education and project details from the cv. In qualification, education and project need to include data in pargraph. You need to provide data in given json format. format is 
                {{
                    name ,
                    email,
                    contact,
                    education,
                    qualification,
                    project
                }}         
                
                Query : {query}
                Context : {context}

                Answer :      
            """).format(query = shaped_text, context = context)
    
    return prompt


# get response from the gemini
def get_gemini_response(prompt):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")
    gemini_response = model.generate_content(prompt)
    return gemini_response.text



def process_cv():
    query = "Give the applicant details about name, contact, email, education, qualification, projects"
    context = get_relevance_content(query)
    prompt = create_prompt(query, context)
    response = get_gemini_response(prompt)

    if response:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)

            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                return data
            else:
                raise ValueError("No JSON found in response.")

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Raw response:", response)
        except ValueError as e:
            print(f"Error: {e}")
