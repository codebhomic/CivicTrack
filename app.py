from flask import Flask,render_template,request,jsonify,session,flash
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for
from flask_login import login_required, current_user
from models import db, Issue, IssueCategory,User
from flask_login import LoginManager,login_required
from auth import auth  # ← important: import the Blueprint, not the file

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)

# Register Blueprint
app.register_blueprint(auth, url_prefix='/auth')

all_issues = [
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "2.4 km"
        },
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "1.1 km"
        },
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "3.5 km"
        },
        {
            "title": "Streetlight not working",
            "description": "Dark corner near Park Avenue needs fixing.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=Streetlight",
            "status": "In Progress",
            "distance": "1.5 km"
        },
    ]

@app.route('/')
def home():
    global all_issues
    per_page = 3
    page = int(request.args.get("page", 1))
    total_pages = (len(all_issues) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_issues = all_issues[start:end]
    return render_template("homepage.html",issues=paginated_issues,
                           current_page=page,total_pages=total_pages)

@app.route('/api/issues')
def get_issues():
    global all_issues
    per_page = 3
    page = int(request.args.get("page", 1))
    total = len(all_issues)
    start = (page - 1) * per_page
    end = start + per_page
    page_issues = all_issues[start:end]
    return jsonify({
        "issues": page_issues,
        "page": page,
        "total": total,
        "per_page": per_page
    })


@app.route("/report", methods=["GET", "POST"])
@login_required
def report_issue():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        category_id = request.form["category"]
        image_url = request.form.get("image_url", "")
        latitude = float(request.form.get("latitude", 0))
        longitude = float(request.form.get("longitude", 0))

        new_issue = Issue(
            title=title,
            description=description,
            category_id=category_id,
            image_url=image_url,
            latitude=latitude,
            longitude=longitude,
            user_id=current_user.id
        )
        db.session.add(new_issue)
        db.session.commit()
        flash("Issue reported successfully!", "success")
        return redirect(url_for("report_issue"))

    categories = IssueCategory.query.all()
    return render_template("report.html", categories=categories)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
