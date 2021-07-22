# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo "Installing Docker..."
sudo apt-get update
sudo apt-get remove docker docker-engine docker.io
echo '* libraries/restart-without-asking boolean true' | sudo debconf-set-selections
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg |  sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
      "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"
sudo apt-get update
sudo apt-get install -y docker-ce
# Restart docker to make sure we get the latest version of the daemon if there is an upgrade
sudo service docker restart
# Make sure we can actually use docker as the vagrant user
sudo usermod -aG docker vagrant
sudo docker --version

# Packages required for nomad & consul
sudo apt-get install unzip curl vim -y

echo "Install Hashicorp key"
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
echo "Installing Nomad..."
sudo apt-get update && sudo apt-get install -y nomad
echo "Installing Consul..."
sudo apt-get install -y consul

(
cat <<-EOF
[Unit]
Description="HashiCorp Consul - A service mesh solution"
Documentation=https://www.consul.io/
Requires=network-online.target
After=network-online.target
ConditionFileNotEmpty=/etc/consul.d/consul.hcl

[Service]
Type=notify
User=consul
Group=consul
ExecStart=/usr/bin/consul agent -config-dir=/etc/consul.d/
ExecReload=/bin/kill --signal HUP $MAINPID
KillMode=process
KillSignal=SIGTERM
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

EOF
) | sudo tee /etc/systemd/system/consul.service
sudo systemctl daemon-reload
(
cat <<-EOF
datacenter = "rocha"

data_dir = "/opt/consul"

client_addr = "0.0.0.0"

ui_config {
  enabled = true
}

server = true

bind_addr = "[::]" # Listen on all IPv6
bind_addr = "0.0.0.0" # Listen on all IPv4

advertise_addr = "192.168.15.71"

bootstrap_expect=1
EOF
) | sudo tee /etc/consul.d/consul.hcl

sudo systemctl enable consul.service
sudo systemctl start consul

for bin in cfssl cfssl-certinfo cfssljson
do
  echo "Installing $bin..."
  curl -sSL https://pkg.cfssl.org/R1.2/${bin}_linux-amd64 > /tmp/${bin}
  sudo install /tmp/${bin} /usr/local/bin/${bin}
done

(
cat <<-EOF
data_dir  = "/opt/nomad/data"
bind_addr = "0.0.0.0"

datacenter  = "rocha"
region      = "minasgerais"

server {
  #license_path = "/etc/nomad.d/nomad.hcl"
  enabled = true
  bootstrap_expect = 1
}

client {
  enabled = true
  network_interface = "eth1"
  servers = ["127.0.0.1:4646"]
}

advertise {
  http = "192.168.15.7${MACHINE_ID}"
  rpc  = "192.168.15.7${MACHINE_ID}"
  serf = "192.168.15.7${MACHINE_ID}:5648"
}

consul {
 address = "192.168.15.7${MACHINE_ID}:8500"
}

EOF
) | sudo tee /etc/nomad.d/nomad.hcl

nomad -autocomplete-install

(
cat <<-EOF
NOMAD_ADDR=http://192.168.15.7${MACHINE_ID}:4646
EOF
) | sudo tee /etc/profile.d/nomad.sh

sudo systemctl enable nomad 
sudo systemctl start nomad

SCRIPT

Vagrant.configure(2) do |config|
  # config.vm.box = "bento/ubuntu-18.04" # 18.04 LTS
  config.vm.box         = "generic/ubuntu2004"
  config.vm.box_check_update = true

  N=1
  (1..N).each do |machine_id|
    # Variable 
    # default_router = "192.168.15.1"

    config.vm.define "machine#{machine_id}" do |machine|
    machine.vm.hostname = "nomad#{machine_id}"
      # machine.vm.network "private_network", ip: "192.168.121.1"
      machine.vm.network "public_network", ip: "192.168.15.#{70+machine_id}", bridge: "eno1"
      # Define machine size
      machine.vm.provider "virtualbox" do |vb|
        vb.memory = "4096"
        vb.cpus = 2
        vb.customize ["modifyvm", :id, "--cpuexecutioncap", "#{100/N}"]
      end 
      # machine.vm.provision :shell, :inline => "ip route delete default 2>&1 >/dev/null || true; ip route add default via #{default_router}"
      machine.vm.provision "shell", 
        inline: $script, 
        env: { "MACHINE_ID" => "#{machine_id}" },
        privileged: false
    end
  end
  
  # Expose the nomad api and ui to the host
  # config.vm.network "forwarded_port", guest: 4646, host: 4646, auto_correct: true, host_ip: "127.0.0.1"

end
