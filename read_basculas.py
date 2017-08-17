import csv

from pull_data import pull_data


def read_basculas(file_name='basculas'):

    """
    Read all information from basculas.csv file
    Args:
        :param file_name: The input file containing all sensor information

    TODO:
        At this function, the program pulls in all sensor data, then process it sensor by sensor.
        Change the program a little bit so that it can read and process data sensor by sensor.
    """

    # with open('file/basculas.csv','r') as basculas:
    with open('file/' + file_name + '.csv','r') as basculas:
        next(basculas)
        reader = csv.reader(basculas)
        rows = []
        for row in reader:

            name = row[0].strip(' "\'');
            id_raw = row[2].strip(' "\'');

            print(name,id_raw)
            pull_data(name, id_raw)

# For testing purpose:
# read_basculas()