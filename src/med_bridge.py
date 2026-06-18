import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class UserType(Enum):
    HEALTHCARE_PROFESSIONAL = 1
    PATIENT = 2

@dataclass
class User:
    id: int
    name: str
    user_type: UserType

@dataclass
class Data:
    id: int
    content: str
    encrypted: bool = False

class MedBridge:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.data: Dict[int, Data] = {}

    def add_user(self, user: User):
        self.users[user.id] = user

    def add_data(self, data: Data):
        self.data[data.id] = data

    def encrypt_data(self, data_id: int):
        if data_id in self.data:
            self.data[data_id].encrypted = True
            return True
        return False

    def authenticate(self, user_id: int, user_type: UserType):
        if user_id in self.users and self.users[user_id].user_type == user_type:
            return True
        return False

    def authorize(self, user_id: int, data_id: int):
        if user_id in self.users and data_id in self.data:
            return True
        return False

    def transfer_data(self, sender_id: int, receiver_id: int, data_id: int):
        if self.authenticate(sender_id, UserType.HEALTHCARE_PROFESSIONAL) and self.authorize(receiver_id, data_id):
            return json.dumps({"data_id": data_id, "receiver_id": receiver_id})
        return None
