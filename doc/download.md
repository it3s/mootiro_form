Download
========

The source code is available on [GitHub](https://github.com/it3s/mootiro_form), you can either download the source code via Git or download a TAR package [here](https://github.com/it3s/mootiro_form/tarball/master)

##Requirements ##

### Operating System ###

Mootiro Form should run fine on Linux (recommended), Unix and Mac OS. 

All development has been made under Linux, so, if you want to try on Windows, you're on your own.  

### Python ###

Python 2.7 or higher is required. __Python 3 is not supported yet__

We recommend using virtualenv for installing the necessary libraries.

### Database ###

*  PostgreSQL 8 or 9 (recommended)
    *  Make sure to install the psycopg2 library. On Ubuntu Natty, you can install it with `sudo apt-get install python-psycopg2`
*  Sqlite 3

### SMTP Server ###

Mootiro Form should run fine on any server supporting the SMTP protocol.
We recommend using Postfix.
