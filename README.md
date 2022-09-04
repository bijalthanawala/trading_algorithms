[![unittest](https://github.com/bijalthanawala/trading_algorithms/actions/workflows/unittest.yml/badge.svg)](https://github.com/bijalthanawala/trading_algorithms/actions/workflows/unittest.yml)


#### This is a simple exercise aimed at learning and practicing programming.

## DESCRIPTION
This simple project determines time to buy and sell a single stock.

Rules:
- Only one unit of stock is bought at a time, is held between a minimum (30 minutes) and a maximum (60 minutes) period before selling
- Buy and sell operations does not overlap

-----------------------

### USAGE

#### In its simplest form, run the following command in the root directory of the project.
```
python3 -m main.py
```
The above will run with run with detfult arguments

#### See all the supported arguments with the *--help* switch

```
python3 main.py --help
usage: main.py [-h] [--file FILE] [--algorithm {adjacent,minmax,highest,higher,max,new}] [--verbose]

Trading Algorithm

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Name of the input CSV file (Default=test/market_conditions_100.csv)
  --algorithm {adjacent,minmax,highest,higher,max,new}, -a {adjacent,minmax,highest,higher,max,new}
                        Algorithm short name (Default=adjacent)
                        ['adjacent = algorithm_buy_sell_adjacent_low_highs',
                         'minmax = algorithm_pair_min_max',
                         'highest = algorithm_purchase_next_highest',
                         'higher = algorithm_purchase_next_higher',
                         'max = algorithm_purchase_max',
                         'new = algorithm_new_unimplemented']
  --verbose, -v
```

#### An example command with arguments

```
python3 main.py --verbose --file test/market_conditions_100.csv --algorithm adjacent
```

#### Output of the example command above
```
Reading CSV file: test/market_conditions_100.csv
Read 100 rows
Running: Algorithm of buying and selling adjacent lows and highs
Trades are:
Open at 00000(1.0708), close 00031(1.1047) (hold for 030 minutes) for profit 0.0339
Open at 00001(1.3258), close 00032(1.3804) (hold for 030 minutes) for profit 0.0546
Open at 00006(1.0250), close 00037(1.3644) (hold for 030 minutes) for profit 0.3394
Open at 00008(1.3159), close 00039(1.3890) (hold for 030 minutes) for profit 0.0731
Open at 00010(1.0126), close 00041(1.1870) (hold for 030 minutes) for profit 0.1744
Open at 00011(1.1243), close 00042(1.2164) (hold for 030 minutes) for profit 0.0921
Open at 00012(1.0069), close 00043(1.1114) (hold for 030 minutes) for profit 0.1045
.
.
.
Open at 00062(1.1449), close 00093(1.1518) (hold for 030 minutes) for profit 0.0069
Open at 00063(1.2400), close 00094(1.3755) (hold for 030 minutes) for profit 0.1355
Open at 00065(1.0278), close 00096(1.3693) (hold for 030 minutes) for profit 0.3415
Open at 00067(1.0453), close 00098(1.2366) (hold for 030 minutes) for profit 0.1913
Total profit 4.7419
```

-----------------------

### CSV FILE

#### Sample of CSV data file:

```
Time,Price
0,1.1010
1,1.1015
2,1.1008
3,1.1012
```

-----------------------

### UNIT TEST

Run the unitests by running the following command in the root directory of the project

```
python3 -m unittest --verbose
```

#### OR

##### Run the unit tests with coverage[^coverage]
```
coverage run --branch --module unittest --verbose
coverage report --show-missing --omit=test/*
coverage html # (Then view htmlcov/index.html in the browser)
```

-----------------------

### CONTRIBUTE

Follow these steps to make contribution easier:
- Install and **activate** Python virtual environment[^venv]
- Install *pip* packages required by this project [^requirements]
- Activate the *pre-commit* hooks[^pre-commit]

-----------------------


### TODO

Read the accompanied todo.txt for pending items and wishlist of improvements


[^coverage]: Install *coverage* like with the following command if it is already not (preferably in a Python virtual environment):

    ```pip install coverage```

[^venv]: Follow these instructions to install virtual environment: https://docs.python.org/3/library/venv.html

[^requirements]: Run the following command to install required *pip* packages:

    ```pip install --requirement requirements.txt```

[^pre-commit]: Run the following command to activate *pre-commit* hooks:

    ```pre-commit install```

    Read more about *pre-commit* here: https://pre-commit.com/
