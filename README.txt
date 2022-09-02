This is a simple exercise aimed at learning and practicing programming.

DESCRIPTION:
This simple project determines time to buy and sell a single stock.
Rules:
- Only one unit of stock is bought at a time, is held between a minimum (30 minutes) and a maximum (60 minutes) period before selling
- Buy and sell operations does not overlap

-----------------------

USAGE:
python3 main.py --help
usage: main.py [-h] [--file FILE] [--algorithm {1,2,3,4}] [--verbose]

Trading Algorithm

options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Name of the input CSV file (Default=data_10.csv)
  --algorithm {1,2,3,4}, -a {1,2,3,4}
                        Specify one of the algorithm numbers (Default=1)
                        {1: 'algorithm_least_purchases',
                         2: 'algorithm_quick_purchases',
                         3: 'algorithm_most_purchases',
                         4: 'algorithm_new_unimplemented'}
  --verbose, -v

-----------------------

Sample of CSV data file:
Time,Price
0,1.1010
1,1.1015
2,1.1008
3,1.1012

-----------------------


Read the accompanied todo.txt for pending items and wishlist of improvements
