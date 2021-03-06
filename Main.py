import schedule as schedule

from PlotBySkill import plotBySkill
from jsonGenerator import jsonGenerator
from skillsInfo import skills_info
from sumPlot import sumPlot
from tutBySkillsInfo import tutBySkillsInfo
from jproperties import Properties

props = Properties()
with open("system.properties", "rb") as f:
    props.load(f, "utf-8")

def scraping_job():
    target_resource = props.get("targetResource").data
    if target_resource == "tutBy":
        region_code = props.get("tutBy.cityCode").data
        target_job = props.get("tutBy.targetJob").data
        tutBySkillsInfo(region_code, target_job)
    else:
        if target_resource == "indeed":
            city = props.get("indeed.city").data
            state = props.get("indeed.state").data
            target_job = props.get("indeed.targetJob").data
            skills_info(city, state, target_job)


start_time = props.get("system.startTime").data
schedule.every().day.at(str(start_time)).do(scraping_job)
while True:
    schedule.run_pending()

# Right now we are searching for data scientist jod, it's hardcoded for now in functions.

# skills_info() takes city name and state code like on indeed.com

# tutBySkillsInfo() takes region id from jobs.tut.by.
# 16 - Belarus
# 1002 - Minsk
# 1003 - Gomel
# 1005 - Vitebsk
# 1007 - Brest
# 1006 - Hrodno
# 1004 - Mogilev
# 115 - Kiev
# 1 - Moscow
# 113 - Russia
# Process could take some time especially for large locations.
