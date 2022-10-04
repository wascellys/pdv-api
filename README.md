# pdv-api


##Adicionar variáveis de ambiente

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
