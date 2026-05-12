## SafeWork - Monitorização Inteligente de EPIs
O SafeWork é uma solução de Visão Computacional e Inteligência de Negócio (BI) focada na automação da segurança do trabalho. 
O sistema utiliza Inteligência Artificial para identificar em tempo real o uso de Equipamentos de Proteção Individual (EPIs),
 transformando fluxos de vídeo em indicadores estratégicos para a prevenção de acidentes.

## Stack de Desenvolvimento
A stack foi selecionada para garantir baixa latência no processamento de vídeo e alta escalabilidade de dados:

1. Backend & Inteligência Artificial
   Linguagem: Python 3.10+
   IA & Visão: YOLOv11 (Detecção de objetos), OpenCV (Processamento de imagem) e Dlib (Reconhecimento Facial).
   API Framework: FastAPI (Processamento assíncrono para lidar com streams de vídeo em tempo real).
   Comunicação: WebSockets para alertas instantâneos ao Dashboard.

2. Frontend & Visualização
   Framework: React.js com Tailwind CSS.
   Gráficos (BI): Chart.js ou Recharts para visualização de KPIs de conformidade.

3. Infraestrutura & Dados
   Banco de Dados: PostgreSQL (Dados relacionais e históricos de BI).
   Storage: Firebase Storage (Armazenamento de evidências fotográficas das infrações).

## Arquitetura do Sistema
O SafeWork adota a Clean Architecture (Arquitetura Limpa), organizada através do Modelo C4 (Níveis 1 a 3).
![alt text](<SafeWork - Diagrama de Contêineres (C4 Nível 2).drawio.png>) ![alt text](<SafeWork - Diagrama de Contexto (C4 Nível 1).drawio.png>) ![alt text](<SafeWork - Componentes da API Backend (C4 Nível 3).drawio (1).png>) ![alt text](<SafeWork - Detalhamento da Estrutura de Classes (C4 Nível 4).drawio (2).png>)

## Por que Clean Architecture?
   
    1.Implementamos a Clean Architecture para garantir que o SafeWork seja um software sustentável:
    2.Desacoplamento do Modelo de IA: Se precisarmos trocar o YOLOv11 por outra tecnologia no futuro, alteramos apenas a pasta ai_engine, mantendo o restante do sistema intacto.
    3.Regras de Negócio Isoladas: As políticas de segurança (ex: "Capacete obrigatório no Setor A") residem na camada domain, longe de detalhes técnicos como bancos de dados ou interfaces web.
    4.Escalabilidade Profissional: Esta estrutura permite que diferentes desenvolvedores trabalhem em partes distintas (IA, Front ou Back) sem gerar conflitos de código.

## Regra de Negócio (Lógica de Funcionamento)
A regra de negócio principal é o Pipeline de Conformidade:

    1. Ingestão: Recebe o stream de vídeo via RTSP.
    2. Deteção (YOLOv11): Identifica classes como Pessoa, Capacete, Colete, Luvas.
    3. Validação de Política: O sistema consulta o banco de dados para saber quais EPIs são obrigatórios para aquela câmara/setor específico.
    4. Identificação Facial: Se uma falta de EPI for detetada, o motor de reconhecimento facial entra em ação para identificar o colaborador recidivo.

## Ação & BI:

1. O frame da infração é enviado para o Firebase.
2. Um alerta é disparado via WebSocket para o gestor.
3. Os dados alimentam tabelas de Fato e Dimensão para análise de BI (Ex: "Qual setor tem mais infrações às terças-feiras?").

## Protótipo Estrutural do Projeto
O repositório será organizado em micro-módulos para facilitar o desenvolvimento paralelo:

SAFEWORK_TCC/
├── backend/                    # Core do Sistema (Python/FastAPI)
│   ├── app/
│   │   ├── api/                # Rotas (v1/endpoints.py) e WebSockets
│   │   ├── core/               # Configurações globais (Security, Config, Env)
│   │   ├── domain/             # Regras de Negócio Puras (Entidades e Modelos)
│   │   ├── services/           # Lógica de Orquestração (Inference & Safety Engine)
│   │   └── infrastructure/     # Conexão com DB (PostgreSQL) e Firebase Client
│   ├── ai_engine/              # Motor de Visão Computacional
│   │   ├── models/             # Pesos do YOLOv11 (.pt) e Face Recognition
│   │   ├── processors/         # Scripts de processamento de frames/OpenCV
│   │   └── utils/              # Helpers para desenho de bounding boxes
│   ├── tests/                  # Testes unitários e de integração
│   ├── main.py                 # Ponto de entrada do FastAPI
│   └── requirements.txt        # Dependências (ultralytics, fastapi, etc.)
├── frontend/                   # Interface do Usuário (React.js)
│   ├── public/                 # Arquivos estáticos
│   ├── src/
│   │   ├── assets/             # Imagens, Ícones e Estilos (Tailwind)
│   │   ├── components/         # Componentes Reutilizáveis (Cards, Sidebar, VideoPlayer)
│   │   ├── pages/              # Telas (Dashboard, Relatórios, Configurações)
│   │   ├── services/           # Integração com API (Axios) e WebSockets
│   │   └── context/            # Gerenciamento de estado global
│   ├── package.json
│   └── tailwind.config.js
├── docs/                       # Documentação Técnica
│   ├── diagrams/               # Diagramas (Sequência, C4, Casos de Uso)
│   └── architecture/           # Explicações detalhadas da arquitetura
├── .gitignore                  # Arquivos ignorados (venv, .env, __pycache__)
└── README.md                   # Documentação Principal do Projeto

1. Camada de Inteligência Artificial (AI Engine)
YOLOv11: Escolhido por ser a versão mais atualizada da arquitetura YOLO, oferecendo o melhor equilíbrio entre precisão (mAP) e velocidade de inferência em dispositivos de borda (Edge).

OpenCV: Utilizado para o tratamento de streams de vídeo RTSP e manipulação de matrizes de imagem.

Dlib/Face Recognition: Implementado para garantir a identificação civil automática em caso de reincidência de infrações.

2. Camada de Backend (API & Business Logic)
FastAPI: A escolha se deu pelo suporte nativo a operações assíncronas (asyncio), permitindo que o sistema processe múltiplos feeds de vídeo simultaneamente sem travar a API.

PostgreSQL: Base de dados robusta para suportar a modelagem dimensional (Star Schema) necessária para as análises de BI.

Firebase Storage: Utilizado como um "Data Lake" para evidências visuais, garantindo que as fotos das infrações fiquem seguras na nuvem.

3. Camada de Frontend (Dashboard & BI)
React.js: Permite a criação de um Dashboard dinâmico onde os alertas de segurança aparecem em tempo real via WebSockets, sem necessidade de recarregar a página.

---
*Desenvolvido por Emilly Crisallys e Gustavo Rodrigues.*
