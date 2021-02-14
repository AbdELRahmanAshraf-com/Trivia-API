#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

#----------------------------------------------------------------------------#
# Helping Methods.
#----------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10
# Pagination Method.


def pagination(lists, request):
    formatted_questions = [list.format() for list in lists]
    page = request.args.get("page", 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start+QUESTIONS_PER_PAGE
    return formatted_questions[start:end]

#----------------------------------------------------------------------------#
# APP.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    #  Setting up CORS and Allowing all of origins.
    CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Using the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        # Set Access Control
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # Getting requests for all available categories.
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        if categories is None or len(categories) == 0:
            abort(404)
        cats = {}
        for cat in categories:
            cats[cat.id] = cat.type
        return jsonify({
            "categories": cats,
            "success": True
        })

   # Getting requests for all questions with pagination.
    @app.route("/questions")
    def get_questions():
        questions = Question.query.all()
        categories = Category.query.all()
        pagination_list = pagination(questions, request)
        if pagination_list is None or len(pagination_list) == 0 or categories is None or len(categories) == 0:
            abort(404)
        cats = {}
        for cat in categories:
            cats[cat.id] = cat.type
        return jsonify({
            "questions": pagination_list,
            "total_questions": len(questions),
            "categories": cats,
            "success": True
        })

    # Deleting question using a question ID.
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            "deleted_question_id": question_id,
            "total_questions": len(Question.query.all()),
            "success": True
        })

    # Creating a new question and get questions based on a search term if found.
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        question = body.get("question")
        answer = body.get("answer")
        category = body.get("category")
        difficulty = body.get("difficulty")
        search_term = body.get("searchTerm")
        if search_term:
            ques = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            formatted_list = pagination(ques, request)
            if formatted_list is None or len(formatted_list) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "questions": formatted_list,
                "total_questions": len(ques)
            })
        else:
            if question and answer and category and difficulty:
                try:
                    question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                    question.insert()
                    return jsonify({
                        "new question id": question.id,
                        "success": True,
                        "questions": pagination(Question.query.all(), request),
                        "total_questions": len(Question.query.all())
                    })
                except:
                    abort(400)
            else:
                abort(422)

    # Getting questions based on category.
    @app.route("/categories/<int:category_id>/questions")
    def get_question_by_category(category_id):
        question = Question.query.filter_by(category=category_id).all()
        category = Category.query.get(category_id)
        formatted_list = pagination(question, request)
        if formatted_list is None or len(formatted_list) == 0:
            abort(404)
        return jsonify({
            "current_category": category.type,
            "questions": formatted_list,
            "total_questions": len(Question.query.all()),
            "category_questions": len(question),
            "success": True
        })

    # Getting questions randomly to play the quiz.
    @app.route("/quizzes", methods=['POST'])
    def get_questions_to_play():
        body = request.get_json()
        pre_ques = body.get("previous_questions")
        category = body.get("quiz_category")
        if category is None:
            abort(400)
        previous_questions = []
        if pre_ques:
            previous_questions = pre_ques
        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category['id']).all()
        random_ques = random.choice(questions)
        if len(previous_questions) == len(questions):
            return jsonify({
                "question": None,
                "success": True
            })
        while random_ques.id in previous_questions:
            random_ques = random.choice(questions)
        previous_questions.append(random_ques.id)
        return jsonify({
            "question": random_ques.format(),
            "success": True
        })

    # Creating error handlers for all expected errors
    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Un Processable Entry"
        }), 422

    return app
