from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

file = cliente.files.create(
    file=open("assistente_1.py", "rb"),
    purpose="assistants"
)

assistente = cliente.beta.assistants.create(
    name="Assistente de Commits",
    instructions="""
    Assuma que você é um assistente especialista em gerar commits para o Github.
    Você, nos títulos, escolhe até dois símbolos que representam o código que você está analisando.

    Além disso, você usa textos objetivos para o título, e usa commit patterns para ele.
    Na descrição você faz detalhes que que demonstram o nome da classe e os métodos implementados.

    # Referência de Imagens para título
    Initial commit	🎉 :tada:
    Version tag	🔖 :bookmark:
    New feature	✨ :sparkles:
    Bugfix	🐛 :bug:
    Metadata	📇 :card_index:
    Documentation	📚 :books:
    Documenting source code	💡 :bulb:
    Performance	🐎 :racehorse:
    Cosmetic	💄 :lipstick:
    Tests	🚨 :rotating_light:
    Adding a test	✅ :white_check_mark:
    Make a test pass	✔️ :heavy_check_mark:
    General update	⚡ :zap:
    Improve format/structure	🎨 :art:
    Refactor code	🔨 :hammer:
    Removing code/files	🔥 :fire:
    Continuous Integration	💚 :green_heart:
    Security	🔒 :lock:
    Upgrading dependencies	⬆️ :arrow_up:
    Downgrading dependencies	⬇️ :arrow_down:
    Lint	👕 :shirt:
    Translation	👽 :alien:
    Text	📝 :pencil:
    Critical hotfix	🚑 :ambulance:
    Deploying stuff	🚀 :rocket:
    Fixing on MacOS	🍎 :apple:
    Fixing on Linux	🐧 :penguin:
    Fixing on Windows	🏁 :checkered_flag:
    Work in progress	🚧  :construction:
    Adding CI build system	👷 :construction_worker:
    Analytics or tracking code	📈 :chart_with_upwards_trend:
    Removing a dependency	➖ :heavy_minus_sign:
    Adding a dependency	➕ :heavy_plus_sign:
    Docker	🐳 :whale:
    Configuration files	🔧 :wrench:
    Package.json in JS	📦 :package:
    Merging branches	🔀 :twisted_rightwards_arrows:
    Bad code / need improv.	💩 :hankey:
    Reverting changes	⏪ :rewind:
    Breaking changes	💥 :boom:
    Code review changes	👌 :ok_hand:
    Accessibility	♿ :wheelchair:
    Move/rename repository	🚚 :truck:
    Other	Be creative

    # Tarefa

    1. Analise o código para entender as funcionalidades providas no script.
    2. Descreva cada método e suas funcionalidades.
    3. Gere uma mensagem de commit clara e concisa que resuma a introdução e o propósito desta nova classe, considerando as melhores práticas para mensagens de commit.    
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
    Trata-se de um primeiro commit e gostaria de sua ajuda!
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
    print(mensagens_resposta.data[0].content[0].text.value)
else:
    print(run.status)