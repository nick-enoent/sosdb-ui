ACLOCAL_AMFLAGS = -I m4

SUBDIRS = sosgui \
	static \
	templates \
	sos_db \
	jobs \
	component \
	container \
	objbrowser \
	sosdb_auth

main_PYTHON = manage.py
maindir = ${prefix}/

main_pkgdata_DATA = README.md
main_pkgdatadir = ${prefix}/

EXTRA_DIST = autogen.sh COPYING $(main_pkgdata_DATA)

#rpm:
#	mkdir -p $@/{BUILD, BUILDROOT, RPMS, SOURCES, SPECS, SRPMS}
#	cp $(distdir).tar.gz $@/SOURCES
#	cp sos_web_svcs.spec $@/SPECS
#	rpmbuild --buildroot 'pwd'


