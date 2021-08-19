#!/bin/bash
set -x
mkdir -p /tmp/nomad
cp -r ~/Documents/projects/pessoal/hashicorp/nomad/esufmg-multidisc/nomad_vagrant/single_server /tmp/nomad
cd /tmp/nomad/single_server
sed -i -e 's/4096/3072/g' Vagrantfile
if [ ${1} = 2 ]; then
  vagrant up machine2 machine3 machine4;
else 
  vagrant up machine5 machine6;
fi
read -p "Press enter to continue"
exit 0