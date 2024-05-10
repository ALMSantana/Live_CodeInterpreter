from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file = cliente.files.create(
    file=open("ex3/customer_data.csv", "rb"),
    purpose="assistants"
)

assistente = cliente.beta.assistants.create(
    name="Assistente de Dados",
    instructions="""
    Você é um assistente, de análise de dados, capaz de gerar descobertas e percepções acerca de 
    dados relacionados a vendas em um e-commerce. Você faz análises minuciosas e garante que 
    todas as suas ações sejam descritas e explicadas. Você priorizar demonstrar dados com 
    gráficos que sejam simples, mas em situações mais complexas, desenha uma tabela.

 
    """,
    model="gpt-4-turbo",
    tools=[
        {
            "type":"code_interpreter"
        }
    ],
    tool_resources={
        "code_interpreter":{
            "file_ids": [file.id]
        }
    }
)

thread = cliente.beta.threads.create()

message = cliente.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=""""
    Liste os cinco clientes que mais gastaram na plataforma e gere um gráfico de barras.
    """
)

run = cliente.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistente.id
)

if run.status == "completed":
    mensagens_resposta = cliente.beta.threads.messages.list(
        thread_id=thread.id
    )
    
    for uma_mensagem in mensagens_resposta.data[0].content:
        if hasattr(uma_mensagem, "text") and uma_mensagem.text is not None:
            print("\n")
            print(uma_mensagem.text.value)
        elif hasattr(uma_mensagem, "image_file") and uma_mensagem.image_file is not None:
            resposta_da_openai = cliente.files.retrieve(uma_mensagem.image_file.file_id)
            image_data = cliente.files.content(resposta_da_openai.id)
            image_data_bytes = image_data.read()

            with open("grafico.png", "wb") as file:
                file.write(image_data_bytes)
else:
    print(run.status)