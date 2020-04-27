import requests
import xml.etree.ElementTree as ET

class Film:
    def __init__(self, id, title):
        self.id = id
        self.title = title

class FilmInfo:
    def __init__(self, hash, size):
        self.hash = hash
        self.size = size

def createParam(_value):
    param = ET.Element('param')
    value = ET.SubElement(param, 'value')
    ET.SubElement(value, 'string').text = _value
    return param

def createLoginRequest():
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName').text = 'LogIn'
    params = ET.SubElement(root, 'params')
    params.append(createParam('hirtus'))
    params.append(createParam('gfhjkm'))
    params.append(createParam('en'))
    params.append(createParam('SolEol 0.0.8'))
    return ET.tostring(root)

def createSearchMovieRequest(token, query):
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName').text = 'SearchMoviesOnIMDB'
    params = ET.SubElement(root, 'params')
    params.append(createParam(token))
    params.append(createParam(query))
    return ET.tostring(root)

def createMovieDetailsInfo(token, id):
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName').text = 'GetIMDBMovieDetails'
    params = ET.SubElement(root, 'params')
    params.append(createParam(token))
    params.append(createParam(id))
    return ET.tostring(root)

def createSearchSubtitlesRequest(token, filmInfo):
    root = ET.Element('methodCall')
    ET.SubElement(root, 'methodName').text = 'SearchSubtitles'
    params = ET.SubElement(root, 'params')
    params.append(createParam(token))
    param = ET.SubElement(params, 'param')
    value = ET.SubElement(param, 'value')
    array = ET.SubElement(value, 'array')
    data = ET.SubElement(array, 'data')
    _value = ET.SubElement(data, 'value')

    params.append(createParam(filmInfo.hash))
    return ET.tostring(root)

def getMember(xml, name):
    token = xml.find(f".//member/[name='{name}']/value/string").text
    return token


def send(data):
    url = 'http://api.opensubtitles.org/xml-rpc'
    print(data)
    print("Sending...")
    result = requests.post(url, data)
    if result.status_code == 200:
        return result.text
    else:
        print(f"Login failed: {result.reason}")
        exit(1)

def login(username, password):
    data = createLoginRequest()
    response = ET.fromstring(send(data))
    token = getMember(response, 'token')
    return token

def searchMovie(token, searchString):
    data = createSearchMovieRequest(token, searchString)
    response = send(data)
    films = list()
    xml = ET.fromstring(response).findall(".//array/data/value/")
    for element in xml:
        id = getMember(element, "id")
        title = getMember(element, "title")
        films.append(Film(id, title))
    return films

def getMovieDetails(token, id):
    data = createMovieDetailsInfo(token, id)
    response = send(data)
    xml = ET.fromstring(response)
    hash = xml.find("")




token = loginJSON('hirtus', 'gfhjkm')
print(token)
films = searchMovie(token, "dirk gently")
for film in films:
    print(f"{film.id}: {film.title}")
