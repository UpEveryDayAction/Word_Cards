from flask_migrate import Migrate
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
#from flaskext.markdown import Markdown
import random

app = Flask(__name__)
#Markdown(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///memo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app,db)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eigo = db.Column(db.Text())
    nihongo = db.Column(db.Text())


@app.route('/')
def list():

    message = '単語リスト'
    posts = Post.query.all()

    return render_template('list.html', message = message, posts = posts)


@app.route('/show/<int:id>')
def show_post(id):

    message = '単語'
    post = Post.query.get(id)

    return render_template('show.html', message = message, post = post)


@app.route('/new')
def new_post():

    message = '新しい単語を登録する'
    return render_template('new.html', message = message)


@app.route('/create', methods=['POST'])
def create_post():

    message = '登録した単語'

    new_post = Post()
    new_post.eigo = request.form['eigo']
    new_post.nihongo = request.form['nihongo']
    db.session.add(new_post)
    db.session.commit()

    post = Post.query.get(new_post.id)

    return render_template('show.html', message = message, post = post)

@app.route('/edit/<int:id>')
def edit_post(id):

    message = '単語の編集をする ' + str(id)
    post = Post.query.get(id)

    return render_template('edit.html', message = message, post = post)

@app.route('/update/<int:id>', methods=['POST'])
def update_post(id):

    message = 'Update your memo ' + str(id)

    post = Post.query.get(id)
    post.eigo = request.form['eigo']
    post.nihongo = request.form['nihongo']
    db.session.commit()

    return render_template('show.html', message = message, post = post)

@app.route('/destroy/<int:id>')
def destroy_post(id):

    message = 'memoを削除しました。'

    destroy_post = Post.query.get(id)
    db.session.delete(destroy_post)
    db.session.commit()

    posts = Post.query.all()

    return render_template('list.html', message = message, posts = posts)

@app.route('/test')
def do_test():

    message = '次の英語を日本語に訳せよ'

    posts = Post.query.all()
    tests = []
    for i in range(15):
        temp = posts[int(random.random()*len(posts))]
        if temp not in tests:
            tests.append(temp)
        if len(tests) == 5:
            break;

    return render_template('test.html', message = message, tests = tests)

