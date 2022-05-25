import pymongo.errors
from pymongo import MongoClient
import discord

def get_database():
    CONNECTION_STRING = "mongodb+srv://admin:OCZE6kCJnLcPRLfx@yg-discord-bot.qaje7.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['yg_members']

def insert_new_user(member: discord.Member):
    userInformation = {
        "_id": member.id,
        "user_name": member.name,
        "timesJoined": 1,
        "timesKicked": 0,
        "timesBanned": 0,
        "userNotes": {},
        "banking": {
            "leaderBoard": 0,
            "money": 0,
            "xp": 0,
            "daily": 0,
        }
    }
    collection_name = get_database()[str(member.id)]
    try:
        collection_name.insert_one(userInformation)
    except pymongo.errors.WriteError as e:
        print(e)
    except pymongo.errors.WriteConcernError as e:
        print(e)
    return collection_name.insert_one(userInformation).inserted_id == member.id

# def addNoteToUser(member: discord.Member, note):
#     userNotes = get_database()[str(member.id)].find_one()['userNotes']
#     print("UserNotes", userNotes)
#     userNotes[len(userNotes)] = note
#     print("New Notes", userNotes)
#     get_database()[str(member.id)].update_one(userNotes)

def getExistingUserData(member: discord.Member):
    return get_database()[str(member.id)].find_one()

def queryExistingUser(member: discord.Member):
    if str(member.id) in get_database().list_collection_names():
        return True
    return False
