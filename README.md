# AlienBot Discord Chatbot
A Discord bot powered by Google's Gemini AI that resopnds with personality based on custom intents.

## Technologies
* **Google Gemini AI** - Free tier LLM for natural conversation
* **Discord.py** Discord bot framework
* **Python-dotenv** - Environment variable management

## Setup
1. Clone and create virtual environment

```
python3 -m venv venv
source venv/bin/activate # Mac/Linux
# OR
venv\Scripts\activate # Windows
```

2. Install dependencies:

`pip install -r requirements.txt`

3. Get API Keys

Put Discord Bot Token and Gemini API Key into new .env file, like so:

``` 
DISCORD_BOT_TOKEN=your_discord_token
GEMINI_API_KEY=your_gemini_key_here
```

4. Run the bot:

`python Alienbot.py`

## Usage
The bot responds in channels named `alienbot-channel` or `admin`.

Commands:
* `.hello` - Test command
* `.clear` - Clear conversation history

The bot's personality is defined in `intents.json` and uses Gemini to generate natural responses in character

## Notes

- Require Python 3.10+
- Uses Gemini's free tier (1500 requests/day)
- Maintains conversation context per channel