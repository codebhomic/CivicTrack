from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Issue, IssueCategory, StatusLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civictrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
