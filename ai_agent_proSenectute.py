from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms.mlx_pipeline import MLXPipeline
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
import gradio as gr

document = PyPDFLoader("./documents/WegleitungRIF01012025.pdf").load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=100,
).split_documents(document)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={
        "normalize_embeddings": True,
    },
)

vectorstore = Chroma.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

llm = MLXPipeline.from_model_id(
    "mlx-community/QwQ-32B-4bit",
    #   "mlx-community/gemma-3-27b-it-4bit",
    pipeline_kwargs={"max_tokens": 1000, "temp": 0.1},
)

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three paragraphs maximum and keep the answer concise.
Question: {input} 
Context: {context} 
Answer:"""

prompt = ChatPromptTemplate.from_template(template)
doc_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, doc_chain)

# Function to handle user queries
def ask_question(query):
    response = chain.invoke({"input": query})
    return response["answer"]

# Gradio app
if __name__ == "__main__":
    with gr.Blocks() as app:
        gr.Markdown("# AI Assistant with RAG-based Document Search")
        query_input = gr.Textbox(label="Ask a question about the documents")
        response_output = gr.Textbox(label="Answer", interactive=False)
        ask_button = gr.Button("Ask")
        ask_button.click(ask_question, inputs=[query_input], outputs=[response_output])

    # Launch the app with explicit host and port
    app.launch(server_name="0.0.0.0", server_port=7860)
