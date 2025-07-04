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

✅ Entrada via string JSON (campo json_data, exite limite para o tamanho do JSON)

✅ Entrada via upload de arquivo .json contendo os dados (De prioridade para o test com esses end points )

### 👤 Autenticação e Gerenciamento de Usuários

- Foi implementado um **CRUD completo de usuários**
- Suporte à **autenticação JWT (JSON Web Token)** com endpoints para login e criação de token.
- ⚠️ **Observação importante**: os endpoints de visualização de imagem **não exigem autenticação JWT** por padrão.

✅ **Testar autenticação JWT**

Para testar os endpoints protegidos com autenticação, utilize as credenciais padrão abaixo (úteis em ambiente de desenvolvimento):

```env
INITIAL_USER_LOGIN_JWT=admin
INITIAL_USER_PASSWORD_JWT=automate123.
```

## 📄 Documentação Interativa (Swagger)

A documentação interativa é gerada automaticamente pelo FastAPI utilizando o Swagger UI, e foi configurada para fornecer uma interface amigável para explorar e testar todos os endpoints da API.

### ➤ Acessar Swagger

Após subir a aplicação (`docker-compose`), acesse no navegador:

- http://localhost:32195/docs


> 💡 Caso tenha alterado a porta no `docker-compose.yml`, ajuste a URL conforme necessário.

### ➤ Na interface Swagger você pode:

- Testar os endpoints diretamente.
- Visualizar os parâmetros necessários.
- Fazer upload de imagem e JSON de forma prática.
- Observar respostas (imagem de saída gerada) diretamente.

## 🧪 Sugestão para Testes
Dê preferência para testar os endpoints usando o upload do arquivo JSON (UploadFile) em vez do envio como string via campo json_data, especialmente para JSONs grandes ou gerados a partir de outras ferramentas (como Kibana ou Elasticsearch diretamente).


✅ **Todos os endpoints podem ser testados diretamente na interface Swagger** 

### 🎯 Endpoints Disponíveis

#### 🚫 Não Recomendados (envio via string `json_data`)
Estes endpoints utilizam `FormData` com string JSON. Úteis para testes rápidos, mas **podem causar problemas com arquivos grandes**.

| Método | Rota                  | Descrição                              |
|--------|-----------------------|----------------------------------------|
| POST   | `/draw/bbox`          | Desenhar bounding boxes                |
| POST   | `/draw/heatmap`       | Gerar heatmap da imagem                |
| POST   | `/draw/heatmap_bbox`  | Gerar heatmap com bounding boxes       |

---

#### ✅ Recomendados (envio via upload de arquivo `.json`)
Estes endpoints usam `UploadFile` para enviar o JSON — **mais confiável**, sem limites de tamanho, ideal para produção.

| Método | Rota                        | Descrição                                           |
|--------|-----------------------------|-----------------------------------------------------|
| POST   | `/draw/bbox_file`           | Desenhar bounding boxes (com arquivo JSON)         |
| POST   | `/draw/heatmap_file`        | Gerar heatmap da imagem (com arquivo JSON)         |
| POST   | `/draw/heatmap_bbox_file`   | Gerar heatmap com bounding boxes (com arquivo JSON)|

---




