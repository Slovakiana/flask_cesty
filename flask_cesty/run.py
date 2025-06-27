from app import app, db
from app.models import User, Trip

with app.app_context():
    db.create_all()

app.run(debug=True)
