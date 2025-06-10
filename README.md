# asterisk-install
Collection of scripts and configuration files for building Asterisk.

## Scripts

- `asterisk20-install.sh` – Install Asterisk 20 on Debian 12.
- `asterisk20-bookworm-pi-install.sh` – Install Asterisk 20 on Raspberry Pi OS Bookworm.

## Configuration

After running one of the install scripts, copy the example configuration files to `/etc/asterisk`:

```bash
sudo cp config/*.conf /etc/asterisk/
```

Edit `/etc/asterisk/pjsip.conf` and replace the placeholder values:

- Set the password fields under `[yealink-auth]` and `[zoiper-auth]` to match the credentials used by your Yealink phone and Zoiper softphone.
- Provide your SIPGate account information in `[sipgate-trunk]` and `[sipgate-auth]` (username, password and client URI).

Make sure your phones register with the usernames defined in these sections (`yealink-t42s` and `zoiper`).
