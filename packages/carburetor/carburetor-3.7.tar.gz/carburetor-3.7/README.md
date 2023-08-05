# Carburetor

[![Translation status](https://hosted.weblate.org/widgets/carburetor/-/translations/svg-badge.svg)](https://hosted.weblate.org/engage/carburetor/?utm_source=widget)

This is a graphical settings app for tractor which is a package uses Python stem library to provide a connection through the onion proxy and sets up proxy in user session, so you don't have to mess up with TOR on your system anymore. 

## Install
In Debian based distros, make sure that you have `software-properties-common` package installed an then do as following:

    sudo add-apt-repository ppa:tractor-team/tractor
    sudo apt update
    sudo apt install carburetor

If you are using a distro other than Ubuntu, please check if the release name in the relevant file located in `/etc/apt/sources.list.d/` is a supported one (e.g. bionic).

If your distro is not Debian based or you don't want to use PPA, just copy `carburetor` file to `/usr/bin/` directory, but note that you will miss the updates and many desktop features. However you are welcome in contributing package build recepie of your distro to carburetor.

## Run
you can run `carburetor` by command line or through your desktop environment.
