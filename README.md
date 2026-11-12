# Kibana Alerting to Discord

A small Python script that watches a Kibana JSON log file and forwards alert entries to a Discord webhook.

It uses [watchdog](https://pypi.org/project/watchdog/) to detect changes to the log file. On each change it reads the newest line. If that line's `log.logger` field matches the configured value, it posts the line's `message` to Discord, with any `Server log: ` prefix removed.

This pairs well with a Kibana rule that uses the **Server log** connector: Kibana writes the alert to its log, and this script relays it to Discord.

## Requirements

- Python 3.9+
- [watchdog](https://pypi.org/project/watchdog/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

```bash
pip install -r requirements.txt
```

## Configuration

The script loads its settings from `/opt/kibanaalerting/config.env`. To use a different location, edit the `load_dotenv(...)` path in `kibanaalert.py`.

```bash
sudo mkdir -p /opt/kibanaalerting
sudo cp config.env.example /opt/kibanaalerting/config.env
sudo chmod 600 /opt/kibanaalerting/config.env
```

| Variable | Description |
| --- | --- |
| `WEBHOOK_URL` | Discord webhook URL to send alerts to |
| `LOG_FILE_PATH` | Path to the Kibana JSON log file to watch |
| `TARGET_MESSAGE` | Value of `log.logger` that marks an alert entry |
| `APPLICATION_LOG_FILE_PATH` | Where the script writes its own logs |

## Usage

```bash
python3 kibanaalert.py
```

Stop it with `Ctrl+C` or `SIGTERM`.

### Running as a systemd service (optional)

```ini
# /etc/systemd/system/kibanaalert.service
[Unit]
Description=Kibana alert forwarder to Discord
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 /opt/kibanaalerting/kibanaalert.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now kibanaalert
```
