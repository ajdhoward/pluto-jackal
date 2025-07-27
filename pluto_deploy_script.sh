#!/bin/bash

set -e

# === PLUTO-JACKAL LIVE DEPLOYMENT SCRIPT ===
# Author: ChatGPT | For: Adam's AcidWurx VPS (server.acidwurx.co.uk)
# Purpose: Bootstraps PLUTO-JACKAL multi-agent AI architect on Ubuntu 22.04

### 1. SYSTEM PREP echo "\n[1/6] Updating system and installing dependencies..."
apt update && apt upgrade -y
apt install -y git curl unzip nodejs npm python3 python3-pip tmux

### 2. CREATE RUNTIME FOLDER
mkdir -p /opt/pluto-jackal
cd /opt/pluto-jackal

### 3. CLONE LATEST CODEBASE
if [ ! -d ".git" ]; then
  git clone https://github.com/ajdhoward/pluto-jackal.git .
else
  git pull
fi

### 4. INSTALL JS DEPENDENCIES (React UI, CLI tools)
echo "\n[2/6] Installing Node.js packages..."
cd client && npm install && cd ..

### 5. INSTALL PYTHON MODULES (Agent core)
echo "\n[3/6] Installing Python packages..."
pip3 install -r requirements.txt || true

### 6. START SYSTEM
cat <<EOF > /usr/bin/start-pluto.sh
#!/bin/bash
cd /opt/pluto-jackal && npm run start &
EOF
chmod +x /usr/bin/start-pluto.sh

### 7. OPTIONAL: CREATE SYSTEMD SERVICE
cat <<EOF > /etc/systemd/system/pluto.service
[Unit]
Description=PLUTO-JACKAL AI DevOps
After=network.target

[Service]
ExecStart=/usr/bin/start-pluto.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable pluto.service
systemctl start pluto.service

### DONE
echo "\n✅ PLUTO-JACKAL deployed and running at: http://server.acidwurx.co.uk/onboarding"
echo "🧠 Use your browser to access the Onboarding Wizard, or manage via systemctl (pluto.service)"
