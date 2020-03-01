import re
import urllib2
from collections import Counter
from time import sleep

import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup

from textCleaner import text_cleaner


def skills_info(city=None, state=None, job=""):
    final_job = str(job.replace(" ", "+"))

    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,
                           '%2C+', state]
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list)

    base_url = 'http://www.indeed.com'

    try:
        request = urllib2.Request(final_site, headers={"Accept": "text/html",
                                                       "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"})

        html = urllib2.urlopen(request).read()
    except:
        'That city/state combination did not have any jobs. Exiting . . .'
        return
    soup = BeautifulSoup(html, "html.parser")

    num_jobs_area = soup.find(id='searchCountPages').string.encode('utf-8')

    job_numbers = re.findall('\d+', num_jobs_area)

    if len(job_numbers) >= 3:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[1]) * 1000) + int(job_numbers[2])
    else:
        total_num_jobs = int(job_numbers[1])

    city_title = city
    if city is None:
        city_title = 'Nationwide'

    # print 'There were', total_num_jobs, 'jobs found,', city_title

    num_pages = total_num_jobs / 10
    job_descriptions = []

    for i in xrange(1, num_pages + 1):
        print 'Getting page', i
        start_num = str(i * 10)
        current_page = ''.join([final_site, '&start=', start_num])

        html_page = urllib2.urlopen(current_page).read()

        page_obj = BeautifulSoup(html_page, "html.parser")
        job_link_area = page_obj.find(id='resultsCol')

        job_URLS = [base_url + str(link.get('href')) for link in
                    job_link_area.find_all('a')]

        job_URLS = filter(lambda x: 'clk' in x, job_URLS)

        for j in xrange(0, len(job_URLS)):
            final_description = text_cleaner(job_URLS[j])
            if final_description:
                job_descriptions.append(final_description)
            sleep(
                1)  # in order not to get a capcha

    print 'Done with collecting the job postings!'
    # print 'There were', len(job_descriptions), 'jobs successfully found.'

    doc_frequency = Counter()
    [doc_frequency.update(item) for item in job_descriptions]

    prog_lang_dict = Counter({'R': doc_frequency['r'], 'Python': doc_frequency['python'],
                              'Java': doc_frequency['java'], 'C++': doc_frequency['c++'],
                              'Ruby': doc_frequency['ruby'],
                              'Perl': doc_frequency['perl'], 'Matlab': doc_frequency['matlab'],
                              'JavaScript': doc_frequency['javascript'], 'Scala': doc_frequency['scala']})

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

    final_frame.NumPostings = (final_frame.NumPostings) * 100 / len(
        job_descriptions)

    final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)

    final_plot = final_frame.plot(x='Term', kind='bar', legend=None,
                                  title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_title)

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure()
    plt.show()
    return fig, final_frame
