from joblib import Parallel, delayed
from textblob import TextBlob
from textblob.translate import NotTranslated

import argparse
import os
import pandas as pd

NAN_WORD = "_NAN_"


def translate(comment, language):
    if hasattr(comment, "decode"):
        comment = comment.decode("utf-8")

    text = TextBlob(comment)
    try:
        text = text.translate(to=language)
        text = text.translate(to="en")
    except NotTranslated:
        pass

    return str(text)

def translate_noen(comment, language):
    if hasattr(comment, "decode"):
        comment = comment.decode("utf-8")
    b = TextBlob(comment)
    x = b.detect_language()
    try:
        if x == 'zh-CN':
            b = b.translate(from_lang=x,to='en')
        else:
            b = b.translate(from_lang=x,to='en')
            print(x)
    except:
        print("wrong")
    return str(b)


def main():
    parser = argparse.ArgumentParser("Script for extending train dataset")
    parser.add_argument("--train_file_path",default="../data/train.csv")
    parser.add_argument("--languages", nargs="+", default=["es"])
    parser.add_argument("--thread-count", type=int, default=4)
    parser.add_argument("--result-path", default="extended_data")

    args = parser.parse_args()

    train_data = pd.read_csv(args.train_file_path)
    train_data=train_data[:100]
    comments_list = train_data["Discuss"].fillna(NAN_WORD).values

    if not os.path.exists(args.result_path):
        os.mkdir(args.result_path)

    parallel = Parallel(args.thread_count, backend="threading", verbose=30)
    for language in args.languages:
        print('Translate comments using "{0}" language'.format(language))
        translated_data = parallel(
                            delayed(translate_noen)
                            (comment, language) for comment in comments_list
                                )
        train_data["Disscuss"] = translated_data

        result_path = os.path.join(args.result_path, "test_clean" + language + ".csv")
        train_data.to_csv(result_path, index=False)


if __name__ == "__main__":
    main()
