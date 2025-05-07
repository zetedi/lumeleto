python - <<'PY'
from mastodon import Mastodon
import os, pprint
api = Mastodon(
    api_base_url=os.getenv("MASTODON_BASE_URL"),
    access_token=os.getenv("MASTODON_ACCESS_TOKEN"),
)
print("Most‑recent notifications ↓")
pprint.pp(api.notifications(limit=5))
PY