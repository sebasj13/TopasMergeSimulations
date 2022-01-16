# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 15:53:41 2021

@author: Sebastian Schäfer
@institution: Martin-Luther-Universität Halle-Wittenberg
@email: sebastian.schaefer@student.uni-halle.de
"""

#############EDIT HERE:#############

filename = ""

files = []

histories = []

####################################

import sys


def read_data(path, histories):

    """
    Function that reads the data in a TOPAS simulation scorer output file.
    Assumes the simulation scored a quantity and its standard deviation, meaning
    only two values follow the three coordinates of the scoring voxel.
    Returns the two scored quantities as an arrays of floats along with the header
    lines and coordinates of the scoring voxels. The latter two are used to re-
    constuct the file into the same format using create_new_file().
    """

    with open(path) as file:

        value, std_dev, header, coords = [], [], [], []  # initialize empty arrays

        for line in file:

            if "#" in line:  # only include header lines

                header += [line]

            if not "#" in line:  # only include data lines
                coords += [line.split(",")[:3]]  # save x,y,z coordinates
                values = line.split(",")[3:]  # cut off x,y,z values
                values = [
                    float(value.replace("e", "E").replace("\n", "")) for value in values
                ]  # convert to float
                value += [values[0]]  # unpack value
                std_dev += [values[1]]  # unpack standard deviation

    return value, std_dev, header, coords


def combine_batches(files, histories):

    """
    Recalculates the total quantity and standard deviation if the simulation was
    split up into multiple parts. Formula taken from:
        
    @MISC {3604634,
    TITLE = {Can I work out the variance in batches?},
    AUTHOR = {heropup (https://math.stackexchange.com/users/118193/heropup)},
    HOWPUBLISHED = {Mathematics Stack Exchange},
    NOTE = {URL:https://math.stackexchange.com/q/3604634 (version: 2020-04-03)},
    }
    """

    if len(files) != len(
        histories
    ):  # test case, each file must have a supplied history
        print("\nNot all simulation had their history count specified!\n")
        sys.exit()

    initial_value, initial_stddev, header, coords = read_data(
        files[0], histories[0]
    )  # initialize values from first file
    hist_0 = histories[0]

    for i in range(
        1, len(files)
    ):  # loop until all files have been merged, excludes first file

        additional_value, additional_stddev = read_data(files[i], histories[i])[
            :2
        ]  # read data from next file
        hist_1 = histories[i]
        new_value = [
            (hist_0 * initial_value[j] + hist_1 * additional_value[j])
            / (hist_0 + hist_1)
            for j in range(len(initial_value))
        ]
        new_stddev = [
            (
                (
                    (
                        (hist_0 - 1) * initial_stddev[j]
                        + (hist_1 - 1) * additional_stddev[j]
                    )
                    / (hist_0 + hist_1 - 1)
                )
                + (
                    (hist_0 * hist_1 * (initial_value[j] - additional_value[j]) ** 2)
                    / ((hist_0 + hist_1) * (hist_0 + hist_1 - 1))
                )
            )
            for j in range(len(initial_value))
        ]

        initial_value = new_value  # set calculated values, standard deviation, and new
        initial_stddev = (
            new_stddev  # number of histories as initial values for next calculation
        )
        hist_0 += hist_1

    return initial_value, initial_stddev, header, coords


def create_new_file(filename, value, stddev, header, coords):

    """
    Creates a .csv file with the same formatiing as the input files, with updated and 
    recalculated values.
    """
    # create array of strings with calculated information
    datalines = [
        str(coords[i][0])
        + ", "
        + str(coords[i][1])
        + ", "
        + str(coords[i][2])
        + ", "
        + str(value[i])
        + ", "
        + str(stddev[i])
        + "\n"
        for i in range(len(value))
    ]

    with open("{}.csv".format(filename), "w+") as file:

        file.writelines(header)
        file.writelines(datalines)

    return


if __name__ == "__main__":

    try:
        create_new_file(filename, *combine_batches(files, histories))
    except IndexError:
        print("No input files specified!")
        sys.exit()
