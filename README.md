# asterisk-install
Collection of scripts and configuration files for building Asterisk.

## Scripts

- `asterisk20-install.sh` – Install Asterisk 20 on Debian 12.
- `asterisk20-bookworm-pi-install.sh` – Install Asterisk 20 on Raspberry Pi OS Bookworm.
- `setup-asterisk.sh` – Wrapper that installs Asterisk and deploys the sample files.

## Installation

Run the wrapper script with `sudo` and specify the target system:

```bash
sudo ./setup-asterisk.sh --debian   # Debian based systems
sudo ./setup-asterisk.sh --pi       # Raspberry Pi OS
```

The script installs Asterisk 20, copies the configuration files to `/etc/asterisk` and places the AGI scripts under `/var/lib/asterisk/agi-bin`.

## Configuration

Edit `/etc/asterisk/pjsip.conf` and replace the placeholder values:

- Update the passwords in `[yealink-auth]` and `[zoiper-auth]` to match your phone credentials.
- Provide your SIPGate account details in `[sipgate-trunk]` and `[sipgate-auth]` (`client_uri`, `username`, `password`).

Edit `/etc/asterisk/chan_mobile.conf` and set the Bluetooth adapter and mobile phone addresses for your environment.

After modifying the files, reload the Asterisk service so the changes take effect.

## Running the IVR

The demo IVR script is installed as `/var/lib/asterisk/agi-bin/ivr/demo_ivr.py` and is invoked by extension `250` in `extensions.conf`. Dial `250` from one of the configured phones to test it. The IVR configuration files can be found in `/var/lib/asterisk/agi-bin/ivr/config`.
