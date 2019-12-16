# Spectrum Conversion for Sound Recognition

## Requirements

### Install Packages / Modules

```sh
$ pip install -r requirments.txt
```

+ pydub
+ numpy
+ pandas
+ matplotlib
+ seaborn
+ scipy
+ Pillow
+ librosa

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

When you exec script, it will create a folder. And a plotted image, or a spectrogram image is saved in the folder.  
The folder name is `filename` that without extension.

<br>

You can switch action(function) by changing value of `global_variable.py`.  
Basically, it can use, just switch `True` or `False`.

Example, 

1. save images or waves.

   ```python
   # If you want to save images, it is True.
   self.is_save_img = True
   
   # If you want to save waves, it is True.
   self.is_save_wav = True
   ```

2. separate wave data every one second.

   ```python
   self.is_separate = True
   ```

3. crop image (for using as learning data).

   ```python
   self.is_crop = True
   ```

4. show spectrogram on window.

   ```python
   # You should specify which one.
   
   # If you want to show spectrogram images one by one, it is True.
   # In this case, you have to close a window and next spectrogram images will showed.
   self.plt_show_img = True
   
   # If you want to show spectrogram images continuously, it is True.
   # In this case, you do not have to close a window.
   self.plt_show_pause = True
   ```

5. show X and Y axes.

   ```python
   self.plt_conf = {
   	'xy': True,
       # ...
   }
   ```

6. show color bar.

   ```python
   self.plt_conf = {
   	'cbar': True,
       # ...
   }
   ```

<br>

**Note:** When you specified wave files were not `.wav`, their files are ignored automatically.