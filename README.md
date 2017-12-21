PAM Face
========

PAM Face is a Linux Pluggable Authentication Module (PAM) for password-less face authentication using [OpenCV](https://opencv.org). Only a webcam is required.

Per default the password authentication is set as fallback. Two-factor authentication is also possible. The module has to be configured by the `pamface-conf` program.

Installation
------------

There are two ways of installing PAM Face: Installation of the stable or latest version. The stable version is distributed through the PM Code Works APT repository and is fully tested but does not contain the latest changes.

### Installation of the stable version

Add PM Codeworks repository

* Debian 8:

    `~# echo "deb http://apt.pm-codeworks.de jessie main" | tee /etc/apt/sources.list.d/pm-codeworks.list`

* Debian 9:

    `~# echo "deb http://apt.pm-codeworks.de stretch main" | tee /etc/apt/sources.list.d/pm-codeworks.list`

Add PM Codeworks key

    ~# wget -qO - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -
    ~# apt-get update

Install the packages

    ~# apt-get install libpam-face

### Installation of the latest version

The latest version contains the latest changes that may not have been fully tested and should therefore not be used in production. It is recommended to install the stable version.

Install required packages for building

    ~# apt-get install git devscripts

Clone this repository

    ~$ git clone https://github.com/philippmeisberger/pam-face.git

Build the package

    ~$ cd ./pam-face/
    ~$ dpkg-buildpackage -uc -us

Install the package

    ~# dpkg -i ../libpam-face*.deb

Install missing dependencies

    ~# apt-get install -f

Setup
-----

Enable PAM Face for a user

    ~# pamface-conf --add-user <username>

Test if everything works well

    ~# pamface-conf --check-user <username>

Questions and suggestions
-------------------------

If you have any questions to this project just ask me via email:

<team@pm-codeworks.de>
