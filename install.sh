#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
    echo "Run this installer as root: sudo bash install.sh" >&2
    exit 1
fi

if ! command -v apt-get >/dev/null 2>&1; then
    echo "This installer supports Debian/Ubuntu VPS hosts with apt." >&2
    exit 1
fi

if ! command -v systemctl >/dev/null 2>&1; then
    echo "systemd is required to install MineHosting as a service." >&2
    exit 1
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "${SCRIPT_DIR}/app.py" || ! -f "${SCRIPT_DIR}/requirements.txt" ]]; then
    echo "Run install.sh from the MineHosting project directory." >&2
    exit 1
fi

read -r -p "Admin username [admin]: " ADMIN_USERNAME
ADMIN_USERNAME="${ADMIN_USERNAME:-admin}"
if [[ ! "${ADMIN_USERNAME}" =~ ^[a-zA-Z0-9_.-]{1,80}$ ]]; then
    echo "Username may contain only letters, numbers, dots, underscores, and hyphens." >&2
    exit 1
fi

apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip

if ! id -u minehosting >/dev/null 2>&1; then
    useradd --system --home-dir /opt/minehosting --shell /usr/sbin/nologin minehosting
fi

install -d -o minehosting -g minehosting -m 0750 /opt/minehosting
install -d -o minehosting -g minehosting -m 0750 /var/lib/minehosting
install -o minehosting -g minehosting -m 0640 "${SCRIPT_DIR}/app.py" /opt/minehosting/app.py
install -o minehosting -g minehosting -m 0640 "${SCRIPT_DIR}/requirements.txt" /opt/minehosting/requirements.txt

python3 -m venv /opt/minehosting/venv
/opt/minehosting/venv/bin/pip install --disable-pip-version-check -r /opt/minehosting/requirements.txt

ADMIN_PASSWORD="$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')"
SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
umask 077
cat > /etc/minehosting.env <<EOF
ADMIN_USERNAME=${ADMIN_USERNAME}
ADMIN_PASSWORD=${ADMIN_PASSWORD}
SECRET_KEY=${SECRET_KEY}
DATABASE_PATH=/var/lib/minehosting/status.db
PORT=2000
COOKIE_SECURE=0
EOF
chown root:minehosting /etc/minehosting.env
chmod 0640 /etc/minehosting.env

cat > /etc/systemd/system/minehosting.service <<'EOF'
[Unit]
Description=MineHosting website and status page
After=network.target

[Service]
Type=simple
User=minehosting
Group=minehosting
WorkingDirectory=/opt/minehosting
EnvironmentFile=/etc/minehosting.env
ExecStart=/opt/minehosting/venv/bin/gunicorn --workers 2 --bind 0.0.0.0:2000 --timeout 30 app:app
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/minehosting

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now minehosting.service

echo
echo "MineHosting is installed and running."
echo "Website:     http://YOUR_SERVER_IP:2000/"
echo "Status page: http://YOUR_SERVER_IP:2000/status"
echo "Admin:       http://YOUR_SERVER_IP:2000/admin"
echo "Username:    ${ADMIN_USERNAME}"
echo "Password:    ${ADMIN_PASSWORD}"
echo
echo "Save this password now. For public production use, put HTTPS in front of the service"
echo "and set COOKIE_SECURE=1 in /etc/minehosting.env, then restart minehosting.service."
