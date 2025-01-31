import os
from decouple import config

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = config("GROQ_API_KEY")

class AI_Bot:

    def __init__(self):
        self.__chat = ChatGroq(model="deepseek-r1-distill-llama-70b")

    # Template para a manipulação da IA
    def invoke(self, question):
        prompt = PromptTemplate.from_template(
            input_variables=["question"],
            template='''Você é um especialista em filmes, séries e livros, de diferentes gêneros. 
            Responda as questões do usuário fazendo diferentes recomendações, com base na exigência do usuário.
            Se o usuário não dizer os gêneros que ele gosta, pergunte sobre eles.
            Forneça a sinopse de cada filme, série ou livro recomendado, o titulo e o ano.
            Se o usuário for perguntar sobre um filme, série ou livro, responda com uma avaliação de 1 a 10, com base na sua experiência, e diga o motivo.
            Sempre responda de forma agradavel, com emojis e de forma que o usuário possa entender.
            <question>
            {question}
            <question>
            '''
        )

        # Cadeia de funções, Output de uma é o Input da outra, para que a resposta seja feita de forma correta
        chain = prompt | self.__chat | StrOutputParser()

        response = chain.invoke({
            "question": question,
        })

        return response
        