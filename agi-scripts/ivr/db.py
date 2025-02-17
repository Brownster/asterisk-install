def get_conversation_history(self, caller_cli, limit=10):
    session = self.get_session()
    try:
        entries = session.query(ChatHistory)\
            .filter_by(caller_cli=caller_cli)\
            .order_by(ChatHistory.timestamp.asc())\
            .limit(limit).all()
        history = []
        for entry in entries:
            history.append({
                "role": entry.role,
                "message": entry.message,
                "timestamp": entry.timestamp.isoformat() if entry.timestamp else None
            })
        return history
    except Exception as e:
        logger.error(f"Error fetching conversation history for caller {caller_cli}: {e}")
        return []
    finally:
        session.close()
