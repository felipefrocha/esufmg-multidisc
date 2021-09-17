SHELL = /bin/bash

install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

clear:
	@vagrant destroy -f

vms:
	@echo Up vagrant
	@vagrant up --no-provision

servers: vms
	@vagrant provision machine1 machine2 machine3

clients:
	@vagrant provision machine4 machine5 machine6

cp_files:
	@scp -r Project machine1:/home/vagrant/
	@scp -r Project machine2:/home/vagrant/
	@scp -r Project machine3:/home/vagrant/
	@scp -r Project machine4:/home/vagrant/
	@scp -r Project machine5:/home/vagrant/
	@scp -r Project machine6:/home/vagrant/