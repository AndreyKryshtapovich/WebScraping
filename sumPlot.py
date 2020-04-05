import os
import matplotlib.pyplot as plt
import pandas as pd

# Assumption: all files that are required are in one directory and he have files for interesting dates
def sumPlot():
    final_job = 'software+engineer'
    all_frames = []
    num_of_all_vacancies = 0

    directory = 'd:\\Magister\\WebScraping\\data\\'

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

    final_frame = final_frame.from_dict(final_dict)
    final_frame.NumPostings = (final_frame.NumPostings) * 100 / num_of_all_vacancies
    final_frame.sort_values(by='NumPostings', ascending=False, inplace=True)

    final_plot = final_frame.plot(x='Term', y='NumPostings', kind='bar', legend=None,
                                  title='Percentage of ' + final_job.replace('+', ' ') + ' Job Ads with a Key Skill, ')

    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure()
    # plt.show(fig)
    plt.show()
    return fig, final_frame
