import json


def parse_json_file(filepath):
    with open(filepath, 'r') as f:
        json_data = f.read()
    return json.loads(json_data)


def dump_json_to_file(data_type, json_data, destination_file):
    if data_type == 'emoji':
        emoji_dict = {}
        for emoji in json_data:
            emoji_dict[emoji.name] = str(emoji)
        data = json.dumps(emoji_dict, indent=4)
        with open(destination_file, 'w+') as f:
            f.write(data)
