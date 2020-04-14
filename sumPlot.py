import os
import matplotlib.pyplot as plt
import pandas as pd

# Assumption: all files that are required are in one directory and he have files for interesting dates
def sumPlot():
    final_job = 'software+engineer'
    region = 'Minsk'
    all_frames = []
    num_of_all_vacancies = 0

    directory = 'd:\\Magister\\WebScraping\\data\\'

    #for only one file
    # frame = pd.read_json(os.path.join(directory, 'jobs_frame_2020-04-11_TheCity.json'), orient='table')
    # num_of_all_vacancies = num_of_all_vacancies + frame.NumOfVacancies[0]
    # frame = frame.drop('NumOfVacancies', 1)
    # all_frames.append(frame)
    # for all files in directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            frame = pd.read_json(os.path.join(directory, filename), orient='table')
            num_of_all_vacancies = num_of_all_vacancies + frame.NumOfVacancies[0]
            frame = frame.drop('NumOfVacancies', 1)
            all_frames.append(frame)

    final_frame = pd.DataFrame(columns=['Term', 'NumPostings'])
    final_dict = {}

    for frame in all_frames:
        dicts = frame.to_dict('records')
        for dict in dicts:
            if dict['Term'] in final_dict: # if for ex. Java is already in final_dict
                final_dict[dict['Term']] = final_dict.get(dict['Term']) + dict['NumPostings']
            else:
                final_dict[dict['Term']] = dict['NumPostings']
    final_dict = {
        'Term': final_dict.keys(),
        'NumPostings': final_dict.values()
    }

    # Bar chart plot
    # final_frame = final_frame.from_dict(final_dict)
    # final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)
    #
    # final_plot = final_frame.plot(x='Term', y='NumPostings', kind='bar', legend=None,
    #                               title='Percentage of ' + final_job.replace('+', ' ') + ' Job Ads with a Key Skill, ')
    #
    # final_plot.set_ylabel('Percentage Appearing in Job Ads')


    # Pie chart plot
    final_frame = final_frame.from_dict(final_dict)
    final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)
    # the top 5
    final_frame_pie = final_frame[:7].copy()
    # others
    new_row = pd.DataFrame(data={
        'Term': ['Others'],
        'NumPostings': [final_frame['NumPostings'][7:].sum()]
    })
    # combining top 5 with others
    final_frame_pie = pd.concat([final_frame_pie, new_row])

    final_frame_pie.NumPostings = (final_frame_pie.NumPostings) * 100 / num_of_all_vacancies
    plot_title = 'Top skills for {} Job Ads, {}'.format(final_job.replace('+', ' '), region)
    final_plot = final_frame_pie.plot(x='Term', y='NumPostings', kind='pie', labels=final_frame_pie['Term'],
                                      autopct='%1.1f%%',
                                      legend=None, startangle=140, title=plot_title)
    final_plot.set_ylabel('')

    fig = final_plot.get_figure()
    plt.show(fig)
    return fig, final_frame
