#!/bin/bash

# Wrapper script to install Asterisk and deploy configuration/AGI files
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

usage() {
    echo "Usage: $0 [--debian | --pi]" >&2
    exit 1
}

if [ $# -ne 1 ]; then
    usage
fi

case "$1" in
    --debian)
        "$SCRIPT_DIR/asterisk20-install.sh"
        ;;
    --pi)
        "$SCRIPT_DIR/asterisk20-bookworm-pi-install.sh"
        ;;
    *)
        usage
        ;;
esac

# Deploy AGI scripts
echo "Copying AGI scripts to /var/lib/asterisk/agi-bin ..."
sudo mkdir -p /var/lib/asterisk/agi-bin
sudo cp -r "$SCRIPT_DIR"/agi-scripts/* /var/lib/asterisk/agi-bin/
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin

# Install Dynamic IVR with LLM integration
echo "Installing Dynamic IVR..."
sudo apt-get install -y python3-pip python3-venv mariadb-server git
if [ ! -d /var/lib/asterisk/agi-bin/asterisk-ivr ]; then
    sudo git clone https://github.com/Brownster/asterisk-ivr.git \
        /var/lib/asterisk/agi-bin/asterisk-ivr
fi
sudo chown -R asterisk:asterisk /var/lib/asterisk/agi-bin/asterisk-ivr
sudo pip3 install -r /var/lib/asterisk/agi-bin/asterisk-ivr/requirements.txt

# Create database for the IVR
echo "Setting up MariaDB database for IVR..."
sudo mysql <<'EOF'
CREATE DATABASE IF NOT EXISTS freepbx_llm;
CREATE USER IF NOT EXISTS 'freepbx_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON freepbx_llm.* TO 'freepbx_user'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "Setup complete. Edit /etc/asterisk/pjsip.conf and chan_mobile.conf to set your credentials."
