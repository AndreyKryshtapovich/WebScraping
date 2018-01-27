import urllib2
from collections import Counter
from time import sleep

import re

import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup

from textCleaner import text_cleaner


def skills_info(city=None, state=None):
    '''
    This function will take a desired city/state and look for all new job postings
    on Indeed.com. It will crawl all of the job postings and keep track of how many
    use a preset list of typical data science skills. The final percentage for each skill
    is then displayed at the end of the collation.

    Inputs: The location's city and state. These are optional. If no city/state is input,
    the function will assume a national search (this can take a while!!!).
    Input the city/state as strings, such as skills_info('Chicago', 'IL').
    Use a two letter abbreviation for the state.

    Output: A bar chart showing the most commonly desired skills in the job market for
    a data scientist.
    '''

    final_job = 'data+scientist'  # searching for data scientist exact fit("data scientist" on Indeed search)

    # Make sure the city specified works properly if it has more than one word (such as San Francisco)
    if city is not None:
        final_city = city.split()
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,
                           '%2C+', state]  # Join all of our strings together so that indeed will search correctly
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list)  # Merge the html address together into one string

    base_url = 'http://www.indeed.com'

    try:
        html = urllib2.urlopen(final_site).read()  # Open up the front page of our search first
    except:
        'That city/state combination did not have any jobs. Exiting . . .'  # In case the city is invalid
        return
    soup = BeautifulSoup(html)  # Get the html from the first page

    # Now find out how many jobs there were

    num_jobs_area = soup.find(id='searchCount').string.encode('utf-8')  # Now extract the total number of jobs found
    # The 'searchCount' object has this

    job_numbers = re.findall('\d+', num_jobs_area)  # Extract the total jobs found from the search result

    if len(job_numbers) > 3:  # Have a total number of jobs greater than 1000
        total_num_jobs = (int(job_numbers[2]) * 1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[1])

    city_title = city
    if city is None:
        city_title = 'Nationwide'

    print 'There were', total_num_jobs, 'jobs found,', city_title  # Display how many jobs were found

    num_pages = total_num_jobs / 10  # This will be how we know the number of times we need to iterate over each new
    # search result page
    job_descriptions = []  # Store all our descriptions in this list

    for i in xrange(1, num_pages + 1):  # Loop through all of our search result pages
        print 'Getting page', i
        start_num = str(i * 10)  # Assign the multiplier of 10 to view the pages we want
        current_page = ''.join([final_site, '&start=', start_num])
        # Now that we can view the correct 10 job returns, start collecting the text samples from each

        html_page = urllib2.urlopen(current_page).read()  # Get the page

        page_obj = BeautifulSoup(html_page)  # Locate all of the job links
        job_link_area = page_obj.find(id='resultsCol')  # The center column on the page where the job postings exist

        job_URLS = [base_url + str(link.get('href')) for link in
                    job_link_area.find_all('a')]  # Get the URLS for the jobs

        job_URLS = filter(lambda x: 'clk' in x, job_URLS)  # Now get just the job related URLS

        for j in xrange(0, len(job_URLS)):
            final_description = text_cleaner(job_URLS[j])
            if final_description:  # So that we only append when the website was accessed correctly
                job_descriptions.append(final_description)
            sleep(
                1)  # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot!

    print 'Done with collecting the job postings!'
    print 'There were', len(job_descriptions), 'jobs successfully found.'
    print(job_descriptions)

    doc_frequency = Counter()  # This will create a full counter of our terms.
    [doc_frequency.update(item) for item in job_descriptions]  # List comp

    # Now we can just look at our final dict list inside doc_frequency

    # Obtain our key terms and store them in a dict. These are the key data science skills we are looking for

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

    overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict  # Combine our Counter objects

   # print(prog_lang_dict)

    final_frame = pd.DataFrame(overall_total_skills.items(),
                               columns=['Term', 'NumPostings'])  # Convert these terms to a
    # dataframe

    # Change the values to reflect a percentage of the postings

    final_frame.NumPostings = (final_frame.NumPostings) * 100 / len(
        job_descriptions)  # Gives percentage of job postings
    #  having that term

    # Sort the data for plotting purposes

    final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)

    # Get it ready for a bar plot

    final_plot = final_frame.plot(x='Term', kind='bar', legend=None,
                                  title='Percentage of Data Scientist Job Ads with a Key Skill, ' + city_title)

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure()  # Have to convert the pandas plot object to a matplotlib object
    print "TEST !!!!"

    plt.show(fig)
    return fig, final_frame  # End of the function
