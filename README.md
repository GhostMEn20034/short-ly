# short.ly
# Running the App
### 1. Make sure you are in the root project directory.
### 2. Use the following command to run the app:
```bash
docker compose up -d --build
```
### 3. Go to [localhost:8000](http://localhost:8000)

# Running tests
### 1. Make sure you are in the root project directory.
### 2. Create env file with the name `.env.test`:
```bash
touch .env.test
```
### 3. Open the file in any editor and paste the same variables as in `.env` file:
```bash
Values will be provided later
```
### 4. Use the following command to run tests:
```
docker-compose -f docker-compose-test.yml --env-file .env.test up --build
```
### 5. After the tests' execution, click `Ctrl + C` to stop containers