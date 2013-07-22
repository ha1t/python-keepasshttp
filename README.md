# python-keypasshttp

ChromeIPass を利用するには KeePass Plugin である、 KeePassHttp を利用しなければいけませんが、
KeePass Pluginは、実質 Windows でしか動作しないため、OSXやLinuxユーザーには利用できません。

そこで、Python から、KeePass DB を読み出し、 ChromeIPass からのリクエストに応じてレスポンスを返す仕組みを作りました。
python-keepasshttp を利用する事で、OSX や Linux からも ChromeIPass が利用できます。

# setup

最初に [kptool](https://github.com/shirou/kptool) をインストールしてください。

あとは、 `` python main.py [db_path] `` を実行して、DBのパスワードを入れるだけです。

Google ChromeにChromeIPassをインストールして、ログインが必要なページにアクセスしてください。
