
# MyTwitterApi

> MyTwitterApi é um case de exemplo de uma aplicação onde são implementados os três pilares da Observabilidade: Logs, Métricas e Eventos.

![Badge](https://img.shields.io/badge/MyTwitterApi-%23CB563E?style=for-the-badge&logo=twitter) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Conteúdo
=================
<!--ts-->
   * [Ambientes](#Ambientes)
      * [Aplicação](#Aplicação)
         * [twrestapi](#twrestapi)
         * [twitterctl](#twitterctl)
      * [Database](#database)
      * [Logs](#logs)
      * [Métricas](#métricas)
<!--te-->


<h4 align="center"> 
	🚧  Python Select 🚀 Em construção...  🚧
</h4>

# Ambientes

Todos os ambientes são executados em [containers](https://www.docker.com/resources/what-container) no Docker. 



Os arquivos do projeto estão estruturados da seguinte forma:

    mytwitterapi
    ├── infralogs                   # Arquivos de configuração do ambiente de logs
    ├── inframetrics                # Arquivos de configuração do ambiente de métricas
    ├── postman                     # Arquivo de coleção do Postman 
    ├── twitterctl                  # Client de linha de comando twitterctl.py
    ├── twrestapi                   # Código fonte da api
    ├── docker-compose.yml          # Arquivo do Compose para deploy dos containers 
    ├── LICENSE
    └── README.md

## Aplicação

### twrestapi

Api Rest para publicação e consulta de posts do Twitter:

- [x] Publicação de posts do twitter
- [x] Listagem de usuários com mais seguidores
- [x] Contagem de posts publicados por hora do dia
- [x] Contagem de posts publicados de um usuário de acordo com uma determinada tag agrupados por localização ou linguagem

Tecnologias:

* [Flask](https://flask.palletsprojects.com/en/1.1.x/): Framework para desenvolvimento web.
* [mongoengine](http://mongoengine.org/): Object-Document Mapper para MongoDB.

### twitterctl

Client de linha de comando para busca de posts no Twitter e publicação na twrestapi:

- [x] Busca de posts no twitter a partir de um conjunto de tags especificos
- [x] Publicação de posts do twitter na twresapi

Tecnologias:

* [Fire](https://github.com/google/python-fire): biblioteca para gerar CLI's a partir de qualquer objeto Python.

## Database

A aplicação utiliza o banco de dados NoSQL [MongoDB](https://www.mongodb.com/1).

## Logs

Ambiente de logs executando:

* [Elasticsearch](https://www.elastic.co/pt/elasticsearch/) para armazenamento e indexação dos logs da aplicação.
* [Kibana](https://www.elastic.co/pt/kibana) para visualização e analise dos logs.
* [Vector](https://vector.dev/docs/about/what-is-vector/) para envio dos logs da aplicação para o Elasticsearch.


## Métricas

* [Prometheus](https://prometheus.io/) para coleta e armazenamento de métricas.
* [Grafana](https://grafana.com/) para visualização e analise de métricas.


# Deploy dos Ambientes

Antes de começar a executar o ambiente, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

* [Git](https://git-scm.com)
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [Docker-Compose](https://docs.docker.com/compose/install/)




```bash
# Clone este repositório
$ git clone https://github.com/ezequielsbarros/mytwitterapi.git

# Acesse a pasta do projeto no terminal/cmd
$ cd mytwitterapi

# Faça o deploy dos containers com o Compose
# A opção "--build" serve para criar o container da api rest. 
# O uso dessa opção só é nescessária na primeira execução
# Ou caso o código da aplicação twrestapi seja modificado  
$ docker-compose up --build

# Opcional: use a opção "-d" para executar os containers em backgroud
$ docker-compose up --build -d

```

## Publicando dados na API

Inicialmente a API não vem com dados populados.

Você pode publicar dados na API utilizando o CLI twitterctl.py

Considetando que vc está dentro do diretório do projeto, execute o seguinte comandos para poder utilizar o CLI:

```bash
$ pip3 install -r ./twitterctl/requirements.txt
$ chmod +x ./twitterctl/twitterctl.py
```

Execute o comando abaixo para realizar uma busca de tweets recentes por tags e publicar na twrestapi.

Os parâmetros devem ser informados entre aspas:
* Substituir <BEARER TOKEN> por um token Bearer válido da API do Twitter
* Substituir <LISTA DE HASHTAGS SEPARADAS POR VÍRGULA> pela sua lista de tags. Você pode incluír quantas tags quiser.

```bash
$ ./twitterctl/twitterctl.py search "<BEARER TOKEN>" "<LISTA DE HASHTAGS SEPARADAS POR VÍRGULA>"
```

Exemplo de busca de tweets por hashtag:

```bash
$ ./twitterctl/twitterctl.py search "AAAAAAAAAAAAAAAAAAAAAM%faketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenA" "#hashtag1, #hashtag2, #hashtag3"
```

### Autor
---

Ezequiel de Souza Barros

[![Linkedin Badge](https://img.shields.io/badge/-Ezequiel-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/ezequielbarros/)](https://www.linkedin.com/in/ezequielbarros/) 
[![Gmail Badge](https://img.shields.io/badge/-ezequiel.sbarros@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:tgmarinho@gmail.com)](mailto:ezequiel.sbarros@gmail.com)