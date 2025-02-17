from prometheus_client import start_http_server, Histogram, Counter

SPEECH_RECOGNITION_ERRORS = Counter(
    'speech_recognition_errors_total',
    'Total speech recognition errors',
    ['error_type']
)
CALL_DURATION = Histogram(
    'call_duration_seconds',
    'Total call duration'
)
STATE_TRANSITIONS = Counter(
    'state_transitions_total',
    'State machine transitions',
    ['from_state', 'to_state']
)

def start_monitoring():
    start_http_server(9100)
