
all:

# get version number from git describe
RELEASE_VERSION := $(shell git describe)

release:
	# insert version number into binary
	sed -i "s/^VERSION.*/VERSION = '${RELEASE_VERSION}'/" bbpgsql/option_parser.py
	# build pyinstaller
	./make_installer
	# build .deb, passing in version number
	./make_deb ${RELEASE_VERSION}
