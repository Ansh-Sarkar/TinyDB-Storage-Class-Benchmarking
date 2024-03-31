#!/usr/bin/env python3
import os
import sys
from tqdm import tqdm
from time import perf_counter

import requests
from tinydb import TinyDB

import storages.YamlStorage1 as YamlStorage1
import storages.YamlStorage2 as YamlStorage2

def benchmark(data, model, iterations = 100, verbose = False):
    """
    Takes a Storage Class / Model and Tests Read-Write Performance
    """
    print(f"\n\033[92m Benchmarking Storage Class / Model: {model.__name__} \033[00m")
    avg_read, avg_write, avg_creation = 0.0, 0.0, 0.0
    _handle = f'db-{model.__name__}.yaml'

    for i in tqdm(range(iterations), desc = "Performing Read-Write Operations... "):
        # removing older database files
        if os.path.exists(_handle):
            os.remove(_handle)

        # creating db and connecting to storage
        db_creation_timer_s = perf_counter()
        db = TinyDB(_handle, storage=model)
        db_creation_timer_e = perf_counter()
        if verbose:
            print("Iter {iteration}: DB Setup / Creation Time = {setup}".format(
                iteration = i + 1,
                setup = db_creation_timer_e - db_creation_timer_s
            ))

        # writing data to database
        db_write_timer_s = perf_counter()
        db.insert_multiple(data)
        db_write_timer_e = perf_counter()
        if verbose:
            print("Iter {iteration}: DB Write Time = {write_time}".format(
                iteration = i + 1,
                write_time = db_write_timer_e - db_write_timer_s
            ))

        # reading from database
        db_read_timer_s = perf_counter()
        _data = db.all()
        db_read_timer_e = perf_counter()
        if verbose:
            print("Iter {iteration}: DB Read Time = {read_time}".format(
                iteration = i + 1,
                read_time = db_read_timer_e - db_read_timer_s
            ))

        # adding to the variables. we divide by number of iterations at the end
        avg_read += (db_read_timer_e - db_read_timer_s)
        avg_write += (db_write_timer_e - db_write_timer_s)
        avg_creation += (db_creation_timer_e - db_creation_timer_s)

    avg_read /= iterations
    avg_write /= iterations
    avg_creation /= iterations

    print(f"Average DB Setup / Creation Time: {avg_creation}")
    print(f"Average DB Data Read Time: {avg_read}")
    print(f"Average DB Data Write Time: {avg_write}")

    # cleanup benchmarking database
    # if os.path.exists(_handle):
    #     os.remove(_handle)

def main():
    """
    Benchmarking multiple Models / Storage Classes for TinyDB
    w.r.t Setup and Read-Write Performance
    """
    data, api_url = None, "https://tenders.guru/api/es/tenders"
    models = [ YamlStorage1, YamlStorage2 ]
    data_multiplier = 1

    print("Fetching Benchmarking Data from API")
    try:
        response = requests.get(api_url)
        data = response.json()['data'] * data_multiplier
    except requests.exceptions as error:
        print(f"Error: {error}")
        data = [
            dict(name = 'Ansh Sarkar', age = 21),
            dict(name = 'Supreeta Nayak', age = 20),
            dict(name = 'Nittishna Dhar', age = 21)
        ]
    print("Benchmarking Data Fetched from API (Size = {benchmark_data_size} bytes)".format(
        benchmark_data_size = sys.getsizeof(data)
    ))

    for model in models:
        benchmark(data = data, model = model, iterations = 20, verbose = False)

if __name__ == '__main__':
    main()