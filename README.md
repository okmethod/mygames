# mygames

## やること
pygameを使用して、pythonでゲームを実装する。

## 目的
- オブジェクト指向プログラミングの練習をする。
- MVC(Model/View/Controller)に基づき、設計や再利用の練習をする。
- 実装を通して、ゲームへの理解を深める。

## ディレクトリ構成
    .
    ├── README.md
    ├── bin
    │   └── <project>
    │       ├── __init__.py
    │       ├── __main__.py
    │       └── *.py
    ├── lib
    │   └── <package>
    │       ├── __init__.py
    │       └── *.py
    └── media
        ├── png
        │   └── *.png
        ├── wav
        │   └── *.wav
        │   ...
        └── etc

※現状は、ソースファイルごとに`sys.path.append('自作モジュール格納先ディレクトリパス')`を記載してimportしている。   
※将来的には、インストール可能なパッケージにしたい。   

## 実装済みゲーム一覧
- 顔面リバーシ
- 坊主めくり（作成中）
- 
