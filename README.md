# FAQ Wizzard

Instead of searching through a long word file for your answer, ask the FAQ wizzard, which will find relevant questions within the document and, using RAG, will send your question to an LLM to summarize the answers into one response. 

![alt text](image.png)


## Usage

1. Clone the repository:

   ```
   git clone https://github.com/zstankow/local_llm_without_gpu.git
   ```

2. Install the requirements:
    ```
    pip install -r requirements.txt
    ```

3. Start the docker container:

    ```
    cd local_llm_without_gpu
    docker-compose up
    ```

4. Open a separate terminal and access the Docker container:

    ```
    cd local_llm_without_gpu
    docker exec -it ollama bash
    ```
    Then pull the required model:

    ```
    ollama pull phi3
    ```

5. Index the documents:
    ```
    python index_documents.py
    ```

6. Run the streamlit app:
    ```
    streamlit run qa_faq.py
    ```

