 # Tech-Spec.md

## Stack
- Language: TypeScript for a modern and scalable approach, with strong support for web and Node.js.
- Framework: Express.js for building the API, providing a minimal and flexible foundation.
- Runtime: Node.js for server-side execution, ensuring compatibility with a wide range of operating systems.

## Hosting
- Free-tier-first: Initially, host on AWS Amplify, utilizing their free tier to minimize costs during the MVP phase.
- Specific Platforms: AWS Elastic Beanstalk for production deployment, providing scalability and reliability.

## Data Model
- Tables/Collections:
  - Users (id, username, password_hash, email, role, location)
  - HealthcareProfessionals (id, user_id, specialty, hospital_name)
  - Patients (id, user_id, age, gender, medical_history)
  - MedicalData (id, patient_id, data_type, data)

- Key Fields:
  - `id`: Unique identifier for each entity.
  - `user_id`: Foreign key linking users to healthcare professionals and patients.
  - `data_type`: A field to categorize the medical data (e.g., X-ray, MRI, lab results).

## API Surface
- Endpoints (5-10):
  1. `POST /auth/register`: Register a new user.
  2. `POST /auth/login`: Authenticate a user.
  3. `GET /healthcare-professionals`: Retrieve a list of healthcare professionals.
  4. `GET /healthcare-professionals/:id`: Retrieve a specific healthcare professional.
  5. `GET /patients`: Retrieve a list of patients.
  6. `GET /patients/:id`: Retrieve a specific patient.
  7. `POST /medical-data`: Upload medical data for a patient.
  8. `GET /medical-data/:id`: Retrieve a specific medical data item.
  9. `GET /medical-data/:patient_id`: Retrieve all medical data for a patient.
  10. `GET /medical-data/:patient_id/:data_type`: Retrieve all data of a specific type for a patient.

## Security Model
- Auth: Implement JWT-based authentication for user sessions.
- Secrets: Store sensitive data (e.g., API keys) in AWS Secrets Manager.
- IAM: Utilize AWS IAM policies to control access to resources.

## Observability
- Logs: Use AWS CloudWatch for centralized logging and monitoring.
- Metrics: Implement custom metrics using AWS CloudWatch and Prometheus for monitoring application performance.
- Traces: Use Jaeger for distributed tracing to debug and optimize the system.

## Build/CI
- Use AWS CodePipeline for continuous integration and deployment.
- Leverage AWS CodeBuild for building and testing the application.
- Utilize Docker for containerization and consistent environment setup.