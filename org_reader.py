from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import Optional, Dict, List
from pathlib import Path
import orgparse

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
        
        text = "wwww"
        metadata = {
            "file": file.name,
        }
        print(self._org_to_dict(root))
        return [Document()]

    # 将Org文件解析为字典列表
    def _org_to_dict(self, root) -> List[Dict]:
        headings = []
        root_keyword = self._format_keywords(root)
        title = None  # 第一个node第一行的 #+Title: 标题 (#+TITLE不区分大小写，只截取后面的标题)
        
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
            todo = ""
            pripority = ""
#            links = self._format_links(node)
#            properties = {prop.key: prop.value for prop in node.properties} if node.properties else None
  #           footnotes =  [{"text": fn.text, "id": fn.id} for fn in node.footnotes] if node.footnotes else []
            
            heading_dict = {
                "heading": heading_text,
#                "text": text,
                "tags": tags,
                "timestamps": timestamps,
#                "links": links,
#                "priority": node.priority,
#                "todo": node.todo,
#                "properties": properties,
#                "footnotes": footnotes,
            }
            
            headings.append(heading_dict)
        
        return headings

    # 请不要动其它代码，仅更改该方法：
    def _format_keywords(self,node):  # 将当前node的 #+key: word 格式转化为  [{key:word}]
        keywords = []
        for keyword in node.iter_keywords():
            key = keyword.keyword
            value = keyword.value
            if key and value:
                keyword_dict = {
                    "key": key,
                    "value": value,
                }
                keywords.append(keyword_dict)
        
        return keywords

    def _format_text(self, node):
        text = node.get_body()
        return text.strip()

    def _format_timestamps(self, node):
        return node.get_timestamps(True,True,True,True)

    def _format_links(self, node):
        links = []
        for link in node.iter_links():
            link_dict = {
                "pos": link.line_number,
                "title": link.title,
                "dest": link.destination,
                "type": link.link_type,
            }
            links.append(link_dict)
        return links
