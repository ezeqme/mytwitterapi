
# MyTwitterApi

> MyTwitterApi é um case de exemplo de uma aplicação onde são implementados os três pilares da Observabilidade: Logs, Métricas e Eventos.

![Badge](https://img.shields.io/badge/MyTwitterApi-%23CB563E?style=for-the-badge&logo=twitter) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# Conteúdo
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

# Pré-Requisitos

Você pode executar esses ambientes em qualquer sistema operacional com suporte a docker mas não posso garantir que tudo vai funcionar como esperado portando recomendo testar seguindo os requisitos abaixo:

* Sistema Operacional: Ubuntu 18 LTE
* Memória RAM: >= 6GB

()

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

Para validar se todos os containers estão up execute o seguinte comando:

```bash
$ docker ps
CONTAINER ID        IMAGE                                                  COMMAND                  CREATED             STATUS              PORTS                                            NAMES
0b4abb8b7747        prom/prometheus                                        "/bin/prometheus --c…"   42 minutes ago      Up 42 minutes       0.0.0.0:9090->9090/tcp                           mytwitterapi_prometheus_1
991fd6f5fb9d        twrestapi:python3-alpine                               "sh entrypoint.sh"       42 minutes ago      Up 42 minutes       0.0.0.0:80->8080/tcp                             mytwitterapi_twitterapi_1
3f347620045e        docker.elastic.co/kibana/kibana:6.8.13                 "/usr/local/bin/kiba…"   42 minutes ago      Up 42 minutes       0.0.0.0:5601->5601/tcp                           mytwitterapi_kibana_1
8af6ae1d3e2f        timberio/vector:latest-alpine                          "/usr/local/bin/vect…"   42 minutes ago      Up 42 minutes       0.0.0.0:9014->9014/tcp, 0.0.0.0:9514->9514/tcp   mytwitterapi_vector_1
69722b86cfff        mongo                                                  "docker-entrypoint.s…"   42 minutes ago      Up 42 minutes       0.0.0.0:27017->27017/tcp                         mytwitterapi_mongodb_1
1798f0f53988        docker.elastic.co/elasticsearch/elasticsearch:6.8.13   "/usr/local/bin/dock…"   42 minutes ago      Up 42 minutes       0.0.0.0:9200->9200/tcp, 0.0.0.0:9300->9300/tcp   mytwitterapi_elasticsearch_1
d3156c34e125        grafana/grafana                                        "/run.sh"                42 minutes ago      Up 42 minutes       0.0.0.0:3000->3000/tcp                           mytwitterapi_grafana_1
```

## Acessando os serviços

Os serviços podem ser acessados pelas seguintes urls após o deploy:

* twitterapi: [http://localhost](http://localhost)
* MongoDB: [http://localhost:27017](http://localhost:27017)
* Elasticsearch: [http://localhost:9200](http://localhost:9200)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Kibana: [http://localhost:5601](http://localhost:5601)
* Grafana: [http://localhost:3000](http://localhost:3000)


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
$ ./twitterctl/twitterctl.py search "AAAAAAAAAAAAAAAAAAAAAM%faketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenfaketokenA" "#openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing"
```

# Logs e Métricas

## Dashboard de logs no Kibana

Para visualizar os logs do no Kibana foi disponibilizado um dashboard para ser importado:

Para realizar o import:
* Acesse o kibana: http://localhost:5601/
* Na aba esquerda clique na opção "Management" --> "Saved Objects" --> "Import"
* Clique em import novamente e selecione o arquivo com os dados exportados do dashboard:
   * Arquivo dentro do projeto: exports/kibana-dashboar-twrestapi-export.json
* Clique em "Import"
* Se aparecer a mensagem "Import sucessful" o dashboard foi importado corretamente
* Acesse na aba lateral "Dashboard" --> "Twitter API"

## Dashboard de métricas no Grafana

O dashboard de métricas já é importado automaticamente ao inicializar o container do grafana. Basta acessar o serviço http://localhost:3000/

Usuário: admin
Senha: admin

Observação: será solicitado a troca da senha no primeiro acesso.

### Autor
---

Ezequiel de Souza Barros

[![Linkedin Badge](https://img.shields.io/badge/-Ezequiel-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/ezequielbarros/)](https://www.linkedin.com/in/ezequielbarros/) 
[![Gmail Badge](https://img.shields.io/badge/-ezequiel.sbarros@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:tgmarinho@gmail.com)](mailto:ezequiel.sbarros@gmail.com)