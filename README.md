# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

# Getting Started

## Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

### BACKEND

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running the server :

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

### FRONTEND

#### Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: **npm i** is shorthand for **npm install**

#### Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Testing

To run the tests, run

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

# API References

## Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

## Error Handling

- Errors are returned as JSON objects in the following format:

```
{
   "success": False,
   "error": 400,
   "message": "bad request"
}
```

- The API will return three error types when requests fail:

```
   400: Bad Request
   404: Resource Not Found
   422: Not Processable
```

## Endpoints Library

### GET /categories

- General:
  - Returns a list of category objects, success value, and total number of categories
- Sample: `curl http://127.0.0.1:5000/categories`

```
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

### GET /questions

- General:
  - Returns a list of question objects, list of categories, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    ...
  ],
  "success": true,
  "total_questions": 18
}
```

### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and success value
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

```
{
  "deleted_question_id": 2,
  "success": true
  "total_questions": 18
}
```

### POST /questions/

- General: This endpoint either creates a new question or returns search results.

  - Searches for questions using search term in JSON request parameters.
    - Returns JSON object with paginated matching questions.
  - Creates a new qurstion using the submitted question, answer, difficulty and category.
    - Returns the id of the created question, success value, total questions, and questions list based on current page number to update the frontend.

- sample `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d "{\"searchTerm\":\"which\"}"`

```
{
  "questions": [
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
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type:application/json" -d "{\"question\":\"What are you doing?\", \"answer\":\"Playing\", \"difficulty\":\"1\", \"category\":\"1\"}"`

```
{
  "new question id": 36,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    ...
  ],
  "success": true,
  "total_questions": 16
}
```

### GET /categories/{category_id}/questions

- General:

  - Returns a list of questions objects, current category, success value, and total number of questions
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

```
{
  "category_questions": 4,
  "current_category": "Science",
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
      "answer": "Elsayed",
      "category": 1,
      "difficulty": 1,
      "id": 36,
      "question": "Who are you?"
    }
  ],
  "success": true,
  "total_questions": 16
}
```

### POST /quizzes

- General:

  - Returns a random questions objects and success value

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type:application/json" -d "{\"previous_questions\": [], \"quiz_category\": {\"type\": \"Sports\", \"id\": \"6\"}}"`

```
{
  "question": {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  "success": true
}
```

# Authors

Abd El Rahman Ashraf authored the API (`__init__.py`), test suite (test_flaskr.py), and this README.
All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/)
