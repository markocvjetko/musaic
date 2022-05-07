import pandas as pd


def note_statistics(df):
    '''
    Takes a midicsv pandas dataframe, returns the number of occurences of each note,
    octaves not treated separately
    :param df:
    :return:
    '''

    pass


col_names = ['track', 'time', 'command', 'c-param-1', 'c-param-2', 'c-param-3', 'c-param-4', 'c-param-5']
df = pd.read_csv('bach-goldberg-variations/988-aria.csv', names=col_names)

print(df.dtypes)
print(df.iloc[[80]])
df_notes = df[df['command'].str.contains('Note_on_c')]
note_counts = df_notes["c-param-2"].apply(lambda x : x - 12 if x >= 12 else x)
print(note_counts)
note_counts = df_notes["c-param-2"].value_counts(normalize=True)
note_counts = note_counts.apply(lambda x : x - 12 if x >= 12 else x)
print(note_counts)
