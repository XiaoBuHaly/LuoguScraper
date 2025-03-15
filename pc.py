import requests
from bs4 import BeautifulSoup
import json
import time
import sys

# 允许用户输入范围（如 1000-1010）
start_id, end_id = map(int, input("请输入题号范围（如 1000-1010）：").split('-'))

# HTTP 头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Session 保持连接
session = requests.Session()

# ANSI 控制符：清除当前行和移动光标
CLEAR_LINE = "\033[K"
CURSOR_UP_ONE = "\033[A"

# 定义 spinner 的字符及初始下标
spinner_chars = ['|', '/', '-', '\\']
spinner_index = 0

def get_spinner():
    global spinner_index
    ch = spinner_chars[spinner_index % len(spinner_chars)]
    spinner_index += 1
    return ch

# 用于记录已成功提取的题号和失败的题号
completed_problems = []
failed_problems = []

# 定义进度条长度
PROGRESS_BAR_LENGTH = 30

# 定义各步骤提示（顺序不可变）
steps = ["请求连接", "解析HTML", "读取数据", "构造文本", "写入文本"]

# 打印状态函数：current 为当前题号，progress 为进度条进度（0～PROGRESS_BAR_LENGTH），current_step 为已完成步骤数量
def show_status(current, progress, current_step):
    # 清理之前输出的多行（2 行状态 + len(steps) 行步骤）
    total_lines = 2 + len(steps)
    for _ in range(total_lines):
        sys.stdout.write(CURSOR_UP_ONE + CLEAR_LINE)
    
    # 第一行：已完成范围
    if completed_problems:
        completed_range = f"{completed_problems[0]}-{completed_problems[-1]}" if len(completed_problems) > 1 else f"{completed_problems[0]}"
        sys.stdout.write(f"已经完成：P{completed_range}\n")
    else:
        sys.stdout.write("暂无已完成的题目\n")
    
    # 第二行：在“正在爬取”前方添加 spinner
    bar = "█" * progress + "-" * (PROGRESS_BAR_LENGTH - progress)
    sys.stdout.write(f"{get_spinner()} 正在爬取P{current} [{bar}]\n")
    
    # 后续行：逐行输出各步骤状态，已完成的在后面添加 ✓
    for i, state in enumerate(steps):
        if i < current_step:
            sys.stdout.write(f"{state} ✓\n")
        else:
            sys.stdout.write(f"{state}\n")
    
    sys.stdout.flush()

# 根据当前步数更新进度条（总步骤为 len(steps)）
def update_progress(current_step):
    return int(current_step * PROGRESS_BAR_LENGTH / len(steps))

# 爬取函数
def fetch_problem(problem_id):
    total_steps = len(steps)
    current_step = 0
    url = f'https://www.luogu.com.cn/problem/P{problem_id}'
    retry_count = 3
    html_content = None
    
    # Step 1: 发起请求
    for i in range(retry_count):
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text
            current_step = 1
            show_status(problem_id, update_progress(current_step), current_step)
            time.sleep(0.005)
            break
        except requests.exceptions.RequestException as e:
            show_status(problem_id, update_progress(current_step), current_step)
            time.sleep(2)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        script_tag = soup.find('script', {'id': 'lentille-context'})
        
        if script_tag:
            try:
                # Step 2: 解析 HTML
                data = json.loads(script_tag.string)
                problem = data['data']['problem']
                current_step = 2
                show_status(problem_id, update_progress(current_step), current_step)
                time.sleep(0.005)

                # Step 3: 读取数据
                title = problem.get('title', '未知标题')
                description = problem['content']['description']
                input_format = problem['content'].get('formatI', '无')
                output_format = problem['content'].get('formatO', '无')
                hint = problem['content'].get('hint', '无')
                samples = problem.get('samples', [])
                current_step = 3
                show_status(problem_id, update_progress(current_step), current_step)
                time.sleep(0.005)

                # Step 4: 构造 Markdown 文本
                md_result = f"# {title}\n\n"
                md_result += f"## 题目描述\n\n{description}\n\n"
                md_result += f"## 输入格式\n\n{input_format}\n\n"
                md_result += f"## 输出格式\n\n{output_format}\n\n"
                
                if samples:
                    md_result += f"## 输入输出样例\n\n"
                    for i, (inp, out) in enumerate(samples):
                        md_result += f"### 输入 #{i + 1}\n```\n{inp}\n```\n\n"
                        md_result += f"### 输出 #{i + 1}\n```\n{out}\n```\n\n"
                
                current_step = 4
                show_status(problem_id, update_progress(current_step), current_step)
                time.sleep(0.005)

                # Step 5: 写入文件
                with open(f'P{problem_id}.md', 'w', encoding='utf-8') as file:
                    file.write(md_result)
                
                completed_problems.append(problem_id)
                current_step = 5
                show_status(problem_id, update_progress(current_step), current_step)
                time.sleep(0.005)
                
            except Exception as e:
                failed_problems.append(problem_id)
                show_status(problem_id, update_progress(current_step), current_step)
                sys.stdout.write(f"解析失败：{e}\n")
                sys.stdout.flush()

# 执行批量爬取
for problem_id in range(start_id, end_id + 1):
    # 每个题目开始时，显示初始状态（所有步骤均未完成）
    show_status(problem_id, update_progress(0), 0)
    fetch_problem(problem_id)
    time.sleep(0.005)

# 任务完成后，输出最终状态
show_status("完成", PROGRESS_BAR_LENGTH, len(steps))
sys.stdout.write("\n所有题目抓取完成！\n")
