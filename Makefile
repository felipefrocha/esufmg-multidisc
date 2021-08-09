install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

clear:
	@cd nomad_vagrant/single_server; vagrant destroy -f
	@cd nomad_vagrant/ha_server; vagrant destroy -f
	@cd nomad_vagrant/all_in_one; vagrant destroy -f

single_server:
	@echo Up vagrant
	@cd nomad_vagrant/single_server && make consul_server && vagrant up --provision

cp_files:
	@scp -i nomad_vagrant/${FOLDER}/.vagrant/machines/machine1/virtualbox/private_key -r ./Project/docker vagrant@192.168.15.71:/mnt/nfs_share/

