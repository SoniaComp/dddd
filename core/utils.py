import pytz
import strgen

def localize_time(tz_str, t):
    return pytz.timezone(tz_str).localize(t)


def generate_random_string(length=10):
    return strgen.StringGenerator('[\w\d]{%d}'%length).render()
