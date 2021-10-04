from os import link
from flask import Flask, render_template, url_for, redirect, request, jsonify, make_response
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, current_user, logout_user
from wtforms.validators import Email
import college_list
import forms
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hierarchy_translations


app = Flask(__name__, static_folder='static')

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# Create tables


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    school = db.Column(db.String(250), nullable=False)
    upvote_count = db.Column(db.Float)
    date = db.Column(db.DateTime, nullable=False)


class Upvotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    school = db.Column(db.String(250), nullable=False)
    post_id = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(250), nullable=False)
    section = db.Column(db.String(250), nullable=False)
    data = db.Column(db.String(250), nullable=False)
    source = db.Column(db.String(400), nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class FinData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(250), nullable=False)
    section = db.Column(db.String(250), nullable=False)
    data = db.Column(db.String(250), nullable=False)
    source = db.Column(db.String(400), nullable=False)
    in_use = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Hierarchy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(250), nullable=False)
    in_use = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    source = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    rigor = db.Column(db.String(250), nullable=False)
    rank = db.Column(db.String(250), nullable=False)
    gpa = db.Column(db.String(250), nullable=False)
    test_scores = db.Column(db.String(250), nullable=False)
    essay = db.Column(db.String(250), nullable=False)
    recommendations = db.Column(db.String(250), nullable=False)
    interview = db.Column(db.String(250), nullable=False)
    extracurriculars = db.Column(db.String(250), nullable=False)
    talent = db.Column(db.String(250), nullable=False)
    character = db.Column(db.String(250), nullable=False)
    first_generation = db.Column(db.String(250), nullable=False)
    alumni = db.Column(db.String(250), nullable=False)
    geographical = db.Column(db.String(250), nullable=False)
    state_residency = db.Column(db.String(250), nullable=False)
    religion = db.Column(db.String(250), nullable=False)
    race = db.Column(db.String(250), nullable=False)
    volunteer = db.Column(db.String(250), nullable=False)
    work_experience = db.Column(db.String(250), nullable=False)
    interest_level = db.Column(db.String(250), nullable=False)


# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template('index.html', schools=college_list.colleges)


@app.route('/<school>/')
def school(school):
    if school in college_list.urls:
        school_index = college_list.urls.index(school)
        hierarchy = db.session.query(
            Hierarchy).filter(Hierarchy.school == school, Hierarchy.in_use == '1').first()
        translations = {
            "very_important": "Very important",
            "important": "Important",
            "considered": "Considered",
            "not_considered": "Not Considered"
        }
        hierarchy_list = hierarchy_translations.raw
        posts = db.session.query(Posts).filter(
            Posts.school == school).order_by(Posts.upvote_count.desc())

        admissions_stats = db.session.query(Data).filter(
            Data.school == school, Data.in_use == '1')
        fin_stats = db.session.query(FinData).filter(
            FinData.school == school, FinData.in_use == '1')
        upvotes_id = []
        if current_user.is_authenticated:
            user_upvotes = db.session.query(Upvotes).filter(
                Upvotes.email == current_user.email, Upvotes.school == school
            )
            for upvote in user_upvotes:
                upvotes_id.append(int(upvote.post_id))

        return render_template('school.html', school=college_list.colleges[school_index], admissions_stats=admissions_stats, posts=posts, hierarchy=hierarchy, hierarchy_list=hierarchy_list, translations=translations, fin_stats=fin_stats, upvotes_id=upvotes_id)
    else:
        return "We can't find it...I'M SORRY!"


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data.lower()).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'

    return render_template('login.html', form=form)


@ app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = forms.RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data.lower(),
                        email=form.email.data.lower(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
        # return f'<h1>{ form.username.data } { form.email.data } { form.password.data }</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard/')
@login_required
def dashboard():
    uploads = Posts.query.filter_by(
        email=current_user.email).order_by(Posts.date.desc())
    upvotes = Upvotes.query.filter_by(
        email=current_user.email)
    dataz = Data.query.filter_by(
        email=current_user.email).order_by(Data.date.desc())
    hierarchies = Hierarchy.query.filter_by(
        email=current_user.email).order_by(Hierarchy.date.desc())
    fin_data = FinData.query.filter_by(
        email=current_user.email).order_by(FinData.date.desc())
    links = {}
    for vote in upvotes:
        vote_id = int(vote.post_id)
        vote = Posts.query.get(vote_id)
        links[vote.id] = vote.url
    return render_template('dashboard.html', uploads=uploads, upvotes=upvotes, links=links, dataz=dataz, fin_data=fin_data, hierarchies=hierarchies)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Submit edit pages


@app.route('/<school>/data/', methods=["GET", "POST"])
@login_required
def data(school):
    form = forms.DataForm()
    if form.validate_on_submit():
        new_change = Data(school=school, section=form.section.data, data=form.change.data.lower(),
                          source=form.source.data.lower(), in_use=True, email=current_user.email, date=datetime.now())
        db.session.add(new_change)
        db.session.commit()
        return redirect(url_for('school', school=school))
    # if school in college_list.urls:
    #     school_index = college_list.urls.index(school)
    return render_template('data.html', form=form)


@app.route('/<school>/hierarchy/', methods=["GET", "POST"])
@login_required
def hierarchy(school):
    # if school in college_list.urls:
    #     school_index = college_list.urls.index(school)
    form = forms.HierarchyForm()
    if form.validate_on_submit():
        new_change = Hierarchy(school=school,
                               in_use=True,
                               email=current_user.email,
                               source=form.source.data,
                               date=datetime.now(),
                               rigor=form.rigor.data,
                               rank=form.rank.data,
                               gpa=form.gpa.data,
                               test_scores=form.test_scores.data,
                               essay=form.essay.data,
                               recommendations=form.recommendations.data,
                               interview=form.interview.data,
                               extracurriculars=form.extracurriculars.data,
                               talent=form.talent.data,
                               character=form.character.data,
                               first_generation=form.first_generation.data,
                               alumni=form.alumni.data,
                               geographical=form.geographical.data,
                               state_residency=form.state_residency.data,
                               religion=form.religion.data,
                               race=form.race.data,
                               volunteer=form.volunteer.data,
                               work_experience=form.work_experience.data,
                               interest_level=form.interest_level.data
                               )
        db.session.add(new_change)
        db.session.commit()
        return redirect(url_for('school', school=school))
    return render_template('hierarchy.html', form=form)


@app.route('/<school>/aid/', methods=["GET", "POST"])
@login_required
def aid(school):
    form = forms.AidForm()
    if form.validate_on_submit():
        new_change = FinData(school=school, section=form.section.data, data=form.change.data.lower(),
                             source=form.source.data.lower(), in_use=True, email=current_user.email, date=datetime.now())
        db.session.add(new_change)
        db.session.commit()
        return redirect(url_for('school', school=school))
    # if school in college_list.urls:
    #     school_index = college_list.urls.index(school)
    return render_template('data.html', form=form)


@app.route('/<school>/anectodes/', methods=["GET", "POST"])
@login_required
def anectodes(school):
    form = forms.AnectodeForm()
    if form.validate_on_submit():
        new_post = Posts(email=current_user.email,
                         url=form.url.data,
                         school=school,
                         upvote_count=0,
                         date=datetime.now()
                         )
        db.session.add(new_post)
        db.session.commit()
        redirect(url_for('school', school=school))
    # if school in college_list.urls:
    #     school_index = college_list.urls.index(school)
    return render_template('anectodes.html', form=form)


@app.route('/upvote/', methods=["POST"])
def upvote():

    req = request.get_json()

    print(req['checked'])

    if req['checked'] == True:

        new_upvote = Upvotes(
            email=req['user'],
            school=req['school'],
            post_id=req['post_id'],
            date=datetime.now()
        )
        related_post = Posts.query.get(req['post_id'])
        related_post.upvote_count += 1
        db.session.add(new_upvote)
        db.session.commit()
        return 'New upvote submitted'
    elif req['checked'] == False:
        upvote_id = Upvotes.query.filter_by(
            post_id=float(req['post_id'])).first()
        print(upvote_id)
        related_post = Posts.query.get(req['post_id'])
        related_post.upvote_count -= 1
        db.session.delete(upvote_id)
        db.session.commit()

    res = make_response(jsonify({'message': "OK"}), 200)

    return res


if __name__ == "__main__":
    app.run(debug=True)
