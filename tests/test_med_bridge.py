from med_bridge import MedBridge, EncryptionMethod, MedicalRecord

def test_upload_record():
    med_bridge = MedBridge()
    med_bridge.upload_record("patient1", "medical_data", EncryptionMethod.AES)
    assert med_bridge.records["patient1"].data == "medical_data_encrypted"

def test_download_record():
    med_bridge = MedBridge()
    med_bridge.upload_record("patient1", "medical_data", EncryptionMethod.AES)
    assert med_bridge.download_record("patient1", EncryptionMethod.AES) == "medical_data"

def test_download_record_not_found():
    med_bridge = MedBridge()
    try:
        med_bridge.download_record("patient1", EncryptionMethod.AES)
        assert False
    except ValueError as e:
        assert str(e) == "Patient record not found"

def test_authenticate():
    med_bridge = MedBridge()
    assert med_bridge.authenticate("admin", "password", "123456") == True

def test_authenticate_invalid_credentials():
    med_bridge = MedBridge()
    assert med_bridge.authenticate("invalid", "password", "123456") == False

def test_get_status():
    med_bridge = MedBridge()
    med_bridge.upload_record("patient1", "medical_data", EncryptionMethod.AES)
    assert med_bridge.get_status("patient1") == "Record uploaded successfully"

def test_ensure_hipaa_compliance():
    med_bridge = MedBridge()
    data = "sensitive_data"
    assert med_bridge.ensure_hipaa_compliance(data) == "redacted"
