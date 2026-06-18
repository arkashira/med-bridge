from med_bridge import MedBridge, User, UserType, Data

def test_add_user():
    med_bridge = MedBridge()
    user = User(1, "John Doe", UserType.HEALTHCARE_PROFESSIONAL)
    med_bridge.add_user(user)
    assert user.id in med_bridge.users

def test_add_data():
    med_bridge = MedBridge()
    data = Data(1, "Hello World")
    med_bridge.add_data(data)
    assert data.id in med_bridge.data

def test_encrypt_data():
    med_bridge = MedBridge()
    data = Data(1, "Hello World")
    med_bridge.add_data(data)
    assert med_bridge.encrypt_data(1) == True
    assert med_bridge.data[1].encrypted == True

def test_authenticate():
    med_bridge = MedBridge()
    user = User(1, "John Doe", UserType.HEALTHCARE_PROFESSIONAL)
    med_bridge.add_user(user)
    assert med_bridge.authenticate(1, UserType.HEALTHCARE_PROFESSIONAL) == True
    assert med_bridge.authenticate(2, UserType.HEALTHCARE_PROFESSIONAL) == False

def test_authorize():
    med_bridge = MedBridge()
    user = User(1, "John Doe", UserType.HEALTHCARE_PROFESSIONAL)
    med_bridge.add_user(user)
    data = Data(1, "Hello World")
    med_bridge.add_data(data)
    assert med_bridge.authorize(1, 1) == True
    assert med_bridge.authorize(2, 1) == False

def test_transfer_data():
    med_bridge = MedBridge()
    sender = User(1, "John Doe", UserType.HEALTHCARE_PROFESSIONAL)
    med_bridge.add_user(sender)
    receiver = User(2, "Jane Doe", UserType.PATIENT)
    med_bridge.add_user(receiver)
    data = Data(1, "Hello World")
    med_bridge.add_data(data)
    assert med_bridge.transfer_data(1, 2, 1) == '{"data_id": 1, "receiver_id": 2}'
    assert med_bridge.transfer_data(2, 1, 1) == None
