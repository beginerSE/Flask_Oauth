import sqlite3


# データベースの基本設定
dbpath = 'crypto.sqlite'


def search_user(access_token):
    """[アクセストークンからユーザー情報を検索して一致するものがあればTrue
    なければFalseを返す関数]

    Returns:
        [dict] -- [辞書型のアクセストークン]

    Returns:
        [List] -- [userのデータ]
    """

    c = sqlite3.connect(dbpath, check_same_thread=False)
    cur = c.cursor()

    user_token = access_token['oauth_token']
    user_secret = access_token['oauth_token_secret']
    user_id = access_token['user_id']

    query = "select * from user_info where user_token=" + "'" + user_token + "'" + " and" + \
        ' user_secret=' + "'" + user_secret + "'" + " and" + ' user_id=' + user_id

    cur.execute(query)
    user_data = cur.fetchall()
    print(user_data)
    c.close()

    if user_data == []:
        return False
    else:
        return user_data[0]


def register_userinfo(access_token):
    """[アクセストークンから取得したユーザー情報をテーブルにINSERTする関数]

    Returns:
        [dict] -- [辞書型のアクセストークン]

    Returns:
        [type] -- [description]
    """

    c = sqlite3.connect(dbpath, check_same_thread=False)
    cur = c.cursor()

    user_oauth_token = access_token['oauth_token']
    user_oauth_token_secret = access_token['oauth_token_secret']
    user_id = int(access_token['user_id'])
    user_screen_name = access_token['screen_name']
    provider = 'twitter'

    insert_query = f"'{user_id}','{user_screen_name}','{provider}','{user_oauth_token}', '{user_oauth_token_secret}'"
    sql = 'insert into user_info(user_id,user_screen,provider,user_token,user_secret) VALUES (' + \
        insert_query + ');'
    cur.execute(sql)
    c.commit()
    c.close()
