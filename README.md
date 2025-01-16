# short.ly

# Features
- [x] User signup
- [x] Auth
- [x] Create, read, update user's information
- [x] Password Change
- [x] Create, Read, Update, Delete Shortened URL
- [x] Custom short codes for shortened URLs
- [x] A public API that redirects to a long URL using a short code.
- [ ] QR codes with encoded shortened URLs
- [ ] Analytics
  - [ ] Top performing Date ( The date when the user had the most clicks and scans ) 
  - [ ] Clicks + scans by device
  - [ ] Clicks + scans over time
  - [ ] Top-Performing Location (The location with the highest number of scans)
  - [ ] Clicks + scans by location 

# Setup
**Note that the setup assumes you are using any Linux distribution**
### 1. Clone the project:
```bash
git clone https://github.com/GhostMEn20034/short-ly.git
```
### 2. Change permissions for `init-database.sh`:
```bash
chmod +x init-database.sh
```
### 3. Create a `.env` file, using the following command:
```bash
touch .env
```
### 4. Open the file created above in whatever editor you want
### 5. Insert the next variables:
```bash
DB_CONNECTION_STRING=postgresql+asyncpg://<SQL_USER>:<SQL_PASSWORD>@db:5432/<SQL_DATABASE>
SQL_USER=your_db_user
SQL_PASSWORD=your_db_password
SQL_DATABASE=your_database_name
SUPER_USER_PWD=your_postgres_user_password
JWT_SECRET_KEY=your_jwt_secret key # Secret key required for signing JWT Tokens, you can generate it on https://jwtsecret.com/generate
REDIS_HOST=redis # If you use docker compose to run the app, then the specified value must be "redis"
REDIS_PASSWORD=your_redis_pwd # if you use docker compose, it's not necessary to include the variable into this file
REDIS_PORT=your_redis_port # It’s not necessary to include the value if the port of your redis db is 6379
```
# Running the App
### 1. Make sure you are in the root project directory and the `.env` file is populated.
### 2. Use the following command to run the app:
```bash
docker compose up -d --build
```
### 3. Go to [localhost:8000](http://localhost:8000)

# Running integration tests
### 1. Make sure you are in the root project directory.
### 2. Create env file with the name `.env.test`:
```bash
touch .env.test
```
### 3. Open the file in any editor and paste the same variables as in `.env.test` file:
```bash
DB_CONNECTION_STRING=postgresql+asyncpg://<SQL_USER>:<SQL_PASSWORD>@db:5432/<SQL_DATABASE>
SQL_USER=your_db_user
SQL_PASSWORD=your_db_password
SQL_DATABASE=your_database_name
SUPER_USER_PWD=your_postgres_user_password
JWT_SECRET_KEY=your_jwt_secret key # Secret key required for signing JWT Tokens, you can generate it on https://jwtsecret.com/generate
REDIS_HOST=redis # If you use docker compose to run the app, then the specified value must be "redis"
REDIS_PASSWORD=your_redis_pwd # if you use docker compose, it's not necessary to include the variable into this file
REDIS_PORT=your_redis_port # It’s not necessary to include the value if the port of your redis db is 6379
```
### 4. Use the following command to run containers:
```
docker-compose -f docker-compose-test.yml --env-file .env.test up --build
```
### 5. Create another terminal session and get into a Docker container's shell using command:
```shell
docker exec -it fastapi_url_fold_test sh
```
### 6. Inside the container enter the command:
```shell
pytest -v --tb=short --disable-warnings ./tests/integration/
```

### 7. After the tests' execution, switch back to the first session and click `Ctrl + C` to stop containers

# Running unit tests
**Note:**
- **To run unit tests you don't need docker containers** <br/>
- **You can just create a virtual environment using venv or conda for example**
#### **If you want to run unit tests in virtual environment, you also need to install all dependencies using command:**
```shell
pip install -r requirements.txt
```
### 1. Command to run unit tests:
```shell
pytest -v --tb=short --disable-warnings ./tests/unit/
```