from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'guess_secret_key'  # Required for session handling

@app.route('/', methods=['GET', 'POST'])
def game():
    # Initialize secret number and attempt count
    if 'secret' not in session:
        session['secret'] = random.randint(1, 100)
        session['attempt'] = 0

    message = ''
    if request.method == 'POST':
        try:
            user_guess = int(request.form['number'])
            session['attempt'] += 1

            if user_guess < session['secret']:
                message = "Too low! Try a higher number."
            elif user_guess > session['secret']:
                message = "Too high! Try a lower number."
            else:
                message = f"Correct! The number was {session['secret']}. It took you in {session['attempt']} attempts."
                # Reset game after win
                session.pop('secret', None)
                session.pop('attempt', None)

        except (ValueError, KeyError):
            message = "Please enter a valid number."

    return render_template("index.html", message=message, attempt=session.get('attempt', 0))

if __name__ == '__main__':
    app.run(debug=True)
