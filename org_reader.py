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

        docments = _parse_org(file)
        
        if extra_meta is not None:
            for doc in docments:
                doc.metadata.update(extra_meta)
        
        return docments

    def _parse_org(self, file) -> List[Document]:
        root = orgparse.load(file)
        
        text = self._parse_org(file)
        metadata = {
            "file": file.name,
        }
        return []

    # 将Org文件解析为字典列表
    def _org_to_dict(self, root) -> List[Dict]:
        headings = []
        for node in root:
            heading_text = ""
            if node.heading:
                heading_text = " ".join(node.heading)
            
            text = self._format_text(node)
            tags = [tag.name for tag in node.tags] if node.tags else None
            timestamps = self._format_timestamps(node)
            links = self._format_links(node)
            properties = {prop.key: prop.value for prop in node.properties} if node.properties else None
            footnotes = [{"text": fn.text, "id": fn.id} for fn in node.footnotes] if node.footnotes else []
            
            heading_dict = {
                "heading": heading_text,
                "text": text,
                "tags": tags,
                "timestamps": timestamps,
                "links": links,
                "priority": node.priority,
                "todo": node.todo,
                "properties": properties,
                "footnotes": footnotes,
            }
            
            headings.append(heading_dict)
        
        return headings

    def _format_text(self, node):
        text = ""
        for item in node:
            if isinstance(item, orgparse.OrgNode):
                text += self._format_text(item)
            elif isinstance(item, str):
                text += item + "\n"
        return text.strip()

    def _format_timestamps(self, node):
        timestamps = []
        for timestamp in node.timestamps:
            timestamps.append(timestamp.isoformat())
        return ", ".join(timestamps)

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
