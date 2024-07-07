from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class OllamaConnector:
    def __init__(self, ollama_url):
        self.llm = Ollama(model="llama3", base_url=ollama_url)
        self.basePrompt = ChatPromptTemplate.from_messages([
            ("system","respond in 50 words or less. don't deviate from the subject"),
            ("human","{input}")
        ])
        self.chain = self.basePrompt > self.llm > StrOutputParser()

    def get_response(self, text):
        return self.chain.invoke(text)