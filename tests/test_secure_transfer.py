import pytest
from secure_transfer import SecureTransferEngine, TransferLog

def test_upload_file():
    engine = SecureTransferEngine("encryption_key")
    with open("test_file.txt", "w") as f:
        f.write("Hello World")
    transfer_log = engine.upload_file("test_file.txt", 1024 * 1024 * 1024)
    assert transfer_log.upload_time > 0
    assert transfer_log.file_size > 0
    assert transfer_log.transfer_time > 0

def test_upload_file_too_large():
    engine = SecureTransferEngine("encryption_key")
    with open("test_file.txt", "w") as f:
        f.write("a" * (1024 * 1024 * 10))  # Smaller file size to avoid MemoryError
    with pytest.raises(ValueError):
        engine.upload_file("test_file.txt", 1024 * 1024)

def test_get_transfer_logs():
    engine = SecureTransferEngine("encryption_key")
    with open("test_file.txt", "w") as f:
        f.write("Hello World")
    engine.upload_file("test_file.txt", 1024 * 1024 * 1024)
    transfer_logs = engine.get_transfer_logs()
    assert len(transfer_logs) == 1

def test_upload_file_non_existent():
    engine = SecureTransferEngine("encryption_key")
    transfer_log = engine.upload_file("non_existent_file.txt", 1024 * 1024 * 1024)
    assert transfer_log is None
