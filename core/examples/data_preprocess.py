import pandas as pd
import json
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split

CORE_DIR = Path(__file__).absolute().parent / '../'
DATA_CSV = CORE_DIR / 'data/data.csv'


def main():
    json_file = sys.argv[1]

    print('processing json file: {}...'.format(json_file))

    with open(json_file, 'rb') as f:
        data = f.read()

    data = data.decode('latin-1').encode().decode()

    columns = list(json.loads(data.split('\n')[0]).keys())
    rows = [list(json.loads(r).values()) for r in data.split('\n')[:-1]]
    df = pd.DataFrame(data=rows, columns=columns)

    print('saved to data.csv ...')

    df.to_csv(DATA_CSV)

    df = df.drop(["review_id", "user_id", "business_id", "useful", "funny", "cool", "date"], axis=1)

    train, test = train_test_split(df, test_size=0.2)
    train.to_csv(CORE_DIR / 'data/train.csv', index=False)
    test.to_csv(CORE_DIR / 'data/val.csv', index=False)
    print('saved to train.csv, val.csv')


if __name__ == '__main__':
    main()
