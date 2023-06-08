from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
question_ids = len(satisfaction_survey.questions)


@app.route('/')
def root_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey.html', title=title, instructions=instructions, id=0)



@app.route('/question/<int:id>')
def show_question(id):
    if id == len(responses):
        if id < question_ids:
            question = satisfaction_survey.questions[id]
            return render_template('question.html', id=id, question=question)
        elif id == question_ids:
            return redirect('/thanks')
    flash("Please answer our question in the following order!")
    return redirect('/')


@app.route('/question/<int:id>', methods=['POST'])
def handle_response(id):
    if id == len(responses):
        response = request.form.get('answer')
        responses.append(response)
    return redirect(f'/question/{id + 1}')


@app.route('/thanks')
def thanks():
    
    return render_template('thanks.html')