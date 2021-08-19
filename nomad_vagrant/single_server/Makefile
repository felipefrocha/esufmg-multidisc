SHELL = /bin/bash

export NOMAD_ADDR=http://192.168.15.71:4646

install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

# vms:
# 	@echo Up vagrant
# 	@vagrant up 

# servers: vms
# 	@vagrant provision machine1 machine2 machine3

# clients:
# 	@vagrant provision machine4 machine5 machine6

# cp_files:
# 	@scp -r Project machine1:/home/vagrant/
# 	@scp -r Project machine2:/home/vagrant/
# 	@scp -r Project machine3:/home/vagrant/
# 	@scp -r Project machine4:/home/vagrant/
# 	@scp -r Project machine5:/home/vagrant/
# 	@scp -r Project machine6:/home/vagrant/


clear_client2:
	@terminator -T "Client 2" -e "ssh pegasus 'bash -s' < vagrantdown.sh"

clear_client1:
	@terminator -T "Client 1" -e "ssh andromeda 'bash -s' < vagrantdown.sh"

clear:
	@vagrant destroy -f

clear_all: clear
	@rm -rf .vagrant
	@make clear_client2 clear_client1

consul_server:
	@docker container rm -f $$(docker container ls -aq) || echo ""
	@docker run -d \
		--name consul \
		--net=host \
		-v $$PWD/consul/data:/opt/consul/data \
		-v $$PWD/consul/config:/etc/consul.d:ro\
		-p 8300-8302:8300-8302 \
		-p 8500-8502:8500-8502 \
		-p 8600:8600 \
		consul agent -config-dir /etc/consul.d


client1:
	@terminator -T "Cliente 1" -e "ssh andromeda 'bash -s' < vagrantup.sh 2 && exit 0"

client2:
	@terminator -T "Cliente 2" -e "ssh pegasus 'bash -s' < vagrantup.sh 3 && exit 0"

single_server: client1 
	@vagrant up  machine1

provision:
	@cd provisioning/ansible && ansible-playbook -i hosts main.yml

base_job:
	@cd nomad && or i in $$(ls | grep .nomad);do nomad job run $i;done;


	