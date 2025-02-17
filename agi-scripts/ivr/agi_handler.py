from allowed_callers import load_allowed_callers
from utils.greetings import select_greeting

# In your IVRHandler.handle_call() method:
raw_caller_id = self.agi.env.get('agi_callerid', 'UNKNOWN')
caller_id = validate_caller_id(raw_caller_id)

owner_callers = load_owner_callers()  # Loaded from config/owner_callers.yml
allowed_callers = load_allowed_callers()  # Loaded from config/allowed_callers.yml

if caller_id in owner_callers:
    greeting = select_greeting('internal')
    self.agi.verbose(greeting, 3)
    self._handle_owner_caller()
elif caller_id in allowed_callers:
    handle_allowed_caller_conversation(self.agi, self.llm_handler, self.call_id, caller_id)
else:
    handle_unknown_caller(self.agi, self.llm_handler, self.call_id)
