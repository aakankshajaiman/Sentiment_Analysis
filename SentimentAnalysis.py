__author__ = 'Aakanksha Jaiman'
import json
import sys
import matplotlib.pyplot as plt
import datetime
import string
import csv

# FILE_PATH = "/Users/aakanksha/Downloads/SentimentAnalysis/"
FILE_PATH = '/Volumes/Personal/MSA/2ndSEM/INFS772/INFS772_Project1/'


def processWords(inputfile, outputfile):
    inFile = open(inputfile, "r")

    line = inFile.readlines()
    line = sorted(set(line))  # remove duplicates by converting into set and then sort

    outFile = open(outputfile, "wb")  # open output file
    for l in line:
        outFile.write(l);

    # Close opend file
    outFile.close()

    return


def read_stocktwits():
    f = open(FILE_PATH + "BAC.json", "r")

    json_txt = f.read()
    decoded = json.loads(json_txt)

    l1 = []
    l2 = []
    l3 = []

    # Extracting dictionaries from json file
    for i in decoded:
        dlist = i['created_at'], i['body'], i["entities"]
        dlist = list(dlist)

        # Extracting Dates and formatting it
        date = dlist[0].values()[0]
        date_t = datetime.datetime.fromtimestamp(date / 1000.0).strftime('%m/%d/%Y %H:%M')

        # Appending dates to the list 'l1'
        l1.append(date_t)

        # Extracting text and formatting it
        body = dlist[1].encode('ascii', 'ignore').lower()
        punct = set(string.punctuation)
        tweet = ''.join(i for i in body if i not in punct)
        tweet = tweet.replace("\n", "")

        # Appending text to the list 'l2'
        l2.append(tweet)

        # Extracting sentiment and formatting it
        sentiment = dlist[2].values()
        for i in sentiment:
            if i == {u'basic': u'Bullish'} or i == {u'basic': u'Bearish'}:
                senti = i.values()[0].encode('ascii', 'ignore')
            else:
                senti = 'Unknown'

                # Appending sentiments to the list 'l3'
            l3.append(senti)

    final_list = zip(l1, l2, l3)

    f = open(FILE_PATH + "BAC.csv", "wb")
    writer = csv.writer(f, delimiter=',')
    for line in final_list:
        writer.writerow(list(line))
    return


def sentiment_analysis():
    f = open(FILE_PATH + "BAC.csv", "r")

    csv_data = f.readlines()
    csv_data = map(str.strip, csv_data)
    csv_data = [i.split(',') for i in csv_data]

    for i in csv_data:
        if i[-1] == 'Unknown':
            dic_file = sentiment_count(i[1])
            if dic_file.get('pos_words') > dic_file.get('neg_words'):
                i[-1] = 'Bullish'
            elif dic_file.get('pos_words') < dic_file.get('neg_words'):
                i[-1] = 'Bearish'
            elif dic_file.get('pos_words') == dic_file.get('neg_words'):
                i[-1] = 'Neutral'
            else:
                i[-1] = 'Neutral'

    # Create date and sentiment lists and merge them together
    lis1 = []
    lis2 = []

    for i in csv_data:
        lis1.append(i[0])
        lis2.append(i[-1])
    the_list = zip(lis1, lis2)

    # Writing the BAC2.CSV File
    with open(FILE_PATH + "BAC2.csv", "wb") as file:
        writer = csv.writer(file, delimiter=',')
        for row in the_list:
            writer.writerow(list(row))

    return


def sentiment_count(text):
    # Open and read text files of positive and negative words
    file1 = open(FILE_PATH + "positive_words.txt", "r")
    file2 = open(FILE_PATH + "negative_words.txt", 'r')

    # create lists of positive and negative words
    p_words = []
    n_words = []

    for word in file1:
        p_words.append(word)
    for word in file2:
        n_words.append(word)

    # remove '\n' from the text
    pos_words = map(str.strip, p_words)
    neg_words = map(str.strip, n_words)

    text_words = text.split()

    # now count positive and negative words in text
    count = 0
    dict = {}
    for w in text_words:
        if w in pos_words:
            count = count + 1
            dict['pos_words'] = count
        else:
            if w in neg_words:
                count = count + 1
                dict['neg_words'] = count
    return dict


def get_sentiment_dates(start_date, end_date):
    positive_dict = {}
    negative_dict = {}
    neutral_dict = {}

    # convert start_date and end_date parameters to datetime objects
    s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # store dates between start date and end date
    delta_list = []

    date_diff = e_date - s_date
    for i in range(date_diff.days + 1):
        delta_list.append(s_date + datetime.timedelta(days=i))

    f = open(FILE_PATH + "BAC2.csv", "r")

    csv_data = f.readlines()
    csv_data = map(str.strip, csv_data)
    csv_data = [i.split(',') for i in csv_data]

    convert_date_list = []

    for i in csv_data:
        convert_date_list.append([datetime.datetime.strptime(i[0], '%m/%d/%Y %H:%M').replace(hour=0, minute=0), i[1]])

    pos_date = []
    neg_date = []
    neu_date = []

    for i in convert_date_list:
        if i[0] in delta_list:
            if i[1] == 'Bullish':
                pos_date.append(i[0])
            if i[1] == 'Bearish':
                neg_date.append(i[0])
            if i[1] == 'Neutral':
                neu_date.append(i[0])

    for i in delta_list:
        if i in pos_date:
            positive_dict[i] = pos_date.count(i)
        else:
            positive_dict[i] = 0
        if i in neg_date:
            negative_dict[i] = neg_date.count(i)
        else:
            negative_dict[i] = 0
        if i in neu_date:
            neutral_dict[i] = neu_date.count(i)
        else:
            neutral_dict[i] = 0
    return [positive_dict, negative_dict, neutral_dict]


def drawing_pie(start_date, end_date):
    dict_count = get_sentiment_dates(start_date, end_date)

    pos = 0
    neg = 0
    neu = 0

    for i in dict_count:
        if i is dict_count[0]:
            pos = sum(i.values())
        if i is dict_count[1]:
            neg = sum(i.values())
        if i is dict_count[2]:
            neu = sum(i.values())

    total = float(pos) + float(neg) + float(neu)

    positive = round((pos / total) * 100, 1)
    negative = round((neg / total) * 100, 1)
    neutral = round((neu / total) * 100, 1)

    # create lists for sentiments,label and color to draw chart
    sentiments = [positive, negative, neutral]
    label = ['Positive', 'Negative', 'Neutral']
    cols = ['b', 'g', 'r']

    plt.pie(sentiments, labels=label, colors=cols, autopct='%1.1f%%', shadow=True)

    # create title for the chart based on the overall sentiment
    if positive > negative and positive > neutral:
        plt.title('Sentiment is Positive')
    if negative > positive and negative > neutral:
        plt.title('Sentiment is Negative')
    if neutral > positive and neutral > negative:
        plt.title('Sentiment is Neutral')
    if positive == negative:
        plt.title('Sentiment is Neutral')
    if positive == neutral and positive > negative:
        plt.title('Sentiment is Positive')
    if positive == neutral and positive < negative:
        plt.title('Sentiment is Negative')
    if negative == neutral and negative > positive:
        plt.title('Sentiment is Negative')
    if negative == neutral and negative < positive:
        plt.title('Sentiment is Positive')

    return plt.show()


def drawing_lines(start_date, end_date):
    dict_count = get_sentiment_dates(start_date, end_date)

    pos_lis = dict_count[0]
    neg_lis = dict_count[1]
    neu_lis = dict_count[2]

    # Intializing different lists
    pos_dates = []
    neg_dates = []
    neu_dates = []

    pos_counts = []
    neg_counts = []
    neu_counts = []

    for i in dict_count:
        if i == pos_lis:
            for key in sorted(i.iterkeys()):
                pos_dates.append(key)
                pos_counts.append(i[key])

        if i == neg_lis:
            for key in sorted(i.iterkeys()):
                neg_dates.append(key)
                neg_counts.append(i[key])

        if i == neu_lis:
            for key in sorted(i.iterkeys()):
                neu_dates.append(key)
                neu_counts.append(i[key])

    # plot the line graph
    fig, ax = plt.subplots()
    ax.plot(pos_dates, pos_counts, 'o-', neg_dates, neg_counts, 'o-', neu_dates, neu_counts, 'o-')
    fig.autofmt_xdate()

    plt.legend(('Positive', 'Negative', 'Neutral'))

    plt.title('Sentiment between %s and %s' % (start_date, end_date))

    return plt.show()


def main():
    processWords(FILE_PATH + "positive_words.txt", FILE_PATH + "positive_words_updated.txt")
    processWords(FILE_PATH + "negative_words.txt", FILE_PATH + "negative_words_updated.txt")
    read_stocktwits()  # output: BAC.csv
    sentiment_analysis()  # output BAC2.csv
    print get_sentiment_dates('2013-01-02', '2013-01-31')
    drawing_pie('2013-01-02','2013-01-31')
    drawing_lines('2013-01-02', '2013-01-31')
    return


if __name__ == '__main__':
    main()
