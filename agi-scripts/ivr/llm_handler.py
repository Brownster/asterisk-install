import json
from llm.llm_client import LLMClient, TooManyRequests

class LLMHandler:
    def __init__(self):
        self.llm = LLMClient()

    def get_response(self, prompt):
        try:
            response = self.llm.get_response(prompt)
            content = response.get('text', '{}')
            if content.strip().startswith('{') and content.strip().endswith('}'):
                structured = json.loads(content)
            else:
                structured = {'message': content}
            return structured
        except json.JSONDecodeError:
            return {"message": "Sorry, I didn't understand."}
        except Exception as e:
            return {"message": f"Error processing request: {e}"}
