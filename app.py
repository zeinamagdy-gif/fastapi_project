from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret'

users = {
    'admin': '1234',
    'zeina': '1234',
    'youssef': '1234',
    'ganna': '1234',
    'aly': '1234'
}

user_data = {
    'zeina': {
        "name": "Zeina Beshr",
        "title": "Data Analyst & Web Developer",
        "about": "Passionate about data and clean code. Always learning, always building.",
        "skills": ["Power BI", "Excel", "HTML", "CSS", "JavaScript", "Python", "Odoo ERP"],
        "experience": [
            {"company": "Haus+", "role": "Event Organizer", "years": "2024–Present"},
            {"company": "Infinity", "role": "Registration Assistant", "years": "2022–2023"}
        ],
        "education": [{"degree": "Bachelor in Business Informatics", "institution": "University", "year": "2025"}],
        "email": "zeina@example.com",
        "linkedin": "linkedin.com/in/zeinabeshr",
        "github": "github.com/zeinabeshr"
    },
    "youssef": {
        "name": "Youssef",
        "title": "Software Engineer",
        "about": "I enjoy backend development and working on scalable systems.",
        "skills": ["Python", "Flask", "SQL", "Docker"],
        "experience": [{"company": "TechCorp", "role": "Backend Dev", "years": "2023–Present"}],
        "education": [{"degree": "BSc in Computer Science", "institution": "University", "year": "2024"}],
        "email": "youssef@example.com",
        "linkedin": "linkedin.com/in/youssef",
        "github": "github.com/youssefdev"
    },
    "ganna": {
        "name": "Ganna",
        "title": "UI/UX Designer",
        "about": "Creative mind with a love for elegant and user-friendly interfaces.",
        "skills": ["Figma", "Sketch", "HTML", "CSS"],
        "experience": [{"company": "DesignHub", "role": "UI Designer", "years": "2022–Present"}],
        "education": [{"degree": "BSc in Design", "institution": "Art University", "year": "2024"}],
        "email": "ganna@example.com",
        "linkedin": "linkedin.com/in/ganna",
        "github": "github.com/gannadesigns"
    },
    "aly": {
        "name": "Aly",
        "title": "Data Scientist",
        "about": "I use data to uncover insights and build predictive models.",
        "skills": ["Python", "Pandas", "Scikit-learn", "TensorFlow"],
        "experience": [{"company": "DataGen", "role": "Data Scientist", "years": "2023–Present"}],
        "education": [{"degree": "MSc in AI", "institution": "Science Uni", "year": "2025"}],
        "email": "aly@example.com",
        "linkedin": "linkedin.com/in/aly",
        "github": "github.com/alyds"
    }

}

# Power BI page URLs (replace pageName values with your actual Power BI page names)
POWERBI_PAGES = {'homepage': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=54d03fd1b6b893b34049&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45',
                 'readme': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=6fe92debf7ede8d4d65a&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45',
                 'main_data': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=ReportSection3&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45',
                 'forecast': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=5947ee896c1712abac6f&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45',
                 'container_utilization': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=630c6af5a1baa4112e04&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45',
                 'cor_kpis': 'https://app.powerbi.com/reportEmbed?reportId=54a882f8-a907-44e5-a648-febb93b00fa3&pageName=c5fd0c40eeeb0d6b2f3e&autoAuth=true&ctid=736ee586-9e83-43c4-85b0-6368fca06b45'}

# Home route
@app.route('/')
def home():
    return redirect(url_for('dashboard'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form['username'].lower()
        passwd = request.form['password']
        if uname in users and users[uname] == passwd:
            session['username'] = uname
            return redirect(url_for('dashboard'))
        else:
            error = "Username or password is incorrect"
    return render_template('login.html', error=error)



# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Profile page


# Dashboard view
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    page = request.args.get('page', 'main_data')
    year = request.args.get('year')

    powerbi_url = POWERBI_PAGES.get(page, POWERBI_PAGES['main_data'])

    # Year-specific bookmarks (if provided)
    year_supported_pages = ['main_data', 'cor_kpis']
    report_urls_by_year = {
        '2023': {
            'main_data': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/46ff293de6bdb7703a22?experience=power-bi&bookmarkGuid=7373d346-5697-44c1-a362-665139c34864",
            'cor_kpis': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/c5fd0c40eeeb0d6b2f3e?experience=power-bi&bookmarkGuid=7373d346-5697-44c1-a362-665139c34864"

        },
        '2024': {
            'main_data': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/46ff293de6bdb7703a22?experience=power-bi&bookmarkGuid=e2422c3f-fab7-4d50-93dc-ad9f8d07187f",
            'cor_kpis': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/c5fd0c40eeeb0d6b2f3e?experience=power-bi&bookmarkGuid=e2422c3f-fab7-4d50-93dc-ad9f8d07187f"
        },
        '2025': {
            'main_data': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/46ff293de6bdb7703a22?experience=power-bi&bookmarkGuid=10502272-8f23-4bd9-8bc7-8d5522bc5b04",
            'cor_kpis': "https://app.powerbi.com/groups/me/reports/fd392461-8763-49ee-84de-61974d018cd7/c5fd0c40eeeb0d6b2f3e?experience=power-bi&bookmarkGuid=10502272-8f23-4bd9-8bc7-8d5522bc5b04"
        }
    }
    if year in report_urls_by_year and page in year_supported_pages:
        powerbi_url = report_urls_by_year[year].get(page, powerbi_url)

    return render_template(
        'dashboard.html',
        username=username,
        current_page=page,
        current_page_title=page.replace('_', ' ').title(),
        powerbi_url=powerbi_url,
        user_data=user_data  # ✅ This must be passed to the template
    )
@app.route('/report_problem', methods=['GET', 'POST'])
def report_problem():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    if request.method == 'POST':
        category = request.form.get('category')
        sub_page = request.form.get('sub_page')
        description = request.form.get('description')
        print(f"Reported by {username}: {category} > {sub_page} - {description}")
        return render_template("report_problem.html", success=True, username=username, user_data=user_data, current_page_title="Report a Problem")

    return render_template("report_problem.html", success=False, username=username, user_data=user_data, current_page_title="Report a Problem")


@app.route('/user/<username>')
def user_profile(username):
    username = username.lower()
    if username not in user_data:
        return "User not found", 404
    return render_template('user_profile.html', user=user_data[username])


@app.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect('/login')

    user = user_data.get(username)
    if not user:
        return "User profile not found"

    return render_template('profile.html', user=user)







if __name__ == '__main__':
    app.run(debug=True)
