# asterisk-install
Collection of scripts and configuration files for building Asterisk.

## Scripts

- `asterisk20-install.sh` – Install Asterisk 20 on Debian 12.
- `asterisk20-bookworm-pi-install.sh` – Install Asterisk 20 on Raspberry Pi OS Bookworm.
- `setup-asterisk.sh` – Wrapper that installs Asterisk and deploys the sample files.

## Installation

First copy `config/settings.sample` to `config/settings.conf` and edit the values for
your phones, SIP trunk and Bluetooth settings. Then run the wrapper script with `sudo`
and specify the target system:

```bash
sudo ./setup-asterisk.sh --debian   # Debian based systems
sudo ./setup-asterisk.sh --pi       # Raspberry Pi OS
```

The script installs Asterisk 20, copies the configuration files to `/etc/asterisk`,
places the AGI scripts under `/var/lib/asterisk/agi-bin`, and deploys the
Dynamic IVR project with its dependencies.

## Configuration

All configuration values are stored in `config/settings.conf`. Update this file with the
credentials for your phones, SIP trunk and Bluetooth trunk before running the installer.

### Finding Bluetooth Details

The installer expects the MAC address of your USB Bluetooth adapter and the phone you
plan to use as a trunk. Discover the adapter address with either command:

```bash
hcitool dev          # list adapters
# or
bluetoothctl list    # alternative command
```

Use the displayed address for `ADAPTER_MAC`. To determine the phone's MAC address and
RFCOMM port, connect the device and run:

```bash
sudo asterisk -rx "mobile search"
```

Note the values shown in the output and assign them to `MOBILE_MAC` and `MOBILE_PORT`
in `config/settings.conf`.

## Running the IVR

The demo IVR script is installed as `/var/lib/asterisk/agi-bin/ivr/demo_ivr.py` and is invoked by extension `250` in `extensions.conf`. Dial `250` from one of the configured phones to test it. The IVR configuration files can be found in `/var/lib/asterisk/agi-bin/ivr/config`.

### Dynamic IVR with LLM

This repository's setup script also deploys Brownster's [Dynamic IVR with LLM Integration](https://github.com/Brownster/asterisk-ivr).
The project is cloned to `/var/lib/asterisk/agi-bin/asterisk-ivr` and the Python
dependencies are installed automatically. A local MariaDB database named
`freepbx_llm` is created along with a `freepbx_user` account whose password is
set from `DB_PASSWORD` in `config/settings.conf`. Update the credentials in
`asterisk-ivr/config/db_config.yml.yaml` if needed.

The new IVR can be tested by dialing extension `260` once the installation
completes.
