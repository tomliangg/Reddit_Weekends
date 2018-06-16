# Reddit_Weekends-CMPT353_e5
<h3>This repo is created for documentation purpose. The repo contains my personal work toward the SFU CMPT353 (Computational Data Science) course. You may use my solution as a reference. The .zip archive contains the original exercise files. For practice purpose, you can download the .zip archive and start working from there.</h3>

<p><a href="https://coursys.sfu.ca/2018su-cmpt-353-d1/pages/AcademicHonesty">Academic Honesty</a>: it's important, as always.</p>
<br/>
<p> The task of this exercise is to use inferential stats (T-test, p-value, variance teset, normal test, etc.) to analyze the Reddit comment counts data. We will find out whether there are different number of Reddit comments posted weekdays than on weekends.</p>
<br/>
<p>Below is the exercise description </p>
<hr>

<div class="wikicontents creole tex2jax_process"><p>Due <span title="2018-06-15T23:59:59-07:00">Friday June 15 2018</span>.</p>
<p>Some files are provided that you need below: <a href="E5.zip">E5.zip</a>. <strong>You may not write any loops</strong> in your code.</p>
<h2 id="h-summary-statistics-and-data">Summary Statistics and Data Exploration</h2>
<p>In this question, you will produce some summary statistics for various data sets. Submit a Jupyter Notebook <code>summary.ipynb</code> with whatever code you used to produce the values. There is no specific requirement for the format (and if writing loops here makes you happy, then go ahead).</p>
<p>Each of the <code>data-*.csv</code> data sets provided contains \((x,y)\) data points. Create a file <code>summary.txt</code> and for each data set, give:</p>
<ul><li>The mean, standard deviation, and range (min and max) of both the \(x\) and \(y\) variables.
</li><li>The correlation coefficient (\(r\)) between the  \(x\) and \(y\) variables.
</li><li>A one sentence description of what's in the data set: describe the data set to someone and say what you think someone needs to know about it.
</li></ul>
<p>Your code does <strong>not</strong> have to produce the <code>summary.txt</code> file. We only want to see the code you used to produce the values.</p>
<h2 id="h-reddit-weekends">Reddit Weekends</h2>
<p>This question uses data derived from the <a href="http://files.pushshift.io/reddit/">Reddit Comment archive</a>, which is a collection of every Reddit comment, distributed as 150<span>&nbsp;</span>GB of compressed JSON.</p>
<p>I have done some aggregation on that so you don't have to: the provided file <code>reddit-counts.json.gz</code> contains a count of the number of comments posted daily in each Canadian-province subreddit, and in /r/canada itself. (The values will differ slightly from The Truth: I haven't done the timezones correctly, so there will be some comments categorized incorrectly around midnight: I'm willing to live with that.) Again, the format is gzipped line-by-line JSON. It turns out Pandas (<span>&ge;</span>0.21) can handle the compression automatically and we don't need to explicitly use <code>gzip</code>:</p>
<pre class="highlight lang-py">counts = pd.read_json(sys.argv[1], lines=True)</pre>
<p>The question at hand: <strong>are there a different number of Reddit comments posted on weekdays than on weekends?</strong></p>
<p>For this question, we will <strong>look only at values</strong> (1) in 2012 and 2013, and (2) in the /r/canada subreddit. Start by creating a DataFrame with the provided data, and separate the weekdays from the weekends. Hint: check for <a href="%2BPTYHON_DOCS%2Blibrary/datetime.html%23datetime.date.weekday"><code>datetime.date.weekday</code></a> either 5 or 6.</p>
<p>Create a program <code>reddit_weekends.py</code> for this question. Output is described below. Take the input data file on the command line:</p>
<pre class="highlight lang-bash">python3 reddit_weekends.py reddit-counts.json.gz</pre>
<h3 id="h-student-s-t-test">Student's T-Test</h3>
<p>Use <a href="https://docs.scipy.org/doc/scipy/reference/stats.html"><code>scipy.stats</code></a> to do a T-test on the data to get a \(p\)-value. Can you conclude that there are a different number of comments on weekdays compared to weekends?</p>
<p>Try <code>stats.normaltest</code> to see if the data is normally-distributed, and <code>stats.levene</code> to see if the two data sets have equal variances. Now do you think you can draw a conclusion? (Hint: no. Just to check that we're on the same page: I see a <span>&ldquo;</span>0.0438<span>&rdquo;</span> here.)</p>
<h3 id="h-fix-1-transforming-data-might-save-us">Fix 1: transforming data might save us.</h3>
<p>Have a look at a histogram of the data. You will notice that it's skewed: that's the reason it wasn't normally-distributed in the last part.</p>
<p>Transform the counts so the data doesn't fail the normality test. Likely options for transforms: <code>np.log</code>, <code>np.exp</code>, <code>np.sqrt</code>, <code>counts**2</code>. Pick the one of these that comes closest to normal distributions.</p>
<p>[Unless I missed something, none of them will pass the normality test. The best I can get: one variable with normality problems, one okay; no equal-variance problems.]</p>
<h3 id="h-fix-2-the-central-limit-theorem-might">Fix 2: the Central Limit Theorem might save us.</h3>
<p>The central limit theorem says that if our numbers are large enough, and we look at sample means, then the result should be normal. Let's try that: we will combine all weekdays and weekend days <strong>from each year/week</strong> pair and take the mean of their (non-transformed) counts.</p>
<p>Hints: you can get a <span>&ldquo;</span>year<span>&rdquo;</span> and <span>&ldquo;</span>week number<span>&rdquo;</span> from the first two values returned by
<a href="https://docs.python.org/3//library/datetime.html#datetime.date.isocalendar"><code>date.isocalendar()</code></a>. This year <strong>and</strong> week number will give you an identifier for the week. Use Pandas to group by that value, and aggregate taking the mean. Note: the year returned by <code>isocalendar</code> <strong>isn't always the same</strong> as the date's year (around the new year). Use the year from <code>isocalendar</code>, which is correct for this.</p>
<p>Check these values for normality and equal variance. Apply a T-test if it makes sense to do so. (Hint: yay!)</p>
<p>We should note that we're subtly changing the question here. It's now something like <span>&ldquo;</span>do the number of comments on weekends and weekdays for each week differ?<span>&rdquo;</span></p>
<h3 id="h-fix-3-a-non-parametric-test-might-save">Fix 3: a non-parametric test might save us.</h3>
<p>The other option we have in our toolkit: a statistical test that doesn't care about the shape of its input as much. The <a href="https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test">Mann–Whitney U-test</a> does not assume normally-distributed values, or equal variance.</p>
<p>Perform a U-test on the (original non-transformed, non-aggregated) counts.</p>
<p>Again, note that we're subtly changing the question again. If we reach a conclusion because of a U test, it's something like <span>&ldquo;</span>it's not equally-likely that the larger number of comments occur on weekends vs weekdays.<span>&rdquo;</span></p>
<h3 id="h-output">Output</h3>
<p>The provided <code>reddit_weekends_hint.py</code> provides a template for the output that will produce a consistent result that we can check easily. Output all of the relevant (and one irrelevant) p-values from the tests you did on the data in the format provided.</p>
<h2 id="h-questions">Questions</h2>
<p>Answer these questions in a file <code>answers.txt</code>.</p>
<ol><li>Which of the four transforms suggested got you the closest to satisfying the assumptions of a T-test?
</li><li>I gave imprecise English translations of what the by-week test, and the Mann-Whitney test were actually testing. Do the same for the original T-test, and for the transformed data T-test. That is, describe what the conclusion would be if you could reject the null hypothesis in those tests.
</li><li>Of the four approaches, which do you think actually does a better job of getting an answer for the original question: <span>&ldquo;</span>are there a different number of Reddit comments posted on weekdays than on weekends?<span>&rdquo;</span> Briefly explain why. (It's not clear to me that there is a single correct answer to this question.)
</li><li>When are more Reddit comments posted in /r/canada, on average weekdays or weekends?
</li></ol>
