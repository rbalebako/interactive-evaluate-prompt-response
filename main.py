
import os
import singlepromptmetrics
from flask import Flask, render_template, request

app = Flask(__name__)


## TODO https://stackoverflow.com/questions/22463939/demystify-flask-app-secret-key
#import secrets
#foo = secrets.token_urlsafe(16)
#app.secret_key = foo

#all_queries = list()

# TODO this probably doesn't need to be it's own function
# Request the evaluation results 
def get_eval_results(bad_string, good_string):
    return singlepromptmetrics.run_all_evaluations(bad_string, good_string)


# the home page has a form and we do stuff when there is a POST
@app.route('/', methods=['GET', 'POST'])
def index():
    bad_response = "this is a sample string to evaluate"
    if request.method == 'POST':
        bad_response = request.form['bad_response']
        good_response = request.form['good_response']
        #all_queries.append(bad_response)
        results = get_eval_results(bad_response, good_response)
        return render_template('index.html', results=results, eval_string=bad_response)
    return render_template('index.html', results="", eval_string="")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    #app.run(host="0.0.0.0", port=8080)



