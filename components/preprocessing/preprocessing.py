import spacy
import pandas as pd
import click
import dill
from sklearn.model_selection import train_test_split

nlp = spacy.load('en_core_web_lg')

@click.command()
@click.option('--data_file', default='/mnt/bts.data', help='Path to the data file.')
@click.option('--preprocess_file', default='/mnt/bts_preprocessed.data', help='Path to the output file.')
@click.option('--train_file', default='/mnt/bts_train.data', help='Path to the training set file.')
@click.option('--test_file', default='/mnt/bts_test.data', help='Path to the test set file.')
@click.option('--validation_file', default='/mnt/bts_validation.data', help='Path to the validation set file.')
@click.option('--split_size', default=0.2, help='Size of the validation set.')

def preprocess(data_file, train_file, test_file, validation_file, split_size, preprocess_file):
    # load data
    print('Loading data...')
    with open(data_file, 'r') as f:
        data = dill.load(f)
    print('Data loaded')

    # preprocess data
    print('Preprocessing data...')
    data['comment_text'] = data['comment_text'].apply(lambda x: ' '.join([token.lemma_ for token in nlp(x)]))
    print('Data preprocessed')

    #split training set to validation set
    print('Splitting data...')
    train, test, target, target_test = train_test_split(data, test_size=split_size, random_state=42)
    train, validation, target, target_validation = train_test_split(train, test_size=split_size, random_state=42)

    print('Data splitted')
    print(len(train), 'train examples')
    print(len(validation), 'validation examples')
    print(len(test), 'test examples')


    # save data
    print('Saving data...') 
    with open(train_file, 'w') as f:
        dill.dump(train, f)
    with open(validation_file, 'w') as f:
        dill.dump(validation, f)
    with open(target, 'w') as f:
        dill.dump(target, f)
    with open(target_validation, 'w') as f:
        dill.dump(target_validation, f)
    with open(target_test, 'w') as f:
        dill.dump(target_test, f)
    with open(test_file, 'w') as f:
        dill.dump(test, f)
    with open(preprocess_file, 'w') as f:
        dill.dump(data, f)
   
    return



