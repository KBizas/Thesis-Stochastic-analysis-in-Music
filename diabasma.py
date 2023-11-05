from termcolor import colored
import mido
import os
from modelo import Modelz

class InputFile():
    def __init__(self, folder_name, file_name, data):
        self.folder_name = folder_name
        self.file_name = file_name
        self.data = data


def extract_midi(input_file):
    mid = mido.MidiFile(f'{input_file}', clip=True)
    tracks=mid.tracks
    track=max(tracks,key=len)
    maintrack = Modelz(track)                           ########## KALESMA MODELS ############# !!!!

    dist=maintrack.hist
    dist=dist[0]
    dist=list(dist)
    dump=dist.pop(-1)    
    return maintrack

################################################################

def take_input_from_user():
    intake=input(colored('dwse onoma csv:\n', 'red'))
    print(f'diabazw to {intake}')
    os.chdir('C:/Users/user/Desktop/bigg/')
    return extract_midi(intake)

def take_input_from_folder():
    folders=os.listdir('C:/Users/user/Desktop/bigg/data/input')
    data = []
    for folder in folders:
        files = os.listdir('C:/Users/user/Desktop/bigg/data/input/' + folder)
        for file in files:
            maintrack = extract_midi('C:/Users/user/Desktop/bigg/data/input/' + folder + '/' + file)
            data.append(InputFile(folder, file, maintrack))
    return data

################################################################

