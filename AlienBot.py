import discord
from discord.ext import commands
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Load intents for personality
with open('intents.json') as f:
    intents_data = json.load(f)

# Build personality prompt from intents
personality_context = "You are AlienBot. Here's your personality based on how you respond:\n\n"
for intent in intents_data['intents']:
    personality_context += f"When asked about {intent['tag']}, you say things like: {intent['responses'][0]}\n"

personality_context += "\nKeep responses concise, casual, and in character. Use emojis like :eye:, :flying_saucer:, :wave: when appropriate."

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

conversations = {}

@bot.event
async def on_ready():
    print(f"Bot is ready as {bot.user}.")


@bot.command()
async def hello(ctx):
    await ctx.send("hi")


@bot.command()
async def clear(ctx):
    if ctx.channel.id in conversations:
        conversations[ctx.channel.id] = []
    await ctx.send("Conversation history cleared")


@bot.event
async def on_message(message):
    # Process commands first
    await bot.process_commands(message)

    # Only respond in specific channels
    if message.channel.name not in ["alienbot-channel", "admin"]:
        return

    # Don't respond to self or commands
    if message.author == bot.user or message.content.startswith('.'):
        return

    # Get or create conversation history
    channel_id = message.channel.id
    if channel_id not in conversations:
        conversations[channel_id] = []

    # Initialize with personality
    if not conversations[channel_id]:
        conversations[channel_id].append({
            'role': 'user',
            'parts': [personality_context]
        })
        conversations[channel_id].append({
            'role': 'model',
            'parts': ['Got it, I\'ll stay in character as AlienBot.']
        })

    # Add user message
    conversations[channel_id].append({
        'role': 'user',
        'parts': [message.content]
    })

    try:
        # Generate response
        chat = model.start_chat(history=conversations[channel_id][:-1])
        response = chat.send_message(message.content)

        # Add bot response to history
        conversations[channel_id].append({
            'role': 'model',
            'parts': [response.text]
        })

        # Keep history a reasonable length
        if len(conversations[channel_id]) > 20:
            # Keep system prompt and last 18 messages
            conversations[channel_id] = conversations[channel_id][:2] + conversations[channel_id][-18:]

        await message.channel.send(response.text)

    except Exception as e:
        print(f"Error: {e}")
        await message.channel.send("Sorry, I had trouble processing that.")

# Run bot
bot.run(os.getenv('DISCORD_BOT_TOKEN'))
