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
            extra_info: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse File"""
        if not isinstance(file, Path):
            file = Path(file)
        
        text = self._parse_org(file)
        metadata = {"file_name": file.name}
        
        if extra_info is not None:
            metadata.update(extra_info)
        return [Document(text=text, metadata=metadata or {})]

    def _parse_org(self,file):
        root = orgparse.load(file)
        
        for node in root:
            print(node)
        return str(root)
