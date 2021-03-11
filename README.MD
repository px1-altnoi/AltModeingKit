# このツールについて
平面上ないしはその延長線上ににvertexを再配置するツールです。

# How to USE
まず、基準とする3つのvertexを選択して、Set baseボタンを押して基準を設定します。
設定が終わったら平面上に動かしたいvertexを選択し、実行ボタンを押すと移動が実行されます。

# オプションの説明
三点に囲まれた内側のみに実行にチェックを入れると、動かしたいと選択したvertexのうち基準となる3点の内側に移動するもののみに移動が実行されます。

# インストール方法
右上のCodeをクリックして、Download Zipを選択してファイル群をダウンロードします。
![image](https://user-images.githubusercontent.com/54178323/110753588-18e9b800-828a-11eb-8dab-9f92393d5933.png)

ダウンロードしたら展開して、AltModelingKitをMayaのscriptフォルダー(~/document/maya/VERSION/scripts)に配置します。
それが完了したら、Script Editorから以下のコードを実行すると正しくインストールされていればウィンドウが立ち上がります。
```
import AltModelingKit.AltFlatten.ui as flatui

flatten_ui = flatui.flattenMainUI()
flatten_ui.show_dialog()
```
![image](https://user-images.githubusercontent.com/54178323/110753626-2606a700-828a-11eb-9381-1ac2fd34bca7.png)

これをshelfに登録しておきたい場合は`file > save script to shelf`から行うことが可能です。

# 頂点がうまく動いてくれない
動かしたい頂点と、基準となっている3点の距離が近いほうがうまくいきやすいです。それ以外で何か問題を発見した場合などは、twitterなどで作者にご報告ください。

# 現状認識している問題
きわめてまれな例であるが、内部でゼロ除算が発生するのを防止するために一部の頂点にうまく適用されないことがある。(内部の連立方程式を解くアルゴリズムの仕様による)
目下の対処療法としては、ベースとしている3点のうち一つを少しだけ動かしてやるだけで解消することが可能。
今後のアップデートで改善する予定。

# 今後の改良予定
上記問題の修正。
現在のアルゴリズムでは、平面に対して90°に投射されるようになっているのでそれ以外の角度でも行えないかの検討。

# ライセンス
MIT LICENCE(http://opensource.org/licenses/mit-license.php)
