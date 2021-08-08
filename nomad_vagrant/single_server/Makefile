SHELL = /bin/bash

install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

clear:
	@ssh andromeda \
		"cd ~/Documents/projects/pessoal/hashicorp/nomad/esufmg-multidisc/nomad_vagrant/single_server && vagrant destroy -f"

vms:
	@echo Up vagrant
	@vagrant up --no-provision

servers: vms
	@vagrant provision machine1 machine2 machine3


		# -p 8300-8302:8300-8302 \
		# -p 8500-8502:8500-8502 \
		# -p 8600:8600 \

clients:
	@vagrant provision machine4 machine5 machine6

cp_files:
	@scp -r Project machine1:/home/vagrant/
	@scp -r Project machine2:/home/vagrant/
	@scp -r Project machine3:/home/vagrant/
	@scp -r Project machine4:/home/vagrant/
	@scp -r Project machine5:/home/vagrant/
	@scp -r Project machine6:/home/vagrant/

clear_all: clear
	@rm -rf .vagrant

consul_server:
	@docker run -d \
		--name consul \
		--network host \
		-v ./consul/data:/opt/consul/data \
		-v ./consul/config:/etc/consul.d/:ro\
		hashicorp/consul

single_server:
	@vagrant up machine1
	@ssh andromeda \
		"cd ~/Documents/projects/pessoal/hashicorp/nomad/esufmg-multidisc/nomad_vagrant/single_server && vagrant up machine2 machine3 machine4"
	# @vagrant up machine5 machine5 machine7