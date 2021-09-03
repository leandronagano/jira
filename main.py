import json
import csv
import requests

urlBusca = 'https://jira.bradesco.com.br:8443/rest/api/2/search?jql=filter='
urlFilter = 'https://jira.bradesco.com.br:8443/rest/api/2/filter/'

paramFields = '&fields=key'
paramMax = '&maxResults=1'

headers = {
    'Accept': '*/*',
    'User-Agent': 'request',
}

usuario = 'm232682'
senha = ''

filtroId = []
filtroName = ['Vila','Value Stream','Squad','Referência']

with open('filtros.json') as json_fileFilter:
    dataFiltro = json.load(json_fileFilter)

    for filtro in dataFiltro['filtros']:
        requestFiltro = requests.get(urlFilter + filtro['id'], headers=headers, auth=(usuario, senha))
        jsonfiltro = json.loads(requestFiltro.text)
        filtroName.append(jsonfiltro['name'])
        filtroId.append(jsonfiltro['id'])
    json_fileFilter.close()

with open('censo.json') as json_file:
    data = json.load(json_file)

    with open(r'consolidado.csv', 'w') as f:
        f.truncate()
        writerHeader = csv.writer(f)
        writerHeader.writerow(filtroName)
        for vila in data['vilas']:
            for vs in vila['vs']:
                for squad in vs['squads']:
                    rowlist = [vila['name'],vs['name'],squad['name'],squad['isReferencia']]
                    for busca in dataFiltro['filtros']:
                        if (busca['isTeam']):
                            getCount = requests.get(urlBusca+busca['id']+' and '+squad['filtro']+paramFields+paramMax, headers=headers, auth=(usuario, senha))
                            jsonCount = json.loads(getCount.text)
                            rowlist.append(jsonCount['total'])
                        else:
                            getCount = requests.get(urlBusca+busca['id']+' and project='+vs['project']+paramFields+paramMax, headers=headers, auth=(usuario, senha))
                            jsonCount = json.loads(getCount.text)
                            rowlist.append(jsonCount['total'])                
                    print(rowlist)
                    writer = csv.writer(f)
                    writer.writerow(rowlist)
json_file.close()
