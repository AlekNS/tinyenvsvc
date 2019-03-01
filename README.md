Tiny Environment Service
========================



Installation
------------

### Vagrant

Works in the OS console (terminal).

Pre-requisites
---------------
1. [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtaulBox](https://www.virtualbox.org/wiki/Downloads).


Installation
-------------
1. `$ vagrant plugin install vagrant-vbguest` to install VM guest tools.
1. `$ vagrant up`
1. Wait, until it's finished. On successfully end it's displayed "Ready. Enjoy!"

Run
----
Go to the url in your browser: `http://192.168.10.112:8080`


### Docker

Pre-requisites
---------------
1. [Docker](https://docs.docker.com/install/)
1. [Docker Compose](https://docs.docker.com/compose/install/)


Installation
-------------
1. `$ docker-compose up -d`
1. Wait, until it's finished. On successfully end it's displayed "Ready. Enjoy!"


Run
----
Go to the url in your browser: `http://localhost:18080/`


Troubleshooting
----------------
