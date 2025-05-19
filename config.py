# config.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import logging

load_dotenv(Path(__file__).parent / ".env")

NCBI_API_KEY = os.getenv("NCBI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
INPUT_FILE = os.getenv("INPUT_FILE")
CLINVAR_API_URL = os.getenv("CLINVAR_API_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("clinvar-agent")
