'''
file: classes_mailroom.py
elmar_m / 22e88@mailbox.org
Lesson09: classes for OOP mailroom program 
'''

import sqlite3, time
from collections import defaultdict 

class Donor:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname
        self.uid = '{}_{}'.format(fname, lname) 
        self.db= sqlite3.connect('BLABLA.db')
        self.dcursor = self.db.cursor()
        self.dcursor.execute('''create table if not exists donors
                     (uid TEXT PRIMARY KEY, 
                    fname TEXT, lname TEXT, last_donation INT DEFAULT 0)''')


    def check_existence(self, uid):
        self.dcursor.execute('select * from donors where uid = ?', (uid,))
        result = self.dcursor.fetchall()
        if len(result) == 0:
            return None
        else:
            return True
        
    
    def create(self, uid, fname, lname, last_donation=None):
        try:
            self.dcursor.execute('''insert into donors 
                    (uid, fname, lname, last_donation)
                     values (?, ?, ?, ?)''', (uid, fname, lname, last_donation))
            self.db.commit()
            return True
        except sqlite3.Error as e:
            print('Exception raised: {}'.format(e))
            return False


    def get_last_donation(self, donor):
        try:
            self.dcursor.execute('select from donors (last_donation) where uid = ?', (donor))
            return self.dcursor.fetchall()
        except sqlite3.Error as e:
            print('Exception raised: {}'.format(e))
            return None
                    

class Mailroom:
    def __init__(self):
        self.db= sqlite3.connect('BLABLA.db')
        self.cursor = self.db.cursor()
        self.cursor.execute('''create table if not exists mailroom
                     (donation_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                    date TEXT, donor TEXT, donation INT DEFAULT 0)''')


    def add_donation(self, donor, amount):
        ts = time.strftime('%Y%m%d-%H%M%S')
        try: 
            self.cursor.execute('insert into mailroom (date, donor, donation) values(?, ?, ?)', (ts, donor, amount)) 
            self.cursor.execute('update donors set last_donation = ? where uid = ?', (amount, donor)) 
            self.db.commit()
            return True
        except sqlite3.Error as e:
            print('Exception raised: {}'.format(e))


    def get_donations(self, donor):
        self.cursor.execute('select date, donation from mailroom where donor = ?', (donor,))
        return self.cursor.fetchall()


    def _get_average_donation(self, donor):
        total = self._get_donations_total(donor)
        num = self._get_number_of_donations(donor)
        avg = total / num
        return format(avg, '.2f')
        

    def _get_number_of_donations(self, donor):
        self.cursor.execute('select * from mailroom where donor = ?', (donor,))
        num = self.cursor.fetchall()
        return len(num)

    
    def _get_donations_total(self, donor):
        self.cursor.execute('select donation from mailroom where donor = ?', (donor,))
        res = self.cursor.fetchall()
        dlist = [x[0] for x in res]
        total = sum(dlist) 
        return total
    

    def get_all_donors(self):
        self.cursor.execute('select donor from mailroom')
        raw = set(self.cursor.fetchall())    # unifying result by putting it into a set
        return raw
    

    def multiply(self, factor, above=None, below=None):
        if above is None and below is None:
            sql_show = 'select count(*) from mailroom where donation'
            sql_total = 'select sum(donation) from mailroom where donation'
            sql = 'update mailroom set donation = donation * ?'
            args = (factor,)
            self._preview(sql_show)
            self.map_multiply(factor)
            self._preview_total(sql_total, factor)
            self._decide(sql, args)
        elif below:
            sql_show = 'select count(*) from mailroom where donation < ' + below
            sql_total = 'select sum(donation) from mailroom where donation < ' + below
            sql = 'update mailroom set donation = donation * ? where donation < ?'
            args = (factor, below)
            self._preview(sql_show)
            self.map_multiply(factor, below=below)
            self._preview_total(sql_total, factor)
            self._decide(sql, args)
        elif above:
            sql_show = 'select count(*) from mailroom where donation > ' + above
            sql_total = 'select sum(donation) from mailroom where donation > ' + above
            sql = 'update mailroom set donation = donation * ? where donation > ?'
            args = (factor, above)
            self._preview(sql_show)
            self.map_multiply(factor, above=above)
            self._preview_total(sql_total, factor)
            self._decide(sql, args)
        return True
    
    
    def _decide(self, sql, args):
        decision = input('\n\tDo you really want to accept this CHALLENGE ? (Y/N)')
        if decision == 'Y':
            self._write_to_db(sql, args)
        else:
            print('\n\tCHALLENGE aborted.')


    def _preview(self, show):
        self.cursor.execute(show)
        rows = self._beautify(self.cursor.fetchall())
        print('\n\tThis operation would affect {} already existing donations!'.format(rows[0]))
        print('\tSee a listing:\n')

    
    def _preview_total(self, total, factor): 
        self.cursor.execute(total)
        value = self._beautify(self.cursor.fetchall())
        value_int = int(value[0])
        result = value_int * int(factor)
        print('\n\tYou would have to give an additional donation of {} to pass the CHALLENGE !'.format(result))


    def _write_to_db(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
            print('\n\tThank you! Donations successfully updated in database.')
        except sqlite3.Error as e:
            print('Exception raised 4: {}'.format(e))
        

    def map_multiply(self, factor, above=None, below=None):
        self.cursor.execute('select donation from mailroom where donation')
        donations_all = self._beautify(self.cursor.fetchall())
        if above is None and below is None: 
            donations_after = list(map(lambda x: x * int(factor), donations_all))
            for i in zip(donations_all, donations_after):
                print('\tcurrent donation: {:<10}   multiplied: {}'.format(i[0], i[1]))
        elif below:
            donations_below = list(filter(lambda x: x < int(below), donations_all))
            donations_after = list(map(lambda x: x * int(factor), donations_below))
            for i in zip(donations_below, donations_after):
                print('\tcurrent donation: {:<10}   multiplied: {}'.format(i[0], i[1]))
        elif above:
            donations_above = list(filter(lambda x: x > int(above), donations_all))
            donations_after = list(map(lambda x: x * int(factor), donations_above))
            for i in zip(donations_above, donations_after):
                print('\tcurrent donation: {:<10}   multiplied: {}'.format(i[0], i[1]))


    # ToDo: make more consistent usage of this function throughout the program... or omit it at all.
    def _beautify(self, listoftuples):
        ''' cursor.fetchall() returns a list of tuples (in our case mostly one-element tuples).
            This method changes that into a list of single items (INT, STRING, whatever). 
        '''
        resultlist = [x[0] for x in listoftuples]       
        return resultlist
        

    def report(self):
        donordict = defaultdict(list)
        maxn = 0
        for i in self.get_all_donors():
            person = i[0]
            total = self._get_donations_total(person)
            slen = len(str(total))
            if slen > maxn:
                maxn = slen
            num = self._get_number_of_donations(person)
            avg = self._get_average_donation(person)
            donordict[person].append(total)
            donordict[person].append(num)
            donordict[person].append(avg)
        maxn += 3
        fstring = '\t{:<20} ' + '|' + '{:>' + str(maxn) + '} ' + '|' + '{:>9}' + '|' + '{:>20}' 
        print(fstring.format('Donor Name', 'Total', 'Num Gifts', 'Average Gift'))  
        print('\t' + '-' * (maxn + 54)) 
        for i in donordict:
            print(fstring.format(i, donordict[i][0], donordict[i][1], donordict[i][2])) 
        
    
    def mail(self):
        with open('./MAIL_TEMPLATE', 'r') as fr:
            lines = fr.readlines()
            for name in self._beautify(self.get_all_donors()):
                ts = time.strftime('%Y%m%d-%H%M%S')
                filename = name + '_' + ts + '.txt'
                self.cursor.execute('select * from donors where uid = ?', (name,))
                result = self.cursor.fetchall()
                if len(result) == 0:
                    print('====Last_donation not found: {}'.format(name))
                else:
                    last_donation = result[0][3]
                    donation = str(last_donation)
                with open(filename, 'w') as fw:
                    for i in lines:
                        if 'NAME' in i:
                            new = i.replace('NAME', name)
                            fw.write(new)
                        elif 'DONATION' in i:
                            new = i.replace('DONATION', donation)
                            fw.write(new)
                        else:
                            fw.write(i)
                    print('\tMailtext for {} successfully written to {}'.format(name, filename))
                    
               

