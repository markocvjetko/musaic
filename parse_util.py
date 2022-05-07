import re
import glob
from music21 import *
from File_util import *
import music21

TIME_QUANT = 60

def transpose_interval(path):
    score = converter.parse(path)
    key = score.analyze('key')
    interval = music21.interval.Interval(key.tonic, music21.pitch.Pitch('C')).semitones
    return interval

def track(line):
    return int(line.split(',')[0])


def timestamp(line):
    return int(line.split(',')[1])


def command(line):
    return line.split(',')[2].strip()


def pitch(line):
    if command(line) == 'Note_on_c' or command(line) == 'Note_off_c':
        return int(line.split(',')[4])
    else:
        return None


def volume(line):
    if command(line) == 'Note_on_c' or command(line) == 'Note_off_c':
        return int(line.split(',')[5])
    else:
        return None


def cut_non_instrumental_tracks(file):
    END_OF_RELEVANT_DATA_REGEX = '([4-9]+, 0, Start_track\n[4-9]+, 0, MIDI_port, 0\n([3-9]+, 0, Title_t, .+\n)?[3-9]+, 0, End_track|0, 0, End_of_file)'
    START_OF_RELEVANT_DATA_REGEX = '2, 0, Start_track'
    cut_before_index = re.search(START_OF_RELEVANT_DATA_REGEX, file).start()
    cut_after_index = re.search(END_OF_RELEVANT_DATA_REGEX, file).start()

    return file[cut_before_index:cut_after_index]


def split_tracks(file):
    '''
    :return: list of strings, each corresponding to a track containing a piece of music
    '''
    tracks = []
    track_num = 1

    while True:
        track_start_regex = str(track_num) + ', [0-9]+, Start_track'
        track_end_regex = str(track_num) + ', [0-9]+, End_track'

        track_start_match = re.search(track_start_regex, file)
        track_end_match = re.search(track_end_regex, file)
        if track_start_match:
            tracks.append(file[track_start_match.start():track_end_match.end()])
        else:
            return tracks
        track_num += 1


def clean_instrumental_track(track):
    cleaned_track = ''
    for line in track.splitlines():
        if command(line) == 'Note_on_c' or command(line) == 'Note_off_c':
            cleaned_track += line + '\n'
    return cleaned_track


def merge_clean_instrumental_tracks(tracks):
    lines = []
    for track in tracks:
        for line in track.splitlines():
            lines.append(re.sub(pattern='[0-9]+', repl='2', string=line, count=1))
    lines.sort(key=lambda x: timestamp(x))
    return '\n'.join(lines)


def midi_note_to_char(note):
    return chr(note - 21 + 33)

def char_to_midi_note(note):
    return ord(note) + 21 - 33

def note_on_command_str(timestamp, pitch, channel=2, volume=100):
    return str(channel) + ', ' + str(timestamp) + ', Note_on_c, 0, ' + str(pitch) + ', ' + str(volume)

def note_off_command_str(timestamp, pitch, channel=2):
    return str(channel) + ', ' + str(timestamp) + ', Note_on_c, 0, ' + str(pitch) + ', ' + str(0)

def carycompressed_to_midicsv(cary, track_title='untitled'):
    track = []
    track.append('0, 0, Header, 1, 2, 480')
    track.append('1, 0, Start_track')
    track.append('1, 0, Time_signature, 4, 2, 24, 8')
    track.append('1, 0, Tempo, 500000')
    track.append('1, 0, Title_t,' + '"' + track_title + '"')
    track.append('1, 0, SMPTE_offset, 96, 0, 3, 0, 0')
    track.append('1, 0, End_track')
    track.append('2, 0, Start_track')
    track.append('2, 0, MIDI_port, 0')
    track.append('2, 0, Control_c, 0, 7, 100')
    track.append('2, 0, Control_c, 0, 10, 74')
    timestamp = 0
    active_notes = []
    for current_notes in cary.split(' '):
        for note in active_notes:
            if note not in current_notes:
                active_notes.remove(note)
                track.append(note_off_command_str(timestamp, char_to_midi_note(note)))
        for note in current_notes:
            if note not in active_notes:
                active_notes.append(note)
                track.append(note_on_command_str(timestamp, char_to_midi_note(note)))
        timestamp += TIME_QUANT

    track.append('2, ' + str(timestamp) + ', End_track')
    track.append('0, 0, End_of_file')
    return '\n'.join(track)

def midicsv_to_carycompressed(midicsv, transpose_interval=0):

    tracks = split_tracks(midicsv)
    tracks = [clean_instrumental_track(track) for track in tracks]
    track = merge_clean_instrumental_tracks(tracks)

    lines = track.splitlines()
    max_time = timestamp(lines[-1])
    active_notes = []
    cary = [' ']
    current_time = 0
    i = 0
    while current_time < max_time or i >= len(lines):
        line = lines[i]
        if timestamp(line) > current_time:
            current_notes = ''.join([midi_note_to_char(note + transpose_interval) for note in active_notes])
            current_notes = ''.join(sorted(list(dict.fromkeys(current_notes))))
            cary.append(current_notes)
            #print(*cary)
            current_time += TIME_QUANT
        else:
            if command(line) == 'Note_on_c' and volume(line) > 0:
                active_notes.append(pitch(line))
                cary[-1] = cary[-1].replace(midi_note_to_char(pitch(line)), '')
            if command(line) == 'Note_on_c' and volume(line) == 0 or command(line) == 'Note_off_c':
                try:
                    active_notes.remove(pitch(line))
                except ValueError:
                    print('x not in list')
            i += 1
            # print(active_notes)
    return ' '.join(cary)


def parse_midicsv_folder_to_cary(root_dir, encoding='latin-1'):
    paths = list_files_recursive(root_dir, '.csv')
    new_paths = [path.replace('.csv', '.cary') for path in paths]
    for path, midicsv in zip(new_paths, read_files(paths, encoding=encoding)):
        print(path)
        midfile = path.replace('cary', 'mid')
        try:
            interval = transpose_interval(midfile)
        except:
            print('error in determining the key, skipping...')
            continue

        cary = midicsv_to_carycompressed(midicsv, interval)
        write_file(path, cary)

def parse_cary_folder_to_midicsv(root_dir, encoding='latin-1'):
    paths = list_files_recursive(root_dir, 'cary')
    new_paths = [path.replace('cary', '.csv') for path in paths]
    for path, cary in zip(new_paths, read_files(paths, encoding=encoding)):
        midicsv = carycompressed_to_midicsv(cary)
        write_file(path, midicsv)

#parse_midicsv_folder_to_cary('data')
#parse_cary_folder_to_midicsv('bach')
