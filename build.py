import os
import json
import re

def extract_title_and_content(md_content):
    """从 Markdown 内容中提取标题（第一个 # 开头行）和正文"""
    lines = md_content.split('\n')
    title = "无标题"
    for line in lines:
        if line.strip().startswith('# '):
            title = line.strip()[2:].strip()
            break
    return title, md_content

def build():
    articles = []
    path = "quotes"
    if os.path.exists(path):
        for f in sorted(os.listdir(path)):
            if f.endswith(".md"):
                file_path = os.path.join(path, f)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        title, full_content = extract_title_and_content(content)
                        slug = f.replace('.md', '')
                        articles.append({
                            "slug": slug,
                            "title": title,
                            "content": full_content
                        })
    
    # 生成两个文件：列表数据和文章详细数据
    with open('articles.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    # 为每篇文章生成单独的 JSON 文件（供详情页使用）
    os.makedirs('articles', exist_ok=True)
    for article in articles:
        with open(f'articles/{article["slug"]}.json', 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    build()
