from llama_index.readers.base import BaseReader
from llama_index import Document
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
        
        metadata = {"file_name": file.name}
        if extra_info is not None:
            metadata.update(extra_info)
        return [Document(text=text, metadata=metadata or {})]
