import openai
from flask import Flask, request, jsonify, render_template
import langchain.chains as lc
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate



app = Flask(__name__)
app.debug = True
ALLOWED_HOSTS = ['*']

# Initialize the OpenAI API client
openai.api_key = '****'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        query = request.json.get('query')
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        # Initialize components from the new code
        loader = PyPDFLoader("dummy_data.pdf")
        docs = loader.load_and_split()

        llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        embeddings = OpenAIEmbeddings()

        chroma_db = Chroma(persist_directory="data",
                           embedding_function=embeddings,
                           collection_name="lc_chroma_demo")

        # Check if there are existing documents before accessing their IDs
        collection = chroma_db.get()
        if len(collection['ids']) == 0:
            chroma_db = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory="data",
                collection_name="lc_chroma_demo"
            )
            chroma_db.persist()  # Persist the database after adding documents

        # Prepare query
        print('Similarity search:')
        print(chroma_db.similarity_search(query))
        print('Similarity search with score:')
        print(chroma_db.similarity_search_with_score(query))

        # Add a custom metadata tag to the first document (if it exists)
        if len(collection['ids']) > 0:  # Check if there's a document before adding metadata
            docs[0].metadata = {"tag": "source"}

            # Update the document in the collection (if it exists)
            chroma_db.update_document(
                document=docs[0],
                document_id=collection['ids'][0]
            )

        # Find the document with the custom metadata tag (if it exists)
        collection = chroma_db.get(where={"tag": "demo"})
        
        prompt_template = """
        
        If the context is not relevant, 
        
        please answer the question by using your own knowledge about the topic {context}
        
        Question: {question}
        """

        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        chain_type_kwargs = {"prompt": PROMPT}
        # Prompt the model
        chain = lc.RetrievalQA.from_chain_type(llm=llm,
                                               chain_type="stuff",
                                               retriever=chroma_db.as_retriever(),
                                               chain_type_kwargs=chain_type_kwargs
                                               )

        # Execute the chain
        response = chain.invoke(query)

        # If no matching documents found, provide a custom fallback response
        if not response['result']:
            fallback_response = "I'm sorry, I couldn't find relevant information for your query."
            # Log the query for further analysis
            print(f"Query '{query}' did not match any documents.")
            return jsonify({'response': fallback_response}), 200

        chroma_db.delete_collection()

        # Return the generated response
        return jsonify({'response': response['result']}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
