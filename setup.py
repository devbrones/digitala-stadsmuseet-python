import os

# check if _ign and _imgcache folders exist
if not os.path.exists('_ign'):
    os.makedirs('_ign')
if not os.path.exists('_imgcache'):
    os.makedirs('_imgcache')
    os.makedirs('_imgcache/200')
    os.makedirs('_imgcache/800')
    os.makedirs('_imgcache/2048')



