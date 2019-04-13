Nakul Verma's advice

1- Be careful of adding dependant features! So I can't add Total Magnetic Field if I am placing Magnetic Field in (x, y, z)

Work Flow: 
* Please Note. Test/Train set will be in completely seperate CSVs. This is because I have both time and spatial
data. Therefore say I have scans for Monday, Tuesday, Wenesday, Thursday, Friday. I can pick Tuesday, Thursday, Friday as Training set
and have the other days be my test set. *

1- Read all CSV data (in my case only training data)
While(true)
{
1- Split into Train/Test (NOT APPLICABLE HERE)
2- Split Training set into Training and CV set (ALREADY DONE IN GRIDSEARCH/RANDOMSEARCH)
3- Tune all Classifiers (ALREADY DONE IN GRIDSEARCH/RANDOMSEARCH, This uses the CV set)!
*TUNE ONE PARAMETER AT A TIME. NOTICE TEST ERROR DROP WITH ONE PARAMETER. YOU SHOULD GET A PARABOLA. GET THE BEST PARAMETER*.
It is ENTIRELY possible the default might be too big/small. If you see an obvious gradient down, KEEP GOING!  
4- Fit(train_x, train_y). Get Training and Test Error
PLOT TRAIN AND TEST ERROR
}

OTHER:
1- Tuning parameters and values (Defaults put in scripts).
2- Minimum number of labels. At least 10 for 10-fold CV. Be sure to add slack so say 15? More is better
3- Plots: Best to plot train vs. test error.


Final Step:
With your three best classifiers. Input them in combined classifier. Repeat the train/test...

To be asked later:
1- Ask Professor Verma on incremental learning. 
A- Tuning Parameters
B- Triple Classifier system? Picking best classifier in crowd source environment?
C- Semi-supervised learning or clustering?

Usaage:
python3 main_driver <training-set> <test-set>

This is assuming that both files are CSV files. It also assumes that features and classes are all floating point values!
When complete view Results.txt for scoring. This will generate the CV-plots to assist with parameter tuning and Confusion Matrices to assist with scoring.
