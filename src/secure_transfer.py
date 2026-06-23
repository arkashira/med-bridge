import argparse
import json
import dataclasses
import hashlib
import hmac
import os
import time
from typing import Optional

@dataclasses.dataclass
class TransferLog:
    upload_time: float
    file_size: int
    transfer_time: float

class SecureTransferEngine:
    def __init__(self, encryption_key: str):
        self.encryption_key = encryption_key
        self.transfer_logs = []

    def upload_file(self, file_path: str, connection_speed: int) -> Optional[TransferLog]:
        if not os.path.exists(file_path):
            return None

        file_size = os.path.getsize(file_path)
        upload_time = time.time()
        transfer_time = file_size / connection_speed
        if transfer_time > 30 * (file_size / (1024 * 1024 * 1024)):
            raise ValueError("Upload would take too long")

        # Simulate upload
        time.sleep(transfer_time)

        # Encrypt file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        encrypted_data = hmac.new(self.encryption_key.encode(), file_data, hashlib.sha256).digest()

        # Store transfer log
        transfer_log = TransferLog(upload_time, file_size, transfer_time)
        self.transfer_logs.append(transfer_log)

        return transfer_log

    def get_transfer_logs(self) -> list:
        return self.transfer_logs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-path', required=True)
    parser.add_argument('--connection-speed', type=int, required=True)
    parser.add_argument('--encryption-key', required=True)
    args = parser.parse_args()

    engine = SecureTransferEngine(args.encryption_key)
    transfer_log = engine.upload_file(args.file_path, args.connection_speed)
    if transfer_log:
        print(json.dumps(dataclasses.asdict(transfer_log)))
    else:
        print("Upload failed")

if __name__ == '__main__':
    main()
