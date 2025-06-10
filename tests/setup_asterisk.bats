#!/usr/bin/env bats

setup() {
  TMPDIR="$BATS_TEST_TMPDIR/testdir"
  mkdir -p "$TMPDIR/bin"
  cp "$BATS_TEST_DIRNAME/../setup-asterisk.sh" "$TMPDIR/"
  chmod +x "$TMPDIR/setup-asterisk.sh"
  mkdir -p "$TMPDIR/config"
  cp "$BATS_TEST_DIRNAME/../config/settings.sample" "$TMPDIR/config/settings.conf"
  cat > "$TMPDIR/asterisk20-install.sh" <<'EOM'
#!/bin/bash
echo "DEBIAN_INSTALL"
EOM
  chmod +x "$TMPDIR/asterisk20-install.sh"
  cat > "$TMPDIR/asterisk20-bookworm-pi-install.sh" <<'EOM'
#!/bin/bash
echo "PI_INSTALL"
EOM
  chmod +x "$TMPDIR/asterisk20-bookworm-pi-install.sh"
  cat > "$TMPDIR/bin/sudo" <<'EOM'
#!/bin/bash
echo "sudo $@" >> "$BATS_TEST_TMPDIR/sudo.log"
exit 0
EOM
  chmod +x "$TMPDIR/bin/sudo"
  PATH="$TMPDIR/bin:$PATH"
  SCRIPT="$TMPDIR/setup-asterisk.sh"
}

@test "prints usage with no arguments" {
  run "$SCRIPT"
  [ "$status" -eq 1 ]
  [[ "$output" == Usage:* ]]
}

@test "runs debian installer" {
  run "$SCRIPT" --debian
  [ "$status" -eq 0 ]
  [[ "$output" == DEBIAN_INSTALL* ]]
}

@test "runs pi installer" {
  run "$SCRIPT" --pi
  [ "$status" -eq 0 ]
  [[ "$output" == PI_INSTALL* ]]
}

@test "invokes sudo operations" {
  run "$SCRIPT" --debian
  [ "$status" -eq 0 ]
  grep -q "mkdir -p /var/lib/asterisk/agi-bin" "$BATS_TEST_TMPDIR/sudo.log"
  grep -q "apt-get install -y python3-pip python3-venv mariadb-server git" "$BATS_TEST_TMPDIR/sudo.log"
}
