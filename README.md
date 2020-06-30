# mmsensor_cam
三密予防システム　人数検知カメラ

# 概要
  
 三密要望システムの人数検知カメラプログラムです。
  
 PiCameraを装着したRaspberryPi側で動作し、カメラ内で検知された人数を指定のURLに投稿します。

# 導入方法
  
RaspberryPi上で以下を実行します。
  
# ソースのチェックアウト
```
git clone https://github.com/tt-hasegawa/mmsensor_cam.git
```

# URLの編集
  
 PopulationSensor.pyの冒頭以下の部分を環境に即した値に変更する。

``` 
url='http://192.168.46.128:3000' # 接続先herokuサーバのURL
proxies = { # Proxyがある場合
    'http': 'http://proxy:12080',
    'https': 'http://proxy:12080'
}
proxies = { # Proxyが無い場合
   'http': None,
   'https': None
}
```

# 実行登録
  
 以下のコマンドを実行し、cronに登録があるか、確認する。
```
crontab -l
``` 
 有無を確認する行
```
@reboot /bin/sh /home/pi/mmsensor_cam/population-sensor.sh
```
 登録が無ければ、以下のコマンドでcronの編集モードに入り、追記する。
```
crontab -e
```
末尾に以下を追記する。
```
@reboot /bin/sh /home/pi/mmsensor_cam/population-sensor.sh
```

# 再起動する。
```
sudo reboot
```
# ログ確認
 以下のコマンドで実行ログを確認する。

```
tail -f /tmp/sensor-popluation.log
```
 ログ確認を止める場合、Ctrl + C
