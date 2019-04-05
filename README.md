Overview
========

This is a Django project for the SOS Web GUI and Plotting facilities. 
It relies on sosdb >=3, `django`, and `django-http-proxy` (install
via python pip is the easiest)..

Installation Dependencies
=========================
    "Development Tools"
    autoconf
    automake
    libtool
    python-devel (2.7)
    swig
    libevent-devel
    openssl-devel
    sosdb >= 3.4
    cmake
    httpd-devel (apache)
    mod_wsgi (libache2-mod-wsgi on ubuntu) - install with yum, pip will not install to correct directory
    numpy
    libyaml-devel
    Cython
    pip (Install the following with pip:)
	Django Version >= 1.10
	django-cors-headers
	pandas
	django-http-proxy


Configure sosgui/settings.py
=====================
Rename settings.py.example to settings.py
Add the host you want to  access the GUI from to:
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'example.com'
    ]
Edit SOS_ROOT to point to the directory of your SOS container(s)
    e.g. SOS_ROOT = "/home/SOS/"
Edit TIMEZONE to reflect your local time zone.
    e.g. for PST:
        TIMEZONE = -(8*3600)
    e.g. for PDT:
        TIMEZONE = -(7*3600)

Optional:
    Change location of sos_web_svcs log file. Default is sosgui.log

Install package from source
===========================
./autogen.sh
mkdir build
cd build
../configure --prefix=<default /var/www/sos_web_svcs>
make
make install

Create db for webserver
=======================
    python manage.py migrate
    python manage.py migrate --run-syncdb
    python manage.py createsuperuser
        Follow prompt to create admin user after running command
    
Deploy with Apache2/mod_wsgi
============================
    Example configuration template for Debian:
        apache2.conf
    Example configuration template for CentOS:
        httpd.conf
    Configure IP and file locations as needed for your machine.
    run ./manage.py collectstatic
