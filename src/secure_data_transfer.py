import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class EncryptionProtocol(Enum):
    TLS = "tls"

@dataclass
class User:
    id: int
    role: str

@dataclass
class Data:
    content: str
    encryption_protocol: EncryptionProtocol

class SecureDataTransfer:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.data: Dict[int, Data] = {}

    def add_user(self, user: User):
        self.users[user.id] = user

    def add_data(self, data_id: int, data: Data):
        self.data[data_id] = data

    def transfer_data(self, sender_id: int, receiver_id: int, data_id: int) -> str:
        if sender_id not in self.users or receiver_id not in self.users:
            raise ValueError("Sender or receiver not found")

        if data_id not in self.data:
            raise ValueError("Data not found")

        data = self.data[data_id]
        encrypted_data = self._encrypt_data(data.content, data.encryption_protocol)
        return encrypted_data

    def _encrypt_data(self, content: str, encryption_protocol: EncryptionProtocol) -> str:
        # Simulate encryption using TLS
        return f"TLS:{content}"

    def authenticate(self, user_id: int, role: str) -> bool:
        if user_id not in self.users:
            return False

        return self.users[user_id].role == role

    def authorize(self, user_id: int, data_id: int) -> bool:
        if user_id not in self.users or data_id not in self.data:
            return False

        return True
