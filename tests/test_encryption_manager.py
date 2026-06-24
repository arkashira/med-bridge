from encryption_manager import EncryptionManager, EncryptionKey, AccessControlManager, Logger, AuditReadyEncryption

def test_generate_key():
    encryption_manager = EncryptionManager()
    key = encryption_manager.generate_key("key1")
    assert key.key_id == "key1"
    assert key.key_value == "generated_key_value"

def test_get_key():
    encryption_manager = EncryptionManager()
    encryption_manager.generate_key("key1")
    key = encryption_manager.get_key("key1")
    assert key.key_id == "key1"
    assert key.key_value == "generated_key_value"

def test_delete_key():
    encryption_manager = EncryptionManager()
    encryption_manager.generate_key("key1")
    encryption_manager.delete_key("key1")
    try:
        encryption_manager.get_key("key1")
        assert False
    except ValueError:
        assert True

def test_configure_access():
    access_control_manager = AccessControlManager()
    access_control_manager.configure_access("admin", "read_write")
    assert access_control_manager.get_access_level("admin") == "read_write"

def test_get_access_level():
    access_control_manager = AccessControlManager()
    access_control_manager.configure_access("admin", "read_write")
    assert access_control_manager.get_access_level("admin") == "read_write"

def test_log_activity():
    logger = Logger()
    logger.log_activity("activity1")
    assert logger.get_log() == ["activity1"]

def test_setup_audit_ready_encryption():
    audit_ready_encryption = AuditReadyEncryption()
    audit_ready_encryption.setup_audit_ready_encryption()
    assert audit_ready_encryption.get_encryption_key("key1").key_id == "key1"
    assert audit_ready_encryption.get_access_level("admin") == "read_write"
    assert audit_ready_encryption.get_log() == ["Setup audit ready encryption"]
