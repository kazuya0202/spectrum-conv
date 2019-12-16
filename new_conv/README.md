# Spectrum Convertion

## Requirements

### Install Packages / Modules

```sh
$ pip install -r requirments.txt
```

<br>

## Usage

### Exec Script

+ Default

  ```sh
  $ python main.py <wav_path>
  ```

+ Specify multi wave files

  ```sh
  $ python main.py <wav1_path> <wav2_path> ...
  # or 
  $ python main.py *.wav
  ```

<br>

### Details

When you exec script, it will create a folder. And plotted image, or spectrogram is saved in the folder.  
The folder name is `filename` that without extension.

<br>

You can switch action(function) by changing value of `global_variable.py`.  
Basically, it can use, just switch `True` or `False`.

Example, 

1. show spectrogram on window.
2. show X and Y axes.
3. show color bar.
4. crop image for using as learning data.

