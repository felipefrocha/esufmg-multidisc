#!/bin/bash
set -e
cd /tmp/nomad/single_server
ls
vagrant destroy -f && sudo rm -rf /tmp/nomad/single_server
exit 0