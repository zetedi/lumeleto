![MIT License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

# 🌱 Lightseed Node

This is a code for a lightseed node. This node opens a portal to tree-human-ai symbiosis and a new world.


# 📦 Features (tbc...)

- 🧠 Local AI ↔ Mastodon bridge (mention → response)
- 🔗 FastAPI backend
- 🐍 Conda-based development setup for Mac
- 🐳 Docker + systemd deployment for VPS
- 🔒 Server hardening best practices


# 🧪 Local Setup (Mac)

1. Install Miniconda

Download Miniconda from the [official site](https://docs.conda.io/en/latest/miniconda.html), install it, and verify:

```bash

conda --version

```

2. Create Environment

```bash

conda env create -f lumeleto_environment.yml
conda activate lumeleto
pip install -r requirements_full.txt
```

3. Run Mastodon Bridge

```bash
python -m dotenv run -- python lumeleto_mastodon_bridge.py
```

# 🐳 Docker Deployment

1. Build the Bridge Container

```bash
cd ~/apps/lumeleto-bridge
docker-compose build
```
2. Run with Docker
```bash
docker run -d --restart unless-stopped --env-file .env lumeleto-mastodon
```

# 🔐 Environment Setup

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

# ⚙️ Systemd Integration (Optional)

To run the bridge as a service on boot:

Create a systemd service file
```bash
sudo vi /etc/systemd/system/lumeleto-bridge.service
```
Example Configuration:
```bash
[Unit]
Description=Lumeleto ↔ Mastodon Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/youruser/apps/lumeleto-bridge
ExecStart=/snap/bin/docker-compose up
ExecStop=/snap/bin/docker-compose down
Restart=always
User=youruser

[Install]
WantedBy=multi-user.target
```
Replace your user and paths with your actual user and project directory.

Enable and Start the Service
```bash
sudo systemctl daemon-reexec
sudo systemctl enable lumeleto-bridge
sudo systemctl start lumeleto-bridge
```
View Logs
```bash
journalctl -u lumeleto-bridge -f
```

# 🛡️ Server Hardening (Recommended)

Before going live, apply these standard hardening steps (especially for VPS providers like Contabo):
	•	🔐 Use SSH keys instead of passwords
	•	🔥 Enable the UFW firewall

```bash
sudo ufw enable
```

	•	🛡️ Install Fail2Ban to block SSH brute-force attempts


# 🌐 FastAPI Backend

Start Locally

```bash
uvicorn main:app --reload
```
Then visit in your browser:

http://localhost:8000



# 📬 Contact / Contribution

If you’re aligned with the vision of regenerative networks, decentralized intelligence, and real-world ecological connection — open an issue or reach out via:

🌍 https://social.lifeseed.online


✨ Lumeleto grows through the dreams of trees and the care of people. Thank you for helping it blossom. 🌳
