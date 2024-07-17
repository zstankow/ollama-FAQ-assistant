import streamlit as st
import time

from elasticsearch import Elasticsearch
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',
)

es_client = Elasticsearch('http://localhost:9200') 


def elastic_search(query, course, index_name="course-questions"):
    # Base search query
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }

    # Add filter only if course is not None
    if course:
        search_query["query"]["bool"]["filter"] = {
            "term": {
                "course": course
            }
        }

    response = es_client.search(index=index_name, body=search_query)
    
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_source'])
    
    return result_docs


def build_prompt(query, search_results):
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def llm(prompt):
    response = client.chat.completions.create(
        model='phi3',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


def rag(course, query):
    search_results = elastic_search(query, course)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt)
    return answer


def main():
    st.title("FAQ Wizard")

    choices = ["General question", "Data Engineering", "MLOPS", "Machine Learning"]
    values = [None, "data-engineering-zoomcamp", "mlops-zoomcamp", "machine-learning-zoomcamp"]
    choice_to_value = dict(zip(choices, values))

    option = st.selectbox(
        "Choose a category:", choices
    )

    user_input = st.text_input("Enter your question:")
    if st.button("Ask"):
        course = choice_to_value[option]
        with st.spinner('Processing...'):
            output = rag(course, user_input)
            st.success("Completed!")
            st.write(output)

if __name__ == "__main__":
    main()