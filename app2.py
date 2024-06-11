from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
# from IPython.display import display, Markdown
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.indexes import VectorstoreIndexCreator
# from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
import tiktoken

import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

query = None
llm_model = "gpt-3.5-turbo"
txt_file_path = 'MYEG_data.txt'
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")
data = loader.load()

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(data, embedding=embeddings)

# Create conversation chain
llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
memory = ConversationBufferMemory(
memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
        )

chat_history = []

while True:
    if not query:
        query = input("Prompt: ")
    result = conversation_chain({"question": query, "chat_history": chat_history})
            
    response = result['answer']
    if response:
        print(f"Bot: {response}")
        chat_history.append((query, response))
    else:
        print("Sorry, I couldn't find an answer in your dataset.")
    
    query = None

