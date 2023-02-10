# Digitala Stadsmuseet Python API
#
# This is a Python API for the Digitala Stadsmuseet (Stockholm's Digital City Museum)
# It is based on the FotoWare API, which is documented at https://api.fotoware.com/docs/
#
# The API is written in Python 3.10
# It uses the following libraries:
# - requests
# - json
# - os
# - glob
#
# The following functions are available:
# - get_collections() - returns a list of all collections in the museum
# - get_archive_by_id(id) - returns an archive object with all the assets in the archive
# - get_asset_by_id(id) - returns an asset object with all the metadata for the asset
# - get_assets_by_keyword(keyword) - returns a list of asset objects with all the metadata for the asset
# - get_assets_by_city(city) - returns a list of asset objects with all the metadata for the asset
# - get_assets_by_location(location) - returns a list of asset objects with all the metadata for the asset
# - get_assets_by_country(country) - returns a list of asset objects with all the metadata for the asset
# - get_asset_by_uid(uid) - returns an asset object with all the metadata for the asset
#
# Copyright: Devbrones 2023 under GNU General Public License v3.0

import requests
import json
import os
import glob

class ssdsm:
    class asset:
        name:str = ""
        ftype:str = ""
        px_res:tuple = (0,0)
        cm_res:tuple = (0,0)
        cspace:str = ""
        href:str = ""
        upphov:str = ""
        ty_start:int = ""
        ty_end:int = ""
        cclicense:str = ""
        keywords:str = ""
        person:str = ""
        stad:str = ""
        ort:str = ""
        land:str = ""
        projektnamn:str = ""
        uid:str = ""
        fulltext:str = ""
        shorttext:str = ""
        def __init__(self, name, ftype, px_res, cm_res, cspace, href, upphov, ty_start, ty_end, cclicense, keywords, person, stad, ort, land, projektnamn, uid, fulltext, shorttext):
            self.name = name
            self.ftype = ftype
            self.px_res = px_res
            self.cm_res = cm_res
            self.cspace = cspace
            self.href = href
            self.upphov = upphov
            self.ty_start = ty_start
            self.ty_end = ty_end
            self.cclicense = cclicense
            self.keywords = keywords
            self.person = person
            self.stad = stad
            self.ort = ort
            self.land = land
            self.projektnamn = projektnamn
            self.uid = uid
            self.fulltext = fulltext
            self.shorttext = shorttext
        
    class archive:
        name:str = ""
        uid:str = ""
        editor:str = ""
        assets = []
        def __init__(self, name, uid, editor):
            self.name = name
            self.uid = uid
            self.editor = editor
            self.assets = [] # will be a list of asset objects, so we can access them by index
    rootpoint = "https://digitalastadsmuseet.stockholm.se"
    entrypoint = "https://digitalastadsmuseet.stockholm.se/fotoweb/archives/"
    cache_resolution = 1 # 200 800 2048 px
    headers = { "Accept": "application/json" }
    collections = []
    # Get the list of all collections and returns a json object 
    def get_collections(self):
        collections = requests.get(self.entrypoint, headers=self.headers).json()
        for collection in collections["data"]:
            self.collections.append({"name": collection["name"], "id": (collection["data"].split("/"))[3], "editor": collection["metadataEditor"]["href"]})
        return collections

    def get_archive_by_id(self, id):
        # create the archive object
        #archive = self.archive(archive["name"], archive["uid"], archive["metadataEditor"]["href"])
        # iterate through all pages in the archive and cache them for further use. do this until we get response:
        # {
        #   "value": "FolderNotFound",
        #   "heading": "Mapp hittades inte",
        #   "description": "",
        #   "technicalInfo": "",
        #   "requestId": "xxxxxxxxxxxxxxxxxxxxxxxxx"
        #}
        # which means we have reached the end of the archive
        # set the page count to the last page we have cached by getting the highest number in the _ign folder
        # if the folder is empty, set it to 0
        if os.path.exists("_ign"):
            if len(os.listdir("_ign")) > 0:
                page = max([int(x.split(".")[0]) for x in [x.split("_")[-1] for x in glob.glob("_ign/*.json")]])
            else:
                page = 0
        #while True or page <= 50:
        #    page += 1
        #    archive = requests.get(self.entrypoint + id + "/;p="+ str(page), headers=self.headers).json()
        #    try:
        #        if archive["value"] == "FolderNotFound":
        #            break
        #    except:
        #        pass
        #    # we have a valid page, so we can cache it to a file in _ign
        #    with open("_ign/" + id + "_" + str(page) + ".json", "w") as f:
        #        json.dump(archive, f, indent=4)
        
        # now we have all the pages cached, so we can iterate through them and create the asset objects
        # we also need to get the metadata for each asset, so we can create the asset objects
        # we can get the metadata by iterating through the assets in the archive and getting the metadata for each asset
    
        # get the list of all files in the _ign folder
        files = glob.glob("_ign/*.json")
        # iterate through the files
        for file in files:
            print(file)
            # open the file and get the json object
            with open(file, "r") as f:
                archive = json.load(f)
            # iterate through the assets in the archive
            for asset in archive["data"]:
                # get the metadata for the asset from the json
                metadata = {
                    "attributes": {
                        "name": asset["filename"],
                        "fileType": asset["doctype"],
                        "pixelWidth": asset["attributes"]["imageattributes"]["pixelwidth"],
                        "pixelHeight": asset["attributes"]["imageattributes"]["pixelheight"],
                        "cmWidth": "NA",
                        "cmHeight": "NA",
                        "colorSpace": asset["attributes"]["imageattributes"]["colorspace"],
                        "href": asset["quickRenditions"][self.cache_resolution]["href"],
                        "photographer": asset["metadata"]["80"]["value"],
                        "yearStart": asset["metadata"]["539"]["value"],
                        "yearEnd": asset["metadata"]["533"]["value"],
                        "ccLicense": asset["metadata"]["590"]["value"],
                        "keywords": "", #asset["metadata"]["25"]["value"],
                        "person": "NA",
                        "city": "",
                        "place": "",
                        "country": "",
                        "projectName": "NA",
                        "uid": asset["metadata"]["187"]["value"],
                        "fullText": asset["metadata"]["120"]["value"],
                        "shortText": asset["metadata"]["5"]["value"]
                    }
                }
                # create the asset object
                asset = self.asset(
                    metadata["attributes"]["name"],
                    metadata["attributes"]["fileType"],
                    (metadata["attributes"]["pixelWidth"], metadata["attributes"]["pixelHeight"]),
                    (metadata["attributes"]["cmWidth"], metadata["attributes"]["cmHeight"]),
                    metadata["attributes"]["colorSpace"],
                    metadata["attributes"]["href"],
                    metadata["attributes"]["photographer"],
                    metadata["attributes"]["yearStart"],
                    metadata["attributes"]["yearEnd"],
                    metadata["attributes"]["ccLicense"],
                    metadata["attributes"]["keywords"],
                    metadata["attributes"]["person"],
                    metadata["attributes"]["city"],
                    metadata["attributes"]["place"],
                    metadata["attributes"]["country"],
                    metadata["attributes"]["projectName"],
                    metadata["attributes"]["uid"],
                    metadata["attributes"]["fullText"],
                    metadata["attributes"]["shortText"]
                )
                # add the asset to the archive
                self.archive.assets.append(asset)
        return self.archive
    def get_asset_by_id(self, id):
        # get the metadata for the asset from the json
        metadata = {
            "attributes": {
                "name": asset["filename"],
                "fileType": asset["doctype"],
                "pixelWidth": asset["attributes"]["imageattributes"]["pixelwidth"],
                "pixelHeight": asset["attributes"]["imageattributes"]["pixelheight"],
                "cmWidth": "NA",
                "cmHeight": "NA",
                "colorSpace": asset["attributes"]["imageattributes"]["colorspace"],
                "href": asset["quickRenditions"][self.cache_resolution]["href"],
                "photographer": asset["metadata"]["80"]["value"],
                "yearStart": asset["metadata"]["539"]["value"],
                "yearEnd": asset["metadata"]["533"]["value"],
                "ccLicense": asset["metadata"]["590"]["value"],
                "keywords": "", #asset["metadata"]["25"]["value"],
                "person": "NA",
                "city": "",
                "place": "",
                "country": "",
                "projectName": "NA",
                "uid": asset["metadata"]["187"]["value"],
                "fullText": asset["metadata"]["120"]["value"],
                "shortText": asset["metadata"]["5"]["value"]
            }
        }
        # create the asset object
        asset = self.asset(
            metadata["attributes"]["name"],
            metadata["attributes"]["fileType"],
            (metadata["attributes"]["pixelWidth"], metadata["attributes"]["pixelHeight"]),
            (metadata["attributes"]["cmWidth"], metadata["attributes"]["cmHeight"]),
            metadata["attributes"]["colorSpace"],
            metadata["attributes"]["href"],
            metadata["attributes"]["photographer"],
            metadata["attributes"]["yearStart"],
            metadata["attributes"]["yearEnd"],
            metadata["attributes"]["ccLicense"],
            metadata["attributes"]["keywords"],
            metadata["attributes"]["person"],
            metadata["attributes"]["city"],
            metadata["attributes"]["place"],
            metadata["attributes"]["country"],
            metadata["attributes"]["projectName"],
            metadata["attributes"]["uid"],
            metadata["attributes"]["fullText"],
            metadata["attributes"]["shortText"]
        )
        return asset
        
    
