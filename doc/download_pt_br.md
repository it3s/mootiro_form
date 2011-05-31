Download
========

O código-fonte está disponível para download no [GitHub](https://github.com/it3s/mootiro_form). Você pode baixar o código-fonte via Git ou baixar um pacote TAR [aqui](https://github.com/it3s/mootiro_form/tarball/master)

## Requisitos ##

### Sistema Operacional ###

Mootiro Form deve funcionar sem problemas no Linux (recomendado), Unix e Mac OS. 

Todo o desenvolvimento foi feito em Linux então, se você quiser tentar usá-lo em Windows, faça por sua própria conta e risco.

### Python ###

Necessário Python 2.7 ou superior. __Python 3 ainda não é suportado__

Recomendamos usar o virtualenv para instalar as bibliotecas necessárias.

### Banco de Dados ###

*  PostgreSQL 8 ou 9 (recomendado)
    *  Certifique-se de instalar a biblioteca psycopg2. No Ubuntu Natty, você consegue instalá-la com `sudo apt-get install python-psycopg2`
*  Sqlite 3

### Servidor SMTP###

Mootiro Form deve funcionar sem problemas em qualquer servidor que suporte o protocolo SMTP.
Recomendamos o Postfix.
