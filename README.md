# Spectrum-conv

<br>

### パッケージ・モジュール

```bash
$ pip install -r requirements.txt
```
+ pydub
+ numpy
+ pandas
+ matplotlib
+ seaborn

<br>

### 実行

※ デフォルトでは`crossing1.wav`が指定されている

```bash
$ python spectrum-conv.py
```

<br>

+ ファイルを指定する場合

```bash
$ python spectrum-conv.py {wavファイル}
```

+ ディレクトリを指定する場合

```bash
$ python spectrum-conv.py {wavファイルのディレクトリ}
```

<br>

### 出力結果

+ crossing1.wav - result
![crossing1.jpg](https://github.com/kazuya0202/spectrum-conv/blob/master/spectrum-save-img/crossing1_001.jpg)

+ cat1.wav - result
  ![cat.1jpg](https://github.com/kazuya0202/spectrum-conv/blob/master/spectrum-save-img/cat1_001.jpg)

<br>

---

<br>

### separate-wav.py

wavファイルを1秒間隔で、0.1秒ずつずらしながら分割保存する。

```bash
$ python separate-wav.py {wavファイル}
$ python separate-wav.py {wavファイルのディレクトリ}
```

>  出力先：`export/`

<br>

+ ファイルを指定する場合

  + ファイル名（拡張子なし）のフォルダが作られ保存される。

    ```bash
    # 例
    $ python separate-wav.py audio.wav
    
    # => export/audio/audio_0.wav
    # => export/audio/audio_1.wav ...
    ```

+ ディレクトリを指定する場合

  + ディレクトリ / ファイル名のフォルダが作られ保存される。

    ```bash
    # 例
    $ python separate-wav.py data/
    
    # => export/data/audio1/audio_0.wav
    # => export/data/audio1/audio_1.wav ...
    ```

    > data/
    >     audio1.wav
    >     audio2.wav
    >     ...

<br>

### run-conv.py

分割保存したデータをスペクトログラムに変換する。（内部で`spectrum-conv.py`を実行する）

+ `separate-wav.py`と同じ引数を渡す。（自動的に`export/`内の分割ファイルを参照する）
