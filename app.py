from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def home():
    all_issues = [num for num in range(0,10)]  # List of all issues
    per_page = 6
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

if __name__ == '__main__':
    app.run(debug=True)
