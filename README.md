Mootiro Form
============

Mootiro Form is a web application for web form creation, collection of entries and report generation.

Mootiro is a effort by [IT3S](www.it3s.org) to build web tools for NGOs. 

The license is BSD. See the file LICENSE.txt

Technical Instructions
======================

Mootiro Form is a web app built on top of Python, Pyramid, SQLAlchemy, Genshi, JQuery and other libraries.

Installation follows pretty much the same instructions as any pyramid web app.

Specific settings are covered in the INSTALL.txt file

Installation instructions
=========================

Requirements
============

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

### HTTP Server ###

We recommend using Apache with mod\_wsgi, but theoretically, any server supporting [WSGI](http://wsgi.org) interface should do fine.

It can be installed on Ubuntu Natty with `sudo apt-get install apache2 libapache2-mod-wsgi`

### SMTP Server ###

We tested under Postfix, but any SMTP-Compliant server should do fine.
