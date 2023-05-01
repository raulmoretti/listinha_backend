# Listinha
## _A lista online de supermercado da sua família_

## Características

- Crie sua conta
- Cadastre, edite, remova produtos
- Crie grupos (famílias) em que os participantes compartilham um mesmo carrinho
- Crie um carrinho de compra para sua família
- Membros participantes podem inserir, editar e excluir ordens de compra (com seus produtos cadastrados) no carrinho da família
- Conclua a listinha após ter sido finalizada a compra do supermercado, e começe outra!

Listinha é uma aplicação que permite que membros de uma família possam inserir produtos de casa que precisam ser comprados/repostos. A ideia é, quando um produto acaba, basta regista-lo na plataforma e emitir uma ordem de compra no carrinho da sua família, para que a pessoa responsável pelas compras possa ter acesso aos itens necessários mais rapidamente. Isso é bom, por exemplo, para pessoas que vão ao mercado após o trabalho não precisarem ir até em casa verificar todos os itens que faltam. Ou ter que entrar em contato com os integrantes da família questionando os itens a serem comrprados.

## Tech

Está aplicação utiliza das seguintes tecnologias, as quais serão instaladas automaticamente pelo Poetry:

- Python 3.10 - Linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.
- Django 4.2 - Framework web de alto nível escrito em Python, que adota o padrão model-template-view.
- Psycopg2 2.9.6 - Biblioteca de acesso ao banco de dados PostgreSQL.
- Django Rest Framework 3.14.0 - Biblioteca de padrões e ferramentas para a criação de APIs RESTful com Django.
- WhiteNoise 6.4.0 - Biblioteca para servir arquivos estáticos em aplicações web Django.
- Pillow 9.5.0 - Biblioteca que fornece uma interface para trabalhar com imagens.
- Django Rest Framework SimpleJWT 5.2.2 - Biblioteca para implementar autenticação JWT com Django Rest Framework.
- DRF Spectacular^0.26.2 - Biblioteca que fornece recursos para testar APIs desenvolvidas com Django REST Framework.
- Django CORS Headers 3.14.0 - Biblioteca para adicionar cabeçalhos CORS ao Django REST Framework.
- Requests 2.28.2 - Biblioteca para realizar requisições HTTP em Python.

## Instalação

### 1. Instale o PostgreSQL
Siga as instruções de instalação na página de download do PostgreSQL para o seu respectivo sistema operacional no link:
https://www.postgresql.org/download/

### 2. Crie um novo banco de dados
No PosgreSQL, crie um banco de dados. Lembre-se que o nome do projeto, o usuário e a senha desse banco serão necessários para configurar o arquivo settings.py do projeto django.

### 3. Configure o settings.py
No arquivo settings.py na pasta listinha, em 'DATABASES', coloque o nome do banco de dados em 'NAME', o usuário em 'USER' e a senha de acesso desse usuário em 'PASSWORD'. Salve, e feche.

### 4. Crie uma Secret Key
Acesso o site https://djecrety.ir/ para gerar uma secret key nova. Na pasta listinha_backend-main, crie um arquivo chamado .env, abra-o no seu editor de texto e coloque SECRET_KEY=suachavesecretasemaspas. Salve, e feche.

### 5. Instale o Poetry
Siga as instruções de instalação na página de documentação do Poetry para o seu respectivo sistema operacional no link:
https://python-poetry.org/docs/

### 6. Novo ambiente virtual, e instalação de dependências
Dentro da pasta listinha_backend-main, abra um terminal e digite o codigo para instalar todas as dependências do projeto:
```sh
poetry install
```
Para iniciar o ambiente:
```sh
poetry shell
```

### 7. Migrar o modelo ao banco de dados
No novo ambiente virtual do Poetry, digite o código:
```sh
python manage.py migrate
```

## Execução
Com a instalação e configurações concluídas, no terminal aberto na pasta listinha_backend-main, com o ambiente virtual do Poetry criado anteriormente aberto, digiteo código:
```sh
python manage.py runserver
```

A página de documentação pode ser acessada em _localhost:8000/api/swagger/_. Para outras urls disponíveis, verifique o arquivo urls.py na pasta do projeto django listinha.

Para conseguir acesso a maioria das APIs é necessário a geração de um token de acesso em /token/. Basta clicar em "Try it out", colocar um email e senha no Request Body, clicar em "Execute" o que criará um token de acesso e um de atualização (mais detalhes disponíveis na documentação da API). Copie o token de acesso gerado, e cole em "Authorize" na parte superior da documentação, e clique em Authorize novamente para que seja feita a autenticação. Feito isso, o usuário estará autenticado e pode utilizar das APIs.




[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
