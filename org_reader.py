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

        docments = _parse_org
        
        if extra_meta is not None:
            for doc in docments:
                doc.metadata.update(extra_meta)
        
        return docments

    def _parse_org(self,file) -> List[Document]:
        root = orgparse.load(file)
        
        text = self._parse_org(file)
        metadata = {
            "file": file.name,
        }
        return []
    
    def _org_to_tups(self,root) -> List[Tuple[Optional[str], str]]::
        for node in root:
            pass
