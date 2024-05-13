from http.client import IncompleteRead
import urllib.request, json
import sys
import os

COUNTRY = 'Canada'
birds = ['Mourning Dove',
         'Black-capped Chickadee',
         'White-breasted Nuthatch',
         'American Robin',
         'Northern Cardinal'
         ]


current_directory = os.getcwd()
#store all audio files in birds directory
os.makedirs(os.path.join(current_directory,"birds_audio"))

def save_json(searchTerms, birdName):
    numPages = 1
    page = 1
    # create a path to save json files and recordings
    path = os.path.join(current_directory,"birds_audio",birdName.replace(':', ''))
    if not os.path.exists(path):
        print("Creating subdirectory " + path + " for downloaded files...")
        os.makedirs(path)
        # download a json file for every page found in a query
    while page < numPages + 1:
        print("Loading page " + str(page) + "...")
        url = 'https://www.xeno-canto.org/api/2/recordings?query={0}&page={1}'.format(searchTerms.replace(' ', '%20'),
                                                                                      page)
        print(url)
        jsonPage = urllib.request.urlopen(url)
        jsondata = json.loads(jsonPage.read().decode('utf-8'))
        filename = path + "/jsondata_p" + str(page) + ".json"
        with open(filename, 'w') as outfile:
            json.dump(jsondata, outfile)
        # check number of pages
        numPages = jsondata['numPages']
        page = page + 1
    print("Found ", numPages, " pages in total.")
    # return number of files in json
    # each page contains 500 results, the last page can have less than 500 records
    print("Saved json for ", (numPages - 1) * 500 + len(jsondata['recordings']), " files")
    return path


# reads the json and return the list of values for selected json part
# i.e. "id" - ID number, "type": type of the bird sound such as call or song
# for all Xeno Canto files found with the given search terms.
def read_data(searchTerm, path):
    data = []
    numPages = 1
    page = 1
    # read all pages and save results in a list
    while page < numPages + 1:
        # read file
        with open(path + "/jsondata_p" + str(page) + ".json", 'r') as jsonfile:
            try:
                jsondata = jsonfile.read()
            except IncompleteRead:
                continue
        jsondata = json.loads(jsondata)
        # check number of pages
        numPages = jsondata['numPages']
        # find "recordings" in a json and save a list with a search term
        for k in range(len(jsondata['recordings'])):
            data.append(jsondata["recordings"][k][searchTerm])
        page = page + 1
    return data


# downloads all sound files found with the search terms into xeno-canto directory
# into catalogue named after the search term (i.e. Apus apus)
# filename have two parts: the name of the bird in latin and ID number
def download_mp3(searchTerms, birdName):
    # create data/xeno-canto-dataset directory
    path = save_json(searchTerms, birdName)
    # get filenames: recording ID and bird name in latin from json
    filenamesID = read_data('id', path)
    filenamesCountry = read_data('cnt', path)
    # get website recording http download address from json
    fileaddress = read_data('file', path)
    numfiles = len(filenamesID)
    print("A total of ", numfiles, " files will be downloaded")
    for i in range(0, numfiles):
        print(fileaddress[i])
        try:
            urllib.request.urlretrieve(fileaddress[i],
                                   path + "/" + birdName + filenamesID[i] + ".mp3")
        except:
            continue

for bird in birds:
    download_mp3(f'{bird} type:song', bird.replace(' ', ''))

