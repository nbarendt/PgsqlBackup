Tutorial link:  http://www.debian.org/doc/manuals/maint-guide/index.en.html

Some packages needed or helpful (many more listed in the above guide):

build-essential
debhelper
dh-make
fakeroot
lintian - helps to verify a deb package
quilt - if you need to "patch" the upstream package, this helps manage a large set of patches.
git-buildpackage
pristine-tar
epm ??? - don't know yet if this will be useful

After doing some more reading, it seems that the wisdom is to NOT mingle the Debian package stuff with the original source or "upstream" repository.  Instead, the upstream repository should include its own build/install procedures, i.e. it should be able to generate a "source tarball" that could be untarred, configured and 'make installed'.  The makefile should be written with the $(DESTDIR) in front of its default install paths.  The debian package build will then create the installable files for the binary package in a fake root.


