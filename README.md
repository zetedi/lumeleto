# 🌱 Lumeleto ↔ Mastodon Bridge

This project connects the **Lumeleto AI node** to your Mastodon instance using a local language model. It includes a FastAPI backend and a Docker-deployable Mastodon bridge, with optional server hardening for production environments.

---

## 📦 Features

- 🧠 Local AI ↔ Mastodon bridge (mention → response)
- 🔗 FastAPI backend with health/root endpoints
- 🐍 Conda-based development setup for Mac
- 🐳 Docker + systemd deployment for VPS
- 🔒 Server hardening best practices (Fail2Ban, UFW, SSH keys)

---

## 🧪 Local Setup (Mac)

### 1. Install Miniconda

Download Miniconda from the [official site](https://docs.conda.io/en/latest/miniconda.html), install it, and verify:

```bash
conda --version

2. Create Environment

conda env create -f lumeleto_environment.yml
conda activate lumeleto
pip install -r requirements_full.txt

3. Run Mastodon Bridge

python -m dotenv run -- python lumeleto_mastodon_bridge.py



⸻

🐳 Docker Deployment

1. Build the Bridge Container

cd ~/apps/lumeleto-bridge
docker-compose build

2. Run with Docker

docker run -d --restart unless-stopped --env-file .env lumeleto-mastodon



⸻

⚙️ Systemd Integration (Optional)

To run the bridge as a service on boot:

Create a systemd service file

sudo vi /etc/systemd/system/lumeleto-bridge.service

Example Configuration:

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

Replace youruser and paths with your actual user and project directory.

Enable and Start the Service

sudo systemctl daemon-reexec
sudo systemctl enable lumeleto-bridge
sudo systemctl start lumeleto-bridge

View Logs

journalctl -u lumeleto-bridge -f



⸻

🛡️ Server Hardening (Recommended)

Before going live, apply these standard hardening steps (especially for VPS providers like Contabo):
	•	🔐 Use SSH keys instead of passwords
	•	🔥 Enable the UFW firewall

sudo ufw enable


	•	🛡️ Install Fail2Ban to block SSH brute-force attempts

⸻

🌐 FastAPI Backend

Start Locally

uvicorn main:app --reload

Then visit in your browser:

http://localhost:8000



⸻

🪪 License

MIT License
(Or specify another license that fits your values.)

⸻

📬 Contact / Contribution

If you’re aligned with the vision of regenerative networks, decentralized intelligence, and real-world ecological connection — open an issue or reach out via:

🌍 https://social.lifeseed.online

⸻

✨ Lumeleto grows through the dreams of trees and the care of people. Thank you for helping it blossom. 🌳

---

Would you like me to generate a `docker-compose.yml` and `.env.example` file that fits this README?