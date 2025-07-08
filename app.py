from julep import Julep
import os
from dotenv import load_dotenv
from flask import Flask
from typing import cast, Literal

load_dotenv()

# Explicitly set static_folder (default is 'static')
app = Flask(__name__, static_folder='static')

env = os.getenv('JULEP_ENVIRONMENT', 'production')
if env not in ['production', 'dev', 'local_multi_tenant', 'local']:
    env = 'production'
client = Julep(
    api_key=os.getenv('JULEP_API_KEY'),
    environment=cast(Literal['production', 'dev', 'local_multi_tenant', 'local'], env)
)

# Test connection
agent = client.agents.create(
    name="Test Agent",
    model="claude-3.5-haiku",
    about="A test agent"
)
print(f"Successfully created agent: {agent.id}")