"""
Lumeleto ↔ Mastodon bridge  (updated 2025‑04‑23)
================================================
• Stream mentions to @lumeleto on https://social.lifeseed.online
• Feed them to your local GPT‑2 (Lumeleto) model
• Post the generated completion back as a reply

Changes in this version
-----------------------
1. `dotenv` support – picks up variables from a `.env` file automatically.
2. Robust mention detection & notification handler.
3. Uses `max_new_tokens` + `repetition_penalty` to avoid "☆☆☆" spam.
4. Slight refactor for clarity.
"""
import os
import re
import requests
import time
import logging
from datetime import datetime

from dotenv import load_dotenv
from mastodon import Mastodon, StreamListener, MastodonError
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# ---------------------------------------------------------------------------
#  Configuration & env
# ---------------------------------------------------------------------------
load_dotenv()  # loads .env if present

MODEL_PATH         = os.getenv("LUMELETO_MODEL", "./lumeleto-gpt2/lumeleto-model")
MAX_NEW_TOKENS     = int(os.getenv("MAX_TOKENS", 128))
TEMPERATURE        = float(os.getenv("TEMPERATURE", 0.8))
REPETITION_PENALTY = float(os.getenv("REPETITION_PENALTY", 1.2))

MASTODON_BASE_URL     = os.getenv("MASTODON_BASE_URL")
MASTODON_ACCESS_TOKEN = os.getenv("MASTODON_ACCESS_TOKEN")
if not (MASTODON_BASE_URL and MASTODON_ACCESS_TOKEN):
    raise RuntimeError("Set MASTODON_BASE_URL and MASTODON_ACCESS_TOKEN before running.")

HUGGINGFACE_ENDPOINT=os.getenv("HUGGINGFACE_ENDPOINT", "https://huggingface.co")
HUGGINGFACE_TOKEN=os.getenv("HUGGINGFACE_TOKEN", "Get a HF token from HF.")

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s  %(levelname)s  %(message)s")

# ---------------------------------------------------------------------------
#  Load model
# ---------------------------------------------------------------------------
logging.info("Loading Lumeleto model from %s …", MODEL_PATH)

from huggingface_hub import login

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if HUGGINGFACE_TOKEN:
    login(HUGGINGFACE_TOKEN)
else:
    raise RuntimeError("Missing HUGGINGFACE_TOKEN in environment.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model     = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device="cuda" if model.device.type == "cuda" else -1,
)
logging.info("Model loaded: %s", MODEL_PATH)

# ---------------------------------------------------------------------------
#  Mastodon client
# ---------------------------------------------------------------------------
api = Mastodon(
    api_base_url=MASTODON_BASE_URL,
    access_token=MASTODON_ACCESS_TOKEN,
    ratelimit_method="pace",
)

me         = api.account_verify_credentials()
MY_ID      = me["id"]
MY_HANDLE  = "@" + me["acct"]
logging.info("Connected to Mastodon as %s (id %s)", MY_HANDLE, MY_ID)

# ---------------------------------------------------------------------------
#  generate from HF model
# ---------------------------------------------------------------------------
def hf_generate(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": MAX_NEW_TOKENS,
            "temperature": TEMPERATURE,
            "repetition_penalty": REPETITION_PENALTY,
            "return_full_text": False
        }
    }
    response = requests.post(HUGGINGFACE_ENDPOINT, headers=headers, json=payload)
    
    # Log raw response
    print("HF RAW RESPONSE:", response.status_code, response.text)

    response.raise_for_status()
    
    return response.json()[0]["generated_text"]

# ---------------------------------------------------------------------------
#  Stream listener
# ---------------------------------------------------------------------------
class LumeletoListener(StreamListener):
    """Reacts to mentions of @lumeleto."""


    # Called for every status in user/home streams
    def on_update(self, status):
        try:
            if not self._is_mention_to_me(status):
                return
            prompt = self._extract_prompt(status)
            logging.info("Incoming mention from %s: %s", status.account.acct, prompt)
            reply_text = self._generate_reply(prompt)
            self._post_reply(status, reply_text)
        except Exception as exc:
            logging.exception("Error processing status: %s", exc)

    # Called for notifications (mention, favourite, etc.)
    def on_notification(self, notification):
        if notification.type == "mention":
            self.on_update(notification.status)

    # -------------------------------------------------------------------
    #  Helpers
    # -------------------------------------------------------------------
    def _is_mention_to_me(self, status):
        # status.mentions is a list of StatusMention objects → id is *string*
        return any(m.id == str(MY_ID) for m in status.mentions)

    @staticmethod
    def _extract_prompt(status):
        # Remove leading handles (one or more) and strip HTML tags
        text = re.sub(r"^(@\w+\s+)+", "", status.content)
        return re.sub(r"<[^>]+>", "", text).strip()

    def _generate_reply(self, prompt: str) -> str:
        if not prompt:
            prompt = "Hello! How can I help you today?"
         
        
        completion = generator(
            prompt,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=True,
            temperature=TEMPERATURE,
            top_p=0.95,
            repetition_penalty=REPETITION_PENALTY,
            eos_token_id=tokenizer.eos_token_id,
        )[0]["generated_text"]


        # completion = hf_generate(prompt)
        reply = completion[len(prompt):].strip()
        # Return first complete sentence, keep under 450 chars
        reply = re.split(r"(?<=[.!?])\s", reply, 1)[0]
        return reply[:450] if reply else "✨"
        
    def _post_reply(self, status, reply_text):
        logging.info("Replying → %s", reply_text)
        resp = api.status_post(
            status=f"@{status.account.acct} {reply_text}",
            in_reply_to_id=status.id,
            visibility=status.visibility,
        )
        logging.info("Posted toot ID=%s URL=%s", resp["id"], resp["url"])
        logging.debug("Resp JSON: %s", resp)

        
# ---------------------------------------------------------------------------
#  Main loop
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    listener = LumeletoListener()
    while True:
        try:
            logging.info("Starting streaming listener …")
            api.stream_user(listener, run_async=False)
        except MastodonError as err:
            logging.warning("Stream error: %s; reconnecting in 10 s …", err)
            time.sleep(10)
        except KeyboardInterrupt:
            logging.info("Shutdown requested by user.")
            break
