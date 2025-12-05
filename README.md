langchain-1.0 入门学习 -  B站：强哥学编程

参考 https://docs.langchain.com/oss/python/learn

安装
一，基础工具
1.	安装 python              https://www.python.org/
2.	安装 anaconda            https://www.anaconda.com/
3.	安装 visual studio code  https://code.visualstudio.com/
4.	安装 git                 https://git-scm.com/

二、开发环境
1.	创建 conda 环境
开始 -> anaconda prompt
(base) C:\Users\xiaoq>conda create -n py311-langchain1.0 python=3.11
(base) C:\Users\xiaoq>conda activate py311-langchain1.0
(py311-langchain1.0) C:\Users\xiaoq>

2. 切换到工作目录
(py311-langchain1.0) d:/ai-ide-workspace/mylangchain1.0

3. 启动VSC
code .

三、安装 langchain 核心包
开始 -> anaconda prompt
(base) C:\Users\xiaoq>conda activate py311-langchain1.0
(py311-langchain1.0) D:/ai-ide-workspace/mylangchain1.0/
pip install langchain
pip install langchain-community

四、安装 Ollama 
1. 安装 Ollama：https://ollama.com/ 
2. 下载模型：https://ollama.com/search
   1）聊天模型：ollama pull deepseek-r1:1.5b
               ollama pull llama3.2:3b
   2）嵌入模型：ollama pull nomic-embed-text
   查看： ollama list
3. 安装 langchain-ollama
   pip install langchain-ollama

五、安装 deepseek api 接口
pip install langchain-deepseek

六、安装向量数据库
pip install chromadb
pip install langchain-chroma

七、git 下载
1. 下载
   git clone https://github.com/yixiaoqiang-design/mylangchain1.0
2. 使用
   pip install -r requirments.txt
   
八、安装dashscope
pip install dashscope
