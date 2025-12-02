#!/bin/bash
set -e

apt-get update
apt-get install -y curl git

curl -LsSf https://astral.sh/uv/install.sh | sh

export PATH="/root/.local/bin:$PATH"

uv --version

uv tool install git+https://github.com/microsoft/amplifier@next

amplifier --version

amplifier collection add git+https://github.com/microsoft/amplifier-collection-toolkit@main
amplifier collection list
