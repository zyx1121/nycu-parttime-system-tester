import subprocess
from zoneinfo import ZoneInfo

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

TZ = ZoneInfo("Asia/Taipei")


def run_marker(marker: str):

    cmd = ["uv", "run", "pytest", "-m", marker, "-s", "-q"]
    subprocess.run(cmd, check=False)


def main():

    load_dotenv()

    sched = BlockingScheduler(timezone=TZ)

    # 08:00 signin
    sched.add_job(
        run_marker, CronTrigger(hour=8, minute=0), args=["signin"], id="signin_0800"
    )

    # 12:00 signout
    sched.add_job(
        run_marker, CronTrigger(hour=12, minute=0), args=["signout"], id="signout_1200"
    )

    # 13:00 signin
    sched.add_job(
        run_marker, CronTrigger(hour=13, minute=0), args=["signin"], id="signin_1300"
    )

    # 17:00 signout
    sched.add_job(
        run_marker, CronTrigger(hour=17, minute=0), args=["signout"], id="signout_1700"
    )

    sched.start()


if __name__ == "__main__":
    main()
