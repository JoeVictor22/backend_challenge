## Resumo
Implementação de uma API para cadastro de usuários utilizando a framework Flask, Pydantic para validação de dados e SQLalchemy como ORM para um banco de dados Postgres.

### docker deployment
- Copiar o arquivo docker-compose.yml deste repositorio para a raiz de sua pasta e utilizar a seguinte estrutura para configurar os containers
```
├── docker-compose.yml
├── backend_challenge/
│   ├── .dev.env
│   ├── .homolog.env
│   ├── docker-compose.dev.yml
│   ├── docker-compose.homolog.yml
│   └── docker/
│   │   ├── backend/
│   │   │   └── Dockerfile
│   │   └── frontend/
│   │   │   └── Dockerfile
├── frontend_challnege/
```
- A partir da raiz, executar:
> docker-compose -f docker-compose.yml -f backend_challenge/docker-compose.[AMBIENTE].yml up

### configuração do banco de dados
#### Geração de tabelas
> python run.py db init</br>
> python run.py db migrate</br>
> python run.py db upgrade</br>

#### Popular com dados base
Executar o seguinte script ou inserir no banco de dados os arquivos cidade_uf.sql e rules.sql encontrados em /utils/scripts/db/.
> python -m utils.scripts.insertData

### testes unitários
- Configurar dentro de um arquivo .env, o banco de dados para realização dos testes
> DATABASE_TEST_URI=postgresql://postgres:root@localhost/web_app_test
- Os testes podem ser realizados executando
> make test

### swagger
- Configurar servidor HTTP com os arquivos necessários
> make swagger
- A Swagger UI pode ser acessada em:
> localhost:8000