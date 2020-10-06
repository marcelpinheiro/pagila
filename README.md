# pagila

Este projeto utiliza a base de dados pagila, que pode ser encontrada em:
https://github.com/devrimgunduz/pagila

O projeto consiste em mapear, criar e persistir dados de um banco de dados Postgre (source/pagila) para MySQL (target)

* Os arquivos actor.py, city.py e film.py localizados na pasta sources são os mapeamentos das tabelas da database pagila
* O arquivo targets\__init__.py cria (caso ainda não exista) todas as tabelas mapeadas do banco Postgre (soruce/pagila) para o novo banco de dados MySQL.
* Por fim, em logic\populate encontram-se os códigos para a cópia dos dados para o novo banco MySQL
