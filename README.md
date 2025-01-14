
---

# **National ID Validation API**
This project provides an API for validating and extracting information from Egyptian National IDs. It includes features like rate limiting, logging, testing capabilities, and **service-to-service authentication using API keys**. Redis is used for caching and rate limiting.

---

## **Features**
1. **Validate National IDs**:
   - Ensures IDs are 14 digits long and contain valid information (birth date, governorate, etc.).
   
2. **Extract Information**:
   - Extracts details such as birth date, gender, and governorate from the National ID.

3. **Rate Limiting**:
   - Prevents excessive requests from the same client using Redis as a backend.

4. **API Call Logging**:
   - Logs details of every API call for tracking and debugging purposes.

5. **Service-to-Service Authentication**:
   - Secures communication between services using API keys validated at the middleware level.

6. **Testing**:
   - Includes unit, integration, and load tests using Django’s test suite and Locust.

---

## **System Requirements**
1. **Python**: Version 3.8 or higher.
2. **Redis**: Required for caching and rate limiting.
3. **Django**: Version 4.x.
4. **Windows OS**: (Windows 10 or higher recommended).

---

## **Project Structure**
```
project_root/
├── national_id/                 # App for National ID-related logic
│   ├── views.py                 # API views
│   ├── serializers.py           # DRF serializers
│   ├── models.py                # Database models
│   ├── services.py              # Business logic for National ID validation
│   ├── validators.py            # Validation logic for National IDs
│   ├── urls.py                  # App-specific URLs
│   ├── tests.py                 # Unit and integration tests
│   ├── rate_limiting.py         # Rate limiter utility
│   ├── exceptions.py            # Custom exceptions
│   ├── middlewares.py           # Middleware for API key validation
├── config/                      # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URLs file
│   ├── wsgi.py                  # WSGI entry point
│   ├── asgi.py                  # ASGI entry point
├── locustfile.py                # Load testing file
├── manage.py                    # Django management script
```

---

## **Installation and Setup (Windows)**

### **1. Install Python**
1. Download Python 3.8+ from the [official Python website](https://www.python.org/).
2. During installation:
   - Check the box **Add Python to PATH**.
   - Complete the installation.

### **2. Install Redis**
1. Download Redis for Windows from the [Microsoft archive](https://github.com/microsoftarchive/redis/releases).
2. Extract the files and navigate to the folder in your terminal.
3. Start the Redis server:
   ```bash
   redis-server.exe
   ```

### **3. Clone the Repository**
1. Open a terminal and clone the repository:
   ```bash
   git clone <repository_url>
   cd project_root/
   ```

### **4. Create a Virtual Environment**
1. Create the virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

### **5. Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **6. Apply Migrations**
Set up the database by applying migrations:
```bash
python manage.py migrate
```

### **7. Seed API Keys**
Use the following command to create API keys for testing:
```bash
python manage.py seed_apikeys
```

Example output:
```
Creating API keys...
Service: Service 1, Key: 123e4567-e89b-12d3-a456-426614174000, Active: True
Service: Service 2, Key: 987e6543-b21a-45d3-bcda-123456789abc, Active: True
Successfully seeded API keys.
```

### **8. Start the Django Server**
Run the Django development server:
```bash
python manage.py runserver
```

- The API will now be accessible at: `http://127.0.0.1:8000`

Here's the adjusted and more detailed version of the **API Endpoints** section, including step-by-step instructions for adding the API key in Postman:

---

## **API Endpoints**

### **1. Validate National ID**
This endpoint validates a given Egyptian National ID and extracts information such as birth date, gender, and governorate.

#### **Endpoint Details**
- **URL**: `/api/v1/validate-id/`
- **Method**: `POST`
- **Headers**:
  ```text
  X-API-KEY: 7522bd82-0454-4818-ae06-48166cbd166d
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
      "national_id": "29801130102345"
  }
  ```

---

### **Step-by-Step Instructions for Using Postman**

1. **Open Postman**:
   - If you don’t have Postman, download it from [here](https://www.postman.com/downloads/) and install it.

2. **Create a New Request**:
   - Click the **`+`** button in the top-left corner to create a new request.
   - Set the method to `POST` and enter the URL:
     ```
     http://127.0.0.1:8000/api/v1/validate-id/
     ```

3. **Add Headers**:
   - Navigate to the **`Headers`** tab in Postman.
   - Add the following key-value pairs:
     | Key           | Value                                      |
     |---------------|--------------------------------------------|
     | `X-API-KEY`   | `7522bd82-0454-4818-ae06-48166cbd166d`    |
     | `Content-Type`| `application/json`                        |

4. **Add the Request Body**:
   - Navigate to the **`Body`** tab in Postman.
   - Select the **`raw`** option.
   - Choose `JSON` from the dropdown next to it.
   - Enter the following JSON:
     ```json
     {
         "national_id": "29801130102345"
     }
     ```

5. **Send the Request**:
   - Click the **`Send`** button.
   - Postman will send the request to the server.

6. **View the Response**:
   - If the request is successful, you’ll see a `200 OK` response with the extracted information:
     ```json
     {
         "birth_date": "1998-01-13",
         "governorate": "Cairo",
         "gender": "Female",
         "serial_number": "0234",
         "checksum": 5
     }
     ```
   - If the request is invalid (e.g., missing or incorrect API key), you’ll see an error response:
     - **Missing API Key** (`401 Unauthorized`):
       ```json
       {
           "error": "API key is missing."
       }
       ```
     - **Invalid API Key** (`403 Forbidden`):
       ```json
       {
           "error": "Invalid or inactive API key."
       }
       ```

---

### **Testing with API Key in Postman**

The hardcoded API key `7522bd82-0454-4818-ae06-48166cbd166d` is ready to use. Follow the steps above, and you’ll be able to test the API quickly and easily.
---

## **Service-to-Service Authentication**

### **How It Works**
1. Every service must include a valid `X-API-KEY` header when making a request.
2. API keys are validated globally using middleware before the request reaches the view.
3. If the key is missing, invalid, or inactive, the request is rejected.

---

## **Testing**

### **1. Unit and Integration Tests**
Run the Django test suite:
```bash
python manage.py test
```

### **2. Load Testing with Locust**

#### **Step 1: Install Locust**
Install Locust using pip:
```bash
pip install locust
```

#### **Step 2: Run Locust**
Run Locust for load testing:
```bash
locust -f locustfile.py --host=http://127.0.0.1:8000
```

#### **Step 3: Access Locust Web Interface**
1. Open your browser and go to `http://127.0.0.1:8089`.
2. Configure:
   - **Number of users**: Total simulated users (e.g., 100).
   - **Spawn rate**: Users spawned per second (e.g., 10).
3. Start the test to generate traffic on the `/api/v1/validate-id/` endpoint.

---

## **Redis Usage**

### **1. Start Redis**
Make sure Redis is running by executing:
```bash
redis-server.exe
```

### **2. Check Redis Keys**
Inspect Redis keys using the Redis CLI:
```bash
redis-cli.exe keys *
```

### **3. Clear Redis Cache**
To clear Redis cache:
```bash
redis-cli.exe FLUSHALL
```

---

## **Environment Recap**
1. **Redis**: Run `redis-server.exe` in one terminal.
2. **Django**: Run `python manage.py runserver` in another terminal.
3. **Locust (optional)**: Run `locust -f locustfile.py` in a third terminal for load testing.

---