from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1Session
import json

# ここに自分のAPI鍵を入力してください
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''


# base urls for oauth
base_url = 'https://api.twitter.com/'
request_token_url = base_url + 'oauth/request_token'
authenticate_url = base_url + 'oauth/authenticate'
access_token_url = base_url + 'oauth/access_token'
base_json_url = 'https://api.twitter.com/1.1/%s.json'
user_timeline_url = base_json_url % ('statuses/user_timeline')


def get_twitter_request_token(oauth_callback):
    """[このアプリと連携しますか？という認証画面を返す関数]]]

    Arguments:
        oauth_callback {[コールバックURL]} -- [デベロッパーツールで指定したURL]

    Returns:
        [認証画面] -- [自分のAPI鍵を付与した認証画面を発行し、アクセスをリダイレクトさせる]
    """

    twitter = OAuth1Session(consumer_key, consumer_secret)
    response = twitter.post(
        request_token_url,
        params={'oauth_callback': oauth_callback}
    )

    request_token = dict(parse_qsl(response.content.decode("utf-8")))

    # リクエストトークンから認証画面のURLを生成
    authenticate_endpoint = '%s?oauth_token=%s' \
        % (authenticate_url, request_token['oauth_token'])

    request_token.update({'authenticate_endpoint': authenticate_endpoint})
    return request_token['authenticate_endpoint']


def get_twitter_access_token(oauth_token, oauth_verifier):
    """[ユーザーの渡してきたリクエストトークンを使ってアクセストークンをツイッター　　から取得する関数]

    Keyword Arguments:
        oauth_token {[str]} -- [ユーザーのトークン１] (default: {oauth_token})
        oauth_verifier {[str]} -- [ユーザーのトークン2] (default: {oauth_verifier})

    Returns:
        [str] -- [アクセストークン]
    """

    # twitterのデータベース？にアクセスする準備
    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_verifier,
    )

    # ユーザーの返してきたアクセストークンと自分のAPI鍵セットした状態でツイッターに殴り込みをかける
    response = twitter.post(
        access_token_url,
        params={'oauth_verifier': oauth_verifier}
    )

    # レスポンスの中にアクセストークンを取得する(これがお目当てのもの)
    access_token = dict(parse_qsl(response.content.decode("utf-8")))

    return access_token


def get_accountdata(_id, oauth_token, oauth_secret):
    """[アクセストークンからアカウントデータを取得する関数]

    Arguments:
        _id {[str]} -- [description]
        oauth_token {[str]} -- [description]
        oauth_secret {[str]} -- [description]

    Returns:
        [json]- [json形式のアカウントデータ]]
    """

    params = {
        'user_id': _id,
        'exclude_replies': True,
        'include_rts': json.get('include_rts', False),
        'count': 20,
        'trim_user': False,
        'tweet_mode': 'extended',    # full_textを取得するために必要
    }

    twitter = OAuth1Session(
        consumer_key,
        consumer_secret,
        oauth_token,
        oauth_secret
    )

    response = twitter.get(user_timeline_url, params=params)
    results = json.loads(response.text)

    return results
