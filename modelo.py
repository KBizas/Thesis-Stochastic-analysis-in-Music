import numpy as np

class Modelz():
    
    def __init__(self, data):
        self.main = data
        self.data = self.descrap()
        self.trim = self.trim_doubles()
        self.notes= self.grab_notes()
        self.times= self.grab_times()
        self.move = self.grab_move()
        self.k = len(self.move)//10
        self.hist = self.get_histo()
        self.heat =  self.make_heat()

    def get_histo(self):
        katanomh = np.histogram(self.move, bins=48, range=(-24,24))
        return katanomh


    def get_first_note_index(self):                                   ### unused
        for i in range(len(self.main)):
            if self.main[i].type == 'note_on': 
                return i

    def trim_doubles(self):
        a=0
        for i in range(0, len(self.data)-1,2):
            if self.data[i].type=='note_on' and self.data[i].note==self.data[i+1].note:
                a=a+1
            if a>len(self.data)/5:
                trim=2
            else:
                trim=1
        return trim

    def grab_notes(self):
        start=self.get_first_note_index()
        notes=[]
        times=[]
        a=1                                                   #### a einai temp metrhths pitchwheel seri pou emfanizontai
        for i in range(0, len(self.data)-1, self.trim):
            if self.data[i].type=='note_on':
                #print(self.data[i])                                      
                notes.append(self.data[i].note)
                times.append(self.data[i].time)
                a=1
            # elif self.data[i].type=='note_off':              !!!! den xreiazetai giati exw to trim doubles parakatw <3
            #     times.append(self.data[i].time)              !!!! mporei na xreiastei se periergo publisher midi
            elif self.data[i].type=='pitchwheel':
                a=a+1

        return notes
    
    def grab_times(self):
        times=[]
        a=1                                                   #### a einai temp metrhths pitchwheel seri pou emfanizontai
        for i in range(0, len(self.data)-1, self.trim):
            if self.data[i].type=='note_on':
                times.append(self.data[i].time)
                a=1
            elif self.data[i].type=='pitchwheel':
                times[i-a]=times[i-a]+self.data[i].time
                a=a+1

        return times

    def descrap(self):
        start=self.get_first_note_index()
        mytrack=[self.main[start]]
        for i in range(start+1, len(self.main)-1):
            if self.main[i].type=='note_on':
                mytrack.append(self.main[i])
            elif self.main[i].type=='pitchwheel':
                mytrack.append(mytrack[-1])
        return mytrack

    def grab_move(self):
        temp=[]
        for i in range(1, len(self.notes)):
            temp.append(self.notes[i]-self.notes[i-1])
            #print(temp[i-1])                                               ###wraio check
        return temp

    def make_heat(self):
        temps=[]
        for i in range(1, len(self.notes)):
            temps.append(self.notes[i]-self.notes[0])
        return temps