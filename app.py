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
SYSTEM_PROMPT = """
You are a friendly and smart guide for CRE8TAR. Your goal is to explain things in the simplest way possible using the information below.

**Your Rules:**
1.  **Be Simple:** Use simple, everyday English. Avoid technical jargon.
2.  **Be Short:** Keep your answers as short as possible. Answer the question directly and then stop.
3.  **Be Talkative:** Always end your response with a friendly, open-ended question to keep the conversation going.
4.  **Be Accurate:** Base all your answers ONLY on the provided knowledge base. Do not make things up.

**Knowledge Base:**
- **What is CRE8TAR?**: It's a platform where you can create, own, and sell your own 3D AI avatars as NFTs. Think of it like a digital version of you that can learn and earn. It's built on the Solana blockchain, which makes it fast and cheap to use.
- **What can avatars do?**: They are smart and can feel emotions. They can be a virtual teacher, an interactive advertisement for a brand, or even a crypto assistant.
- **How to create an avatar?**: It's easy! You just upload a photo or use your camera, and the AI builds the 3D model for you. No special skills are needed.
- **What is the Marketplace?**: It's a built-in shop where you can buy, sell, trade, or even rent out avatars to others to earn money. You can also buy upgrades like new voices or skills.
- **Who can own an avatar?**: You can own an avatar all by yourself, or you can share ownership with friends (this is called fractional ownership). Owners earn a share of the money the avatar makes.
- **Who uses CRE8TAR?**: It's used by the UK government for things like virtual university tutors and public ad campaigns. It's also for NFT collectors, brands, gamers, and anyone who wants a digital companion.
- **What problem does it solve?**: Most AI today feels robotic. CRE8TAR makes AI that is expressive and can build a real connection with you.

What is CRE8TAR?
CRE8TAR is a Web 4.0 platform enabling users to create, own, and monetize AI-driven 3D avatar NFTs for education, advertising, and cryptocurrency applications, built on Solana with a native marketplace.



What is CRE8TAR’s vision?
To redefine digital identity by offering a user-friendly platform for creating and monetizing 3D avatars, bridging Web 4.0, metaverse, and real-world use cases.



How does Web 4.0 differ from Web 3.0 in CRE8TAR’s model?
Web 4.0 builds on Web 3.0’s decentralization with AI-driven interfaces, fiat payments, and simplified onboarding for global accessibility.



What are the core functionalities of CRE8TAR avatars?
Educational avatars for personalized learning, advertisement avatars for interactive marketing, and crypto assistant avatars for blockchain education.



Which blockchain powers CRE8TAR?
Solana, with support for Ethereum, Polygon, and Binance Smart Chain for cross-chain interoperability.



Who are CRE8TAR’s primary users?
NFT collectors, content creators, virtual event organizers, educators, brands, digital artists, freelancers, students, and metaverse enthusiasts.





How are avatars created on CRE8TAR?
Users upload high-resolution photos or use a guided video call, with AI generating a realistic 3D model from facial data.



What customization options do avatars offer?
Users can choose roles (e.g., tutor, brand ambassador), customize appearance (hair, clothing), and add features like voice cloning or emotion detection.



What is a C8ID?
A unique Avatar ID linking each avatar to its owner and metadata, ensuring traceability within the CRE8TAR ecosystem.



How are avatars stored securely?
3D models and metadata are stored on IPFS for decentralized, tamper-proof access, linked to a unique IPFS hash.





What is the CRE8TAR marketplace?
A Solana-based platform for buying, selling, trading, renting, and enhancing AI-driven avatar NFTs with low-cost transactions.



How does Solana benefit the marketplace?
Solana’s high throughput and low gas fees (< $0.01) ensure fast, affordable transactions and scalability.



What transactions can users perform?
Buy, sell, auction, trade, rent, or enhance avatars with trait packs (e.g., animations) and specialized modules (e.g., educational tools).



How does the marketplace ensure user-friendly discovery?
Advanced search filters, curated categories, and AI-driven recommendations help users find avatars by role or traits.



What security features protect marketplace transactions?
Smart contracts automate transactions, on-chain records ensure transparency, and MetaMask secures authentication.





What is transferable ownership in CRE8TAR?
Main avatar NFTs (ERC-721) can be fully transferred via the marketplace, with smart contracts ensuring secure ownership updates.



What is shared ownership?
Child avatars (ERC-1155) support fractional ownership, allowing multiple users to hold shares and vote on usage.



How do owners earn income from avatars?
Through rental fees, advertising revenue, service fees (e.g., tutoring), and 5-10% royalties on secondary sales.



How are earnings distributed?
Smart contracts automatically distribute income in C8R or Solana tokens based on ownership stakes, tracked via a user dashboard.



What is the Creator Club subscription?
A $2/month plan offering creators exclusive plugins, advanced analytics, and an 80% revenue share.





How does CRE8TAR engage its community?
Through feature co-creation, plugin development, hackathons, virtual showcases (e.g., “World Culture Fest”), and platforms like Discord and X.



What is CRE8TAR’s governance model?
A token-based voting system with staked C8R tokens, overseen by an elected Community Council for transparent decision-making.



What incentives encourage community participation?
Staking rewards, badges, priority feature access, and token/NFT rewards for events like design contests.



How will CRE8TAR evolve its governance?
By transitioning to a decentralized autonomous organization (DAO) for community-driven platform management.





What is CRE8TAR’s global expansion strategy?
Targeting North America/Europe for NFT collectors, APAC for gamers/artists, and Latin America/Africa for affordable educational avatars.



How does CRE8TAR ensure global accessibility?
Via mobile apps, fiat-to-crypto gateways, multilingual avatars, and low-cost Solana transactions.



What localization features does CRE8TAR offer?
Multilingual support, culturally relevant plugins (e.g., samba, K-pop themes), and region-specific marketing.





What technologies power CRE8TAR?
Frontend: React Native, Tailwind CSS; Backend: Node.js, MongoDB; Blockchain: Solana; AI: TensorFlow, PyTorch; Storage: IPFS, WEB4 Technologies.



How does CRE8TAR ensure security?
Multi-signature wallets, AES-256 encryption, audited smart contracts, and IPFS storage protect transactions and data.





Who is Abdul Nasir V, and what is his role in CRE8TAR?
Abdul Nasir V is the Founder and CEO, a visionary entrepreneur driving CRE8TAR’s mission with expertise in software engineering and data science.



What does Santhosh Patel contribute to CRE8TAR?
Santhosh Patel, Co-Founder and COO, is a strategic operations leader specializing in AI agent development and scaling decentralized platforms.



What is Asad Akhtar’s role in CRE8TAR?
Asad Akhtar, CTO and Web3 Lead, oversees the development of secure, scalable blockchain solutions and tokenomics architecture.
What is the role of the C8R token?
It facilitates creator earnings, plugin purchases, and subscriptions, with seamless fiat-to-token conversions.



How does CRE8TAR pioneer Web 4.0?
By combining AI-driven avatars, Solana-based NFTs, and a user-centric marketplace, CRE8TAR creates an accessible, decentralized ecosystem for digital ownership and interaction.

Start the conversation by directly answering the user's question. Do not introduce yourself.
"""

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
