import datetime

import re
import urllib2
from collections import Counter
from time import sleep

import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup

from textCleaner import text_cleaner


def tutBySkillsInfo(region_code=None, job=""):
    # final_job = 'data+scientist'
    # final_job = 'java+developer'
    # final_job = 'software+engineer'
    final_job = str(job.replace(" ", "+"))
    region = str(int(region_code))
    if region_code is not None and region.isdigit():
        final_site_list = ['https://jobs.tut.by/search/vacancy?text=', final_job, '&area=', region]
    else:
        final_site_list = ['https://jobs.tut.by/search/vacancy?text=', final_job]

    final_site = ''.join(final_site_list)

    base_url = 'https://jobs.tut.by'

    request = urllib2.Request(final_site, headers={"Accept": "text/html",
                                                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"})

    try:
        html = urllib2.urlopen(request).read()
    except:
        'Could not acces jobs.tut.by. Exiting . . .'
        return
    soup = BeautifulSoup(html, "html.parser")

    num_jobs_area = soup.find("h1", attrs={"class": "bloko-header-1"}).get_text().encode(
        'utf-8')

    job_numbers = re.findall('\d+', num_jobs_area)

    if len(job_numbers) >= 2:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[0]) * 1000) + int(job_numbers[1])
    else:
        total_num_jobs = int(job_numbers[0])

    # print 'There were', total_num_jobs, 'jobs found,'

    num_pages = total_num_jobs / 10
    job_descriptions = []

    for page_number in xrange(num_pages):
        print 'Getting page', page_number + 1
        current_page = ''.join([final_site, '&page=', str(page_number), '&items_on_page=10'])
        page_request = urllib2.Request(current_page, headers={"Accept": "text/html",
                                                              "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"})
        html_page = urllib2.urlopen(page_request).read()
        page_obj = BeautifulSoup(html_page, "html.parser")
        job_link_area = page_obj.find("div", {
            "class": "vacancy-serp"})

        base_vacancy_url = base_url + "/vacancy/"

        job_URLS = [base_vacancy_url + str(link.get("href")).split("vacancy/")[-1].split("?")[0] for link in
                    job_link_area.select('span.g-user-content > a')]
        #'div.search-item-name > a'

        for j in xrange(0, len(job_URLS)):
            final_description = text_cleaner(job_URLS[j])
            if final_description:
                job_descriptions.append(final_description)
            sleep(1)

    print 'Done with collecting the job postings!'
    # print 'There were', len(job_descriptions), 'jobs successfully found.'

    doc_frequency = Counter()
    [doc_frequency.update(item) for item in job_descriptions]

    prog_lang_dict = Counter({'R': doc_frequency['r'], 'Python': doc_frequency['python'],
                              'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                              'Ruby': doc_frequency['ruby'],
                              'Perl': doc_frequency['perl'], 'Matlab': doc_frequency['matlab'],
                              'Swift': doc_frequency['swift'],
                              'Scala': doc_frequency['scala']})

    analysis_tool_dict = Counter({'Excel': doc_frequency['excel'], 'Tableau': doc_frequency['tableau'],
                                  'D3.js': doc_frequency['d3.js'], 'SAS': doc_frequency['sas'],
                                  'SPSS': doc_frequency['spss'], 'D3': doc_frequency['d3']})

    hadoop_dict = Counter({'Hadoop': doc_frequency['hadoop'], 'MapReduce': doc_frequency['mapreduce'],
                           'Spark': doc_frequency['spark'], 'Pig': doc_frequency['pig'],
                           'Hive': doc_frequency['hive'], 'Shark': doc_frequency['shark'],
                           'Oozie': doc_frequency['oozie'], 'ZooKeeper': doc_frequency['zookeeper'],
                           'Flume': doc_frequency['flume'], 'Mahout': doc_frequency['mahout']})

    database_dict = Counter({'SQL': doc_frequency['sql'], 'NoSQL': doc_frequency['nosql'],
                             'HBase': doc_frequency['hbase'], 'Cassandra': doc_frequency['cassandra'],
                             'MongoDB': doc_frequency['mongodb']})

    overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict

    final_frame = pd.DataFrame(overall_total_skills.items(),
                               columns=['Term', 'NumPostings'])
    region_dict = {
        '16': 'Belarus',
        '1002': 'Minsk',
        '1003': 'Gomel',
        '1005': 'Vitebsk',
        '1007': 'Brest',
        '1006': 'Hrodno',
        '1004': 'Mogilev',
        '115': 'Kiev',
        '1': 'Moscow',
        '113': 'Russia',
    }
    final_frame['NumOfVacancies'] = len(job_descriptions)
    final_frame['Region'] = region_dict[region]
    final_frame['Date'] = datetime.date.today().isoformat()
    file_name = 'jobs_frame_' + datetime.date.today().isoformat() +"_" + region_dict[region]
    final_frame.to_json('d:\\Magister\\WebScraping\\data\\' + file_name + '.json', orient='table')
    final_frame.drop('NumOfVacancies', 1, inplace=True)
    final_frame.drop('Region', 1, inplace=True)
    final_frame.drop('Date', 1, inplace=True)

    final_frame.NumPostings = (final_frame.NumPostings) * 100 / len(
        job_descriptions)

    final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)

    final_plot = final_frame.plot(x='Term', kind='bar', legend=None,
                                  title='Percentage of ' + final_job.replace('+', ' ') + ' Job Ads with a Key Skill, ')

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure()
    #plt.show(fig)
    plt.show()
    return fig, final_frame
