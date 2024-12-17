import pandas as pd
import openai
import ast
import fitz  # PyMuPDF
import os
from docx import Document
from openai import OpenAI

key = "" ## Your key here
openai.api_key = key
openai.models.list()
client = OpenAI(api_key = key)

tools = [
        {
            "type": "function",
            "function": {
                "name": "get_resume_info",
                "description": "Extract Name, Email, Company name, Role, and Skills from a resume",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the candidate"
                        },
                        "email": {
                            "type": "string",
                            "description": "Email address of the candidate"
                        },
                        "company": {
                            "type": "string",
                            "description": "Current company of the candidate"
                        },
                        "role": {
                            "type": "string",
                            "description": "Role or position of the candidate"
                        },
                        "skills": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Skills of the candidate"
                        }
                    }
                }
            }
        }
        ]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


# Define the folder path where your resumes are stored
folder_path = 'C:/Users/shiva/Desktop/IITJ/For Darshan/downloaded_pdfs'

# List to store literals for each extracted text
literals = []

# Iterate over each file in the folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    
    # Check if the file is a PDF or DOCX
    if file_name.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_name.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    else:
        continue  # Skip files that are neither PDF nor DOCX

dfs = []

for s in literals:
    response = client.chat.completions.create(
        model="gpt-4.o",
        messages=[{"role": "user", "content": s}],
        tools=tools
    )

    res = response.choices[0].message.tool_calls[0].function.arguments
    my_dict = ast.literal_eval(str(res))
    dfs.append(my_dict)

final_df = pd.DataFrame(dfs)
csv_file_path = 'final_extract_v1.csv'

if not os.path.exists(csv_file_path):
    # Create the CSV file if it doesn't exist
    final_df.to_csv(csv_file_path, index=False)

print("Data Print Successful")