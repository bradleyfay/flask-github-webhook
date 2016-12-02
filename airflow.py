from flask import Flask
app = Flask(__name__)

@app.route('/gitpush', methods=['POST'])
def deploy():
    if request.method == 'POST':
        d
    else:
        



