from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from modals import issues

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///civictrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # database setup temproary sqlite

all_issues = [
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "2.1 km"
        },
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "2.1 km"
        },
        {
            "title": "Pothole near Green Street",
            "description": "A large pothole making it unsafe to drive.",
            "image_url": "https://dummyimage.com/400x400/000/fff/?text=pothole",
            "status": "Reported",
            "distance": "2.1 km"
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
                           current_page=page,
                           total_pages=total_pages,
                           prev_page=page - 1 if page > 1 else 1,
                           next_page=page + 1 if page < total_pages else total_pages)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
