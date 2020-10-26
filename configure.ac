#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.69])
AC_INIT([sosdb-ui], 4.0.0, nick@ogc.us)
AC_CONFIG_MACRO_DIR([m4])
AM_CONFIG_HEADER(config.h)
AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([3.6])

distdir=${PACKAGE_NAME}-${PACKAGE_VERSION}
AC_SUBST(ac_configure_args)
AC_SUBST(prefix)
AC_SUBST(distdir)

AC_CONFIG_FILES([
        Makefile
        sosgui/Makefile
        sos_db/Makefile
        objbrowser/Makefile
        container/Makefile
        jobs/Makefile
        sosdb_auth/Makefile
        static/Makefile
        static/css/Makefile
        static/img/Makefile
        static/js/Makefile
        static/js/DataTables-1.10.5/Makefile
        static/js/jquery-ui-1.11.2/Makefile
        static/js/DataTables-1.10.5/media/Makefile
        static/js/DataTables-1.10.5/media/css/Makefile
        static/js/DataTables-1.10.5/media/images/Makefile
        static/js/DataTables-1.10.5/media/js/Makefile
        static/js/jstree-3.3.3/Makefile
        static/js/jstree-3.3.3/themes/Makefile
        static/js/jstree-3.3.3/themes/default/Makefile
        templates/Makefile
        templates/container/Makefile
        templates/jobs/Makefile
        templates/objbrowser/Makefile
        templates/registration/Makefile
        ])
AC_OUTPUT
