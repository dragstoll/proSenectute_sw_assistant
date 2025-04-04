from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms.mlx_pipeline import MLXPipeline
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
import gradio as gr
from pathlib import Path

# Load and process all PDF documents from the subfolder
def load_all_documents(folder_path):
    documents = []
    for file in Path(folder_path).glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        loaded_docs = loader.load()
        for doc in loaded_docs:
            doc.metadata["source"] = file.name  # Add document name to metadata
        documents.extend(loaded_docs)
    return documents

# Function to handle user queries
def ask_question(query):
    response = chain.invoke({"input": query})
    return response["answer"]

# Function to handle user queries and return both the answer and the chunks used
def ask_question_with_chunks(query):
    response = chain.invoke({"input": query})
    chunks_used = response.get("context", "Keine verwendeten Textabschnitte gefunden.")
    return response["answer"], chunks_used

# Gradio app
if __name__ == "__main__":
    folder_path = "./documents"
    document = load_all_documents(folder_path)
    documents = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=100,
    ).split_documents(document)

    # Append document name and page number to each chunk
    for doc in documents:
        source = doc.metadata.get("source", "Unbekanntes Dokument")
        page = doc.metadata.get("page", "Unbekannte Seite")
        doc.page_content += f" ({source}, Seite {page})"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )

    vectorstore = Chroma.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

    llm = MLXPipeline.from_model_id(
        # "mlx-community/QwQ-32B-4bit",
        #   "mlx-community/gemma-3-27b-it-4bit",
    #    "mlx-community/Qwen2.5-32B-Instruct-4bit",
    # "mlx-community/Mistral-Large-Instruct-2407-4bit",
    "mlx-community/Mistral-Small-24B-Instruct-2501-4bit",
        pipeline_kwargs={"max_tokens": 512, "temp": 0.1},
    )

    template = """INSTRUKTIONEN: Du musst nur auf Deutsch antworten.
    Du bist ein hilfreicher KI-Agent und hilfst mir. Ich bin ein Sozialarbeiter im Einarbeitungsprozess und arbeite bei der Pro Senectute Aargau. 
    Bei der Pro Senectute haben wir das Angebot der Individuellen Finanzhilfe. 
    Bitte Suche in den dir zu zurverfügunggestellen Dokumenten und gibt mir möglichst genaue und hilfreiche Antworten auf meine Fragen. 
    Beachte folgende Wichtige Punkte:
    - Gib mir immer Antwort auf Deutsch
    - Gib mir immer eine Quellenangabe deiner Antwort (z.B. "Dokument 1, Abschnitt 1, Seite 3")
    FRAGE: {input} 
    KONTEXT: {context} 
    ANTWORT:"""

    prompt = ChatPromptTemplate.from_template(template)
    doc_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, doc_chain)

    with gr.Blocks(css=".gradio-container { font-size: 10px; }") as app:
        gr.Markdown("# Pro Senectute Suchassistent zur individuelle Finanzhilfe für Sozialarbeitende")
        query_input = gr.Textbox(label="Formuliere deine Frage", placeholder="Was möchtest du wissen?", lines=2)
        gr.Markdown("## Beispiel: \"Welche Unterlagen benötige ich für ein Gesuch, wenn ich Nebenkosten beantrage?\"", elem_id="example1")
        gr.Markdown("## Beispiel: \"Was muss ich beachten, wenn ich ein Hörgerät beantrage?\"", elem_id="example2")
        gr.Markdown("## Beispiel: \"Ist ein Ehepaar mit einer AHV Rente von 4000.- plus Pensionskasse Rente von 2000.- berechtigt individuelle Finanzhilfe zu beantragen, grundsätzlich?\"", elem_id="example3")

        # Add custom CSS to change font size to 12px
        app.css += """
        #example1, #example2, #example3 {
            font-size: 12px;
        }
        """
        response_output = gr.Textbox(label="Antwort", interactive=False)
        chunks_output = gr.Textbox(label="Verwendete Textabschnitte", interactive=False, lines=10, visible=False)
        ask_button = gr.Button("Ausführen")  # Changed to "Ausführen"
        clear_button = gr.Button("Lösche die Antwort")  # Changed to clear the answer field

        ask_button.click(
            ask_question_with_chunks, 
            inputs=[query_input], 
            outputs=[response_output, chunks_output]
        )
        clear_button.click(lambda: ("", ""), inputs=[], outputs=[response_output, chunks_output])

    # Launch the app with explicit host, port, and public sharing enabled
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
