import json
from pathlib import Path
from typing import Dict, Any, Optional

import requests

def append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def push_to_firebase(
    firebase_db_url: str,
    collection: str,
    record: Dict[str, Any],
    auth_token: Optional[str] = None
) -> int:
    """
    Push a record to Firebase Realtime Database.
    firebase_db_url example: https://YOUR-PROJECT-ID.firebaseio.com
    It will POST to: /<collection>.json
    """
    url = f"{firebase_db_url.rstrip('/')}/{collection}.json"
    params = {"auth": auth_token} if auth_token else None
    r = requests.post(url, json=record, params=params, timeout=15)
    return r.status_code

