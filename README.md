
# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Virtual environment
Create a virtual environment
```bash
python3 -m venv myvenv
source myvenv/bin/activate
```

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```
Populate the database using the `trivia.psql` file provided

```bash
psql trivia < trivia.psql

```
![database](images//database.png)

### Auth0 Setup
### Create Auth0 Application
![application](images//auth0_app.png)

### Create Auth0 API and Permissions
![api_permission](images//auth0_api_permisson.png)

### Create Auth0 Roles and Users
![role](images//auth0_role.png)

Client: 
![client_permisson](images//client_permisson.png)

Employee: 
![employee_permisson](images//employee_permisson.png)
### Run the Server

From within the `./src` directory

To run the server, execute:

```bash
flask run
```

URL backend: http://localhost:5000/

## Test Backend
```bash
dropdb trivia
createdb trivia
psql trivia_test < trivia.psql
python test_flaskr.py
```
Results:
```
.
----------------------------------------------------------------------
Ran 14 tests in 3.597s

```

### Documentation
### API Reference
`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request param: None
- Example reponse:

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

`GET '/questions?page=<page_number>'`
Fetch a pagination dictionary of questions 
- Request param (optional): page:int 
- Example reponse: 
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": 1,
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 22
}

"DELETE '/questions/<int:question_id>'"

- Delete an existing question
- Request param: question_id:int
- Example reponse:

```json
{
    "deleted": 29,
    "success": true,
}
```

`POST '/questions'`

- Create new question
- Request param: {
    "question": string,
    "answer": string,
    "difficulty": int,
    "category": int
}
- Example reponse:

```json
{
    "created": 34,
    "success": true,
}
```
`POST '/questions'`

- Fetches all questions have substring include the search term (not case-sensitive)
- Request param: {
    "searchTerm": string,
}
- Example reponse:

```json
{
    "currentCategory": 1,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

`POST '/categories/<int:category_id>/questions'`

- Fetches all questions for the specified category
- Request param: category_id:int
- Example reponse:

```json
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "123",
            "category": 1,
            "difficulty": 1,
            "id": 34,
            "question": "aloha"
        }
    ],
    "success": true,
    "total_questions": 4
}
```
`POST '/quizzes'`

- Fetch only one random question with a specified category.
- Request param: {
    "previous_questions": array,
    "quiz_category": {
        "type": string,
        "id": number
    }
   }
- Example reponse:

```json
{
    "question": {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "123",
            "category": 1,
            "difficulty": 1,
            "id": 34,
            "question": "aloha"
        }
    ],
    "success": true,
    "total_questions": 4
}
```
The API will return three error types when requests fail:
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Resource Not Found
- `422`: Not Processable
### Users and Roles
`Public`
- Can view all Questions and Categories

`Cilent`
- All permissions a Public user has and…
- Can view questions by categories
- Can play quizzes
- Can search questions by keyword
- Can Create new question

`Employee`
- All permissions a Cilent has and…
- Can delete questions

## Deployment
![render_services](images//render_servers.png)

### Postgres Database
![render_postgres](images//render_postgres.png)

Endpoint: `postgres://macos:Lvqb6jAbNSlbpFbsRkYPpcTeS0tHvR2U@dpg-cki2moke1qns73dbmfa0-a/drink_41ri`

### Server
![render_server](images//render_server.png)

Endpoint Render: https://render-travia-app.onrender.com
- Token experience time: 24h
- Token cilent 1
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0NTM0MDdjNDAzZGRlNmEyNWYzMzEiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5OTMzOTEsImV4cCI6MTY5OTA3OTc5MSwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpjYXRlZ29yaWVzLWNhdGVnb3J5X2lkLXF1ZXN0aW9ucyIsInBhdGNoOnF1aXp6ZXMiLCJwb3N0OnF1ZXN0aW9ucyJdfQ.NoNvpHaagzTGdGTOsvgY_x2I_yzKWxlrN_RWSuZco9F6aiZJhBozywbaSO3Vampic3c2_eeaB3FOlHkrabEWV6u51pBPMc8qG2Xaz668nqGvFsiLY_RPE7s8igmNP5nsByCnMiQIFOw6zjLAjul70_3HOG44kLpwu-w6U_OnUIHVpKMDQqw-_PbXqU_OiTprt3g9F4vD_wCX1BTPry3yh-IcRGV3BaLSbz5CDDW25fKBusD_1xD2PxMZUvY0h3VZLAz_h4fDXgNujGo_oNeh3T35CLYWukfq2a0kbW9ZkNpokC7k2yHRMCueNQoTTLwxNcOIdWvVSTE_AC5es_aHAA`

- Token employee
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklFSkhReGhnY1BGZVFsRGRKN2R6eSJ9.eyJpc3MiOiJodHRwczovL2Rldi1pMWRicW9oMWs1c2wzdzQxLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTQ0MDIzMWNiYTJmZWEyNjE4ZTMzZDIiLCJhdWQiOiJ0cmF2aWEiLCJpYXQiOjE2OTg5OTM0MzYsImV4cCI6MTY5OTA3OTgzNiwiYXpwIjoiZm83cVlTY0FrRU15SGVKaDUzV0pXajRxTW1YN2MzQ2YiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpxdWVzdGlvbnMiLCJnZXQ6Y2F0ZWdvcmllcy1jYXRlZ29yeV9pZC1xdWVzdGlvbnMiLCJwYXRjaDpxdWl6emVzIiwicG9zdDpxdWVzdGlvbnMiXX0.gwb5dX9G94Qbxkjk5xgxOclLo4KBmP0cujwpfeVr7Kla9V8QFJRKRIc152C3e7L7Tl_3wWGQlIEdYMHeN0rBiF-Y8GlhLU7N8jIDu127sgw7XeYk__ZpWT-0LLSpOIAk5wJkkjo8JbCOvT6NpBxJJuLhe-THm8eSVhbgOIoE_dODzkaC7cLaJu-IsqfOgSKB00CIjw0B8nicF9q-u2FwfGJPgQj82u-6vRbvk07RC82tykMkLMx4QVuU0ipIOr_bz3Uko8K-qV-oe1kkCPLwJEYKcE2P3LXsJGpf6GUGvHdOn8oW7M1jSUY08tP-n7PhTitl-d-rWWqYTriqeIes4w`

### Account manager:
- client1@gmail.com
- Password@client1

- employee@gmail.com
- Password@employee

- Link to get new token with login information :
https://dev-i1dbqoh1k5sl3w41.us.auth0.com/authorize?audience=travia&response_type=token&client_id=fo7qYScAkEMyHeJh53WJWj4qMmX7c3Cf&redirect_uri=https://localhost:8080/login-results
