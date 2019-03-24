#  load staff ids for catering training flights
#  flights to load staff in list 'flights', dates in 'dates', def crw_lst_comp checks if user enabled and is crew

import os
import auth
from datetime import datetime, timedelta
import json
import sys


#flights = ['0100', '0102', '0110', '0106', '0200', '0204', '0260', '0208', '0290', '0292']


def get_crw_full_dct():
    print('parsing full crew list...')
    url_crw_list = os.environ['url_main'] + 'admin/ajax/users_all?draw=1&columns[0][data]=staffId&columns[0][name]=staffId&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=username&columns[1][name]=username&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=firstName&columns[2][name]=firstName&columns[2][searchable]=false&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=lastName&columns[3][name]=lastName&columns[3][searchable]=false&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=lastUpdate&columns[4][name]=lastUpdate&columns[4][searchable]=false&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=image&columns[5][name]=image&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=display&columns[6][name]=display&columns[6][searchable]=false&columns[6][orderable]=false&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=delete&columns[7][name]=delete&columns[7][searchable]=false&columns[7][orderable]=false&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=enabled&columns[8][name]=enabled&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start=0&length={}&search[value]=&search[regex]=false&_=1548238774817'
    total = json.loads(session.get(url_crw_list.format('10')).content)['recordsTotal']
    full_list = json.loads(session.get(url_crw_list.format(total)).content)['data']
    full_dct = {crw['staffId']: crw for crw in full_list}
    return full_dct


def get_fl_id(flight, date):
    #print('parsing data for flight ' + flight + '  ' + date)
    url_fl_filtered = os.environ['url_main'] + url_fl_list.format(flight, date)
    r = session.get(url_fl_filtered)
    r = json.loads(r.content)
    if r['data']:
        fl_id = r['data'][0]['DT_RowId'].replace(',', '')
        arr_arpt = r['data'][0]['arrivalAirport'].replace(',', '')
        return fl_id, arr_arpt
    else:
        return None, None


def get_fl_crw(fl_id):
    url_crw = os.environ['url_main'] + url_fl_crw.format(fl_id)
    r = session.get(url_crw)
    r = json.loads(r.content)
    return r['data']


def crw_lst_comp(crw_lst, crw_full_dct):
    crw_lst = [crw for crw in crw_lst if (crw['staffId'] in crw_full_lst.keys()
                                          and 'true' in crw_full_dct[crw['staffId']]['enabled'])]
    crw_lst = [crw for crw in crw_lst if crw['position'] in ('FA', 'CM')]
    return crw_lst


cur_date = datetime.now()
dates = [datetime.strftime(cur_date + timedelta(days=d), '%Y-%m-%d') for d in range(0,2)]


os.environ['url_main'] = 'https://admin-su.crewplatform.aero/'
url_fl_list = 'core/ajax/filter/flights/{{id}}/{{date}}/{{airport}}?draw=4&columns[0][data]=flightNumber&columns[0][name]=flightNumber&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]={}&columns[0][search][regex]=false&columns[1][data]=departureAirport&columns[1][name]=departureAirport&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=departureDate&columns[2][name]=departureDate&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]={}&columns[2][search][regex]=false&columns[3][data]=flightStatusLabel&columns[3][name]=flightStatusLabel&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=arrivalAirport&columns[4][name]=arrivalAirport&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=details&columns[5][name]=details&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&order[0][column]=2&order[0][dir]=desc&start=0&length=20&search[value]=&search[regex]=false&_=1548233858313'
url_fl_crw = 'core/flight/details/crew/{}?draw=1&columns[0][data]=staffId&columns[0][name]=staffId&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=name&columns[1][name]=name&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=position&columns[2][name]=position&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=email&columns[3][name]=email&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&order[0][column]=2&order[0][dir]=asc&start=0&length=20&search[value]=&search[regex]=false&_=1548240002914'


txt = open('flights_noCM_' + datetime.strftime(cur_date, '%Y_%m_%d') + '.txt', 'w')

session = auth.authentication()[0]
crw_full_lst = get_crw_full_dct()



#  here new flights list added
url_fl_with_date = os.environ['url_main'] + 'core/ajax/filter/flights/{{id}}/{{date}}/{{airport}}?draw=3&columns[0][data]=flightNumber&columns[0][name]=flightNumber&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=departureAirport&columns[1][name]=departureAirport&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=departureDate&columns[2][name]=departureDate&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]={}&columns[2][search][regex]=false&columns[3][data]=flightStatusLabel&columns[3][name]=flightStatusLabel&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=arrivalAirport&columns[4][name]=arrivalAirport&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=details&columns[5][name]=details&columns[5][searchable]=false&columns[5][orderable]=false&columns[5][search][value]=&columns[5][search][regex]=false&order[0][column]=2&order[0][dir]=desc&start=0&length=7000&search[value]=&search[regex]=false&_=1538485601876'
url_fl_with_date = url_fl_with_date.format(dates[0])
flights = session.get(url_fl_with_date)
flights = json.loads(flights.content)['data']
flights = [f['flightNumber'] for f in flights]
num_of_noCM = 0
num_of_2CM = 0

def count_CM(crw_list):
    crw_position = [crw['position'] for crw in crw_list if crw['position'] == 'CM']
    if len(crw_position) == 0:
        print('no CM on flight')
        return (1,0)
    if len(crw_position) > 1:
        print('more than 1 CM on flight')
        return (0,1)
    else:
        return (0,0)


for flight in flights:
    for date in dates:
        fl_id, arr_aprt = get_fl_id(flight, date)
        if fl_id is None:
            continue
        crw_lst = get_fl_crw(fl_id)


        if count_CM(crw_lst)[0] == 1:
            print(flight, date)
            num_of_noCM += 1
            crw_lst = crw_lst_comp(crw_lst, crw_full_lst)
            txt.write('SU' + flight + '  ' + arr_aprt + '  ' + date + '\n')
            for crw in crw_lst:
                txt.write(crw['position'] + '  ' + crw['staffId'] + '  ' + crw['name'] + '\n')
            txt.write('\n')

        if count_CM(crw_lst)[1] == 1:
            print(flight, date)
            num_of_2CM += 1
            crw_lst = crw_lst_comp(crw_lst, crw_full_lst)
            txt.write('SU' + flight + '  ' + arr_aprt + '  ' + date + '\n')
            for crw in crw_lst:
                txt.write(crw['position'] + '  ' + crw['staffId'] + '  ' + crw['name'] + '\n')
            txt.write('\n')



