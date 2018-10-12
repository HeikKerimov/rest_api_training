import os
import jsonpickle


def get_file(folder=None, name=None):
    if folder is None:
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "{0}.json".format(name))
    else:
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "{0}/{1}.json".format(folder, name))
    return file


def write_in_json(folder=None, file=None, data=None):
    json_file = get_file(folder=folder, name=file)
    with open(json_file, "w") as f:
        jsonpickle.set_encoder_options("json", indent=3)
        f.write(jsonpickle.encode(data))


def load_from_json(folder=None, file=None):
    json_file = get_file(folder=folder, name=file)
    with open(json_file) as f:
        return jsonpickle.decode(f.read())

