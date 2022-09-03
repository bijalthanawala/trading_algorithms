This is a simple exercise aimed at learning and practicing programming.

DESCRIPTION:
This simple project determines time to buy and sell a single stock.
Rules:
- Only one unit of stock is bought at a time, is held between a minimum (30 minutes) and a maximum (60 minutes) period before selling
- Buy and sell operations does not overlap

-----------------------

USAGE:
python3 main.py --help
usage: main.py [-h] [--file FILE] [--algorithm {least,quick,most,new}] [--verbose]

Trading Algorithm

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Name of the input CSV file (Default=test/market_conditions_100.csv)
  --algorithm {least,quick,most,new}, -a {least,quick,most,new}
                        Algorithm short name (Default=least)
                        {'least': 'algorithm_least_purchases',
                         'most': 'algorithm_most_purchases',
                         'new': 'algorithm_new_unimplemented',
                         'quick': 'algorithm_quick_purchases'}
  --verbose, -v
-----------------------

Sample of CSV data file:
Time,Price
0,1.1010
1,1.1015
2,1.1008
3,1.1012

-----------------------

UNIT TEST:

Run the unitests by running the following command in the root directory of the project

python3 -m unittest

OR

coverage run -m unittest
coverage report -m
coverage html # (Then view htmlcov/index.html in the browser)
-----------------------



Read the accompanied todo.txt for pending items and wishlist of improvements
