import logging
import boto3
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
# from PyPDF2 import PdfReader

load_dotenv()

# Configuração de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "minha_chave_secreta")  # Chave secreta para a sessão

# Credenciais fixas
USERNAME = "usuario"
PASSWORD = "aws&chat"

def generate_conversation(bedrock_client, model_id, messages):
    """Envia mensagens para o modelo."""
    logger.info("Generating message with model %s", model_id)

    # Parâmetros de inferência
    temperature = 0.5
    top_k = 200

    # Configurações de inferência
    inference_config = {"temperature": temperature}
    additional_model_fields = {"top_k": top_k}

    # Envia a mensagem
    response = bedrock_client.retrieve_and_generate(
    input=messages[0],
    retrieveAndGenerateConfiguration={
        "externalSourcesConfiguration": {
            "generationConfiguration": {
                "guardrailConfiguration": { 
                    "guardrailId": "uujvlt1oxsmr",
                    "guardrailVersion": "1"
                },
            },
            "modelArn": "arn:aws:bedrock:us-west-2:432704416414:guardrail/uujvlt1oxsmr",
            "sources": [ 
                {
                    "s3Location": { 
                        "uri": "s3://cf-templates-d9sa1gzub041-us-west-2/2024-10-07T174427.430Z0ff-create-customer-resources.yml"
                    },
                    "sourceType": "S3"
                }
            ],
        },
        "knowledgeBaseConfiguration": {
            "knowledgeBaseId": "F7RNIUVKWU",
            "modelArn": "anthropic.claude-3-haiku-20240307-v1:0",
            'generationConfiguration': {
                'promptTemplate': {
                    'textPromptTemplate': '''Você é um assistente educado e amigável, especializado em responder perguntas sobre a História do Brasil. O usuário pode interagir com você de maneira amigável, fazendo perguntas cordiais, e você sempre responde de forma gentil e acolhedora. Seu objetivo é ajudar o usuário com base nas informações fornecidas no documento de referência (PDF sobre a História do Brasil). Se o usuário fizer uma pergunta que você não puder responder com base nesse material, seja honesto e diga algo como: "Lamento, não consegui encontrar uma resposta exata para sua pergunta no meu material de referência sobre a História do Brasil. Mas posso tentar ajudar com outras perguntas relacionadas a esse assunto."

                    Se o usuário o cumprimentar de maneira amigável, como "Olá, como você está?" ou "Olá, você pode me ajudar?", responda calorosamente, por exemplo: "Olá! Estou aqui para ajudar com perguntas sobre a História do Brasil."

                    Instruções para respostas:

                    - Responda apenas perguntas relacionadas à História do Brasil.
                    - Se a resposta estiver no PDF, use essas informações.
                    - Se a resposta não estiver no PDF ou você não conseguir encontrá-la, seja honesto e diga algo como: "Lamento, não consegui encontrar uma resposta exata para sua pergunta no meu material de referência sobre a História do Brasil. Mas posso tentar ajudar com outras perguntas relacionadas a esse assunto."
                    - Se a pergunta for sobre outro assunto (como a história de outros países), não responda, mas continue sendo educado.
                    - Não declare explicitamente que não pode responder porque se especializa na História do Brasil. Simplesmente evite fornecer uma resposta, mantendo um tom gentil.
                    - Se o usuário fizer perguntas pessoais, como "Qual é o seu nome?" ou "Qual é a sua idade?", responda sempre de maneira amigável. Por exemplo, se perguntarem seu nome, você pode dizer: "Pode me chamar de Jefinho", e se perguntarem sua idade, dê uma resposta apropriada com base na persona que está usando.
                    - Se o usuário enviar uma entrada que não faça sentido ou seja claramente um erro, responda com uma frase educada como: "Desculpe, não entendi o que você quis dizer. Poderia reformular sua pergunta?"

                    Esteja sempre educado, amigável e respeitoso.

                    Exemplos de cumprimentos e despedidas:
                    - "Olá! Como você está? Estou aqui para ajudar com perguntas sobre a História do Brasil!"
                    - "Fique à vontade para fazer mais perguntas!"
                    - "Espero ter sido útil! Até a próxima!"

                    Mantenha o fluxo da conversa sem quebras desnecessárias, mesmo quando não puder responder diretamente a uma pergunta.

                    Aqui estão os resultados numerados da pesquisa: $search_results$
                    '''
                }
            }
        },
        "type": "KNOWLEDGE_BASE",
    },
)


    
    # Log de uso de tokens

    return response


# def read_pdf(file_path):
#     """Lê um arquivo PDF e retorna seu conteúdo como texto."""
#     with open(file_path, "rb") as file:
#         reader = PdfReader(file)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
#     return text

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Verifica as credenciais fornecidas
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            # Autenticação bem-sucedida
            session["authenticated"] = True
            return redirect(url_for("home"))
        else:
            # Autenticação falhou
            return render_template("login.html", error="Credenciais inválidas. Tente novamente.")

    return render_template("login.html")

@app.route("/")
def home():
    # Verifica se o usuário está autenticado
    if not session.get("authenticated"):
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/logout")
def logout():
    # Finaliza a sessão e redireciona para a página de login
    session.pop("authenticated", None)
    return redirect(url_for("login"))

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")

    # Configuração do modelo e mensagens
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    # Prepara a mensagem do usuário
    messages = [{"text": user_question}]

    try:
        # Configuração do cliente boto3
        bedrock_client = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name="us-west-2",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        # Gera a resposta do modelo
        response = generate_conversation(bedrock_client, model_id, messages)

        output_message = response['output']['text']
        messages.append(output_message)
    

        # Retorna a resposta como JSON
        return jsonify({"conversation": messages})

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        messages.append({"role": "bot", "content": [{"text": message}]})
        return jsonify({"conversation": messages})

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        messages.append(
            {
                "role": "bot",
                "content": [{"text": "Ocorreu um erro ao processar sua solicitação."}],
            }
        )
        return jsonify({"conversation": messages})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
