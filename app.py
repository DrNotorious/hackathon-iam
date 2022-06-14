from flask import Flask, json, request
from service import Service, User

app = Flask(__name__)
service = Service()

def obj_dict(obj):
    return obj.__dict__

@app.route('/api/v1/users/all', methods=['GET'])
def getUsers():
    return json.dumps([obj_dict(user) for user in service.getUsers()])

@app.route('/api/v1/groups', methods=['GET'])
def getAllGroups():
    return json.dumps([obj_dict(group) for group in service.getGroups()])

@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()
    userName = data['userName']

    return json.dumps(service.loginUser(userName),default=obj_dict)

@app.route('/api/v1/users', methods=['POST'])
def getMultipleUsers():
    data = request.get_json()
    users = []
    for user in data:
        major = int(user['major'])
        minor = int(user['minor'])

        u = service.getUserFromMajorAndMinor(major,minor)
        if(u): users.append(u)
        
    return json.dumps([obj_dict(user) for user in users])

@app.route('/api/v1/user/groups' , methods=['GET'])
def getUserGroups():
    data = request.get_json()
    userName = data['userName']
    return json.dumps([obj_dict(group) for group in service.getUserGroups(userName)])


@app.route('/api/v1/group/join' , methods=['POST'])
def joinGroup():
    data = request.get_json()
    userName = data['userName']
    groupName = data['groupName']
    service.joinGroup(userName, groupName)
    return json.dumps([obj_dict(group) for group in service.getUserGroups(userName)])

@app.route('/api/v1/notify', methods=['POST'])
def shouldNotify():
    data = request.get_json()
    sender = data['sender']
    receiver = data['receiver']
    
    return json.dumps(service.shouldNotify(sender, receiver))

@app.route('/api/v1/friends', methods=['GET'])
def getUserFriends():
    data = request.get_json()
    userName = data['userName']

    return json.dumps(service.getFriends(userName))

@app.route('/api/v1/addFriend', methods=['POST'])
def addFriend():
    data = request.get_json()
    userName = data['userName']
    friendName = data['friendName']

    return json.dumps(service.addFriend(userName, friendName))

@app.route('/api/v1/removeFriend', methods=['POST'])
def removeFriend():
    data = request.get_json()
    userName = data['userName']
    friendName = data['friendName']

    return json.dumps(service.removeFriend(userName, friendName))

if __name__ == '__main__':
    app.run(debug=False)
    