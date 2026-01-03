# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI

from src.agent.state import AgentState
from src.config import Config

# llm = ChatGoogleGenerativeAI(model=Config.LLM_MODEL, google_api_key=Config.GOOGLE_API_KEY)
# embeddings = GoogleGenerativeAIEmbeddings(model=Config.EMBEDDING_MODEL, google_api_key=Config.GOOGLE_API_KEY)

llm = ChatOpenAI(
    model=Config.LLM_MODEL, 
    api_key=Config.OPENAI_API_KEY,  
)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
def classify_intent_node(state: AgentState):
    question = state["question"]
    
    prompt = f"""
    Classify the user query into one of these three categories:
    1. 'disease': Question is about citrus pests, symptoms, or plant health.
    2. 'scheme': Question is about govt subsidies, insurance, or financial aid.
    3. 'hybrid': Question mentions both a disease/pest and a financial scheme.
    
    Query: {question}
    Return only the category name.
    """
    
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    # intent = response.strip().lower()
    return {**state, "intent": intent}



def retrieve_node(state: AgentState):
    intent = state["intent"]
    question = state["question"]
    
    collections = []
    if intent == "disease":
        collections = [Config.DISEASE_COLLECTION]
    elif intent == "scheme":
        collections = [Config.SCHEME_COLLECTION]
    elif intent == "hybrid":
        collections = [Config.DISEASE_COLLECTION, Config.SCHEME_COLLECTION]
    
    context_list = []
    for col in collections:
        vector_db = Chroma(
            persist_directory=Config.CHROMA_PATH,
            collection_name=col,
            embedding_function=embeddings
        )
        # We retrieve with scores/metadata
        docs = vector_db.similarity_search(question, k=3)
        for d in docs:
            source = d.metadata.get("source", "Unknown")
            page = d.metadata.get("page", "Unknown")
            context_list.append(f"[Source: {source}, Page: {page}]\nContent: {d.page_content}")
        
    return {**state, "context": "\n\n---\n\n".join(context_list)}


def generate_answer_node(state: AgentState):
    context = state["context"]
    question = state["question"]
    intent = state["intent"]


    if not context.strip():
        return {**state, "answer": "I'm sorry, I don't have information on that topic in my database. I can only help with Citrus diseases and Govt schemes.", "success": False}
    
    
    prompt = f"""
    You are an expert Agriculture Assistant. 
    Using ONLY the context provided below, answer the farmer's question.
    
    RULES:
    1. Be helpful, professional, and use simple language.
    2. You MUST cite the Source and Page number at the end of relevant paragraphs.
    3. If the answer is not in the context, say you don't know.
    
    Context:
    {context}
    
    Question: {question}
    """
    
    response = llm.invoke(prompt)
    return {**state, "answer": response.content, "success": True}
