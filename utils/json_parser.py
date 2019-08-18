import json


def parse_json_file(filepath):
    with open(filepath, 'r') as f:
        json_data = f.read()
    return json.loads(json_data)


def dump_json_to_file(data_type, json_data, destination_file, exist=False):
    # get blessings or spelling
    if data_type == 'bless' or data_type == 'spell':
        data = json.dumps(json_data, indent=4)
    # get emoji
    if data_type == 'emoji':
        emoji_dict = {}
        for emoji in json_data:
            emoji_dict[emoji.name] = str(emoji)
        data = json.dumps(emoji_dict, indent=4)
    # get user
    if data_type == 'user':
        if exist:
            data = json.dumps(json_data, indent=4)
        else:
            old_users = parse_json_file('data/server_data/users.json')
            for user in json_data:
                # if user already in data and didn't change his name
                if str(user.id) in old_users\
                and old_users[user.id]["name"] == user.name:
                    continue
                # if the user still in data but change their name
                elif str(user.id) in old_users:
                    old_users[user.id]["name"] = user.name
                else: # if this is a new user
                    user_dict = {}
                    user_dict['name'] = user.name
                    user_dict['bot'] = user.bot
                    user_dict['coins'] = 0
                    user_dict['property'] = {}
                    user_dict['property']['slaps'] = 0
                    old_users[user.id] = user_dict
            data = json.dumps(old_users, indent=4)
    # write data to destination file
    with open(destination_file, 'w+') as f:
        f.write(data)
