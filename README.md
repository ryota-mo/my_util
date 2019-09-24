# util
便利ツールリポジトリ

## get_vacant_gpu.py
dgxなどのnvidia-smiコマンドが利用可能なgpuで最もGPU利用率が低いGPUを返す．

```
os.environ["CUDA_VISIBLE_DEVICES"] = get_vacant_gpu()
```
として利用可能．

## slack_notification.py
SlackのIncoming Webhook を使って通知を送信できる．URLはワークスペースのカスタマイズ内の，カスタムインテグレーションから取得する．他人に迷惑のかからないように自分宛てのDMを選ぶなどすること．

`pip install requests` が必要．

`slack_notification(webhook_url, text, username=None, **kwargs)` で利用．

kwargsにはチャンネルの指定などが考えられる．また， `attachments` 属性にリストを入れるのも良い．

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
