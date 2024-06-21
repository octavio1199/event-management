# Event Manager

Este é um sistema de gerenciamento de eventos construído com Django, Celery e Docker.

## Pré-requisitos

- Python 3.9.6
- Docker
- Docker Compose

## Configuração do Ambiente

1. Clone o repositório para a sua máquina local usando `git clone`.

2. Navegue até o diretório do projeto.

3. Rode as migrations do Django:

```bash
python manage.py migrate
```

4. Construa e inicie os contêineres Docker usando o Docker Compose:

```bash
docker-compose up -d
```

## Executando o Projeto

Depois de iniciar os contêineres Docker, o aplicativo estará disponível em http://localhost:8000.  

## Executando os Testes

Para executar os testes, você pode executar o seguinte comando

```bash
docker exec -it eventmanager-api-1 /bin/bash

python manage.py test
```

## Documentação

A documentação da API está disponível em http://localhost:8000/swagger/ e http://localhost:8000/redoc/.

## Desligando o Projeto
Para parar os contêineres Docker, você pode usar o seguinte comando:

```bash
docker-compose down
```
