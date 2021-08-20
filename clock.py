# 防止睡眠
def DoNotSleep():
    url = "https://linebotceb102.herokuapp.com/"
    r = requests.get(url)

# 防止自動休眠
sched.add_job(DoNotSleep, trigger='interval', id='doNotSleeps_job', minutes=20)