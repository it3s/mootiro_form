Installation instructions
=========================

## Requirements ##

### Operating System ###

Mootiro Form should run fine on Linux (recommended), Unix and Mac OS.

All development has been made under Linux, but deploying in Windows should work, if the required libraries are available.

### Python ###

Python 2.7 or higher is required. __Python 3 is not supported yet.__

We use the Python package manager __setuptools__ to install Python libraries, called Python eggs. On Ubuntu Natty, you can install this package manager with `sudo apt-get install python-setuptools`. That makes the `easy_install` command available.

We also recommend using virtualenv for installing the necessary libraries in an isolated Python environment.

### Database options ###

*  PostgreSQL 8 or 9 (recommended)
    *  Make sure to install the psycopg2 library. On Ubuntu Natty, you can install it with `sudo apt-get install python-psycopg2`
*  Sqlite 3

### Web server ###

We recommend using Apache with mod\_wsgi, but theoretically, any server supporting the [WSGI](http://wsgi.org) interface should do fine.

Apache can be installed on Ubuntu Natty with `sudo apt-get install apache2 libapache2-mod-wsgi`

In our development machines we have been using the Python webserver Paster, which is the default in the Pyramid web framework used by Mootiro Form.

## Installation ##

#### Download ####
Get Mootiro Form source code either on our [Download] page or on our GitHub repository.

#### Create a Database ####
Create an empty database in your software of choice:

For PostgreSQL:

    CREATE DATABASE mootiro_form OWNER mootiro_form ENCODING 'utf8' TEMPLATE template0;

#### Install Libraries ####
You can either download using python's setuptools utility (recommended) or from your package manager.

On Ubuntu Natty, you can install setuptools with `sudo apt-get install python-setuptools`.

If you proceed that way, you just have to type `python setup.py develop` on mootiro form's folder.


#### Configuration of .ini files ####
On mootiro\_form/src folder, there is a file called development.ini-dist. You should copy that file to development.ini, open it, read it and configure the application.

Pay special attention to the fields of e-mail configuration. Mootiro Form can should work with any SMTP server available.

#### Starting the application ####
For development, we use the Paster web server, which comes bundled in Pyramid. It is invoked by this command:

    paster serve development.ini

#### Testing the application ####

If you have created test data, you will have a default account to log in:

* Login: 'stravinsky@geniuses.ru'
* Password: 'igor'


[Download]: http://mootiro.org/Download
