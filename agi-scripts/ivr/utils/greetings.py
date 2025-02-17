import yaml
from datetime import datetime

def load_greetings(config_path='config/greetings.yml'):
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return data.get('greetings', {})

def select_greeting(caller_type='external'):
    greetings = load_greetings()
    now = datetime.now()
    if now.hour < 12:
        time_of_day = 'morning'
    elif now.hour < 18:
        time_of_day = 'afternoon'
    else:
        time_of_day = 'evening'
    return greetings.get(caller_type, {}).get(time_of_day, "Hello, how can I help you?")
