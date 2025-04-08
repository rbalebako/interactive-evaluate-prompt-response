
import os
from flask import Flask, render_template, request

app = Flask(__name__)


## TODO https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key
#import secrets
#foo = secrets.token_urlsafe(16)
#app.secret_key = foo

all_queries = list()

def get_eval_results(eval_string):
    return (4,5,6)



@app.route('/', methods=['GET', 'POST'])
def index():
    eval_string = "this is a sample string to evaluate"
    if request.method == 'POST':
        eval_string = request.form['eval_string']
        all_queries.append(eval_string)
        results = get_eval_results(eval_string)
        return render_template('index.html', results=results, eval_string=eval_string, all_queries=all_queries)
    return render_template('index.html', results=request.method, eval_string=eval_string)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
