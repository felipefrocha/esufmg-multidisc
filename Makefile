SHELL = /bin/bash
.SHELLFLAGS = -evc


DOCKER_IMAGE = felipefrocha89/esufmg:multidisc
APP_FOLDER = ./application

install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

clear:
	@cd nomad_vagrant/single_server && make clear_ll
	@cd nomad_vagrant/ha_server && make clear_ll
	@cd nomad_vagrant/all_in_one && make clear_ll

single_server:
	@echo Up vagrant
	@cd nomad_vagrant/single_server && make consul_server && make single_server

run_local:
	@docker build -t ${DOCKER_IMAGE} ${APP_FOLDER}
	@docker run ${DOCKER_IMAGE}

test_listener:
	@docker build -t lixo listener_producer
	@cd listener_producer && docker run --name lixo --rm -i -v $${PWD}/files:/code/files -u $${UID}:$${GID} lixo


images:
	@docker build -t felipefrocha89/esufmg:multidisc-consumer applications/listener_consumer
	@docker build -t felipefrocha89/esufmg:multidisc-producer applications/listener_producer
	@docker build -t felipefrocha89/esufmg:multidisc-analyzis applications/run_analyze
	@docker push  felipefrocha89/esufmg:multidisc-consumer
	@docker push  felipefrocha89/esufmg:multidisc-producer
	@docker push  felipefrocha89/esufmg:multidisc-analyzis

run_solution: images
	@cd nomad_vagrant/single_server/nomad && nomad job run administer.nomad

clear_jobs:
	@for i in $$(nomad job status | grep city_ | cut -d' ' -f1); do nomad job stop --purge $$i; done