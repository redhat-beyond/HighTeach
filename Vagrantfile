Vagrant.configure("2") do |config|

  config.vm.box = "fedora/34-cloud-base"
  # config.vm.box_download_insecure = true
  config.vm.box_version = "34.20210423.0"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = "2"
  end
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.network(
    "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  )

  config.vm.provision "shell", path: "setup.sh", privileged: false
end
