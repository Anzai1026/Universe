import streamlit as st
import sqlite3
import hashlib
from PIL import Image

img = Image.open('宇宙人.jpeg')

st.set_page_config(page_title='Universe', page_icon=img)

conn = sqlite3.connect('database.db')
c = conn.cursor() 

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def create_user():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_user(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data

# 新しいメモ関連の関数
def create_memo_table():
    c.execute('CREATE TABLE IF NOT EXISTS memostable(username TEXT, content TEXT)')

def add_memo(username, content):
    c.execute('INSERT INTO memostable(username, content) VALUES (?,?)', (username, content))
    conn.commit()

def get_memos(username):
    c.execute('SELECT content FROM memostable WHERE username = ?', (username,))
    memos = c.fetchall()
    return [memo[0] for memo in memos]

def main():

    st.title("Universeログイン")

    menu = ["ホーム","ログイン","サインアップ"]
    choice = st.sidebar.selectbox("メニュー",menu)

    if choice == "ホーム":
        st.subheader("ホーム画面")

    elif choice == "ログイン":
        st.subheader("ログイン画面です")

        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください",type='password')
        if st.sidebar.checkbox("ログイン"):
            create_user()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.success("{}さんでログインしました".format(username))

                # メモ機能の追加
                st.subheader("メモを追加")
                memo_content = st.text_area("メモを入力してください")
                if st.button("メモを保存"):
                    create_memo_table()
                    add_memo(username, memo_content)
                    st.success("メモを保存しました")

                # メモ一覧の表示ボタンを追加
                if st.button("メモ一覧を表示"):
                    st.subheader("メモ一覧")
                    memos = get_memos(username)
                    if memos:
                        for memo in memos:
                            st.write(memo)
                        # メモ一覧を折りたたむボタン
                        with st.expander("メモ一覧をたたむ"):
                            pass
                    else:
                        st.info("まだメモがありません")

            else:
                st.warning("ユーザー名かパスワードが間違っています")

    elif choice == "サインアップ":
        st.subheader("新しいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください",type='password')

        if st.button("サインアップ"):
            create_user()
            add_user(new_user,make_hashes(new_password))
            st.success("アカウントの作成に成功しました")
            st.info("ログイン画面からログインしてください")

if __name__ == '__main__':
    main()
