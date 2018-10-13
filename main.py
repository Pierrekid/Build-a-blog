from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Build-a-blog:12build34@localhost:8889/Build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '12secretkey34'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body= db.Column(db.String(120))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body
        


@app.route('/newpost', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        body = request.form['body']
        title = request.form['title']

        if body == '':
            flash('Please enter message in the body', 'error')
            return render_template('blog_add.html', body=body, title=title)

        if title == '':
            flash('Please enter a title for you blog', 'error')
            return render_template('blog_add.html', body=body, title=title)

        new_blog = Blog(title, body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog?id={}'.format(new_blog.id))
        

    return render_template('blog_add.html')


@app.route('/blog', methods=['GET']) 
def blog_list():

    if request.args:
        blog_id = int(request.args.get('id'))
        blog = Blog.query.get(blog_id)
        return render_template('blog_page.html', blog = blog)

    else:
        blogs = Blog.query.all()
        return render_template('blog_list.html',title="My Blogs!",blogs = blogs)





if __name__ == '__main__':
    app.run()