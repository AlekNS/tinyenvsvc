#!/usr/bin/env sh

user=${1:-vagrant}


echo "Installing Docker and other tools"
apt-get install apt-transport-https ca-certificates
apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
echo 'deb https://apt.dockerproject.org/repo debian-jessie main' > /etc/apt/sources.list.d/docker.list

apt-get install -y apt-transport-https && apt-get update && apt-get install -y docker-engine curl pixz supervisor openjdk-7-jre


echo "Installing Docker Compose"
curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)" > /usr/local/bin/docker-compose && \
chmod +x /usr/local/bin/docker-compose

usermod -a -G docker ${user}


echo "Starting docker compose"
cd /var/www/tinyenvsvc
docker-compose build
docker-compose up -d
