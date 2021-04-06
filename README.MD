# このツールキットについて
Mayaでモデリングしている際に役に立ちそうかなというツール群です。

# Contents
- AltFlatten
　vertexを3点選択し、仮想平面を作成しその平面上に乗るようにそののちに選択したvertexを移動するツールです。
- AltIreko
　MayaのIsolate selectを何度も連続で行えるようにしたツールです。

# インストール方法
[一般ユーザー向け]
現在、ファイルを一つドラッグアンドドロップするだけでインストールを可能にするツールを準備中です。しばらくお待ちください。

[上級者向け]
右上のCodeをクリックして、Download Zipを選択してファイル群をダウンロードします。
![image](https://user-images.githubusercontent.com/54178323/110753588-18e9b800-828a-11eb-8dab-9f92393d5933.png)

ダウンロードしたら展開して、AltModelingKitをMayaのscriptフォルダー(~/document/maya/VERSION/scripts)に配置します。
それが完了したら、Script Editorから以下のコードを実行すると正しくインストールされていればウィンドウが立ち上がります。
```
# AltFlattenを使いたい場合
import AltModelingKit.AltFlatten.ui as flatui

flatten_ui = flatui.flattenMainUI()
flatten_ui.show_dialog()
```

```
# AltIrekoを使いたい場合
import AltModelingKit.AltIreko.ui as ireko

ireko_ui = ireko.IrekoMainWnd()
ireko_ui.show_dialog()
```

![image](https://user-images.githubusercontent.com/54178323/110753626-2606a700-828a-11eb-9381-1ac2fd34bca7.png)

これをshelfに登録しておきたい場合は`file > save script to shelf`から行うことが可能です。

# ライセンス
MIT LICENCE(http://opensource.org/licenses/mit-license.php)
