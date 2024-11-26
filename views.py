from flask import Blueprint, render_template
from flask_login import login_required, current_user

#define urls with blueprint

views = Blueprint('views', __name__)

@views.route('/')
#decoretor to check if user is logged in
@login_required
def home():
    return render_template("index.html", user=current_user)



