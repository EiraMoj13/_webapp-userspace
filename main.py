
from flask import Blueprint, render_template, flash,jsonify
from flask_login import login_required, current_user
from __init__ import create_app, db
from models import User

# main blueprint
main = Blueprint('main', __name__)


@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')


@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/user/delete/<int:user_id>', methods=['GET','DELETE']) #delete user
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404

app = create_app() # initialize our flask app using the __init__.py function

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode
