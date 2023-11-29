import argparse
import copy
import io
import json
import os
import shutil
from datetime import datetime
from time import sleep




# Create wrapper classes for using slack_sdk in place of slacker
class SlackDataLoader:
    '''
    Slack exported data IO class.

    When you open slack exported ZIP file, each channel or direct message 
    will have its own folder. Each folder will contain messages from the 
    conversation, organised by date in separate JSON files.

    You'll see reference files for different kinds of conversations: 
    users.json files for all types of users that exist in the slack workspace
    channels.json files for public channels, 
    
    These files contain metadata about the conversations, including their names and IDs.

    For secruity reason, we have annonymized names - the names you will see are generated using faker library.
    
    '''
    def __init__(self, path):
        '''
        path: path to the slack exported data folder
        '''
        self.path = path
        self.channels = self.get_channels()
        self.users = self.get_users()
    

    def get_users(self):
        '''
        write a function to get all the users from the json file
        '''
        with open(os.path.join(self.path, 'users.json'), 'r') as f:
            users = json.load(f)

        return users
    
    def get_channels(self):
        '''
        write a function to get all the channels from the json file
        '''
        with open(os.path.join(self.path, 'channels.json'), 'r') as f:
            channels = json.load(f)

        return channels

    def get_channel_messages(self, channel_name):
        '''
        write a function to get all the messages from a channel
        
        '''
      
        '''
        get all the messages from a channel        
        '''
        channel_json_files = os.listdir(channel_name)
        channel_msgs = [json.load(open(channel_name + "/" + f)) for f in channel_json_files]
       
    
        #editted to handle issue array miss match
        df = pd.concat([pd.DataFrame([self.get_messages_dict(msgs)])  for msgs in channel_msgs])
        
        print(f"Number of messages in channel: {len(df)}")
        
        return df

    # 
    def get_user_map(self):
        '''
        write a function to get a map between user id and user name
        '''
        userNamesById = {}
        userIdsByName = {}
        for user in self.users:
            userNamesById[user['id']] = user['name']
            userIdsByName[user['name']] = user['id']
        return userNamesById, userIdsByName  
        
    @staticmethod
    def get_messages_dict(msgs):
        msg_list = {
                "msg_id":[],
                "text":[],
                "attachments":[],
                "user":[],
                "mentions":[],
                "emojis":[],
                "reactions":[],
                "replies":[],
                "replies_to":[],
                "ts":[],
                "links":[],
                "link_count":[]
                }
        for msg in msgs:
            
            if "subtype" not in msg:
                try:
                    msg_list["msg_id"].append(msg["client_msg_id"])
                except:
                    msg_list["msg_id"].append(None)
                
                msg_list["text"].append(msg["text"])
                msg_list["user"].append(msg["user"])
                msg_list["ts"].append(msg["ts"])
              
                if "reactions" in msg:
                    msg_list["reactions"].append(msg["reactions"])
                else:
                    msg_list["reactions"].append(None)
    
                if "parent_user_id" in msg:
                    msg_list["replies_to"].append(msg["ts"])
                else:
                    msg_list["replies_to"].append(None)
    
                if "thread_ts" in msg and "reply_users" in msg:
                    msg_list["replies"].append(msg["replies"])
                else:
                    msg_list["replies"].append(None)
                
                if "blocks" in msg:
                    emoji_list = []
                    mention_list = []
                    link_count = 0
                    links = []
                    
                    for blk in msg["blocks"]:
                        if "elements" in blk:
                            for elm in blk["elements"]:
                                if "elements" in elm:
                                    for elm_ in elm["elements"]:
                                        
                                        if "type" in elm_:
                                            if elm_["type"] == "emoji":
                                                emoji_list.append(elm_["name"])
    
                                            if elm_["type"] == "user":
                                                mention_list.append(elm_["user_id"])
                                            
                                            if elm_["type"] == "link":
                                                link_count += 1
                                                links.append(elm_["url"])
    
    
                    msg_list["emojis"].append(emoji_list)
                    msg_list["mentions"].append(mention_list)
                    msg_list["links"].append(links)
                    msg_list["link_count"].append(link_count)
                else:
                    msg_list["emojis"].append(None)
                    msg_list["mentions"].append(None)
                    msg_list["links"].append(None)
                    msg_list["link_count"].append(0)
                    
        return msg_list




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Export Slack history')

    
    parser.add_argument('--zip', help="Name of a zip file to import")
    args = parser.parse_args()

