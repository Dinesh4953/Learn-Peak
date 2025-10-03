###################      AI     ######################
import google.generativeai as genai
import requests
from datetime import datetime
from openai import OpenAI

# api_key = "AIzaSyClUQqRF5WRGJM-rxjmL14AhPIw4OVr3l8"
# serp_api_key = "4a57f4d372db4b4b8bdb9987ac73e71760c27a8370726ff8b29838f423cb084e"

# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# def search_web(query):
#     params = {
#         "engine" : "google",
#         "q" : query,
#         "api_key" : serp_api_key
#     }
#     URL = "https://serpapi.com/search"
#     response = requests.get(url=URL, params=params)
    
#     if response.status_code == 200:
#         results = response.json()
#         snippets = []
#         for result in results.get("organic_results", [])[:3]:
#             title = result.get("title", "")
#             snippet = result.get("snippet", "")
#             link = result.get("link", "")
#             snippets.append(f"- {title}: {snippet} ({link})")
#         return "\n".join(snippets) if snippets else "No information is found"
#     else:
#         return  f"Failed to fetch results. Status code: {response.status_code}"


# def get_final_answer(question):
#     ini_res = model.generate_content(question).text
    
#     search_query = f"{question} as of {datetime.now().strftime('%B %Y')}"
#     real_ans= search_web(search_query)
    
#     final_prompt = f"""
#     Question : {question}
    
#     Gemini's initial answer:
#     {ini_res}
    
#     Web Search results : 
#     {real_ans}
    
#     Now combine both to produce a current, accurate, and well-strctured and answer.
#     """
#     final_response = model.generate_content(final_prompt).text
#     return final_response
    
    
api_key = "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"
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= api_key
)
def get_final_answer(question):
    messages = [
        {
            "role":"system",
            "content": "You are a helpful AI Assistant. When asked for code, always provide: \n"
                       "1️⃣ A code block (in proper language syntax) that can be copy-pasted.\n"
                       "2️⃣ A separate explanation of what the code does.\n"
                       "3️⃣ Use markdown formatting for code blocks.\n"
                       "Always return code in ```python ``` blocks and explanations outside.\n"
                       
        },
        {
            "role" : "user",
            "content" : question
        }
    ]
    completion = client.chat.completions.create(
        model = "nousresearch/deephermes-3-llama-3-8b-preview:free",
        messages=messages
    )
    answer = completion.choices[0].message.content
    return answer
