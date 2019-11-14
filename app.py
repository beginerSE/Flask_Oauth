from flask import Flask, render_template, session
from flask import url_for, redirect, request
import twitter_oauth
import db

app = Flask(__name__)

# Sessionの暗号化に使う任意の文字列
app.secret_key = 'A0Zr98j/3yX Rnaxaixaixai~XHH!jmN]LWX/,?RT'

# トップ画面
@app.route('/')
def index():
    if 'user_name' in session:
        user_name = session['user_name']
    else:
        user_name = []
    return render_template("index.html", user_name=user_name)


# Twitterの認証画面にリダイレクトする
@app.route("/oauth_register")
def redirect_oauth():
    # Twitter Application Management で設定したコールバックURLsのどれか
    oauth_callback = request.args.get('oauth_callback')
    callback = twitter_oauth.get_twitter_request_token(oauth_callback)
    return redirect(callback)


@app.route('/callback')
def execute_userinfo():
    """[認証画面から返されてきた情報を取得して処理する関数]
    Return [ホーム画面('/')にリダイレクトする]
    """

    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')

    # リクエストトークンからアクセストークンを取得
    access_token = twitter_oauth.get_twitter_access_token(
        oauth_token, oauth_verifier)

    # 既に登録していないかチェック、無ければ新規にデータをテーブルにINSERTする
    # 既に登録済みであれば、その情報を返す
    user_data = db.search_user(access_token)

    if user_data is False:
        # 新規ユーザーはアクセストークンの情報をデータベースに保存
        db.register_userinfo(access_token)
        # 登録してからもう一回ユーザーデータを取得
        user_data = db.search_user(access_token)

    # 返された情報をSessionに保存する
    session['user_name'] = access_token['screen_name']
    session['user_id'] = access_token['user_id']
    session['oauth_token'] = access_token['oauth_token']
    session['oauth_token_secret'] = access_token['oauth_token_secret']
    return redirect(url_for('index'))


@app.route("/logout")
def logout():
    # セッションに渡しているデータを削除
    session.pop('user_name', None)
    session.pop('user_id', None)
    session.pop('oauth_token', None)
    session.pop('oauth_secret', None)
    return redirect(url_for('crypto_index'))


app.run(debug=True)
