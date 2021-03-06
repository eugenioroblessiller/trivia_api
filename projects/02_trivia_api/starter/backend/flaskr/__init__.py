from crypt import methods
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, Pagination
from flask_cors import CORS
import random

from sqlalchemy.sql.expression import func, select

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin', '*'
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

    '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''

    @app.route('/categories')
    def get_categories():
        selection_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection_categories:
            categories[category.id] = category.type

        return jsonify({'success': True, 'categories': categories})

    '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)

        # ctaegories
        selection_categories = Category.query.order_by(Category.id).all()
        categories = {}
        for category in selection_categories:
            categories[category.id] = category.type
        # questions
        selection = Question.query.order_by(
            Question.id).paginate(page, QUESTIONS_PER_PAGE, False)
        questions = [question.format() for question in selection.items]

        return jsonify({
            'success': True,
            'questions': questions,
            'totalQuestions': len(questions),
            'categories': categories
        })
    '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter_by(
                Question.id == question_id).one_or_none()
            if question is None:
                not_found(404)
            else:
                question.delete()

                selection = Question.query.order_by(
                    Question.id).paginate(1, QUESTIONS_PER_PAGE, False)
                questions = [question.format() for question in selection.items]
                return jsonify({'success': True, 'question': questions})
        except:
            bad_request(400)

    '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        print('some')
        data = request.get_json()
        if data is None:
            abort(422)
        try:
            question = Question(question=data['question'], answer=data['answer'],
                                category=data['category'], difficulty=data['difficulty'])
            question.insert()

            return jsonify({'success': True, 'created_question': question.question})
        except:
            return unprocessable(422)

    '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
    @app.route('/search-questions', methods=['POST'])
    def search_question():
        page = request.args.get('page', 1, type=int)

        data = request.get_json()
        searchTerm = data.get('searchTerm')
        selected_questions = Question.query.filter(
            Question.question.ilike(f'%{searchTerm}%')).paginate(page, QUESTIONS_PER_PAGE, False)
        questions = [question.format()
                     for question in selected_questions.items]

        if questions is None:
            not_found(404)
        else:
            # print('Estas son las preguntas--->', questions)
            return jsonify({'success': True, 'questions': questions, 'total_questions': len(questions)})
    '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        page = request.args.get('page', 1, type=int)

        category = Category.query.filter_by(id=id).one_or_none()
        if category is None:
            not_found(404)
        else:
            selected_questions = Question.query.filter_by(
                category=category.id).paginate(page, QUESTIONS_PER_PAGE, False)
            questions = [question.format()
                         for question in selected_questions.items]

        return jsonify({'success': True, 'question': questions, 'total_questions': len(questions), 'current_category': category.type})

    '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        data = request.get_json()
        # print('data desde el front----->', data)
        previus_question = data.get('previous_questions')
        category = data.get('quiz_category')

        if category is None or previus_question is None:
            unprocessable(422)

        if category['id'] == 0:
            selected_question = select_random_question(category)
        else:
            selected_question = select_random_question(category)

        while (check_if_question_is_use(previus_question, selected_question)):
            selected_question = select_random_question(category)

        return jsonify({'success': True, 'question': selected_question.format()})

    def select_random_question(category):
        if category['id'] == 0:
            selected_question = Question.query.order_by(
                    func.random()).first()
        else:
            selected_question = Question.query.filter_by(
                    category=category['id']).order_by(func.random()).first()
                
        return selected_question

    def check_if_question_is_use(previus_questions, question):
        is_use = False
        for q in previus_questions:
            if q == question.id:
                is_use = True
        print('que tenemos aqui ---->', is_use)
        return is_use

    
    '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
    @app.errorhandler(404)
    def not_found():
        return jsonify({
            'success': True,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(400)
    def bad_request():
        return jsonify({
            'success': True,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(422)
    def unprocessable():
        return jsonify({
            'success': True,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    return app
