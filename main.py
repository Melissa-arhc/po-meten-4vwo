from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hallo ik ben Melissa!'


app.run(host='0.0.0.0', port=81)