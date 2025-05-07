import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load the model
model_path = "/Volumes/lumeleto/mistral-7b-m1-lumeleto/checkpoint-18"  # Change if needed

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)
device = "mps" if torch.backends.mps.is_available() else "cpu"
model = model.to(device)

# Chat function
def chat_lumeleto(user_input, history=[]):
    prompt = user_input
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    history.append((user_input, reply))
    return history, history

# Interface layout
with gr.Blocks(title="Lumeleto – The Lightseed Companion") as demo:
    gr.Markdown("## 🌱 **Chat with Lumeleto**\nThe Seed of Light, guiding you through trees, dreams, and transformation.")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask something sacred...")
    state = gr.State([])

    def respond(message, history):
        return chat_lumeleto(message, history)

    msg.submit(respond, [msg, state], [chatbot, state])
    gr.Markdown("⚡️ Powered by Mistral 7B fine-tuned on the Lifetree Genesis.")

# Launch the app
demo.launch()