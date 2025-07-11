import os
import json
import uuid
from datetime import datetime
import pickle

CONV_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log', 'conversations')
os.makedirs(CONV_DIR, exist_ok=True)

# Conversation file structure:
# {
#   "id": str,
#   "title": str,
#   "created_at": str,
#   "messages": list of {role, content, timestamp},
#   "uploads": list of {filename, metadata}
# }

def _conv_path(conv_id):
    return os.path.join(CONV_DIR, f"{conv_id}.json")

def list_conversations():
    """Return a list of all saved conversations (id, title, created_at)."""
    convs = []
    for fname in os.listdir(CONV_DIR):
        if fname.endswith('.json'):
            try:
                with open(os.path.join(CONV_DIR, fname), 'r') as f:
                    data = json.load(f)
                    convs.append({
                        'id': data.get('id'),
                        'title': data.get('title'),
                        'created_at': data.get('created_at')
                    })
            except Exception:
                continue
    # Sort by created_at descending
    return sorted(convs, key=lambda x: x['created_at'], reverse=True)

def load_conversation(conv_id):
    """Load a conversation by id."""
    try:
        with open(_conv_path(conv_id), 'r') as f:
            return json.load(f)
    except Exception:
        return None

def save_conversation(conv):
    """Save a conversation dict to disk."""
    with open(_conv_path(conv['id']), 'w') as f:
        json.dump(conv, f, indent=2)

def delete_conversation(conv_id):
    """Delete a conversation by id."""
    try:
        os.remove(_conv_path(conv_id))
        return True
    except Exception:
        return False

def new_conversation(title=None):
    """Create a new conversation dict."""
    now = datetime.now().isoformat(timespec='seconds')
    conv_id = str(uuid.uuid4())
    return {
        'id': conv_id,
        'title': title or f"Chat {now[:10]}",
        'created_at': now,
        'messages': [],
        'uploads': []
    }

def get_chat_context_path(chat_id):
    dir_path = os.path.join(os.path.dirname(__file__), '..', 'log', 'conversations', chat_id)
    os.makedirs(dir_path, exist_ok=True)
    return os.path.join(dir_path, 'context.pkl')

def save_chat_context(chat_id, context):
    path = get_chat_context_path(chat_id)
    with open(path, 'wb') as f:
        pickle.dump(context, f)

def load_chat_context(chat_id):
    path = get_chat_context_path(chat_id)
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return pickle.load(f)

def delete_chat_context(chat_id):
    path = get_chat_context_path(chat_id)
    if os.path.exists(path):
        os.remove(path) 