Install Mootiro Form on Ubuntu Natty
====================================

== Requirements ==

This tutorial assumes:
*  PostgreSQL 8 or 9
*  Apache 2 and mod\_wsgi
*  Python 2.7 and virtualenv for deploying the libraries
*  Git for downloading the latest version from our repository

== Installing all needed libraries ==

*  PostgreSQL: `sudo apt-get install postgresql`
*  Apache:     `sudo apt-get install apache2 libapache2-mod-wsgi`
*  Python libraries: `sudo apt-get install python-psycopg2 python-virtualenv`
*  Git:        `sudo apt-get install git`

== Configuring PostgreSQL User ==

Open a terminal (gnome-terminal will do fine) and then type:

    sudo su postgres
    createuser -I -d -S -R -W myuser

You will be prompted to type a password. We are using 'mypassword', feel free to use whatever you like.
Now, let's create the database. Its name is mootiro\_form:

    createdb -T template0 -E utf8 -O myuser mootiro_form 
    exit

== Setup a Virtual Environment ==

Mootiro form uses a plethora of frequently updated and not thoroughly used Python libraries, so we will contain them in a virtual environment.
With the Virtual Environment, only Mootiro Form will use those libraries, leaving the rest of your system untouched.

Back to the terminal:
    cd /var/local
    sudo mkdir wsgi
    cd wsgi
    sudo virtualenv --no-site-packages venv
    sudo nano venv/mootiro_form.wsgi

Then, on Nano, paste the following text:
    
    from pyramid.paster import get_app
    application = get_app('/var/local/mootiro_form/src/development.ini', 'main')

Save and exit.

== Configure Apache ==

    cd /etc/apache2/sites-available
    sudo nano mootiro

And then, paste the following text:

    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    WSGIPythonHome /var/local/wsgi/venv/lib/python2.7/site-packages
    WSGIDaemonProcess pyramid user=www-data group=www-data processes=1 \
       threads=4 \
       python-path=/var/local/wsgi/venv/lib/python2.7/site-packages
    WSGIScriptAlias /mform /var/local/wsgi/venv/mootiro_form.wsgi
    
    <Directory /var/local/wsgi/venv>
      WSGIProcessGroup pyramid
      Order allow,deny
      Allow from all
    </Directory>

Exit nano, then type:

    sudo a2ensite mootiro
    sudo /etc/init.d/apache2 reload



== Downloading Mootiro Form ==

Right now, you can either download a pre-packaged version from the website or you can download the bleeding edge version from the git repositories. We are downloading trough the git repositories. On a shell, type:

    git clone git@it3s.org:formcreator

Now, go to `formcreator/src` directory and type:

    cp development.ini-dist development.ini
    nano development.ini

Now, change the settings on 

    
