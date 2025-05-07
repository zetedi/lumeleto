# Installing Conda on Mac

To install conda on your Mac, follow these steps:

1. Go to the [Conda website](https://docs.conda.io/en/latest/miniconda.html) and download the latest version of Miniconda for MacOS.
2. Follow the installation instructions to install Miniconda.
3. Once installed, open a new terminal window and type `conda --version` to check that conda has been successfully installed.


conda env create -f lumeleto_environment.yml
conda activate lumeleto
pip install -r requirements_full.txt 
python -m dotenv run -- python lumeleto_mastodon_bridge.py


docker run -d --restart unless-stopped --env-file .env lumeleto-mastodon

Fail2ban, ufw, SSH keys — the usual Contabo hardening.

Edit the service file:

vi /etc/systemd/system/lumeleto-bridge.service

[Unit]
Description=Lumeleto ↔ Mastodon Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=/root/apps/lumeleto (change to user!)
ExecStart=/snap/bin/docker-compose up
ExecStop=/snap/bin/docker-compose down
Restart=always
User=root (change to user!)

[Install]
WantedBy=multi-user.target

------

# 1. Build once
cd ~/apps/lumeleto-bridge
docker-compose build

# 2. Enable and start service
sudo systemctl daemon-reexec
sudo systemctl enable lumeleto-bridge
sudo systemctl start lumeleto-bridge

# 3. Check logs
journalctl -u lumeleto-bridge -f