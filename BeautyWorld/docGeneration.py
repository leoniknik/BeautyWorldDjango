from openpyxl import Workbook
from BeautyWorld.models import *
import random
import os
import time
from shutil import copyfile
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.worksheet import Worksheet
import calendar

#print(wb2.get_sheet_names())
#ws = wb2.worksheets[0]

class WS(Worksheet):
    def wr(self,i,j,d):
        pass

def c(i,j):
    ar=['A','B','C','D']
    return str(ar[i])+str(j+1)


def create_file(salon_id):
    salon = Salon.objects.get(pk=salon_id)

    id = random.randint(11111111111111111,99999999999999999)
    id = calendar.timegm(time.gmtime())
    file_name = "doc"+str(id)+".xlsx"
    file = Path(file_name)
    if (file.exists()):
        os.remove(file)
    copyfile("book.xlsx",file_name)
    time.sleep(1)

    doc = load_workbook(file_name)

    #feedback
    sh = doc.worksheets[0]
    if Feedback.objects.filter(order__salon=salon).count()>0:
        feeds = list(Feedback.objects.filter(salon=salon))
        scores = [0, 0, 0, 0, 0]
    else:
        feeds = []
        scores = [random.randint(1,40),random.randint(1,40),random.randint(1,40),random.randint(1,40),random.randint(1,40)]

    for feed in feeds:
        scores[feed.points-1]+=1

    for i in range(0,len(scores)):

        sh[c(0,i+1)] = i+1
        sh[c(1,i+1)] = scores[i]

    doc.save(file_name)

    #voronka
    sh = doc.worksheets[1]
    array = [0,0,0,0,0]
    array[0]=random.randint(80,100)
    array[1] = random.randint(80, array[0])
    array[2] = random.randint(60, array[1])
    array[3] = random.randint(40, array[2])
    array[4] = random.randint(1,  array[3])

    for i in range(0,len(array)):
        sh[c(1,i+1)] = array[i]
    doc.save(file_name)

    #order stat
    sh = doc.worksheets[2]
    array = []
    date = datetime.datetime.now()
    for i in range(0, 7):
        print(date)
        date -= datetime.timedelta(days=1)
        array.append((date.strftime("%d.%m.%Y"), random.randint(0, 100)))

    for i in range(len(array)):
        sh[c(0, i + 1)] = array[i][0]
        sh[c(1, i + 1)] = array[i][1]
    doc.save(file_name)

    return file_name
