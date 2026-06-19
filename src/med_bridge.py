import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class EncryptionMethod(Enum):
    AES = "AES"
    RSA = "RSA"

@dataclass
class MedicalRecord:
    patient_id: str
    data: str

class MedBridge:
    def __init__(self):
        self.records = {}

    def upload_record(self, patient_id: str, data: str, encryption_method: EncryptionMethod):
        self.records[patient_id] = MedicalRecord(patient_id, self.encrypt(data, encryption_method))

    def download_record(self, patient_id: str, encryption_method: EncryptionMethod):
        if patient_id in self.records:
            return self.decrypt(self.records[patient_id].data, encryption_method)
        else:
            raise ValueError("Patient record not found")

    def encrypt(self, data: str, encryption_method: EncryptionMethod):
        if encryption_method == EncryptionMethod.AES:
            # Simulate AES encryption
            return data + "_encrypted"
        elif encryption_method == EncryptionMethod.RSA:
            # Simulate RSA encryption
            return data + "_rsa_encrypted"

    def decrypt(self, data: str, encryption_method: EncryptionMethod):
        if encryption_method == EncryptionMethod.AES:
            # Simulate AES decryption
            return data.replace("_encrypted", "")
        elif encryption_method == EncryptionMethod.RSA:
            # Simulate RSA decryption
            return data.replace("_rsa_encrypted", "")

    def authenticate(self, username: str, password: str, mfa_code: str):
        # Simulate authentication
        return username == "admin" and password == "password" and mfa_code == "123456"

    def get_status(self, patient_id: str):
        if patient_id in self.records:
            return "Record uploaded successfully"
        else:
            return "Record not found"

    def ensure_hipaa_compliance(self, data: str):
        # Simulate HIPAA compliance check
        return data.replace("sensitive_data", "redacted")
