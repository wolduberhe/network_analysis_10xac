# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # SQLite database
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Create the database and sample data
with app.app_context():
    db.create_all()
    if not Item.query.first():
        db.session.add(Item(name='Item 1'))
        db.session.add(Item(name='Item 2'))
        db.session.commit()

# Define API route to get data
@app.route('/api/data')
def get_data():
    items = Item.query.all()
    data = [{'id': item.id, 'name': item.name} for item in items]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
