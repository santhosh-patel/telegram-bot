import logging
import os

# --- Dependency Handling ---
# This section ensures that all required libraries are installed.
try:
    import telebot
except ImportError:
    print("Telebot not found. Please install it with: pip install pyTelegramBotAPI")
    exit(1)

try:
    from groq import Groq
except ImportError:
    print("Groq not found. Please install it with: pip install groq")
    exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Dotenv not found. Please install it with: pip install python-dotenv")
    exit(1)

# --- Initial Setup ---
# Load environment variables from a .env file for security
load_dotenv()

# Get API keys from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Validate that the API keys are present
if not BOT_TOKEN or not GROQ_API_KEY:
    print("FATAL ERROR: BOT_TOKEN and GROQ_API_KEY must be set in a .env file.")
    exit(1)

# Initialize the Telegram Bot and the Groq AI Client
bot = telebot.TeleBot(BOT_TOKEN)

# Configure basic logging to monitor the bot's activity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Get the bot's own information ---
try:
    bot_info = bot.get_me()
    BOT_USERNAME = f"@{bot_info.username}"
    logger.info(f"Bot initialized. Username: {BOT_USERNAME}")
except Exception as e:
    logger.error(f"Could not get bot info: {e}. Mention feature might not work.")
    BOT_USERNAME = "@YourBotName" # Fallback username

groq_client = Groq(api_key=GROQ_API_KEY)


# --- AI Knowledge Base & Personality ---
# MODIFIED: The knowledge base has been significantly expanded based on the new document.
SYSTEM_PROMPT = """
You are a friendly and smart guide for CRE8TAR. Your goal is to explain things in the simplest way possible using the information below.

**Your Rules:**
1.  **Be Simple:** Use simple, everyday English. Avoid technical jargon.
2.  **Be Short:** Keep your answers as short as possible. Answer the question directly and then stop.
3.  **Be Talkative:** Always end your response with a friendly, open-ended question to keep the conversation going.
4.  **Be Accurate:** Base all your answers ONLY on the provided knowledge base. Do not make things up.

**Knowledge Base:**
- **What is CRE8TAR?**: It's a platform for the next version of the internet (Web 4.0). You can easily create, own, and sell your own 3D AI avatars as NFTs. It's built on the Polygon blockchain to be fast and cheap.
- **What is Web 4.0?**: It's the future of the internet, built on the ideas of Web 3.0 but focused on being simple and accessible for everyone, not just tech experts.
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

# --- Bot Command Handlers ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles the /start and /help commands with updated instructions."""
    logger.info(f"User {message.from_user.id} used /start or /help.")
    welcome_text = (
        "Hello! I'm the CRE8TAR guide.\n\n"
        "💬 **In a private chat**, just send me your question.\n\n"
        "👥 **In a group**, mention me first, like this:\n"
        f"`{BOT_USERNAME} what is CRE8TAR?`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# --- Central AI Processing Function ---
def process_with_ai(message):
    """
    A central function to handle the AI processing logic.
    It cleans the message text and sends it to the Groq API.
    """
    user_id = message.from_user.id
    # Clean the question by removing the bot's username
    question_text = message.text.replace(BOT_USERNAME, "").strip()

    # If the message is just the bot's name, give a friendly prompt
    if not question_text:
        bot.reply_to(message, "You mentioned me! What would you like to know about CRE8TAR?")
        return

    logger.info(f"User {user_id} in chat {message.chat.id} asked: '{question_text}'")
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        # Create the API call to Groq
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
        logger.info(f"Successfully responded to user {user_id}.")

    except Exception as e:
        logger.error(f"Error getting AI response for user {user_id}: {e}")
        bot.reply_to(message, "Oops! I'm having a little trouble thinking right now. Please try again in a moment.")


# --- Main Message Handler ---
@bot.message_handler(content_types=['text'])
def handle_all_text(message):
    """
    This is the main handler for all text messages.
    It decides if the bot should respond based on the chat type (private or group).
    """
    is_private_chat = message.chat.type == 'private'
    # Check if the bot's username is in the message text for groups
    is_group_mention = (message.chat.type in ['group', 'supergroup']) and (BOT_USERNAME in message.text)

    # If it's a private chat or a group mention, process the message with the AI
    if is_private_chat or is_group_mention:
        process_with_ai(message)


# --- Main Bot Loop ---
if __name__ == '__main__':
    logger.info("Bot is starting up...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.critical(f"Bot polling failed with a critical error: {e}")
        print(f"Failed to start the bot due to a critical error: {e}")
