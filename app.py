import logging
import os
import telebot
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request

# --- Initial Setup ---
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
VERCEL_URL = os.environ.get('VERCEL_URL') # Vercel provides this automatically

# Validate that the API keys are present
if not BOT_TOKEN or not GROQ_API_KEY:
    raise ValueError("FATAL ERROR: BOT_TOKEN and GROQ_API_KEY must be set.")

# Initialize Bot and Flask App
bot = telebot.TeleBot(BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)
server = Flask(__name__) # New: Initialize a Flask web server

# --- AI Knowledge Base & Personality (remains the same) ---
SYSTEM_PROMPT = """
You are a friendly and smart guide for CRE8TAR. Your goal is to explain things in the simplest way possible using the information below.

**Your Rules:**
1.  **Be Simple:** Use simple, everyday English. Avoid technical jargon.
2.  **Be Short:** Keep your answers as short as possible. Answer the question directly and then stop.
3.  **Be Talkative:** Always end your response with a friendly, open-ended question to keep the conversation going.
4.  **Be Accurate:** Base all your answers ONLY on the provided knowledge base. Do not make things up.

**Knowledge Base:**
- **What is CRE8TAR?**: It's a platform for the next version of the internet (Web 4.0). You can easily create, own, and sell your own 3D AI avatars as NFTs. It's built on the Polygon blockchain to be fast and cheap.
- **How is CRE8TAR linked to Web 4.0?**: CRE8TAR is a Web 4.0 platform because it makes complex technology easy. It lets you use your local money instead of crypto, and it hides all the complicated blockchain stuff. The goal is to let anyone in the world own digital items as easily as shopping online.
- **How do you pay for things?**: You can use your own local money with a credit card or mobile app (like UPI in India). You don't need to buy or understand cryptocurrency to get started.
- **What can avatars do?**: They are smart and can feel emotions. They can be a virtual teacher, an interactive ad, or a crypto assistant. You can also buy 'plugins' to give them new skills.
- **What are plugins?**: They are extra skills or animations for your avatar, like dancing, cooking, or yoga. Creators from all over the world can make and sell these in the marketplace.
- **How do creators earn money?**: They can sell their creations (like plugins or avatar fashion) in the marketplace and keep a large share of the money (70-80%). They also get royalties from resales.
- **Is it complicated to use?**: Not at all! The blockchain part is invisible. You just use a simple username, and all the tech stuff (like minting NFTs) happens automatically in the background.
- **Who uses CRE8TAR?**: It's for everyone! NFT collectors, brands, gamers, and anyone who wants a digital companion. It's also used by the UK government for virtual tutors and ad campaigns.
- **What is the C8R Token?**: It's the platform's own token. You can use it to vote on decisions (governance), earn rewards by staking it, and get access to special AI services.

Start the conversation by directly answering the user's question. Do not introduce yourself.
"""

# --- Bot Logic (remains mostly the same) ---
def process_with_ai(message):
    try:
        bot_info = bot.get_me()
        BOT_USERNAME = f"@{bot_info.username}"
    except Exception:
        BOT_USERNAME = "@YourBotName"

    user_id = message.from_user.id
    question_text = message.text.replace(BOT_USERNAME, "").strip()

    if not question_text:
        bot.reply_to(message, "You mentioned me! What would you like to know about CRE8TAR?")
        return

    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question_text}
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=200
        )
        response = chat_completion.choices[0].message.content
        bot.reply_to(message, response)
    except Exception as e:
        logging.error(f"Error getting AI response for user {user_id}: {e}")
        bot.reply_to(message, "Oops! I'm having a little trouble thinking right now. Please try again in a moment.")

# --- New: Webhook Endpoint ---
# This is the URL that Telegram will send updates to.
@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# --- New: Webhook Setup Endpoint ---
# This endpoint is used once to tell Telegram where to send updates.
@server.route("/")
def webhook():
    bot.remove_webhook()
    # We use VERCEL_URL as the base, and the bot token as the path.
    # This makes the webhook URL secret and unique to our bot.
    bot.set_webhook(url=f"{VERCEL_URL}/{BOT_TOKEN}")
    return "Webhook set successfully!", 200

# The main handler logic is now inside this function
@bot.message_handler(func=lambda message: True)
def handle_all_text(message):
    # This function now contains the logic that was previously in the main handler
    try:
        bot_info = bot.get_me()
        BOT_USERNAME = f"@{bot_info.username}"
    except Exception:
        BOT_USERNAME = "@YourBotName"

    is_private_chat = message.chat.type == 'private'
    is_group_mention = (message.chat.type in ['group', 'supergroup']) and (BOT_USERNAME in message.text)

    if is_private_chat or is_group_mention:
        process_with_ai(message)
