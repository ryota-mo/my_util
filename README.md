# my_util
便利ツールリポジトリ

## get_vacant_gpu.py
dgxなどのnvidia-smiコマンドが利用可能なgpuで最もGPU利用率が低いGPUを返す．

```
os.environ["CUDA_VISIBLE_DEVICES"] = get_vacant_gpu()
```
として利用可能．ただし，GPU利用率を見ているだけなのであまりに同時実行だと同じ場所が返ってくる可能性がある．

## slack_notification.py
### `slack_notification(text, webhook_url, username=None, **kwargs)`

SlackのIncoming Webhook を使って通知を送信できる．URLはワークスペースのカスタマイズ内の，カスタムインテグレーションから取得する．他人に迷惑のかからないように自分宛てのDMを選ぶなどすること．

`pip install requests` が必要．

`slack_notification(text, webhook_url, username=None, **kwargs)` で利用．

kwargsにはチャンネルの指定などが考えられる．また， `attachments` 属性にリストを入れるのも良い．チャンネル指定の際には `kwargs={'channel': '#general'}` のようにする．

また，webhook_urlはテキストファイルから読み込むこともできる．
```
https://hooks.slack.com/services/team_id/***

```
というテキストファイルを読み込み，このファイルへのパスをwebhook_urlにとればよい．（プログラム中にURLを記載するのを防ぐため）


```
attachments=[
    {
       "fallback":"fallback Test",
       "pretext":"attachments Test",
       "color":"#D00000",
       "fields":[
          {
             "title":"attachment01",
             "value":"This is attachment"
          }
       ]
    }
 ]
```

### `slack_file_upload(filepath, channel, text, token=None, client=None)`
ファイルをアップロードするためのプログラム．

`pip install slackclient` が必要．詳細はwikiをみていただきたい．http://is/pukiwiki/index.php?morimoto%2Fmemo

channelは#generalなども多分使えるが，IDをが必要な可能性もある．channel，tokenは `slack_notification` と同様にファイルからの読み込みに対応．

filepathには送信したいファイルのパスを指定する．

tokenまたはclientのいずれかは必須．clientを再利用する場合にはclientオブジェクトを渡して貰えば良い．
