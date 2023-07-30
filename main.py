import json
from flask import Blueprint, render_template, flash,jsonify, request, json, Response,abort
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
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'status':200,'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'status':404,'message': 'User not found'}), 404
    
@main.route('/user/fetch/<int:user_id>', methods=['GET','POST']) #fetch user
@login_required
def fetch(user_id):
    user = User.query.get(user_id)
    if user:
        
        return jsonify({'status':200, 'id':user_id, 'name':user.name,'email': user.email, 'role':user.role}), 200
    else:
        return jsonify({'status':404,'message': 'User not found'}), 404

# Route to handle the update request
@main.route('/user/update_record/<int:id>', methods=['POST'])
def update_record(id):
    record = User.query.get(id)

    if not record:
        return jsonify({'status':404,'message': 'Record not found'}), 404

    new_name = request.json.get('name')  # Assuming you are updating the 'name' field
    new_email = request.json.get('email') 
    new_role= request.json.get('role') 
    # Update other fields accordingly

    record.name = new_name
    record.email = new_email
    record.role = new_role
    # Update other fields accordingly

    db.session.commit()
    return jsonify({'status':200, 'message': 'Record updated successfully'}), 200
   
@main.route('/manage-users') # manage user page that return 'manage-user'
@login_required
def manage_user():
    if current_user.role == "admin": 
        users = User.query.filter(User.id != current_user.id).all()
        return render_template('manage-users.html',users=users)
    else:
        abort(404, 'Page not found')


app = create_app() # initialize our flask app using the __init__.py function

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode
