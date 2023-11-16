# 創建虛擬Python環境
Python 應用程式會匯入多個函式庫，通常，所需函式庫的不同版本之間可能會發生衝突。但是，您的應用程式可能需要特定的庫版本進行bug調試。建立一個虛擬環境，即針對特定 Python 安裝的一套獨立的函式庫是一個針對偵錯程式碼很好的解決方案。

我們將使用Python 的內建虛擬環境功能，該功能在Python 3.3 版本中引入，並提供[名為venv 的內建環境模組](https://docs.python.org/3/tutorial/venv.html).您可能會問為什麼我們不使用Conda。原因是因為[Conda/Miniconda 現在位於 IBM 的「請勿使用」清單中](https://w3.ibm.com/w3publisher/ossc-process/exception-and-do-not-use)

在下方建立虛擬 Python 環境時，您也會安裝完成本訓練營所需的所有函式庫，包括 Jupyter Notebooks、Watson Machine Learning Python SDK、Hugging Face 函式庫、ChromaDB 和 LangChain。

#### 升級到 Python v3.11 以避免任何衝突
升級 Python 版本可能很複雜，因此在過程中不要害怕尋求協助。我們已記錄了最佳實踐來為您提供幫助。使用 Python 3.8 plus 可能沒有任何問題，但請記住，即使 Python 3.9 也已經有 2.5 歲了。 [請遵循以下最佳實務升級到 Python 3.11](upgrade-python.md).

#### 創建你的Python虛擬環境
建立一個資料夾，您將在其中建立和儲存 Python 虛擬環境。然後打開終端機/控制台視窗並輸入以下命令來建立名為`venv`的 Python 環境。新的虛擬環境將產生一個同名的本機目錄。

```
cd <directory to store your Python environment>
python3 -m venv .venv
```

#### 下載 requirements_venv.txt
下載 [requirements_venv.txt](./requirements_venv.txt) 其中包含要在您的環境中安裝的初始軟體包的清單。在執行命令之前，將requirements.txt 檔案移至您為Python 環境建立的資料夾。請注意，需求檔案應該已經從先前clone的儲存庫中下載！

#### 啟動您的Python虛擬環境
執行以下命令:
```
source .venv/bin/activate
python3 -m pip install -r requirements_venv.txt
```

您可以透過查看終端機/控制台視窗中提示行的開頭來驗證您的環境是否處於活動狀態。如下所示，提示符的開頭會變更為 show (venv)。

<p align="left">
  <img src="images/environment-activated-python.png" width="500"/>
</p>

注意：如果您是 Windows 用戶，請依照[Setting-up-Python-Virtual-Environment-in-Windows.docx](./Setting-up-Python-Virtual-Environment-in-Windows.docx) 執行。

注意：如果您沒有 M1 晶片，您可能會收到以下錯誤：
```
× Building wheel for chroma-hnswlib (pyproject.toml) did not run successfully.
```
如果是這樣，請嘗試這兩個解決方案之一，更換 `python3 -m pip install -r requirements_venv.txt` 為
```
export HNSWLIB_NO_NATIVE=1
python -m pip install -r requirements_venv.txt
```
或者
```
ARCHFLAGS="-arch x86_64" python3 -m pip install -r requirements_venv.txt
```

#### 停用您的 Python 虛擬環境
如果您需要變更到不同的環境，可以使用以下命令停用目前環境：
```
deactivate
```
