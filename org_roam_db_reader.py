from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import Optional, Dict, List
from pathlib import Path
from org_reader import OrgReader
import orgparse
import sqlite3

class OrgRoamDbReader(BaseReader):
    def load_data(
            self,
            file:Path,
            extra_meta: Optional[Dict] = None,
    ) -> List[Document]:
        """Parse File"""
        if not isinstance(file, Path):
            file = Path(file)
        
        self.db_file = file
        self._init_database()
        self._read_nodes()
        self._read_tags()
        self._read_links()

        documents = []
        nodes = self.get_nodes()
        for node_id in nodes:
            node_doc = self.parse_node(nodes[node_id])
            documents = documents + node_doc
        
        if extra_meta is not None:
            for doc in docments:
                doc.metadata.update(extra_meta)
        return documents

    def parse_node(self,node:dict) -> List[Document]:
        file = node["file"]
        links_to = " ".join(node["links_to"])
        tags = node["tags"]
        reader = OrgReader()
        node_docs = []
        node_documents = reader.load_data(file,{"links_to":links_to})
        for node_doc in node_documents:
            node_doc.doc_id = node["id"]
            tag_data = node_doc.metadata["tags"]
            if tag_data:
                node_doc.metadata["tags"] += " ".join(tags)
            else:
                node_doc.metadata["tags"] = " ".join(tags)
        return node_documents
        

    def _read_nodes(self):
        rows = self.query_table("nodes")
        self.nodes = {}
        for row in rows:
            node = {
                "id":row[0].strip('"'),
                "file":row[1].strip('"'),
                "title":row[8].strip('"'),
                "tags":[],
                "links_to":[]
             }
            self.nodes[node["id"]] = node

    def _read_tags(self):
        rows = self.query_table("tags")
        for row in rows:
            id = row[0].strip('"')
            node = self.nodes[id]
            node["tags"].append(row[1].strip('"'))

    def _read_links(self):
        rows = self.query_table("links")
        for row in rows:
            source_id = row[1].strip('"')
            dest_id = row[2].strip('"')
            node = self.nodes[source_id]
            if dest_id in self.nodes:
                dest_node = self.nodes[dest_id]
                node["links_to"].append(dest_node["title"])

    def   _init_database(self):
        self.conn = sqlite3.connect(self.db_file)

    def query_table(self,table:str):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+table)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_nodes(self):
        return self.nodes
