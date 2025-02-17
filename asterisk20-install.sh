#!/bin/bash

# Asterisk Installation Script for Debian 12
# This script automates the installation of Asterisk 20 LTS on Debian 12
# Author: [Your Name]
# Date: February 17, 2025
# License: MIT

# Exit on error
set -e

echo "Starting Asterisk installation on Debian 12..."

# Preparing the System Environment
echo "Step 1: Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y wget curl gnupg build-essential subversion
sudo apt install -y libedit-dev libssl-dev libjansson-dev libxml2-dev libsqlite3-dev

# Ensure system binaries are accessible
echo "Step 2: Ensuring correct PATH configuration..."
export PATH=$PATH:/sbin:/usr/sbin

# Removing AppArmor
echo "Step 3: Disabling and removing AppArmor..."
sudo systemctl stop apparmor
sudo apt remove -y apparmor

# Downloading and Compiling Asterisk
echo "Step 4: Downloading Asterisk source code..."
cd /usr/src
sudo wget http://downloads.asterisk.org/pub/telephony/asterisk/asterisk-20-current.tar.gz
sudo tar xvf asterisk-20-current.tar.gz
cd asterisk-20*/

# Installing Prerequisites
echo "Step 5: Running install_prereq script..."
sudo contrib/scripts/install_prereq install

# MP3 Support
echo "Step 6: Enabling MP3 support..."
sudo contrib/scripts/get_mp3_source.sh

# Configuring the Build
echo "Step 7: Configuring Asterisk build..."
sudo ./configure

# Note: Menuselect is skipped in automated installations, but you can uncomment this line to manually select modules
# sudo make menuselect

# Compilation and Installation
echo "Step 8: Building and installing Asterisk..."
sudo make
sudo make install
sudo make samples
sudo make config

# Configuring System Integration
echo "Step 9: Creating dedicated Asterisk user..."
sudo groupadd asterisk || echo "Group asterisk already exists"
sudo useradd -r -d /var/lib/asterisk -g asterisk asterisk || echo "User asterisk already exists"
sudo usermod -aG audio,dialout asterisk

# Setting Permissions
echo "Step 10: Setting proper directory permissions..."
sudo chown -R asterisk:asterisk /etc/asterisk
sudo chown -R asterisk:asterisk /var/{lib,log,spool}/asterisk
sudo chown -R asterisk:asterisk /usr/lib/asterisk

# Service Configuration
echo "Step 11: Configuring service settings..."
sudo bash -c 'cat > /etc/default/asterisk' << 'EOF'
AST_USER="asterisk"
AST_GROUP="asterisk"
EOF

sudo bash -c 'cat >> /etc/asterisk/asterisk.conf' << 'EOF'
runuser = asterisk
rungroup = asterisk
EOF

# Finalizing the Installation
echo "Step 12: Enabling and starting Asterisk service..."
sudo systemctl enable asterisk
sudo systemctl start asterisk

# Verifying Operation
echo "Step 13: Verifying Asterisk operation..."
echo "To connect to the Asterisk CLI, run: sudo asterisk -rvvv"
echo "You should see output similar to:"
echo "Asterisk 20.X.X, Copyright (C) 1999 - 2025 Sangoma, Inc."
echo "Connected to Asterisk 20.X.X currently running on debian12"

echo "Asterisk installation completed successfully!"
echo "For post-installation configuration, refer to the Asterisk documentation."
