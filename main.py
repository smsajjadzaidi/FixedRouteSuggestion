import argparse
import sys
import numpy as np
import logging


class FixedRouteSuggestion:

    def __init__(self):
        self.fixed_stations = []
        self.suggested_stations = []

    @staticmethod
    def parse_args():

        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input_file', help="Input File")
        parser.add_argument('-o', '--output_file', help='Output File')
        return parser.parse_args()

    def read_input(self, input_file):

        try:
            file = open(input_file, "r")

            number_of_fixed_stations = int(file.readline())
            for i in range(number_of_fixed_stations):
                number_of_fixed_stations = file.readline()
                for j in range(int(number_of_fixed_stations)):
                    line = file.readline().split()
                    station_dict = {'station': line[0], 'coordinates': [int(line[1]), int(line[2])]}
                    self.fixed_stations.append(station_dict)

            number_of_suggested_stations = int(file.readline())
            for i in range(number_of_suggested_stations):
                line = file.readline().split()
                station_dict = {'station': line[0], 'coordinates': [int(line[1]), int(line[2])]}
                self.suggested_stations.append(station_dict)
        except Exception as e:
            logging.error("Error in file reading [{0}] at line [{1}]".format(e, sys.exc_info()[2].tb_lineno))

    def find_closest_station(self, suggested_station_coordinates):

        deltas = self.fixed_station_coordinates_numpy - suggested_station_coordinates
        min_distance = np.einsum('ij,ij->i', deltas, deltas)
        closest_station_index = np.argmin(min_distance)
        closest_station = self.fixed_stations[closest_station_index]['station']
        return closest_station

    def run(self):
        args = self.parse_args()
        input_file = args.input_file
        output_file = args.output_file
        if not input_file:
            logging.error('Please specify input file in arguments')
            raise SystemExit

        if not output_file:
            output_file = input_file.replace(".txt", "_output.txt")

        self.read_input(input_file)
        self.fixed_stations_coordinates = [x['coordinates'] for x in self.fixed_stations]
        self.fixed_station_coordinates_numpy = np.asarray(self.fixed_stations_coordinates)

        try:
            file = open(output_file, "w")
            for station in self.suggested_stations:
                closest_station = self.find_closest_station(station['coordinates'])
                file.write(str(station['station']) + ' ' + str(closest_station) + '\n')
            file.close()
        except Exception as e:
            logging.error("Error in file reading [{0}] at line [{1}]".format(e, sys.exc_info()[2].tb_lineno))


if __name__ == '__main__':
    obj = FixedRouteSuggestion()
    obj.run()
