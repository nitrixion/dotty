from datetime import datetime

def getTime(time):
        #print("parsing: " + time)
        #                   [Sat Aug 21 01:06:00 2021]
        # datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
        return datetime.strptime(time, '%c')