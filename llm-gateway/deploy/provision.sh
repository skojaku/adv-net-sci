#!/usr/bin/env bash
# Provision a fresh Debian/Ubuntu VM as the course LLM gateway.
#
#   scp -r llm-gateway root@smallvm:/opt/
#   ssh root@smallvm 'bash /opt/llm-gateway/deploy/provision.sh llm.example.edu'
#
# Idempotent: safe to re-run after editing the config or pulling new code.
set -euo pipefail

DOMAIN="${1:-}"
APP_DIR=/opt/llm-gateway
CONF_DIR=/etc/llm-gateway
STATE_DIR=/var/lib/llm-gateway

log() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

[[ $EUID -eq 0 ]] || { echo "run as root" >&2; exit 1; }
[[ -n $DOMAIN ]] || { echo "usage: provision.sh <public-hostname>" >&2; exit 1; }

log "packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip curl debian-keyring debian-archive-keyring apt-transport-https

if ! command -v caddy >/dev/null; then
	curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/gpg.key \
		| gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
	curl -fsSL https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt \
		> /etc/apt/sources.list.d/caddy-stable.list
	apt-get update -qq && apt-get install -y -qq caddy
fi

log "service account and directories"
id -u gateway &>/dev/null || useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin gateway
install -d -o gateway -g gateway -m 0750 "$STATE_DIR"
install -d -o root -g gateway -m 0750 "$CONF_DIR"

log "python environment"
python3 -m venv "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/pip" install -q --upgrade pip
"$APP_DIR/.venv/bin/pip" install -q -e "$APP_DIR"
chown -R gateway:gateway "$APP_DIR/.venv"

log "config and secrets"
# The real alias mapping and the provider keys are not in the repo; they are
# placed here by hand once and then left alone.
if [[ ! -f $CONF_DIR/config.yaml ]]; then
	cp "$APP_DIR/config.example.yaml" "$CONF_DIR/config.yaml"
	echo "!! $CONF_DIR/config.yaml is still the EXAMPLE mapping -- edit it before serving traffic"
fi
if [[ ! -f $CONF_DIR/env ]]; then
	cat >"$CONF_DIR/env" <<-EOF
		OLLAMA_API_KEY=
		OPENROUTER_API_KEY=
		GATEWAY_DB=$STATE_DIR/gateway.db
		GATEWAY_CONFIG=$CONF_DIR/config.yaml
	EOF
	echo "!! fill in the API keys in $CONF_DIR/env"
fi
chown root:gateway "$CONF_DIR/config.yaml" "$CONF_DIR/env"
chmod 0640 "$CONF_DIR/config.yaml" "$CONF_DIR/env"

log "systemd"
install -m 0644 "$APP_DIR/deploy/llm-gateway.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable llm-gateway.service

log "caddy"
sed "s/llm\.example\.edu/$DOMAIN/" "$APP_DIR/deploy/Caddyfile" >/etc/caddy/Caddyfile
install -d -o caddy -g caddy /var/log/caddy
systemctl reload caddy || systemctl restart caddy

log "firewall"
# Students reach 443. Nothing needs to reach the gateway port directly.
if command -v ufw >/dev/null; then
	ufw allow 22/tcp >/dev/null
	ufw allow 443/tcp >/dev/null
	ufw allow 80/tcp >/dev/null # ACME http-01
	ufw --force enable >/dev/null
fi

cat <<EOF

Provisioned. Remaining steps, in order:

  1. edit $CONF_DIR/config.yaml   (the real alias -> model mapping)
  2. fill  $CONF_DIR/env          (OLLAMA_API_KEY, OPENROUTER_API_KEY)
  3. sudo -u gateway env \$(grep -v '^#' $CONF_DIR/env | xargs) \\
       $APP_DIR/.venv/bin/gateway-admin check-config
  4. systemctl restart llm-gateway && systemctl status llm-gateway
  5. curl https://$DOMAIN/healthz

Then issue keys:
  gateway-admin issue-batch roster.csv > keys.csv
EOF
