# 課題メモ

>クライアントの作成
まず、ユーザーから入力を受け取り、その入力をサーバに送信するクライアントを作成します。ユーザーの入力は、例えばコマンドラインから受け取るものとします。このクライアントは、ユーザーからの入力を待ち、入力があったらそれをサーバに送信します。


>サーバの作成
次に、クライアントからのメッセージを受け取り、それに対する応答を送り返すサーバを作成します。このサーバは、受け取ったメッセージに基づいて何らかの応答を生成し、それをクライアントに送り返します。


>faker パッケージの利用
faker は Python のパッケージで、様々な種類の偽データを生成することができます。例えば、フェイクの名前、住所、メールアドレス、テキスト等を生成することが可能です。この課題では、サーバ側で faker を使って偽のランダムな文字列やメッセージを生成します。これは、サーバからの応答を模擬するためのもので、実際の応答がない場合やテストの際に役立ちます。Python の faker パッケージは pip を使用してインストールすることができます。

# 利用方法

`just start-chat`

- `exit`で停止可能

例)

```sh
~/work/recursion/local-chat-messenger$ just start-chat
uv run python src/main.py
INFO:root:Starting Client...
INFO:root:Starting Server...
INFO:root:Client Connecting now...
INFO:root:Server accepting now...
hoge
INFO:root:Processing hoge
INFO:root:Server response: Processing hoge
fuga
INFO:root:Processing fuga
INFO:root:Server response: Processing fuga
exit
INFO:root:exit
INFO:root:Ending Server...
INFO:root:Server response: exit
INFO:root:Ending Client...
```

# メモ

- 少し作りが雑かもしれない。もう少し綺麗に書けそう。
- faker使ってない。でもこの課題での使いどころはなさそう。
