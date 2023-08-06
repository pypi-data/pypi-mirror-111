import requests

def upload_file(ufile):
    """This function uploads the given
    file to anonfiles."""
    
    with open(ufile, mode='rb') as file_handler:
        r = requests.post('https://api.anonfiles.com/upload', files={'file': file_handler})
    
    return r.json()['data']['file']['url']['full']

def uploaded_file_info(fileid):
    """This function gives information 
    about the file on anonefiles."""
    r = requests.get(f'https://api.anonfiles.com/v2/file/{fileid}/info')
    data = r.json()['data']['file']['metadata']
    try:
        fid = data['id']
    except:
        fid = None
    try:
        fname = data['name']
    except:
        fname = None
    try:
        fbsize = data['size']['bytes']
    except:
        fbsize = None
    try:
        frsize = data['size']['readable']
    except:
        frsize = None
    return f'''File ID: {fid}\nFile Name: {fname}\nFile Size (in bytes): {fbsize}\nFile Size (readable): {frsize}'''

