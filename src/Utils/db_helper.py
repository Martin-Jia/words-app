import pymongo
import os
from Utils.constants import Constants, ErrorCode, ErrorMessage
import logging
logger = logging.getLogger("restfulapi")

class DatabaseConnector:
    def __init__(self):
        db_connection_string = os.environ['DB_CONNECTION_STRING']
        db_client = pymongo.MongoClient(db_connection_string)
        self.database = db_client["wordapp"]

    def query_user_with_username(self, username):
        col = self.database.get_collection('User')
        if not col:
            logger.error(f'{username}: miss User table in database')
            return 'miss User table in database', None
        return None, col.find_one({'username': username})

    def update_user_token(self, username, token, expire_time):
        col = self.database.get_collection('Token')
        return None, col.update({'username': username}, {'token': token, 'expire_time': expire_time}, upsert=True)

    def query_user_token(self, username):
        col = self.database.get_collection('Token')
        if not col:
            logger.error(f'{username}: miss Token table in database')
            return 'miss Token table in database', None
        return None, col.find_one({'username': username})
        
    def clear_user_token(self, username):
        col = self.database.get_collection('Token')
        if not col:
            logger.error(f'{username}: miss Token table in database')
            return 'miss Token table in database', None
        return None, col.delete_one({'username': username})