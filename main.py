from curses.ascii import isdigit

from flask import Flask, request, render_template, session, redirect

from app.article_list import ArticleList, get_post_list, create_post
from app.bookmark_list import BookmarkList
from app.comment_list import CommentList, get_post_comment_list
from app.session_list import SessionList
from app.user_list import UserList

app = Flask('__name__')

articles = ArticleList()
articles.load_from_file('res/articles.json')

users = UserList()
users.load_from_file('res/users.json')

bookmarks = BookmarkList()
bookmarks.load_from_file('res/bookmarks.json')

comments = CommentList()
comments.load_from_file('res/comments.json')

sessions = SessionList()


def get_user_by_session_id(session_id):
    user_id = sessions.get(session_id)
    return users.get_by_id(user_id)


def get_current_user():
    session_id = session.get('session_id')
    return get_user_by_session_id(session_id), session_id


def render_template_or_login(template_name, user=None, **args):
    current_user, session_id = get_current_user()

    if current_user is None:
        return redirect('/login')
    else:
        as_user = user if user else current_user
        user_bookmarks_count = len(bookmarks.search_records(user_id=as_user.id))

        return render_template(template_name, user=as_user, bookmarks_count=user_bookmarks_count, **args)


@app.route('/')
def index():
    return render_template_or_login('feed.html', items=get_post_list(articles.get_raw_list(), users, bookmarks, comments))


@app.route('/login', methods=['GET'])
def login_form_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def set_session_view():
    form = request.form

    if 'username' in form and 'password' in form:
        user = users.get_by_username(form['username'])

        if user:
            session_id = sessions.open(user.id)

            if session_id:
                session['session_id'] = session_id
                return redirect('/')

    return render_template('login.html')


@app.route('/logout')
def remove_session_view():
    user, session_id = get_current_user()
    sessions.close(session_id)

    return redirect('/login')


@app.route('/bookmarks/switch', methods=['PUT'])
def bookmark_switch():
    user, session_id = get_current_user()

    if user is None:
        return ''

    article_id = request.args.get('id')

    if article_id is None or not isdigit(article_id):
        return ''

    bookmarks.switch(user.id, int(article_id))
    bookmarks.save_to_file()

    filtered_bookmarks = bookmarks.filter_by_article(int(article_id))

    return render_template('bookmarks_label.html', bookmarks_count=len(filtered_bookmarks))


@app.route('/bookmarks/count')
def bookmarks_count():
    user, session_id = get_current_user()

    if user is None:
        return ''

    bookmarks_list = bookmarks.search_records(user_id=user.id)
    return render_template('bookmarks_label.html', bookmarks_count=len(bookmarks_list))


@app.route('/bookmarks')
def bookmarks_view():
    user, session_id = get_current_user()

    if user is None:
        return render_template('404.html')

    bookmarks_list = bookmarks.search_records(user_id=user.id)
    article_list = articles.filter_by_bookmark(bookmarks_list)

    return render_template_or_login('feed_bookmarks.html', items=get_post_list(article_list, users, bookmarks, comments))


@app.route('/users/<username>')
def user_feed_view(username):
    user = users.get_by_username(username)

    if user is None:
        return render_template('404.html')

    article_list = articles.search_records(user_id=user.id)
    return render_template_or_login('feed_user.html', items=get_post_list(article_list, users, bookmarks, comments), user=user)


@app.route('/posts/<int:post_id>')
def article_view(post_id):
    user, session_id = get_current_user()

    article = articles.search_record(id=int(post_id))

    if user is None or article is None:
        return render_template('404.html')

    post = create_post(article, users, bookmarks, comments)
    comments_in_post = get_post_comment_list(comments.search_records(article_id=article.id), users)

    return render_template_or_login('article.html', item=post, comments=comments_in_post)


@app.route('/search', methods=['POST'])
def search_list():
    article_list = articles.filter_by_query(**request.args)

    return render_template_or_login('raw_list.html', items=get_post_list(article_list, users, bookmarks, comments))


@app.route('/search', methods=['GET'])
def search_view():
    article_list = articles.filter_by_query(**request.args)

    return render_template_or_login('search.html', items=get_post_list(article_list, users, bookmarks, comments))


app.secret_key = 'The Secret Key'
app.run(debug=True)

