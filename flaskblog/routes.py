from flaskblog import app,bcrypt,db
from flaskblog.forms import RegistrationForm,loginForm,updateAccount,PostForm
from flask import flash,render_template,redirect,url_for,request,abort
from flaskblog.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
import secrets,os
from PIL import Image


@app.route('/')
@app.route('/home')
def home():
    posts=Post.query.all()
    return render_template('home.html',Posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title='about')

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_pw=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'your account is created! You can Log In now','success')
        return redirect(url_for('login'))
    return render_template('register.html',form=form,title='Register')

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form=loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home')) 

        else:
            flash(f'Invalid email or password','danger')
    
    return render_template('login.html',form=form,title='Title')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    f_name,f_ext=os.path.split(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pic', picture_fn)
    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn





@app.route('/account',methods=['GET','POST'])
@login_required
def account():

    
    form=updateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_fn=save_picture(form.picture.data)
            current_user.image_file=picture_fn

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data= current_user.username
        form.email.data=current_user.email
    image_file=url_for('static',filename='profile_pic/' + current_user.image_file)    
    return render_template('account.html',title='Account',image_file=image_file,form=form)

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is created!','success') 
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form,legend='Create Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',post=post,title=post.title)


@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403)
    form = PostForm()
    # form.title.data = post.title
    # form.content.data = post.content
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post is Updated!','success') 
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET' :
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title='New Post',form=form,legend='Update Post')


@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post is Deleted','success')
    return redirect(url_for('home'))
