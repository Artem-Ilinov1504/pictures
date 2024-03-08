from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///picture.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    picture = db.relationship("Picture", backref="user", uselist=False)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_of_picture = db.Column(db.String(30), nullable=False)
    name_of_picture = db.Column(db.String(40), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


@app.route("/create")
def index():
    user = User(name="Any", surname="body", age=37)
    picture = Picture(type_of_picture="portrait",
                   name_of_picture="My portrait",
                   user=user)

    db.session.add(user)
    db.session.add(picture)
    db.session.commit()

    return "Order is accepted!"


@app.route("/user/<int:user_id>/picture")
def get_document(user_id):
    user = User.query.get_or_404(user_id)
    picture = user.picture
    if picture:
        return f"{picture.id}, {user.name} {user.surname} ,{picture.type_of_picture}, {picture.name_of_picture}"
    else:
        return "You haven't ordered anything yet"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)