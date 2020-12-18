
# MyTwitterApi

> MyTwitterApi é um case de exemplo de uma aplicação onde são implementados os três pilares da Observabilidade: Logs, Métricas e Eventos.

![Badge](https://img.shields.io/badge/MyTwitterApi-%23CB563E?style=for-the-badge&logo=twitter) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Indice
=================
<!--ts-->
   * [Ambientes](#Ambientes)
      * [Aplicação](#Aplicação)
         * [twrestapi](#twrestapi)
         * [twitterctl](#twitterctl)
      * [database](#database)
      * [logs](#logs)
      * [métricas](#métricas)
<!--te-->


<h4 align="center"> 
	🚧  Python Select 🚀 Em construção...  🚧
</h4>

# Ambientes

## Aplicação

### twrestapi

- [x] Publicação de posts do twitter
- [x] Listagem de usuários com mais seguidores
- [x] Contagem de posts publicados por hora do dia
- [x] Contagem de posts publicados de um usuário de acordo com uma determinada tag agrupados por localização ou linguagem

### twitterctl

- [x] Busca de posts no twitter a partir de um conjunto de tags especificos
- [x] Publicação de posts do twitter na twresapi

### database

A aplicação utiliza o banco de dados NoSQL [MongoDB](https://www.mongodb.com/1).

### logs

Ambiente de logs executando:

* [Elasticsearch](https://www.elastic.co/pt/elasticsearch/) para armazenamento e indexação dos logs da aplicação.
* [Kibana](https://www.elastic.co/pt/kibana) para visualização e analise dos logs.
* [Vector](https://vector.dev/docs/about/what-is-vector/) para envio dos logs para o elasticsearch.


### métricas

# Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

* [Git](https://git-scm.com)
* [Docker](https://docs.docker.com/engine/install/ubuntu/)
* [Docker-Compose](https://docs.docker.com/compose/install/)



```bash
# Clone este repositório
$ git clone <https://github.com/ezequielsbarros/mytwitterapi.git>

# Acesse a pasta do projeto no terminal/cmd
$ cd mytwitterapi

# Faça o deploy dos ambientes com o Compose
$ docker-compose up --build

# Opcional: use a opção "-d" para executar os ambientes em backgroud
$ docker-compose up --build

```