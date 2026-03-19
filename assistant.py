from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from config import GOOGLE_API_KEY
#from config import OPENAI_API_KEY
from load_prompt import load_system_prompt
from utils import load_us_to_uk, convert_to_uk_english, is_sentence_correct

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]
 
def create_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=GOOGLE_API_KEY
    )
 
# def create_chain():
#     llm = ChatOpenAI(
#         model="gpt-4o-mini",
#         temperature=0,
#         openai_api_key=OPENAI_API_KEY
#      )
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", load_system_prompt()),
        ("user", "Mode:{mode}\n\nText:{input}")
    ])
 
    chain = prompt_template | llm
 
    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )

def process_input(user_input, mode="grammar and spelling correction"):
    us_to_uk = load_us_to_uk()
 
    converted_text = convert_to_uk_english(user_input, us_to_uk)
    chain = create_chain()
    response = chain.invoke(
        {"input": converted_text, "mode": mode},
        config={"configurable": {"session_id": "session_1"}}
    )
 
    if is_sentence_correct(user_input, response.content):
        return user_input
    return response.content.strip()