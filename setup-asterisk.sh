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

echo "Setup complete. Edit /etc/asterisk/pjsip.conf and chan_mobile.conf to set your credentials."
