Installation instructions
=========================

## Requirements ##

### Operating System ###

Mootiro Form should run fine on Linux (recommended), Unix and Mac OS. 

All development has been made under Linux, but deploying in Windows should work, if the required libraries are available.

### Python ###

Python 2.7 or higher is required. __Python 3 is not supported yet__

We recommend using virtualenv for installing the necessary libraries. On Ubuntu Natty, you can install them with `sudo apt-get install python-setuptools`

### Database ###

*  PostgreSQL 8 or 9 (recommended)
    *  Make sure to install the psycopg2 library. On Ubuntu Natty, you can install it with `sudo apt-get install python-psycopg2`
*  Sqlite 3

### Server ###

We recommend using Apache with mod\_wsgi, but theoretically, any server supporting [WSGI](http://wsgi.org) interface should do fine.

It can be installed on Ubuntu Natty with `sudo apt-get install apache2 libapache2-mod-wsgi`

## Installation ##

#### Download ####
1. Get Mootiro Form source code either on our [Download] page or on our GitHub repository

#### Create a Database ####
2. Create an empty database and accompanying user named `mootiro_form` for example:

For PostgreSQL:
    CREATE ROLE mootiro_form LOGIN ENCRYPTED PASSWORD 'my_password' NOINHERIT VALID UNTIL 'infinity';
    CREATE DATABASE mootiro_form OWNER mootiro_form ENCODING 'utf8' TEMPLATE template0;

#### Install Libraries ####
3. You can either download using python's setuptools utility (recommended) or from your package manager.

On Ubuntu Natty, you can install setuptools with `sudo apt-get install python-setuptools`.

If you proceed that way, you just have to type `sudo python setup.py develop` on mootiro form's folder


#### Configuration of .ini files ####
4. On mootiro\_form/src folder, there is a file called development.ini-dist. You should rename that file to development.ini and open it to check its settings. 

####   ####

1000000. Use default account to log in:

* Login: 'stravinsky@geniuses.ru'
* Password: 'igor'

## SMTP Server configuration ##


[Download]: http://mootiro.org/Download
