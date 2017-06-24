from . import main
from flask import render_template, abort, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import User, Permission, Post, Comment
from .forms import PostForm, CommentForm
from .. import db


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


@main.route('/')
def index():
    if current_user.is_authenticated :
        picSrc = current_user.avatar_url
    else:
        picSrc = "avatar/head.png"
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    number = Post.query.count()
    if number > 5:
        onshows = posts[:4]
    else:
        onshows = posts
    return render_template('main/index.html', posts=posts, pagination=pagination,
                           onshows=onshows, username=current_user.username, picSrc=picSrc)


@main.route('/user/<name>')
@login_required
def user(name):
    u = User.query.filter_by(username=name).first()
    if u is None:
        abort(404)
    '''posts = u.posts.order_by(Post.timestamp.desc()).all()'''
    page = request.args.get('page', 1, type=int)
    pagination = u.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    posts = pagination.items
    return render_template('profile.html', user=u, posts=posts, pagination=pagination)


@main.route('/writeEssay', methods=['GET','POST'])
@login_required
def writeEssay():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(body=title, body_html=content, good_count=0, author_name=current_user.username)
        db.session.add(post)
        return redirect(url_for('main.index'))
    return render_template('main/writeEssay.html', form=form, username=current_user.username, picSrc=current_user.avatar_url)


@main.route('/recommend')
@login_required
def recommend():
    post = Post.query.all()
    number = Post.query.count()
    if number >= 10:
        recommends = post[:9]
    else :
        recommends = post
    return render_template('main/recommend.html', picSrc=current_user.avatar_url,
                           username=current_user.username, recommends=recommends)


@main.route('/questionDetail/<int:id>', methods=['GET','POST'])
@login_required
def question(id):
    form = CommentForm()
    post = Post.query.get_or_404(id)
    comments = post.comments.all()
    number = Post.query.count()
    posts = Post.query.all()
    if number >= 5:
        onshows = posts[:4]
    else:
        onshows = posts
    return render_template('main/questionDetail.html', picSrc=current_user.avatar_url,
                           form=form, post=post, username=current_user.username, comments=comments, onshows=onshows)


@main.route('/addPost/<int:id>')
@login_required
def addPost(id):
    post = Post.query.get_or_404(id)
    post.good_count = post.good_count+1
    db.session.add(post)
    return redirect(url_for('main.index'))


@main.route('/addComment/<int:id>')
@login_required
def addComment(id):
    comment = Comment.query.get_or_404(id)
    comment.good_count = comment.good_count+1
    db.session.add(comment)
    return redirect(url_for('main.question', id=comment.post_id))