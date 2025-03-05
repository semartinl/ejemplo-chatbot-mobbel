import requests
# def extract_questions_and_answers(pdf_path):
#     questions_answers = []
    
#     with open(f"./{pdf_path}", "rb") as file:
#         reader = PyPDF2.PdfReader(file)
#         text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
#     # Expresión regular para capturar preguntas numeradas y sus respuestas
#     pattern = re.compile(r"(\d+)\.\s?(.*?)\?\s*(.*?)(?=\n\d+\.| \Z)", re.S)

    
#     matches = pattern.findall(text)

#     for match in matches:
#         question_number, question_text, answer_text = match
#         question_text = question_text.strip()
#         question_text = question_text.replace("\n", "")

#         answer_text = answer_text.strip()
#         answer_text = answer_text.replace("\n", "")
        
#         questions_answers.append({"question": question_text.strip(), "answer": answer_text})
    
#     document_pattern = pd.DataFrame(questions_answers)
#     document_pattern.to_csv("document_pattern.csv", index=False)
    
#     return questions_answers


# extract_questions_and_answers("Preguntas_cuestionario_resumidas.pdf")

response = requests.post("http://localhost:5000/answers", json={"question": "¿Qué es un modelo de lenguaje?", "answer": "Un modelo de lenguaje es una herramienta que permite a las máquinas entender y generar lenguaje humano."})

print(response.json())