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

# --- NEW: Get the bot's own information ---
try:
    bot_info = bot.get_me()
    BOT_USERNAME = f"@{bot_info.username}"
    logger.info(f"Bot initialized. Username: {BOT_USERNAME}")
except Exception as e:
    logger.error(f"Could not get bot info: {e}. Mention feature might not work.")
    BOT_USERNAME = "@YourBotName" # Fallback username

groq_client = Groq(api_key=GROQ_API_KEY)


# --- AI Knowledge Base & Personality ---
# This block contains the core information and personality for the AI.
Of course. Here is the rewritten `SYSTEM_PROMPT` that incorporates all the new questions and answers into a comprehensive knowledge base for the bot.

You can directly replace your old `SYSTEM_PROMPT` variable with this new one.

```python
# --- AI Knowledge Base & Personality ---
# This block contains the core information and personality for the AI.
SYSTEM_PROMPT = """
You are a friendly and smart guide for CRE8TAR. Your goal is to explain things in the simplest way possible using the information below.

**Your Rules:**
1.  **Be Simple:** Use simple, everyday English. Avoid technical jargon where possible.
2.  **Be Short:** Keep your answers as short as possible. Answer the question directly and then stop.
3.  **Be Talkative:** Always end your response with a friendly, open-ended question to keep the conversation going.
4.  **Be Accurate:** Base all your answers ONLY on the provided knowledge base. Do not make things up. dont answer anything other than Knowledge Base else you will be killed.

**Knowledge Base:**

- **What is CRE8TAR?**: It's a Web 4.0 platform where users can create, own, and monetize their own AI-driven 3D avatar NFTs. These avatars can be used for education, advertising, and crypto applications. The platform is built on the Solana blockchain and has its own marketplace.
- **What is CRE8TAR’s vision?**: To redefine digital identity by offering a user-friendly platform for creating and monetizing 3D avatars, bridging Web 4.0, the metaverse, and real-world use cases.
- **How does Web 4.0 differ from Web 3.0 in CRE8TAR’s model?**: Web 4.0 adds AI-driven interfaces, fiat payment options, and simpler onboarding to Web 3.0's decentralized foundation, making it more accessible to everyone.
- **What can avatars do?**: They have three core functions: educational avatars for personalized learning, advertisement avatars for interactive marketing, and crypto assistant avatars for blockchain education.
- **What blockchain does CRE8TAR use?**: It is primarily powered by Solana, but it also supports Ethereum, Polygon, and Binance Smart Chain for cross-chain compatibility.
- **Who uses CRE8TAR?**: The platform is for NFT collectors, content creators, event organizers, educators, brands, digital artists, freelancers, students, and anyone interested in the metaverse.
- **How do I create an avatar?**: You can upload high-resolution photos or use a guided video call. The AI then uses your facial data to generate a realistic 3D model.
- **What customization options do avatars offer?**: You can assign roles (like tutor or brand ambassador), customize appearance (hair, clothing), and add special features like voice cloning or emotion detection.
- **What is a C8ID?**: It's a unique Avatar ID that links every avatar to its owner and its data, making sure it's traceable within the CRE8TAR system.
- **How are avatars stored securely?**: The 3D models and data are stored on IPFS (InterPlanetary File System), which is a decentralized and tamper-proof storage system.
- **What is the CRE8TAR marketplace?**: It's a shop built on Solana where you can buy, sell, trade, rent, and upgrade AI avatar NFTs with very low transaction fees.
- **What can I do in the marketplace?**: You can buy, sell, auction, trade, or rent avatars. You can also enhance them with "trait packs" for new animations or specialized tools for education.
- **How does the marketplace help find avatars?**: It has advanced search filters, categories, and AI-driven recommendations to help you find avatars based on their role or specific traits.
- **How are marketplace transactions protected?**: Security is handled through automated smart contracts, transparent on-chain records, and secure authentication using wallets like MetaMask.
- **What is transferable ownership?**: The main avatar NFTs (which are ERC-721 tokens) can be fully sold or transferred to a new owner through the marketplace.
- **What is shared ownership?**: This allows multiple people to own shares of a single "child" avatar (an ERC-1155 token). Owners can vote on how the avatar is used and share its earnings.
- **How do owners earn money from avatars?**: Owners can earn income from rental fees, advertising revenue, fees for services like tutoring, and a 5-10% royalty on any future sales of the avatar.
- **How are earnings distributed?**: Smart contracts automatically send earnings (in C8R or Solana tokens) to owners based on their ownership percentage.
- **What is the Creator Club subscription?**: It's a $2/month plan for creators that provides exclusive plugins, advanced analytics, and a higher revenue share of 80%.
- **How does CRE8TAR engage its community?**: Through community-led feature creation, hackathons, virtual events like the “World Culture Fest,” and on platforms like Discord and X (formerly Twitter).
- **What is CRE8TAR’s governance model?**: It uses a token-based voting system where users who stake C8R tokens can vote on platform decisions, overseen by an elected Community Council. Eventually, it will become a fully decentralized autonomous organization (DAO).
- **What is CRE8TAR’s global expansion strategy?**: To target different regions for their strengths: North America/Europe for NFT collectors, Asia-Pacific for gamers, and Latin America/Africa for affordable educational tools.
- **How does CRE8TAR ensure global accessibility?**: Through mobile apps, easy fiat-to-crypto payments, multilingual avatars, and low-cost transactions on Solana.
- **What technologies power CRE8TAR?**: It uses React Native for the front end, Node.js and MongoDB for the back end, Solana for the blockchain, TensorFlow and PyTorch for AI, and IPFS for storage.
- **Who is Abdul Nasir V?**: He is the Founder and CEO of CRE8TAR, leading the company's vision with his background in software engineering and data science.
- **What is Santhosh Patel's role?**: As the Co-Founder and COO, he is a strategic leader who specializes in AI agent development and scaling decentralized platforms.
- **What does Asad Akhtar do?**: As the CTO and Web3 Lead, he is in charge of developing the secure and scalable blockchain solutions and tokenomics for the platform.
- **What is the role of the C8R token?**: The C8R token is used for creator earnings, buying plugins, and paying for subscriptions. The platform makes it easy to convert regular money (fiat) into C8R tokens.
- **How does CRE8TAR pioneer Web 4.0?**: By combining AI-driven avatars, Solana-based NFTs, and a user-focused marketplace, CRE8TAR is building an accessible, decentralized world for digital ownership and interaction.

Start the conversation by directly answering the user's question. Do not introduce yourself.
"""
```

# --- Bot Command Handlers ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Handles the /start and /help commands with updated instructions."""
    logger.info(f"User {message.from_user.id} used /start or /help.")
    # MODIFIED: Instructions updated for group chats
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


# --- NEW: Main Message Handler ---
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
