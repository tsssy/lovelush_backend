# database.py
import logging
from bson import ObjectId
from pymongo import MongoClient

# 配置日志
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def convert_objectid_to_str(data):
    """将字典中的所有ObjectID转换为字符串"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid_to_str(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        convert_objectid_to_str(item)
    return data

class Database:
    client: MongoClient = None
    db = None
    MONGO_URI = "mongodb://localhost:27017/"
    MONGO_DB_NAME = "lovelush_db"

    @classmethod
    def connect(cls):
        """连接到 MongoDB"""
        try:
            cls.client = MongoClient(cls.MONGO_URI, serverSelectionTimeoutMS=5000)
            cls.client.server_info()  # 测试连接
            cls.db = cls.client[cls.MONGO_DB_NAME]
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    def close(cls):
        """关闭 MongoDB 连接"""
        if cls.client:
            cls.client.close()
            logger.info("Closed MongoDB connection")

    @classmethod
    def get_db(cls):
        """获取数据库实例"""
        if cls.db is None:
            raise Exception("Database not connected. Call connect() first.")
        return cls.db

    @classmethod
    def get_collection(cls, collection_name: str):
        """获取集合实例"""
        return cls.get_db()[collection_name]

    @classmethod
    def insert_one(cls, collection_name: str, document: dict):
        """插入单个文档"""
        try:
            result = cls.get_collection(collection_name).insert_one(document)
            logger.info(f"Inserted document with id: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error inserting document: {e}")
            raise

    @classmethod
    def find_one(cls, collection_name: str, query: dict):
        """查找单个文档"""
        try:
            result = cls.get_collection(collection_name).find_one(query)
            return convert_objectid_to_str(result) if result else None
        except Exception as e:
            logger.error(f"Error finding document: {e}")
            raise

    @classmethod
    def update_one(cls, collection_name: str, query: dict, update: dict):
        """更新单个文档"""
        try:
            result = cls.get_collection(collection_name).update_one(query, update)
            logger.info(f"Modified {result.modified_count} document")
            return result.modified_count
        except Exception as e:
            logger.error(f"Error updating document: {e}")
            raise

    @classmethod
    def delete_one(cls, collection_name: str, query: dict):
        """删除单个文档"""
        try:
            result = cls.get_collection(collection_name).delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            raise 