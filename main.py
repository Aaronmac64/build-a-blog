from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:MyNewPass@localhost:3306/buildablog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(255))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Blogpost %r>' % self.title + " " + self.content

@app.route("/")
def index():
    return redirect('/blog')

@app.route("/newPost", methods=['POST', 'GET'])
def newPost():
    if request.method == 'POST':
        blog_title = request.form['blog-title']
        blog_content = request.form['blog-content']
        title_error = ''
        content_error = ''

        if not blog_title:
            title_error = "Please enter a blog title"
        if not blog_content:
            content_error = "Please enter a blog entry"

        if not content_error and not title_error:
            new_entry = Blogpost(blog_title, blog_content)
            db.session.add(new_entry)
            db.session.commit()
            return redirect('blog?id{}'.format(new_entry.id))
        else:
            return render_template('newPost.html', title='New Entry', title_error=title_error, content_error=content_error, blog_title=blog_title, blog_content=blog_content)
    return render_template('newPost.html', title='New Entry')

@app.route("/blog")
def blog():
    entry_id = request.args.get('id')

    if entry_id == None:
        entries = Blogpost.query.all()
        entries.reverse()    
        return render_template('main.html', entries=entries, title='Build-A-Blog')
    else:
        entry = Blogpost.query.get(entry_id)
        return render_template('viewPost.html', entry=entry, title='Blog Entry')

if __name__ == "__main__":
    app.run()