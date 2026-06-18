# Med Bridge

A secure data transfer platform for healthcare professionals and patients.

## Features

* Data encryption using industry-standard protocols
* Authentication and authorization for healthcare professionals and patients
* Secure data storage and transfer between parties

## Usage

1. Create a new user: `med_bridge.add_user(User(1, "John Doe", UserType.HEALTHCARE_PROFESSIONAL))`
2. Add data: `med_bridge.add_data(Data(1, "Hello World"))`
3. Encrypt data: `med_bridge.encrypt_data(1)`
4. Authenticate user: `med_bridge.authenticate(1, UserType.HEALTHCARE_PROFESSIONAL)`
5. Authorize user: `med_bridge.authorize(1, 1)`
6. Transfer data: `med_bridge.transfer_data(1, 2, 1)`
