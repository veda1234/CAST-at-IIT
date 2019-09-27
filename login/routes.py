from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from login import app, db, bcrypt
from login.form import RegistrationForm, LoginForm, UpdateAccountForm, LiedlForm, ChuForm
from login.models import User, Liedl, Chu
import math
import json

import matplotlib
import plotly
import plotly.graph_objs as go

matplotlib.use('Agg')
import pandas as pd


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If the user is already logged in then redirect to home-page
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        # Check if user exist in the db and password entered by the user is correct
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # User exist & password entered is valid, thereby log the user in
            # and redirect to the home-page
            login_user(user, remember=form.remember.data)

            flash('Login Successful', 'success')

            next_page = request.args.get('next')
            return redirect(url_for('account')) if next_page else redirect(url_for('home'))
        else:
            # User credentials are wrong or the user does not exist
            flash('Login Unsuccessful! Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


# @app.route("/post/new", methods=['GET', 'POST'])
# @login_required
# def new_post():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(title=form.title.data, content=form.content.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash('Your post has been created!', 'success')
#         return redirect(url_for('home'))
#     return render_template('create_chu.html', title='New Post', form=form)


@app.route("/multiple_liedl/new", methods=['GET', 'POST'])
@login_required
def multiple_liedl():
    form = LiedlForm()
    if form.validate_on_submit():
        m = form.m.data
        tv = form.tv.data
        a = form.a.data
        ca = form.ca.data
        cd = form.cd.data
        lMax = ((4 * m * m) / (math.pi * math.pi * tv)) * math.log(((a * cd + ca) / ca) * (4 / math.pi))
        #lMax = "%.2f" % lMax
        print(m,tv,a,ca,cd,lMax)
        li = Liedl(m=m, tv=tv, a=a, ca=ca, cd=cd, lMax=lMax, liedl=current_user)
        db.session.add(li)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_liedl.html', title='New Liedl', form=form)

@app.route("/multiple_chu/new", methods=['GET', 'POST'])
@login_required
def multiple_chu():
    form = ChuForm()
    if form.validate_on_submit():
        W = form.Width.data
        Th = form.Transverse_Horizontal_Dispersivity.data
        g = form.Reaction_Stoichiometric_Ratio.data
        Ca = form.Contaminant_Concentration.data
        Cd = form.Reactant_Concentration.data
        e = form.Biological_Factor.data
        lMax = ((math.pi * W * W) / (16 * Th)) * (((g * Cd) / (Ca - e)) ** 2)
        lMax = "%.2f" % lMax
        chu = Chu(Width=W, Transverse_Horizontal_Dispersivity=Th,Reaction_Stoichiometric_Ratio= g,
                   Contaminant_Concentration=Ca, Reactant_Concentration=Cd, Biological_Factor=e, Model_Plume_Length=lMax, chu=current_user)
        db.session.add(chu)
        db.session.commit()
        flash('Your entry has been added!', 'success')
        return redirect(url_for('multiple_chu'))
    chus = Chu.query.filter_by(user_id=current_user.id).all()
    CHU_DATA_ENTRY_COLUMNS = [
        'ID',
        'ID',
        'Width',
        'Transverse Horizontal Dispersivity',
        'Reaction Stoichiometric Ratio',
        'Contaminant Concentration',
        'Reactant Concentration',
        'Biological Factor',
        'Model Plume Length'
    ]
    table_data = []
    for data in chus:
        table_data.append([
            data.id,
            data.id,
            data.Width,
            data.Transverse_Horizontal_Dispersivity,
            data.Reaction_Stoichiometric_Ratio,
            data.Contaminant_Concentration,
            data.Reactant_Concentration,
            data.Biological_Factor,
            data.Model_Plume_Length
        ])
    para = create_chuEtAlPlotMultiple(table_data)
    return render_template('my_posts.html', title='New Chu', form=form,plot=para,
                           chus=chus,table_data=table_data,column_names=CHU_DATA_ENTRY_COLUMNS)

def create_chuEtAlPlotMultiple(table_data):
    df = pd.read_csv('login/static/original.csv')
    userID = [item[0] for item in table_data]
    modelPlumeLength = [item[8] for item in table_data]
    trace1 = go.Scatter(
        x=userID,
        y=modelPlumeLength,
        name='Model Plume Length(LMax)',
        mode='markers',
        marker=dict(
            size=14,
            color='#ffa600'
        )
    )

    trace2 = go.Scatter(
        x=df['Site No.'],
        y=df['Plume length[m]'],
        mode='markers',
        name='Field Plume Length(LMax)',
        marker=dict(
            size=14,
            color='#003f5c'
        )
    )
    data = [trace1, trace2]
    layout = go.Layout(
        titlefont=dict(
            size=25
        ),
        legend={
            "xanchor": "right",
            "y": 1,
            "x": 1
        },
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(229,229,229)',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Site Number',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgb(255,255,255)',
            title='Plume Length (m)',
            titlefont=dict(
                size=18,
                color='#7f7f7f'
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
