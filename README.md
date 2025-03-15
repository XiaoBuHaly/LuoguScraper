# LuoguScraper
**LuoguScraper** 是一个 Python 爬虫程序，旨在自动化地从[洛谷](www.luogu.com.cn)网站抓取编程题目的数据，并将其保存为 Markdown 格式。
爬虫程序能够显示进度条、显示提示信息，能有效地处理错误并重试。

## 特性
- 进度条：提供实时的进度条显示，显示进度。
- 状态提示：爬虫运行时每一步操作（如请求连接、解析HTML）都有对应的状态更新。
- 错误处理：爬虫会在请求失败时进行多次重试，并记录爬取失败的题目序号。
- Markdown 输出

## 安装
### 方法一: git克隆仓库
打开git bash粘贴以下命令
```bash
git clone https://github.com/XiaobuHaly/LuoguScraper.git
cd LuoguScraper
pip install -r requirements.txt
python luogu_scraper.py
```

### 方法二：下载源码ZIP
#### 获取
1. 点击右上角"<>Code"
2. 在下拉菜单中点击最下面的Download ZIP
3. 等待下载完成
4. 解压LouguScraper-main.zip（实际文件名可能有所差异）

#### 使用
1. 进入含有pc.py的目录
2. 在该目录打开cmd
3. 在cmd中输入以下命令以安装依赖
```cmd
pip install requests bs4 json time sys
```
4. 继续在cmd中输入以下命令以启动爬虫
```cmd
python pc.py
```

### **恭喜你现在已经成功地打开了爬虫！**

## 功能描述
1. 当用户输入xxxx-yyyy时爬取洛谷对应的**P**xxxx-**P**yyyy题目
2. 爬虫开始运行后会自动抓取网页数据并显示当前进度。
   在爬取过程中，你会看到每一步的状态更新。
3. 爬虫会将每个题保存为对应的.md文件。

## 输出样例
进入程序
```css
请输入题号范围（如 1000-1010）：1000-1010
```
正在运行
```css
已经完成：P1000-1001
/ 正在爬取P1002 [█████████---------]
请求连接 ✓
解析HTML ✓
读取数据 ✓
构造文本
写入文本
```

## 文件结构（有必要写吗？）
```bash
├── pc.py
├── README.md
└── LICENSE
```

## 依赖说明
- `requests`：用于发送HTTP请求
- `BeautifulSoup`：用于解析网页内容
- `json`：用于处理json数据格式内容
- `time`和`sys`：用于控制爬取进度和输出

## 贡献
欢迎提交问题、建议和拉去请求。如果你有好的想法或功能建议，请题 Issue 或直接发送 Pull Request.

## LICENSE
MIT LECENSE
