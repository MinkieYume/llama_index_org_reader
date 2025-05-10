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

    # chage these method below:
    # 请尽可能只动下面的方法：
    # node 是 orgparse 的 node 对象
    # 尽可能使用orgparse库内置的方法完成。
    # 获取node parent的方法是node.get_parent()
    # 输出的列表中的字典格式 {"heading":"TITLEorNone Heading1 Heading2 ...", #单个标题的路径
    #                         "text":"正文", # 去掉时间戳、链接(转化为仅剩链接的文本)、粗斜体、properties、表格(转化为csv格式的表格，并交给CSV Reader类的load_data方法处理，最好给处理后的表格带上heading元数据)等特殊格式，如果去掉所有特殊格式后为空，则删除该字典，带序号的纯文本列表项格式请保留在正文中。
    #                         "tags":["标签1","标签2"], # 可以为None
    #                         "timestamps":str # 时间戳，暂时仅所有时间戳拼接转化为str文本，可以为None
    #                         "links":[link1={"pos":line_num,"title":"title","dest","dest file or id or linenum or other","type":"file"},link2:dict,link3:dict] #所有链接。
    #                         "priority": "A" # 优先级，可以为None
    #                         "todo" : "TODO" # Todo标签,可以为None
    #                         "properties:":{} # 遍历所有properties，并封装成字典，可以为None
    #                         "footnotes":[] # 所有注脚的字典。
    #                         ""}
    # 用于测试的范例 org文件 保存在 test_file.org
    def _org_to_dict(self,root) -> List[Dict]:
        headings = [{}]
        for node in root:
            pass
        return headings
    
    def _format_timstmps():
        pass
    def _format_links():
        pass

    def _list_to_doc() -> Document:
        pass
