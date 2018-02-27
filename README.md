PAM Face
========

PAM Face is a Linux Pluggable Authentication Module (PAM) for password-less face authentication using [OpenCV](https://opencv.org). Only a webcam is required.

Per default the password authentication is set as fallback. Two-factor authentication is also possible. The module has to be configured by the `pamface-conf` program.

Installation
------------

Please note that PAM Face is currently in development.

### Prequisites
PAM Face is not compatible with OpenCV 3.1 as there is a bug that has been fixed in a later version: <http://answers.opencv.org/question/82294/cant-get-predict-confidence/>

You will get the error: `'int' object has no attribute '__getitem__'`

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

    ~$ pamface-conf --check-user <username>

Questions and suggestions
-------------------------

If you have any questions to this project just ask me via email:

<team@pm-codeworks.de>
