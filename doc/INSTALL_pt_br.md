Instruções de Instalação
========================

## Requisitos ##

### Sistema Operacional ###

Mootiro Form deve funcionar sem problemas no Linux (recomendado), Unix e Mac OS.

Todo o desenvolvimento foi feito no Linux, mas a instalação no Windows deve funcionar, se as bibliotecas necessárias estiverem disponíveis.

### Python ###

É necessário Python 2.7 ou superior. __Python 3 ainda não é suportado.__

Nós usamos o gerenciador de pacotes de Python __setuptools__ para instalar as bibliotecas necessárias. No Ubuntu Natty, você pode instalar esse gerenciador de pacotes com o comando `sudo apt-get install python-setuptools`. 

Também recomendamos usar o virtualenv para instalar as bibliotecas necessárias em um ambiente Python isolado.

### Banco de Dados ###

*  PostgreSQL 8 or 9 (recomendado)
    *  Certifique-se de instalar a biblioteca psycopg2. No Ubuntu Natty, você pode instalá-la com `sudo apt-get install python-psycopg2`
*  Sqlite 3

### Servidor Web ###

Nós recomendamos Apache com mod\_wsgi, mas teoricamente qualquer servidor que suporte a interface [WSGI](http://wsgi.org) deve funcionar.

O Apache pode ser instalado no Ubuntu Natty com `sudo apt-get install apache2 libapache2-mod-wsgi`

Em nossas máquinas de desenvolvimento, usamos o servidor Paster, que é o padrão do framework web Pyramid, utilizado no desenvolvimento.

## Instalação ##

#### Download ####
Pegue o código fonte do MootiroForm em nosso repositório no GitHub ou em nossa página de [[Download]].

#### Criar o Banco de Dados ####
Crie um banco de dados vazuio no software de sua preferência:

Para o PostgreSQL:

    CREATE DATABASE mootiro_form OWNER mootiro_form ENCODING 'utf8' TEMPLATE template0;

#### Instalar Bibliotecas ####
Você pode instalar as bibliotecas utilizando o aplicativo setuptools do Python (recomendado) ou do gerenciador de pacotes de sua distribuição.

Se você utilizar o setuptools, para instalar o MootiroForm, você só precisa digitar `python setup.py develop` no diretório src/ do MootiroForm.


#### Configuração de arquivos .ini ####
No diretório mootiro\_form/src, há um arquivo chamado development.ini-dist. Você deve copiar esse arquivo para development.ini, abri-lo, lê-lo e configurar a aplicação.

Preste bastante atenção nos campos de configuração de e-mail. MootiroForm deve funcionar com qualquer servidor SMTP disponível.

#### Começando a utilizar ####
Para desenvolvimento, utilizamos o servidor Paster, que já vem no Pyramid. Ele é ligado utilizando este comando:

    paster serve development.ini

#### Testando a aplicação ####

Se você ativou a opção 'create test data', você terá uma conta padrão para
login:

* Login: 'stravinsky@geniuses.ru'
* Password: 'igor'


[Download]: http://mootiro.org/Download
