import math

def seconds_to_formatted_time(seconds):
    timeLeft = math.ceil(seconds)
    s = timeLeft % 60
    timeLeft = (timeLeft - s)/60
    m = timeLeft % 60
    timeLeft = (timeLeft - m)/60
    h = timeLeft % 24
    timeLeft = (timeLeft - h) /24
    d = timeLeft

    formattedTime = ''
    if d != 0:
        formattedTime += '{} d'.format(d)
    if h != 0:
        formattedTime += '{} h'.format(h)
    if m != 0:
        formattedTime += '{} m'.format(m)
    if s != 0:
        formattedTime += '{} s'.format(s)

def formatted_time_to_seconds(formattedTime):
    # Parsing
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    if 'd' in formattedTime:
        days = int(formattedTime.split('d')[0])
        formattedTime = formattedTime.split('d')[1]
    if 'h' in formattedTime:
        hours = int(formattedTime.split('h')[0])
        formattedTime = formattedTime.split('h')[1]
    if 'm' in formattedTime:
        minutes = int(formattedTime.split('m')[0])
        formattedTime = formattedTime.split('m')[1]
    if 's' in formattedTime:
        seconds = int(formattedTime.split('s')[0])
    return ((days * 24 + hours) * 60 + minutes) * 60 + seconds