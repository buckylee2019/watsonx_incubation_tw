# 创建虚拟Python环境
Python 应用程序导入多个库，通常，所需库的不同版本之间可能会发生冲突。 但是，您的应用程序可能需要特定的库版本进行bug调试。 创建一个虚拟环境，即针对特定 Python 安装的一套独立的库是一个针对调试代码很好的解决方案。

我们将使用 Python 的内置虚拟环境功能，该功能在 Python 3.3 版本中引入，并提供 [名为 venv 的内置环境模块](https://docs.python.org/3/tutorial/venv.html). 您可能会问为什么我们不使用 Conda。 原因是因为[Conda/Miniconda 现在位于 IBM 的“请勿使用”列表中](https://w3.ibm.com/w3publisher/ossc-process/exception-and-do-not-use) 

在下面创建虚拟 Python 环境时，您还将安装完成本训练营所需的所有库，包括 Jupyter Notebooks、Watson Machine Learning Python SDK、Hugging Face 库、ChromaDB 和 LangChain。

#### 升级到 Python v3.11 以避免任何冲突
升级 Python 版本可能很复杂，因此在此过程中不要害怕寻求帮助。 我们已记录了最佳实践来为您提供帮助。 使用 Python 3.8 plus 可能没有任何问题，但请记住，即使 Python 3.9 也已经有 2.5 岁了。  [请遵循以下最佳实践升级到 Python 3.11](upgrade-python.md).

#### 创建你的Python虚拟环境
创建一个文件夹，您将在其中创建和存储 Python 虚拟环境。 然后打开终端/控制台窗口并输入以下命令来创建名为`venv`的 Python 环境。 新的虚拟环境将产生一个同名的本地目录。

```
cd <directory to store your Python environment>
python -m venv .venv
```

#### 下载 requirements_venv.txt
下载 [requirements_venv.txt](./requirements_venv.txt) 其中包含要在您的环境中安装的初始软件包的列表。 在运行命令之前，将requirements.txt 文件移至您为Python 环境创建的文件夹。 请注意，需求文件应该已经从之前克隆的存储库中下载！

#### 激活您的Python虚拟环境
执行以下命令:
```
source .venv/bin/activate
python -m pip install -r requirements_venv.txt
```

您可以通过查看终端/控制台窗口中提示行的开头来验证您的环境是否处于活动状态。 如下所示，提示符的开头更改为 show (venv)。

<p align="left">
  <img src="images/environment-activated-python.png" width="500"/>
</p>

注意：如果您是 Windows 用户，请按照[Setting-up-Python-Virtual-Environment-in-Windows.docx](./Setting-up-Python-Virtual-Environment-in-Windows.docx) 执行。

注意：如果您没有 M1 芯片，您可能会收到如下错误：
```
× Building wheel for chroma-hnswlib (pyproject.toml) did not run successfully.
```
如果是这样，请尝试这两种解决方案之一，更换 `python -m pip install -r requirements_venv.txt` 为
```
export HNSWLIB_NO_NATIVE=1
python -m pip install -r requirements_venv.txt
```
或者
```
ARCHFLAGS="-arch x86_64" python -m pip install -r requirements_venv.txt
```

#### 停用您的 Python 虚拟环境
如果您需要更改到不同的环境，可以使用以下命令停用当前环境：
```
deactivate
```
