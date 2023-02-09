import requests
import json
import os
import re


class ssdsm:
    entrypoint = "https://digitalastadsmuseet.stockholm.se/fotoweb/archives/"
    headers = { "Accept": "application/json" }
    collections = []
    # Get the list of all collections and returns a json object 
    def get_collections(self):
        collections = requests.get(self.entrypoint, headers=self.headers).json()
        for collection in collections["data"]:
            self.collections.append({"name": collection["name"], "id": (collection["data"].split("/"))[3], "editor": collection["metadataEditor"]["href"]})
        return collections

    def get_archive_by_id(self, id, page):
        archive = requests.get(self.entrypoint + id + "/;p="+ str(page), headers=self.headers).json()
        ## pretty print json to a file with the collection name
        with open("_ign/" + self.collections[0]["name"] +"_page" + str(page) +  ".json", "w") as outfile:
            json.dump(archive, outfile, indent=4)
        return archive

    def get_asset_titles(self, id):
        titles = []
        ## get the titles of all assets in the collection
        archive = self.get_archive_by_id(id)
        for asset in archive["assets"]["data"]:
            titles.append(asset["href"])
        return titles

    def get_asset_metadata(self, uid, asset):
        metadata = {self.get_archive_by_id(uid)["assets"]["data"][asset]["metadata"]["attributes"],self.get_archive_by_id(uid)["assets"]["data"][asset]["metadata"]}
        return metadata



ssdsm = ssdsm()
ssdsm.get_collections()
for collection in ssdsm.collections:
    print(collection["id"])
asset_index=0

test_collection = ssdsm.get_archive_by_id(ssdsm.collections[asset_index]["id"])
# pretty print json to a file with the collection name
with open(ssdsm.collections[0]["name"] + ".json", "w") as outfile:
    json.dump(test_collection, outfile, indent=4)

print("\n\n")


# get the titles of all assets in the collection
titles = ssdsm.get_asset_titles(ssdsm.collections[asset_index]["id"])
print(titles)

##


## assets N metadata 120 = best prompt
