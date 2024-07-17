import requests
from tqdm import tqdm
from elasticsearch import Elasticsearch

# Configure Elasticsearch client
es_client = Elasticsearch("http://localhost:9200")  # Update with your ES URL
index_name = "course-questions"

index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}


if not es_client.indices.exists(index=index_name):
    es_client.indices.create(index=index_name, body=index_settings)
else:
    print(f"Index '{index_name}' already exists.")

# Fetch documents
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

# Process documents
for course in documents_raw:
    course_name = course['course']
    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

# Index documents
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)

print("Documents indexed successfully!")
