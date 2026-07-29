from dotenv import load_dotenv
import os

load_dotenv()

print("BOT TOKEN:")
print(os.getenv("BOT_TOKEN"))

print()

print("OPENAI KEY:")
print(os.getenv("OPENAI_API_KEY"))