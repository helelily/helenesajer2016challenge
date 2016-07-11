This solution includes two main files written in python, and two tests added in addition to the test provided from Insight.

This solution is dependent on several python modules, which are listed below:
* argparse - handles arguments passed to the program from the command line
* json - parses json outputs from venmo transaction feed
* datetime - handles time stamp from json output and rolling window calculation
* statistics - handles median calculation
* networkx - generates network graph, handles degree calculation for each user
* matplotlib.pyplot - handles plotting of network graph

matplotlib itself also has several dependencies listed on their site http://matplotlib.org/users/installing.html (numpy, setuptools, dateutil, pyparsing, libpng, pytz, freetype, cycler) that are not directly imported in the solution but are required for the solution to run.

These imports are referenced in the two python files, main.py and tranprocfunctions.py.

tranprocfunctions.py contains the core functionality for processing the venmo transactions, handling errors within the data output, and calculating network statistics.
main.py is the main body of the program, and iterates through the feed of venmo transactions.  It is wrapped in a larger try block to handle any IO errors that may arise with the file directories.

There is one variable to note called PAUSE_TIME_FOR_PLOT_VIEW in line 4 of main.py.  The program will plot the network graphs over a rolling window interactively, there will not be any manual intervention as it shifts through each transaction.  Currently, this program opens and closes the graphs without "pausing" to allow the viewer to see each network graph.  If the viewer would like, they may change the pause input depending on how long they would like to view each network.  For example, if you set the variable equal to 1.0, each figure will be displayed for one second.

There are two separate test cases, one in test-2-venmo-trans, and the other in test-3-venmo-trans.  Test-2 is meant to ensure that the program runs as expected and covers all aspects of the solution, including updating the rolling time window, outputing the median, and updating the plot.  Test-3 is identical to Test-2, except that it also contains bad data in the input file.  Test-3 is designed to ensure that different possible data errors are handled appropriately.