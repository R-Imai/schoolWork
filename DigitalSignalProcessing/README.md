# FourieTransform.py使用方法

## 環境設定
### pythonインストール
このプログラムはpython3.4を使用して書かれています。
pythonを使用したことの無い方は[こちら](https://www.python.org/downloads/release/python-343/ "Title")からインストーラーをダウンロードしてpythonをインストールしてください。<br>
次にパスの設定があるので、[windows]+[e]でエクスプローラを開き、右上にある「システムのプロパティ」をクリック。<br>
左側にある「システムの詳細設定」へ移動します。
出てきたウィンドウの下の方の「環境変数(N)」をクリック。<br>
「システム環境変数」の中の「Path」をクリックし、「編集」をクリックします。<br>
「変数値」の最後に「c:￥python34;」と加えてください。(このとき元から書いてあるものを消さないように)<br>
パスが通ったか確認するのでコマンドプロンプトを開きます。([Windows]+[R]で出てきたやつに「cmd」と打ちエンター)<br>
「python」とうちエラーが出なかったらOKです。
### 各種ライブラリインストール
今回使用するライブラリは、<br>
・ [numpy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)<br>
・ [scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)<br>
・ [matplotlib](http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib)<br>
の三つです。上記がリンクになったいるのでそれぞれ自分のバージョンに合っているもの(この場合は3.4なのでcp34、win32とwinはbit数の違いです)<br>
それぞれダウンロードして来たら、**管理者権限で**コマンドプロンプトを開きます。<br>
そこに、
```
pip install ダウンロードしてきたファイル
```
と打って上記三種類をインストールします。<br>
ちゃんとインストールできたか確認します。コマンドプロンプトで、「python」と打ってから
```python
import numpy
import scipy
import matplotlib
```
とうってなにも出なければ設定は完了です。

## FourieTransform.py使用方法
このプログラムはフーリエ変換をしてグラフ出力するものです。
使用しているのはscipyのfftpackです。
まずGitHubから任意の場所へFourieTransform.pyをダウンロードしてください。
コマンドプロンプトを開き、
```
cd ダウンロードしたフォルダまでのパス
```
とうち、そのフォルダまで移動します。
次に
```
python FourieTransform.py 入力ファイル名 サンプリング間隔 範囲 値1 値2
```
の順で入力してください。<br>
ここで範囲以降は以下に従って入力してください。<br>
-a: すべての区間　　　　　(値1)(値2)は入力なし<br>
-n: N間隔ですべての領域　 (値1)にNの値を指定。最初からN間隔でフーリエ変換<br>
-s: 開始点のみ(値1)に指定　　　　(値2)は入力なし<br>
-f: 終端点のみ(値1)に指定　　　　(値2)は入力なし<br>
-p: 開始点,終端点を(値1)(値2)に指定<br>

この使い方は
```
python FourieTransform.py help
```
で確認できます。<br><br>
以上が正しく入力出来ているとグラフが表示されるはずです。
