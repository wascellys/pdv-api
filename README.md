# PDV-API

- [Instalação](#instalação)
  - [Usando Docker](#usando-docker)
  - [Usando ambiente virtual](#usando-ambiente-virtual)
  - [Instalação das Dependências ](#instalação-das-dependências)
- [Rodar Projeto](#rodar-projeto)
- [Cobertura de Testes](#cobertura-de-testes)
- [Documentação](#documentação)
- [Front end do projeto](#frontend)



## Instalação

### Clonar repositório
```
git clone https://github.com/wascellys/pdv-api.git
```

### Adicionar variáveis de ambiente

No diretório da aplicação, criar um arquivo .env e adicionar as seguintes variáveis:
```
DB_HOST=db
DB_NAME=pdv-db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DATE_INIT_MAX=0,0,0
DATE_FINAL_MAX=12,0,0
DATE_INIT_MIN=12,0,1
DATE_FINAL_MIN=23,59,59
WEB_HOST=/api/v1
DJANGO_SETTINGS_MODULE=pdv.settings
```

## Usando Docker
Na raiz do projeto, abra o terminal e execute o comando  
```
docker-compose up --build
```

## Usando ambiente virtual
#### Instalação do Python em terminal Linux
```
sudo apt install python3-pip python3-dev libpq-dev virtualenv
```
#### Criando virtualenv
```
virtualenv myenv --python=python3
```
#### Ativação da  virtualenv
```
source myenv/bin/activate
```
## Instalação das Dependências
```
pip install -r requirements.txt
```
## Criar banco de dados
```
psql -h localhost -U postgres
```

#### Criar banco de dados
```
CREATE DATABASE DB;

GRANT ALL ON DATABASE DB TO postgres;
```

## Criar migrações
No diretório raiz do projeto execute o comando:
```
python manage.py makemigrations 
```

```
python manage.py migrate 
```

## Rodar Projeto
No diretório raiz do projeto execute o comando:
```
python manage.py runserver
```

## Cobertura de testes
No diretório do projeto execute o comando:
```
coverage run -m pytest api/tests
```

Para ver os testes em detalhe, execute o comando:
```
coverage report -m
```

Para gerar um relatório com os testes em um arquivo HTML, execute o comando:
```
coverage html
```
Será criada uma nova pasta com o nome "htmlcov", basta abrir no arquivo index.html no navegador.

## Documentação
## Requisições HTTP
Toda requisição para a API são feitas por uma requisição HTTP usando para um dos seguintes métodos:

* `POST` Criar um recurso
* `PUT` Atualizar um recurso
* `GET` Buscar um ou uma lista de recursos
* `DELETE` Excluir um recurso

## Códigos de respostas HTTP
Cada resposta será retornada com um dos seguintes códigos de status HTTP:

* `201` `CREATED` A criação foi bem sucedida
* `200` `OK` A requisição foi bem sucedida
* `400` `Bad Request` Houve um problema com a solicitação (segurança, malformado, validação de dados, etc.)
* `401` `Unauthorized` As credenciais fornecidas à API são inválidas
* `403` `Forbidden` As credenciais fornecidas não têm permissão para acessar o recurso solicitado
* `404` `Not found` Foi feita uma tentativa de acessar um recurso que não existe
* `500` `Server Error` Ocorreu um erro no servidor

## Endpoints

Os endpoints estão abertos, não precisam de autenticação :

## Rotas

CLIENTE
  - *Cadastrar cliente: `POST` `api/v1/clients`*
  - *Atualizar dados do  cliente: `PUT` `api/v1/clients/<id>/`*
  - *Remover cliente: `DELETE` `api/v1/clients/<id>/`*
  - *Detalhar cliente: `GET` `api/v1/clients/<id>/`*
  - *Detalhar cliente: `GET` `api/v1/clients/<id>/`*
  
VENDEDOR
- *Cadastrar vendedor: `POST` `api/v1/sellers`*
- *Atualizar dados do  vendedor: `PUT` `api/v1/sellers/<id>/`*
- *Remover vendedor: `DELETE` `api/v1/sellers/<id>/`*
- *Detalhar vendedor: `GET` `api/v1/sellers/<id>/`*
- *Detalhar comissões de um vendedor: `GET` `api/v1/sellers/<id>/commission/`*
  
  Na consulta por comissão, pode ser passado filtros de periodo de tempo:
  ex: 
  ```
  api/v1/sellers/<id>/commission/?initial_date=10/09/2020&final_date=20/09/2022
  ```
  
VENDA
- *Cadastrar venda: `POST` `api/v1/sales`*
- *Atualizar dados da venda: `PUT` `api/v1/sales/<id>/`*
- *Remover venda: `DELETE` `api/v1/sales/<id>/`*
- *Detalhar venda: `GET` `api/v1/sales/<id>/`*
- *Detalhar itens da venda: `GET` `api/v1/sales/<id>/orders/`*


ITEMS DA VENDA
- *Cadastrar item: `POST` `api/v1/orders`*
- *Atualizar item da venda: `PUT` `api/v1/orders/<id>/`*
- *Remover item: `DELETE` `api/v1/orders/<id>/`*
- *Detalhar item: `GET` `api/v1/orders/<id>/`*
  
## Frontend
  
  O frontend está neste diretório:

https://github.com/wascellys/pdv-web.git


