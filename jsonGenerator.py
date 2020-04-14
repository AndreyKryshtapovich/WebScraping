import collections
import json


def jsonGenerator():
    region = 'TheCity'
    date = '2020-04-11'
    raw_data = {
        'Ruby': 5,
        "Java": 72,
        "NoSQL": 13,
        "Scala": 12,
        'ZooKeeper': 2,
        'Excel': 7,
        'Hadoop': 6,
        'D3.js': 1,
        'Python': 35,
        'Spark': 7,
        'Swift': 7,
        'C++': 22,
        'Tableau': 2,
        'R': 12,
        'Hive': 5,
        'Perl': 3,
        'Shark': 1,
        'MongoDB': 6,
        'Pig': 1,
        'SQL': 53,
        'D3': 82,
        'Cassandra': 9
    }
    base_file_name = 'jobs_frame_'
    directory = 'd:\\Magister\\WebScraping\\data\\'
    num_of_vacancies = 210
    json_content = collections.OrderedDict({
        "schema": {
            "fields": [
                {
                    "type": "integer",
                    "name": "index"
                },
                {
                    "type": "string",
                    "name": "Term"
                },
                {
                    "type": "integer",
                    "name": "NumPostings"
                },
                {
                    "type": "integer",
                    "name": "NumOfVacancies"
                },
                {
                    "type": "string",
                    "name": "Region"
                },
                {
                    "type": "string",
                    "name": "Date"
                }
            ],
            "pandas_version": "0.20.0",
            "primaryKey": [
                "index"
            ]
        }
    }
    )

    index = 0
    data = []
    for term in raw_data.keys():
        term_dict = collections.OrderedDict()
        term_dict['index'] = index
        index += 1
        term_dict['Term'] = term
        term_dict['NumPostings'] = raw_data[term]
        term_dict['NumOfVacancies'] = num_of_vacancies
        term_dict['Region'] = region
        term_dict['Date'] = date
        data.append(term_dict)

    json_content.update({
        'data': data
    })

    filePathNameWExt = directory + base_file_name + date + '_' + region + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(json_content, fp)
