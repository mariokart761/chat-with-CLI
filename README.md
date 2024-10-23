# Introdution
簡單實現使用CLI與OpenAI模型對話的功能

---
# Install dependencies
```sh
pip install -r requirements.txt
```
## or using conda env
```sh
conda create -n chatGPT-client python=3.12
conda activate chatGPT-client
pip install -r requirements.txt
```

---
# Usage
## 免費仔對話 啟動
```sh
python main.py -i g4f
```
使用g4f，第一次對話啟動較慢，預設使用`gpt-4o-mini`模型。

## OpenAI API Key對話 啟動
```sh
python main.py -i openai
```
需要OpenAI API Key，預設使用`gpt-4o-mini`模型。  
API Key可以直接在程式碼裡設置，或是匯出為環境變數（可參考[官方文檔](https://platform.openai.com/docs/quickstart)）。

## 功能
- 在對話框輸入`--save <檔名.md>`可將AI的回覆儲存至`./saved_file`目錄下
- 在對話框輸入`--exit` 可退出