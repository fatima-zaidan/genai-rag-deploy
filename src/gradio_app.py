# src/gradio_app.py
import gradio as gr
from src.pipeline.generate import build_qa_chain
from src.database.models_db import QueryRecord
from src.database.session import SessionLocal
from src.database.session import engine, Base
from src.utils.logger import get_logger

print("🔹 Initializing database...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables ready.")

logger = get_logger(__name__)

qa_chain = build_qa_chain()


def respond(user_message, chat_history):
    if not user_message.strip():
        return chat_history, ""
    
    db = SessionLocal()

    try:
        result = qa_chain.invoke({"query": user_message})
        answer = result.get("result", "No answer returned.")
        retrieved_docs = result.get("source_documents", [])

        # Format sources
        sources_text = "\n".join([doc.page_content[:150].replace("\n", " ") + "..." for doc in retrieved_docs]) \
            if retrieved_docs else "No sources available."

        # Update UI chat history
        chat_history.append((user_message, answer))

        # Save to DB
        query_record = QueryRecord(question=user_message, answer=answer)
        db.add(query_record)
        db.commit()

        logger.info(f"Saved query: {user_message}")
        logger.info(f"Saved answer: {answer}")

        return chat_history, sources_text

    except Exception as e:
        logger.error(f"Error during query: {e}")
        chat_history.append((user_message, "❌ Error generating answer. Check logs."))
        return chat_history, ""
    

    finally:
        db.close()

# Reset chat (UI only)
def reset_chat():
    return [], ""


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# RAG GenAI Assistant\nAsk anything about GenAI, MLOps, RAG, and fine-tuning.")
    chatbot = gr.Chatbot(label="Conversation", height=400)
    user_input = gr.Textbox(placeholder="Type your question here...", label="Your Question")
    sources_output = gr.Textbox(label="Sources")

    with gr.Row():
        submit_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear")

    submit_btn.click(respond, inputs=[user_input, chatbot], outputs=[chatbot, sources_output])
    clear_btn.click(reset_chat, inputs=[], outputs=[chatbot, sources_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)

