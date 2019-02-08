# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.hostname = "vtinyenvsvc.vm"
  config.vm.box      = "debian/stretch64"

  config.vm.network :private_network, ip: "192.168.101.112"
  config.vm.network :forwarded_port, guest: 18443, host: 8443
  config.vm.network :forwarded_port, guest: 18080, host: 8080

  config.vm.synced_folder ".", "/var/www/tinyenvsvc", type: "virtualbox"
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.provision :shell, :path => "scripts/vagrant_provision.sh", :args => ["vagrant"]
end
