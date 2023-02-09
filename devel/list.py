import re
import os
import glob

# set the page count to the last page we have cached by getting the highest number in the _ign folder
# if the folder is empty, set it to 0 using glob
#if len(glob.glob("_ign/*.json")) > 0:
#    page  = re.findall(r'\d+', glob.glob("_ign/*.json"))



alf = glob.glob("_ign/*.json")
# remove everything before the last underscore
alf = [x.split("_")[-1] for x in alf]
# remove the .json extension
alf = [x.split(".")[0] for x in alf]
# convert the list of strings to a list of ints
alf = [int(x) for x in alf]
# get the highest number
page = max(alf)

# make the abve one line
page = max([int(x.split(".")[0]) for x in [x.split("_")[-1] for x in glob.glob("_ign/*.json")]])


print(page)