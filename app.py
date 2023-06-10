from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


RESPONSES = 'responses'


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

question_ids = len(satisfaction_survey.questions)

@app.route('/')
def root_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey.html', title=title, instructions=instructions)


@app.route('/index', methods = ['POST'])
def index():

    session[RESPONSES] = [] 
    return redirect('/question/0')




@app.route('/question/<int:id>')
def show_question(id):
    responses = session.get(RESPONSES)
    if id == len(responses):
        if id < question_ids:
            question = satisfaction_survey.questions[id]
            return render_template('question.html', id=id, question=question)
        elif id == question_ids:
            return redirect('/thanks')
    flash("Please answer our question in the following order!")
    return redirect('/')


@app.route('/answer', methods=['POST'])
def handle_response():
    response = request.form['answer']
    
    responses = session[RESPONSES]
    responses.append(response)
    session[RESPONSES] = responses

    if len(responses) == question_ids:
        return redirect('/thanks')
    else:
       return redirect(f'/question/{len(responses)}')


@app.route('/thanks')
def thanks():
    print(session[RESPONSES]) 
    return render_template('thanks.html')

