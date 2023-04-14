# EMA_with_voice
本專案將 EMA 團隊開發的數學詳解影音動畫生成系統，加上詳解語音。

## 環境建置
本專案將 Anaconda 建置於 VScode 上執行

### Anaconda
> [下載 Anaconda](https://www.anaconda.com/products/distribution)
### VScode
> [下載 VScode 1.76](https://code.visualstudio.com/Download) 或更高版本
### MiKTeX
> [下載 MiKTeX](https://cantor.math.ntnu.edu.tw/workshop/animated_math/files/Latex-x64.zip)
> [下載完成後請以系統管理員執行 install.cmd]

* 創建虛擬環境及 Python 3.10 (或更高版本)
```sh
$ conda create --name ema python=3.10 #創建虛擬環境
$ conda activate ema #啟動虛擬環境
```
* 安裝 manim 及 manim voice-over(注意需要到「Microsoft Azure → 資源 → Text-to-Speech」中取得金鑰)
```sh
$ conda install -c conda-forge manim
$ pip install "manim-voiceover[azure,gtts]" # 注意需要將「電腦設定 → 地區 → UTF-8 全球設定」打勾
```
* 創建動畫及語音
```sh
$ manim test_ema.py
```

##註
已經盡可能把所有安裝過程書寫完善，如有缺漏再麻煩提醒我
