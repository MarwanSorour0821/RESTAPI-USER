from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route("/")
def home():
    return "Hello"

@app.route("/userinfo", methods=['GET'])
def get_user():
    users = User.query.all()
    outputUser = []

    for usr in users:
        userData = {"User name": usr.name, "Description": usr.description}
        outputUser.append(userData)
    return outputUser

@app.route("/userinfo/<id>")
def user(id):
    user = User.query.get_or_404(id)
    return jsonify({"name": user.name, "description": user.description})

@app.route("/userinfo", methods=['POST'])
def add_user():
    data = request.json

    user = User(name=data["name"], description = data["description"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id})

@app.route("/userinfo/<id>", methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return f"User ({id}) has been deleted"

def create_table():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

