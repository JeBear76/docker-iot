from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

class ollamaConnector:
    def __init__(self, ollama_url):
        self.llm = Ollama(model="llama3", base_url=ollama_url)
        self.basePrompt = ChatPromptTemplate.from_messages([
            ("system","respond in 50 words or less. don't deviate from the subject"),
            ("human","{input}")
        ])
        self.chain = self.basePrompt | self.llm | StrOutputParser()

    def getResponse(self, text):
        try:
            return self.chain.invoke(text)
        except Exception as e:
            print(e)
            return "I'm sorry, Ollama is broken right now."