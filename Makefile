
all:

RELEASE_VERSION := $(shell git describe)

release:
	sed -i "" "s/^VERSION.*/VERSION = '${RELEASE_VERSION}'/" bbpgsql/option_parser.py
	# get version number from git describe
	# insert version number into binary
	# build pyinstaller
	# build .deb, passing in version number
