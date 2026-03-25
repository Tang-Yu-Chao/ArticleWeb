import os, json

#位于仓库根目录，把path目录下的所有 .md 变成网页能读的列表存到data.json。
#这里可以改为：1个.md一个句子列表，或识别一个.md中的一个句子(空行或一级标题或二级标题)作为一个句子列表，填到 data.json 
#data.json 是一个列表，里面每个元素是一个字符串（句子或文章）。


def build():
    qs = []
    path = "quotes"
    if os.path.exists(path):
        for f in sorted(os.listdir(path)):
            if f.endswith(".md"):
                with open(os.path.join(path, f), 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    #按空行(不是换行，是2个段落间空一行)拆分文章 
                    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
                    qs.extend(paragraphs) 
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(qs, f, ensure_ascii=False, indent=4)
if __name__ == "__main__":
    
    build()
