from flask import Flask
from flask import render_template, redirect, jsonify
import mariadb
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:secret@localhost/skoly'
app.config['SECRET_KEY'] ="super secret key"

config = {
        'user': 'root',
        'password': 'secret',
        'host': 'localhost',
        'port': 3306,
        'database': 'skoly'
    }
connection = mariadb.connect(**config)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)