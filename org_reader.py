from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import Optional, Dict, List
from pathlib import Path
import orgparse
import re

class OrgReader(BaseReader):
    """
    OrgReader负责解析Org文件
    """
    def load_data(
            self,
            file:Path,
            extra_meta: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse File"""
        if not isinstance(file, Path):
            file = Path(file)

        docments = self._parse_org(file)
        
        if extra_meta is not None:
            for doc in docments:
                doc.metadata.update(extra_meta)
        
        return docments

    def _parse_org(self, file) -> List[Document]:
        root = orgparse.load(file)
        documents = []
        for dict in self._org_to_dict(root):
            text = dict.pop("text")
            dict["file"] = file
            doc = Document(text=text,metadata=dict)
            documents.append(doc)
        return documents

    # 将Org文件解析为字典列表
    def _org_to_dict(self, root) -> List[Dict]:
        headings = []
        root_keyword = self._format_keywords(root)
        title = root_keyword["TITLE"]
        
        for node in root:
            heading_list = []
            heading_text = ""
            if title:
                heading_list.append(title)
            if node.heading:
                for l in range (1,node.level):
                    p_node = node.get_parent(l)
                    heading = p_node.heading
                    heading_list.append(heading)
                heading_list.append(node.heading)
                heading_text = " ".join(heading_list)
            
            text = self._format_text(node)
            tags = [tag for tag in node.tags] if node.tags else None
            timestamps = self._format_timestamps(node)
            keywords = self._format_keywords(node)
            links = self._format_links(node)
            todo = ""
            pripority = "B"
            properties = []
            if node is orgparse.node.OrgNode:
                todo = node.todo
                pripority = node.pripority
            if node.properties:
                properties = node.properties
            
            heading_dict = {
                "heading": heading_text,
                "text": text,
                "tags": tags,
                "timestamps": timestamps,
                "links": links,
                "priority": pripority,
                "todo": todo,
                "properties": properties,
                "keywords":keywords
            }
            
            headings.append(heading_dict)
        
        return headings

    def _format_keywords(self,node):
        keyword_dict = {}
        body_text = node.get_body(format="raw")
        keyword_lines = re.findall(r'^#\+(\w+): (.+)$', body_text, re.M)
        for key, value in keyword_lines:
            keyword_dict[key.upper()] = value
        
        return keyword_dict

    def _format_text(self, node):
        text = node.get_body(format="raw")
        text = self.remove_org_formatting(text)
        link_pattern = r"\[\[([^\[\]]+?)(?:\]\[([^\[\]]+?))?\]\]"
        text = re.sub(link_pattern, r"\2", text)
        dy_pattern = re.compile(r'^\s*["“]?([^"\n:]+)["”]?\s*::', re.MULTILINE)
        text = re.sub(dy_pattern, r"\1:", text)
        text = self.replace_footnotes(text)
        return text.strip()

    def remove_org_formatting(self,text: str) -> str:
        # 把格式符号和内容一起匹配，但只保留内容
        pattern = re.compile(r'''
        (\s|^)                # 空格或行首
        ([*/_~=\-+^])           # 起始符号
        ([^\s].*?[^\s])       # 中间内容，不能以空格开头或结尾
        \2                    # 结束符号必须和起始相同
        (?=\s|$)              # 后面是空格或行尾
        ''', re.VERBOSE)

        # 替换时只保留前缀空格和中间内容
        return pattern.sub(lambda m: m.group(1) + m.group(3), text)

    def replace_footnotes(self,text: str) -> str:
        # 提取所有脚注定义：如 [fn:1] 脚注内容
        footnote_defs = dict(re.findall(r'^\[fn:([^\]]+)\]\s+(.+)$', text, flags=re.MULTILINE))

        # 替换正文中引用 [fn:1] 为 脚注文本
        def replacer(match):
            key = match.group(1)
            value = footnote_defs.get(key, f"未找到脚注：{key}")
            return f'（脚注：{value}）'

        # 替换所有脚注引用
        text_with_replacements = re.sub(r'\[fn:([^\]]+)\]', replacer, text)
        
        # 可选：删除原始脚注定义段落
        text_cleaned = re.sub(r'^\[fn:[^\]]+\]\s+.+$', '', text_with_replacements, flags=re.MULTILINE)
        
        return text_cleaned.strip()


    def _format_timestamps(self, node):
        timestamps = node.get_timestamps(True,True,True,True)
        dates = []
        for timestamp in timestamps:
            dates.append(str(timestamp))
        return dates

    def _format_links(self, node):
        links = []
        text = node.get_body(format="raw")
        pattern = r"\[\[([^\[\]]+?)(?:\]\[([^\[\]]+?))?\]\]"
        results = re.findall(pattern, text)
        for link in results:
            dest = link[0]
            type = "internal link or anchor"
            link_s = dest.split(":")
            text_line = text.split("\n")
            dest_pattern = r'\b' + re.escape(dest) + r'\b' 
            pos = 1
            if len(link_s) > 1:
                type = link_s[0]
            for line in text_line:
                if re.search(pattern, line, re.IGNORECASE):
                    break
                pos+=1
            link_dict = {
                "pos": pos,
                "title": link[1],
                "dest": dest,
                "type": type,
            }
            links.append(link_dict)
        return links

    def _format_targets(self,node):
        pass
