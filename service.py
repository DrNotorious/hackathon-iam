from itertools import groupby
import random
import uuid

from click import group

MAX_VALUE_MAJOR_MINOR = 65535
class User:

    userName = None
    major = 0
    minor = 0
    friends = set()
    groups = set()

    def __init__(self, userName):
        self.userName = userName
        self.major = random.randint(1, MAX_VALUE_MAJOR_MINOR)
        self.minor = random.randint(1, MAX_VALUE_MAJOR_MINOR)
    
    def getUserName(self):
        return self.userName
    
    def addFriend(self, friendId):
        self.friends.add(friendId)

    def removeFriend(self, friendId):
        if friendId in self.friends:
            self.friends.remove(friendId)

    def getFriends(self):
        return self.friends

    def getGroups(self):
        return self.groups

    def joinGroup(self, groupId):
        self.groups.add(groupId)
    
    def leaveGroup(self, groupId):
        if groupId in self.groups:
            self.groups.remove(groupId)
    
class Group:
    groupName = None
    members = set()

    def __init__(self, name):
        self.groupName = name  
    
    def addMember(self, userId):
        self.members.add(userId)

    def removeMember(self, userId):
        if userId in self.members:
            self.members.remove(userId)

    def getAllMembers(self):
        return list(self.members)


class Service:
    users = []
    groups = {"Volleyball": Group("Volleyball"), "Golf": Group("Golf"), "Tennis": Group("Tennis")}

    def checkUserNameExists(self, userName):
        return len(list(filter(lambda x: x.getUserName() == userName , self.users))) > 0
    
    def getUsers(self):
        return self.users

    def getGroups(self):
        return self.groups.values()

    def loginUser(self, userName):
        if (not self.checkUserNameExists(userName)):
            newUser = User(userName)
            self.users.append(newUser)
        return self.getUser(userName)
    
    def getUser(self, userName):
        filtered =  list(filter(lambda x: x.getUserName() == userName , self.users))
        return filtered[0] if len(filtered) > 0 else None
    
    def getGroup(self, groupName):
        return self.groups.get(groupName)

    def joinGroup(self, userName, groupName):
        user = self.getUser(userName)
        group = self.getGroup(groupName)

        if (group is not None):
            user.joinGroup(groupName)
            group.addMember(userName)
    
    def leaveGroup(self, userName, groupName):
        user = self.getUser(userName)
        group = self.getGroup(groupName)

        user.leaveGroup(groupName)
        group.removeMember(userName)

    def addFriend(self, userId, friendId):
        user = self.getUser(userId)
        user.addFriend(friendId)

    def shouldNotify(self, senderObj, receiverName):
        senderMajor = senderObj['major']
        senderMinor = senderObj['minor']
        sender = self.getUserFromMajorAndMinor(senderMajor, senderMinor)
        receiver = self.getUser(receiverName)

        response = {"sender": sender.__dict__, "notify": False}
        if (len(sender.groups.intersection(receiver.groups)) > 0):
            if (receiverName not in sender.getFriends()):
                response["notify"] = True
        
        return response

    def getFriends(self, userName):
        user = self.getUser(userName)
        return list(user.getFriends())

    def addFriend(self, userName, friendName):
        user = self.getUser(userName)
        user.addFriend(friendName)
        return list(user.getFriends())

    def removeFriend(self, userName, friendName):
        user = self.getUser(userName)
        user.removeFriend(friendName)

        return list(user.getFriends())

    def getUserFromMajorAndMinor(self, major, minor):
        filtered =  list(filter(lambda x: (x.major == major and x.minor == minor) , self.users))

        return filtered[0] if len(filtered) > 0 else None

    def getUserGroups(self,userName):
        user = self.getUser(userName)
        groupNames = user.getGroups()
        
        return [self.getGroup(gn) for gn in groupNames]
