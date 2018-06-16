# python reddit_weekends.py reddit-counts.json.gz

import sys
import pandas as pd
import difflib
import numpy as np
import gzip
import matplotlib.pyplot as plt
from scipy import stats

counts = pd.read_json(sys.argv[1], lines=True)
"""
format like (date field is timestamp):
 comment_count       date           subreddit
0                  7 2012-02-20        newfoundland
1                  1 2015-01-26            Manitoba
2                  2 2013-09-07               Yukon
...
15468              2 2011-09-10              Quebec
15469           1127 2012-01-02              canada
"""

# extract the canada subreddit
counts = counts[counts['subreddit']=='canada']

def get_year(dateObj):
    return dateObj.year

def get_weekday(dateObj):
    # 0 - Monday, 6 - Sunday
    return dateObj.weekday()

# extract 2012 and 2013 data only 
counts['year'] = counts['date'].apply(get_year)
counts = counts[(counts['year']==2012) | (counts['year']==2013)]
counts['day'] = counts['date'].apply(get_weekday) 

# separate weekdays and weekends 
counts_weekend = counts[(counts['day']==5) | (counts['day']==6)]
counts_weekday = counts[(counts['day']!=5) & (counts['day']!=6)]

initial_ttest_p = stats.ttest_ind(counts_weekend['comment_count'], counts_weekday['comment_count']).pvalue
# T-test pvalue is super small ~0, but if we want to conclude
# that weekdays and weekends comment counts are different, 
# we need to make sure the data are normally distrbuted and with equal variance

initial_weekend_normality_p = stats.normaltest(counts_weekend['comment_count']).pvalue
initial_weekday_normality_p = stats.normaltest(counts_weekday['comment_count']).pvalue
# both normaltest pvalue are below 0.05, so we conclude that they aren't normally distributed

initial_levene_p = stats.levene(counts_weekend['comment_count'], counts_weekday['comment_count']).pvalue
# pvalue is 0.04 which is below 0.05 so we conclude they have different variance
# thus, the T-test above is not meaningful

# Fix1: transform the data - use np.log
transformed_weekend_normality_p = stats.normaltest(np.log(counts_weekend['comment_count'])).pvalue
transformed_weekday_normality_p = stats.normaltest(np.log(counts_weekday['comment_count'])).pvalue
transformed_levene_p = stats.levene(np.log(counts_weekend['comment_count']), np.log(counts_weekday['comment_count'])).pvalue
# Fix1 apparently can't save us here


# Fix2: central limit theorem
def get_year_week(dateObj):
    return dateObj.isocalendar()[:2] # only get the year and week so I slice it

counts_weekday['year/week'] = counts_weekday['date'].apply(get_year_week)
counts_weekend['year/week'] = counts_weekend['date'].apply(get_year_week)

# below 2 are pandas Series objects
comments_weekday = counts_weekday.groupby(['year/week'])['comment_count'].mean() 
comments_weekend = counts_weekend.groupby(['year/week'])['comment_count'].mean()

# check the pvalue, both are well above 0.05, so now they are normally distributed
weekly_weekday_normality_p = stats.normaltest(comments_weekday).pvalue
weekly_weekend_normality_p = stats.normaltest(comments_weekend).pvalue

# Levene's test pvalue is 0.204 > 0.05, so now they have equal variance 
weekly_levene_p = stats.levene(comments_weekday, comments_weekend).pvalue

# These 2 data have equal variance and normal distribution, let's do a T-test
weekly_ttest_p = stats.ttest_ind(comments_weekday, comments_weekend).pvalue
# the pvalue is near 0, so we conclude that the # of comments on weekends and weekdays are different


# Fix 3: a non-parametric test on the (original non-transformed, non-aggregated) counts
utest_p = stats.mannwhitneyu(counts_weekday['comment_count'], counts_weekend['comment_count']).pvalue
# the pvalue is near 0, so it's not equally-likely that the larger number of comments occur on weekends vs weekdays

# Let's output the results in an organised way
OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)

print(OUTPUT_TEMPLATE.format(
    initial_ttest_p=initial_ttest_p,
    initial_weekday_normality_p=initial_weekday_normality_p,
    initial_weekend_normality_p=initial_weekend_normality_p,
    initial_levene_p=initial_levene_p,
    transformed_weekday_normality_p=transformed_weekday_normality_p,
    transformed_weekend_normality_p=transformed_weekend_normality_p,
    transformed_levene_p=transformed_levene_p,
    weekly_weekday_normality_p=weekly_weekday_normality_p,
    weekly_weekend_normality_p=weekly_weekend_normality_p,
    weekly_levene_p=weekly_levene_p,
    weekly_ttest_p=weekly_ttest_p,
    utest_p=utest_p,
))


# Let's do a plot to help us find out whether weekends or weekdays got more Reddit comments counts
comments_weekday.plot()
comments_weekend.plot()
plt.legend(['weekday counts', 'weekend counts'])
plt.xlabel('Time')
plt.ylabel('Reddit Comment Counts')
plt.show()
# Apparently weekdays got more comments