from med_bridge import MedBridge, ConsentForm

def test_create_consent_form():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = ["signatory1", "signatory2"]
    consent_form = med_bridge.create_consent_form(patient_id, form_id, signatories)
    assert consent_form.patient_id == patient_id
    assert consent_form.form_id == form_id
    assert consent_form.signatories == signatories

def test_sign_consent_form():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = ["signatory1", "signatory2"]
    med_bridge.create_consent_form(patient_id, form_id, signatories)
    signed_form = med_bridge.sign_consent_form(form_id, signatories[0])
    assert signed_form == '{"signatory": "signatory1", "timestamp": "2024-09-16T14:30:00"}'

def test_get_consent_form_status():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = ["signatory1", "signatory2"]
    med_bridge.create_consent_form(patient_id, form_id, signatories)
    status = med_bridge.get_consent_form_status(form_id)
    assert status == "pending"
    med_bridge.sign_consent_form(form_id, signatories[0])
    status = med_bridge.get_consent_form_status(form_id)
    assert status == "signed"

def test_notify_signatories():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = ["signatory1", "signatory2"]
    med_bridge.create_consent_form(patient_id, form_id, signatories)
    med_bridge.notify_signatories(form_id)
    # No assertion, just checking that it runs without error

def test_create_consent_form_edge_case():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = []
    consent_form = med_bridge.create_consent_form(patient_id, form_id, signatories)
    assert consent_form.patient_id == patient_id
    assert consent_form.form_id == form_id
    assert consent_form.signatories == signatories

def test_sign_consent_form_edge_case():
    med_bridge = MedBridge()
    patient_id = "patient1"
    form_id = "form1"
    signatories = ["signatory1", "signatory2"]
    med_bridge.create_consent_form(patient_id, form_id, signatories)
    try:
        med_bridge.sign_consent_form(form_id, "unauthorized_signatory")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Signatory not authorized"
