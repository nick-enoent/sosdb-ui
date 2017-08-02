Overview
========

This is a Django project for the SOS Web GUI and Plotting facilities. 
It relies on sosdb >=3, `django`, and `django-http-proxy` (install
via python pip is the easiest)..


Installation
============
Install Dependencies:
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
    pip (Install the following with pip:)
	Django Version >= 1.10
	django-cors-headers
	pandas
	matplotlib (python-matplotlib)
	django-http-proxy

Configure GUI for your machine
    Set aggregator/sampler hostname and numbers in static/js/config.js
    sosgui/settings.py:
        - SOS_ROOT location
		- location of ldmsd config file
		- IP Address/port number for bhttpd
		- Timezone (e.g. PST = -8)
		- Optional:
			Change file location of dynamic graph for plotting
			Change location of sos_web_svcs log file
    
Deploy with Apache2/mod_wsgi:
    Example configuration template for Debian:
        apache2.conf
    Example configuration template for CentOS:
        httpd.conf
    Configure IP and file locations as needed for your machine.
    run ./manage.py collectstatic
     


TODO
