SHELL = /bin/bash
.SHELLFLAGS = -evc

machine_id ?= 2

export NOMAD_ADDR=http://nomad.server.local:4646

install:
	@echo Installing Libvirt QEMU e KVM
	@sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virtinst virt-manager
	@sudo systemctl enable libvirtd
	@sudo systemctl start libvirtd
	@sudo usermod -aG libvirt $$USER && sudo usermod -aG kvm $$USER

##
# DOCKER COMMANDS
##
images: ## Create all images
	@docker build -t felipefrocha89/esufmg:multidisc-consumer applications/listener_consumer
	@docker build -t felipefrocha89/esufmg:multidisc-producer applications/listener_producer
	@docker build -t felipefrocha89/esufmg:multidisc-analyzis applications/run_analyze
	@docker push  felipefrocha89/esufmg:multidisc-consumer
	@docker push  felipefrocha89/esufmg:multidisc-producer
	@docker push  felipefrocha89/esufmg:multidisc-analyzis

test_listener:
	@docker build -t lixo listener_producer
	@cd listener_producer && docker run --name lixo --rm -i -v $${PWD}/files:/code/files -u $${UID}:$${GID} lixo

##
# SERVERS COMMANDS
##
single_server:
	@echo "Up Vagrant - Single Server & Three Clients initialization"
	@cd vagrant/single_server && make consul_server && make single_server
	@terminator -T "Administer" -e "make run_solution && exit 0"
	@terminator -T "Administer" -e "make start_application && exit 0"

##
# NOMAD COMMANDS
##
run_solution: images
	@until nomad status; do echo "Waiting Nomad Server" && sleep 60; done;
	@make base_jobs
	@until ssh machine1 "cd /mnt/nfs_share/mapas" > /dev/null; do echo "Waiting Folder creation" && sleep 60; done;
	@cd nomad_jobs && nomad job run administer.nomad

base_jobs:
	@nomad job run nomad_jobs/sre/fabio.nomad
	@nomad job run nomad_jobs/sre/monitoring.nomad

##
# APPLICATION COMMANDS
##
start_application:
	@until ssh machine1 "cd /mnt/nfs_share" > /dev/null; do echo "Waiting NFS" && sleep 60; done;
	@ssh machine1 "cd /mnt/nfs_share \
		&& sudo mkdir -p cidades_info cidades_raiz saidas/cidades_temp_result saidas/cidades_temp_imagens mapas \
		&& sudo chmod -R 777 cidades_info cidades_raiz mapas saidas"
	@scp -r data/mapas machine1:/mnt/nfs_share
	@scp -r data/saidas machine1:/mnt/nfs_share
	@scp -r data/cidades_raiz machine1:/mnt/nfs_share
	@until (nomad status administer | grep healthy); do echo "Waiting administer job"; sleep 15; done;
	@nomad node-status
	@nomad status administer
	
copy_files:
	@scp -r data/cidades_info/*.csv machine${machine_id}:/mnt/nfs_clientshare/cidades_info/

clear_process_jobs: clear_files
	@for i in $$(nomad job status | grep city_ | cut -d' ' -f1); do nomad job stop --purge $$i; done

clear_all_jobs:
	@for i in $$(nomad job status | grep -v "ID" | cut -d' ' -f1); do nomad job stop --purge $$i; done

clear_files:
	@ssh machine1 "sudo rm -rf /mnt/nfs_share/cidades_info/*.csv"
	@ssh machine1 "sudo rm -rf /mnt/nfs_share/saidas/**/*.csv"


clear:
	@cd vagrant/single_server && make clear_all
	# @cd vagrant/ha_server && make clear_all
	# @cd vagrant/all_in_one && make clear_all