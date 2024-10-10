## Projeto Chatbot de História do Brasil

### Visão Geral

Este projeto consiste na implementação de um chatbot baseado em Inteligência Artificial (IA) que responde perguntas sobre a História do Brasil até 2019. Ele foi desenvolvido utilizando a infraestrutura da AWS (Amazon Web Services) e a biblioteca **Flask** para o backend. A IA é alimentada por um modelo da **Anthropic Claude-3 Haiku**, selecionado por ser uma opção econômica e rápida, sem a necessidade de usar uma IA mais robusta e complexa, devido ao escopo limitado do projeto.

O chatbot foi programado para interagir de maneira educada, amigável e especializada no tema proposto. O modelo utilizado foi configurado para se basear em um material de referência, o que limita suas respostas às informações contidas em um PDF sobre a História do Brasil.

### Estrutura do Projeto

O projeto é composto pelas seguintes partes principais:

1. **Interface com Flask**: O Flask é utilizado como framework web para construir uma API REST que serve as interações do chatbot. O projeto possui endpoints para envio de perguntas e geração de respostas.

2. **Modelo de IA Claude Haiku**: O modelo de IA utilizado é o Claude-3 Haiku, hospedado na AWS Bedrock. Esse modelo foi escolhido devido ao seu custo-benefício e rapidez de execução, além de atender às necessidades de um projeto que não demanda uma IA muito pesada.

3. **Integração com AWS Bedrock**: A aplicação utiliza a API da AWS Bedrock para enviar perguntas e receber respostas da IA, aproveitando a escalabilidade e a confiabilidade da infraestrutura da AWS.

4. **Comportamento do Chatbot**: O chatbot foi configurado para responder apenas perguntas relacionadas à História do Brasil. Se a resposta não estiver disponível no material de referência, ele indicará que não pode fornecer uma resposta precisa, mas continuará sendo educado e oferecendo alternativas.

5. **Front-end**: O front-end da aplicação web foi desenvolvido com HTML, CSS e JavaScript, permitindo que os usuários façam perguntas diretamente na interface web e vejam as respostas geradas em tempo real.

### Autenticação de Usuário

A aplicação conta com uma tela de autenticação simples que requer login e senha fixos para acessar o chatbot. As credenciais são as seguintes:

- **Usuário**: `usuario`
- **Senha**: `aws&chat`

O login é necessário para garantir que apenas usuários autorizados possam interagir com o chatbot. Após fornecer as credenciais corretas, o usuário é redirecionado para a interface do chat.

### Dependências

- **Flask**: Framework web utilizado para construir a API e servir as páginas HTML.
- **boto3**: Biblioteca utilizada para integração com a AWS, permitindo chamadas para os serviços do Bedrock.
- **dotenv**: Utilizado para carregar as credenciais de ambiente necessárias para acessar a AWS.
- **PyPDF2** (opcional): Inicialmente planejado para leitura do PDF de referência diretamente, mas não utilizado na versão final.

### Endpoints

- **GET /**: Rota principal que serve a página inicial do chatbot (após autenticação).
- **POST /ask**: Rota que recebe a pergunta do usuário e faz uma chamada ao modelo de IA na AWS para gerar a resposta.
- **GET /login**: Rota para exibição da tela de login.
- **POST /login**: Rota para validação das credenciais do usuário.
- **GET /logout**: Rota para encerrar a sessão e redirecionar o usuário para a tela de login.

### Exemplo de Interação com o Chatbot

1. O usuário acessa a tela de login e insere as credenciais corretas (usuário: `usuario`, senha: `aws&chat`).
2. Após autenticar, o usuário entra na interface web e insere uma pergunta, como "Quem foi Pedro Álvares Cabral?".
3. A aplicação envia a pergunta para o modelo Claude-3 Haiku.
4. A resposta é retornada pela IA com base no material de referência, ou uma resposta educada é fornecida caso a IA não possa encontrar a informação.

### Configurações e Execução

1. **Configuração da AWS**: É necessário configurar as credenciais da AWS no arquivo `.env`:
   ```
   AWS_ACCESS_KEY_ID=seu_acesso
   AWS_SECRET_ACCESS_KEY=sua_chave
   AWS_KNOWLEDGE_BASE_ID=seu_knowledge_base
   ```
2. **Configuração da Autenticação**: A autenticação está configurada no código da aplicação com as credenciais fixas mencionadas acima.
3. **Execução da aplicação**:
   - Instale as dependências listadas no arquivo `requirements.txt`.
   - Execute o servidor Flask com o comando:
     ```bash
     python3 app.py
     ```
   - Acesse a aplicação em `http://localhost:5000`.
