from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file = cliente.files.create(
    file=open("ex2/analyze_data.py", "rb"),
    purpose="assistants"
)

assistente = cliente.beta.assistants.create(
    name="Assistente de Qualidade de Código",
    instructions="""
    Você é um assistente de qualidade de código.
    Você receberá um arquivo em python e deve buscar por problemas,
    indicando ao usuário quais métodos, ou instruções precisam ser
    revisadas, indicando sempre uma justificativa.

    Você verifica o nome das variáveis, classes e métodos. Os retornos e as estruturas, e
    indica boas práticas. Para isso, você adota o padrão 'pep8'. 

    Além disso, você também indica falhas de redundância.

    # Formato de Saída
    Indica o problema, apresenta o código e mostra a sugestão de melhoria.  
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
    Eu gostaria de analisar meu script em python.
    Verifique pontos de melhoria no meu código.
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
        print("\n")
        print(uma_mensagem.text.value)
else:
    print(run.status)