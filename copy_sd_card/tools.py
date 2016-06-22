import hashlib

def get_file_hash(path):
    hasher = hashlib.md5()
    with open(path, "rb") as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()
