from app import app,db,headers
from app.models import User, Word, Definition, UserWord
import hashlib
import random
import requests

from flask import  url_for, render_template, redirect, request, session, flash, jsonify

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    word = request.form['word']
    wordObject = Word.query.filter_by(word=word).first()

    if wordObject:
        isWordAdded = bool(UserWord.query.filter_by(word=wordObject, user_id=session['id']).first())
        definitions = Definition.query.filter_by(word=wordObject).all()
        r = {"word": wordObject.word,"isWordAdded": isWordAdded, "definition":[row.definition for row in definitions]}

    else:
        response = requests.request("GET", f'https://wordsapiv1.p.rapidapi.com/words/{word}/definition',
                             headers=headers)

        if response.status_code == requests.codes.ok:
            r = response.json()
            wordObject = Word(word)
            db.session.add(wordObject)
            db.session.commit()
            for definition in r['definition']:
                definitionObject = Definition(wordObject.id, definition)
                db.session.add(definitionObject)
            db.session.commit()
            r.update({"isWordAdded": False})
        else:
            return jsonify({"error": True})
    userWordObject = UserWord.query.filter_by(user_id=session['id'], word=wordObject).first()
    if userWordObject:
        userWordObject.increaseSearchCount()
        userWordObject.calculatePower()
        db.session.add(userWordObject)
        db.session.commit()
    return jsonify(r)

@app.route('/process', methods=['POST'])
def process():

    word = request.form['word']
    wordObject = Word.query.filter_by(word=word).first()
    userWordObject = UserWord.query.filter_by(word=wordObject, user_id = session['id']).first()

    if userWordObject:
        UserWord.query.filter_by(word_id=wordObject.id, user_id=session['id']).delete()
        db.session.commit()
        return jsonify({"word": word, "isWordAdded": False})

    else:
        userWordObject = UserWord(word=wordObject, user_id=session['id'])
        db.session.add(userWordObject)
        db.session.commit()
        return jsonify({"word": word, "isWordAdded": True})


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'user' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            h = hashlib.md5(password.encode()).hexdigest()
            if(not User.query.filter_by(username=user).first()):
                usr = User(user, h)
                db.session.add(usr)
                db.session.commit()
                session['user'] = usr.username
                session['id'] = usr.id
                flash("Successfully Registered!", "green")
                return redirect(url_for('index'))
            else:
                flash("Username already taken, please try another username", "red")
                return redirect(url_for('register'))
        else:
            return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        flash("Already Logged In", "red")
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            user = request.form['username']
            password = request.form['password']
            h = hashlib.md5(password.encode()).hexdigest()
            userObject = User.query.filter_by(username=user).first();
            if h == userObject.password and userObject:
                session['user'] = userObject.username
                session['id'] = userObject.id
                flash("You have been logged in", "green")
                return redirect(url_for('index'))
            else:
                flash("Check your username or password", "red")
                return redirect(url_for('login'))
        else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop("user", None)
        session.pop("id", None)
        flash("Logged out", "green")
    else:
        flash("You are not logged in", "red")
    return redirect(url_for("login"))


@app.route('/profile')
def profile():
    if 'user' in session:
        userObject = User.query.filter_by(username=session['user']).first()
        userWordObjects = UserWord.query.filter_by(user=userObject).all()
        return render_template('profile.html', userWordObjects=userWordObjects)

@app.route('/practice')
def practice():
    userWordObjects = UserWord.query.filter_by(user_id=session['id']).all()
    if len(userWordObjects) >= 10:
        return render_template('practice.html', proper=True)
    else:
        return render_template('practice.html', proper=False)

@app.route('/practice', methods=['POST'])
def practice_post():
    answer = request.form.get('answer')
    pastData = {}
    if answer:
        words = [request.form.get('word1'), request.form.get('word2'), request.form.get('word3')]
        answer = request.form.get('answer')
        trueAnswer = request.form.get('trueAnswer')
        if answer == trueAnswer:
            wordObject = Word.query.filter_by(word=answer).first()
            userWordObject = UserWord.query.filter_by(word=wordObject, user_id=session['id']).first()
            userWordObject.increasePracticePoint(1)
            userWordObject.calculatePower()
            db.session.add(userWordObject)
            db.session.commit()
            pastData = {"word": trueAnswer, "answer": answer }
        else:
            for word in words:
                wordObject = Word.query.filter_by(word=word).first()
                userWordObject = UserWord.query.filter_by(word=wordObject, user_id=session['id']).first()
                pastData = {"word": trueAnswer, "answer": answer}
                if word != trueAnswer:
                    userWordObject.increasePracticePoint(-1)
                    userWordObject.calculatePower()
                    db.session.add(userWordObject)
                else:
                    userWordObject.increasePracticePoint(-2)
                    userWordObject.calculatePower()
                    db.session.add(userWordObject)
                db.session.commit()

    userWordObjects = UserWord.query.filter_by(user_id=session['id']).all()
    sampled_list = random.sample(userWordObjects, 3)
    correct = sampled_list[random.randint(0, 2)]
    words = [userWordObject.word.word for userWordObject in sampled_list ]
    correctWordObject = correct.word
    randomDefinition = random.choice([definitionObject.definition for definitionObject in correctWordObject.definitions ])
    correct.increaseAppearCount()
    db.session.add(correct)
    db.session.commit()
    return jsonify({"words": words, "definition": randomDefinition, "trueAnswer": correctWordObject.word, "pastData": pastData})
