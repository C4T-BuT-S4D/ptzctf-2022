import dataclasses
import json
from typing import Optional, List

import redis
from dataclasses import dataclass


@dataclass
class Note:
    id: str
    name: str
    content: str
    author: str


class DB:
    def __init__(self, redis_cli: redis.Redis):
        self.redis_cli = redis_cli

    def _get_user_password(self, username: str) -> Optional[str]:
        pbytes = self.redis_cli.hget('users', username)
        if pbytes:
            return pbytes.decode()
        return pbytes

    def user_exists(self, username: str) -> bool:
        return self._get_user_password(username) is not None

    def validate_user_credentials(self, username: str, password: str) -> bool:
        up = self._get_user_password(username)
        if up is None:
            return False
        return up == password

    def save_user(self, username: str, password: str):
        self.redis_cli.hset('users', username, password)

    def save_note(self, user_id: str, note: Note):
        serialized = json.dumps(dataclasses.asdict(note))
        self.redis_cli.rpush('notes|' + user_id, serialized)
        self.redis_cli.hset('notes', note.id, serialized)

    def get_note(self, note_id: str) -> Optional[Note]:
        serialized_note = self.redis_cli.hget('notes', note_id)
        if serialized_note is None:
            return None
        return Note(**json.loads(serialized_note))

    def get_user_notes(self, user_id: str) -> List[Note]:
        return [Note(**json.loads(n)) for n in self.redis_cli.lrange('notes|' + user_id, 0, -1)]
