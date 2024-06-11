import os
from dotenv import load_dotenv

from openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import TextLoader
# from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from flask import Flask
from flask_cors import CORS


# app = Flask(__name__)
# CORS(app) 


# Load environment variables
load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

query = None

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# Load the documents
txt_file_path = 'MYEG_data.txt'
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")
data = loader.load()

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(data, embedding=embeddings)

# Customize the retriever to only search within your dataset
# custom_retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})

llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

chain = ConversationalRetrievalChain.from_llm(
    
    retriever=vectorstore.as_retriever(search_kwargs={"k": 1}),
    llm=llm
)



chat_history = []

while True:
    if not query:
        query = input("Prompt: ")
    result = chain.invoke({"question": query, "chat_history": chat_history})
            
    response = result['answer']
    print(f"Bot: {response}")
    chat_history.append((query, response))
    query = None


# if __name__ == '__main__':
#     load_dotenv()
#     envport = (os.getenv('PORT'))
#     app.run(host = '0.0.0.0',port=envport,debug=True)