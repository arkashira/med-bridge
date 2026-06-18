from src.secure_data_transfer import SecureDataTransfer, User, Data, EncryptionProtocol

def test_add_user():
    secure_data_transfer = SecureDataTransfer()
    user = User(1, "healthcare_professional")
    secure_data_transfer.add_user(user)
    assert secure_data_transfer.users[1].role == "healthcare_professional"

def test_add_data():
    secure_data_transfer = SecureDataTransfer()
    data = Data("Hello, World!", EncryptionProtocol.TLS)
    secure_data_transfer.add_data(1, data)
    assert secure_data_transfer.data[1].content == "Hello, World!"

def test_transfer_data():
    secure_data_transfer = SecureDataTransfer()
    user1 = User(1, "healthcare_professional")
    user2 = User(2, "patient")
    secure_data_transfer.add_user(user1)
    secure_data_transfer.add_user(user2)
    data = Data("Hello, World!", EncryptionProtocol.TLS)
    secure_data_transfer.add_data(1, data)
    encrypted_data = secure_data_transfer.transfer_data(1, 2, 1)
    assert encrypted_data == "TLS:Hello, World!"

def test_authenticate():
    secure_data_transfer = SecureDataTransfer()
    user = User(1, "healthcare_professional")
    secure_data_transfer.add_user(user)
    assert secure_data_transfer.authenticate(1, "healthcare_professional") == True
    assert secure_data_transfer.authenticate(1, "patient") == False

def test_authorize():
    secure_data_transfer = SecureDataTransfer()
    user = User(1, "healthcare_professional")
    secure_data_transfer.add_user(user)
    data = Data("Hello, World!", EncryptionProtocol.TLS)
    secure_data_transfer.add_data(1, data)
    assert secure_data_transfer.authorize(1, 1) == True
    assert secure_data_transfer.authorize(2, 1) == False
