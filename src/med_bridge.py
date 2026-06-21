import json
from dataclasses import dataclass
from typing import List

@dataclass
class ConsentForm:
    patient_id: str
    form_id: str
    signatories: List[str]

class MedBridge:
    def __init__(self):
        self.consent_records = {}
        self.blockchain = {}

    def create_consent_form(self, patient_id: str, form_id: str, signatories: List[str]):
        consent_form = ConsentForm(patient_id, form_id, signatories)
        self.consent_records[form_id] = consent_form
        return consent_form

    def sign_consent_form(self, form_id: str, signatory: str):
        if form_id not in self.consent_records:
            raise ValueError("Consent form not found")
        consent_form = self.consent_records[form_id]
        if signatory not in consent_form.signatories:
            raise ValueError("Signatory not authorized")
        self.blockchain[form_id] = json.dumps({"signatory": signatory, "timestamp": "2024-09-16T14:30:00"})
        return self.blockchain[form_id]

    def get_consent_form_status(self, form_id: str):
        if form_id not in self.consent_records:
            raise ValueError("Consent form not found")
        if form_id in self.blockchain:
            return "signed"
        return "pending"

    def notify_signatories(self, form_id: str):
        if form_id not in self.consent_records:
            raise ValueError("Consent form not found")
        consent_form = self.consent_records[form_id]
        for signatory in consent_form.signatories:
            print(f"Notification sent to {signatory}")
