# Author: ludanchufang
# CreatTime: 2024/6/7
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain



def qa_agent(openai_api_key,memory,upload_file,question):
    model = ChatOpenAI(model="gpt-4o",openai_api_key=openai_api_key)
    file_content = upload_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=100,
        separators=["\n\n","\n","。","，",".",",",""]
    )
    texts = text_splitter.split_documents(docs)
    embeddings_model = OpenAIEmbeddings()
    db = FAISS.from_documents(texts,embeddings_model)
    retriever = db.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )
    response = qa.invoke({"chat_history":memory,"question":question})
    return response

