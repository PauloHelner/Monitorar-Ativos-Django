# Monitorar Ativos da B3 em Django

## Funcionalidades:

- Realizar Cadastro e Login.
- Listar código, nome, preço do último fechamento, preço de abertura e preço atual de ativos da B3, com base no banco de dados do Yahoo Finance.
- Selecionar ativos para monitorar com frequência de até 1 minuto.
- Configurar valor de venda e de compra para o monitoramento de ativos.
- Receber e-mails de alerta sobre preço dos ativos.

## Imagens:

![image](https://github.com/PauloHelner/Monitorar-Ativos-Django/assets/74505147/2e5bf107-e2f6-4f59-acc2-8a3112650857)

## Funcionamento:

É feita consulta à API brapi, da qual são obtidos os códigos (tickers) dos ativos listados na B3. A partir daí, esses ativos são utilizados para fazer consultas à API YahooQuery, a qual possui uma frequência maior de atualização de dados que a API brapi.
Ao selecionar um ativo da lista para monitorar, este é salvo no banco de dados e representado por um card para o usuário. Uma thread nova é criada para realizar o monitoramento daquele ativo.

Obs:
> A página inicial faz diversas consultas à database do Yahoo, e pode levar alguns segundos para carregar

Obs:
> O envio de e-mails está implementado, entretanto, optou-se por não realizar o efetivo envio de e-mails por questão de segurança. Por esse motivo, os emails enviados são salvos no diretório /sent_emails. Para realizar o envio efetivo de e-mails, basta realizar as seguintes alterações no arquivo setting.py:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '********'
EMAIL_HOST_PASSWORD = '*******'
EMAIL_PORT = '2525'
```

## Instalação:

Execute os seguintes comandos no terminal:
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
