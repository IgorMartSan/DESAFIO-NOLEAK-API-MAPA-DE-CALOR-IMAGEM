# 🔍 Elasticsearch Vision Analytics API

Este projeto é uma API desenvolvida com **FastAPI** para processar imagens e gerar visualizações com base em dados oriundos do **Elasticsearch**, como mapas de calor (heatmaps) e caixas delimitadoras (bounding boxes) para objetos detectados.

## ✅ Pré-requisitos

Este projeto é empacotado com Docker para facilitar a execução e o deploy. Para rodar a aplicação, você precisa ter o Docker Engine instalado na sua máquina.

## ▶️ Executando o projeto

Para iniciar a aplicação entre no diretório do projeto onde se encontra o arquivo docker-compose.yaml e execute o comando:

```bash
docker compose up 
```

## ⚙️ Configurações de Ambiente

#### ➤ Por padrão, o projeto utiliza as seguintes configurações definidas no arquivo .env:


- PREFIX_PORT=321
- DB_DRIVERNAME=postgresql
- DB_USER=root
- DB_PASSWORD=automate.
- DB_HOST=db_postgres
- DB_PORT=${PREFIX_PORT}96
- DB_DATABASENAME=meubanco

#### ➤  Diretórios de volume e logs: 

- GLOBAL_PATH=./volumes
- PATH_LOGS=${GLOBAL_PATH}/logs
- PATH_VOL_POSTGRES=${GLOBAL_PATH}/postgres

#### ➤ Porta da API FastAPI

- PORT_API=${PREFIX_PORT}95


## 🚀 Funcionalidades

- Geração de **Bounding Boxes** sobre a imagem com base no objeto alvo.
- Geração de **Heatmap** (mapa de calor) para mostrar concentração dos objetos.
- Combinação de **Heatmap + Bounding Boxes**.
- Suporte a entrada via string JSON (Possui limite de tamanho para json) ou upload de arquivo `.json`.

## ✅ Recursos Disponíveis

Geração de Bounding Boxes sobre a imagem com base no objeto alvo.

Geração de Heatmap (mapa de calor) para mostrar a concentração dos objetos.

Combinação de Heatmap + Bounding Boxes para visualização completa.

Suporte a dois formatos de entrada:

✅ Entrada via string JSON (campo json_data)

✅ Entrada via upload de arquivo .json contendo os dados

### 👤 Autenticação e Gerenciamento de Usuários

- Foi implementado um **CRUD completo de usuários**
- Suporte à **autenticação JWT (JSON Web Token)** com endpoints para login e criação de token.
- ⚠️ **Observação importante**: os endpoints de visualização de imagem **não exigem autenticação JWT** por padrão.

## 📄 Documentação Interativa (Swagger)

A documentação interativa é gerada automaticamente pelo FastAPI utilizando o Swagger UI, e foi configurada para fornecer uma interface amigável para explorar e testar todos os endpoints da API.

### ➤ Acessar Swagger

Após subir a aplicação (`docker-compose`), acesse no navegador:

- http://localhost:32196/docs


> 💡 Caso tenha alterado a porta no `docker-compose.yml`, ajuste a URL conforme necessário.

### ➤ Na interface Swagger você pode:

- Testar os endpoints diretamente.
- Visualizar os parâmetros necessários.
- Fazer upload de imagem e JSON de forma prática.
- Observar respostas (imagem de saída gerada) diretamente.



