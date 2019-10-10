# Trend_search_calculation
This Python script reads your CSV file with keywords and checks their Google Trends indexes in batches of five.


# Calculate Search Interest with Pytrends API and Python

Pytrends - unofficial API for Google Trends - and trend analysis formula are going to be the topic of this post. First time I heard about the way of calculating search interest using Pytrends and slope formula was when I read Paul Shapiro’s post on the same topic. I tried to use the script from his post, but with no success. The reason for this I guess is because there were changes on Google’s backend after the script was published.

As Pytrends is not an official or supported API, every time it happens, your script needs to be adjusted. I saw it as an opportunity for learning Python, and decided to come up with my version of this script which you can find in my Github repository. Before I go into details, let’s recap on what Google Trends does actually mean, and how it is calculated.

# What does Google Trends Index mean and how it is calculated?

The most comprehensive explanations on the topic I found in “A Hands-on Guide to Google Data” written by Seth Stephens-Davidowitz during his time at Google. (His TED talk is worth watching btw.) Below you will find the most important points from the guide that you need to know when querying the Pytrends API and working with the retrieved data:

* Google Trends data is a sample of Google search data. Only a percentage of searches are used to compile Trends data. Furthermore, due to privacy considerations, only queries with a meaningful volume are tracked.
Google Trends provides a time series index of the volume of queries users enter into Google in a given geographic area. Google Trends reports an index of search activity. Google Trends uses a fraction of searches for a specific term (“keyword” or “search term”), and then analyses the Google search outcome according to a given geographical location and a defined timeframe. A relative search volume (RSV, or Google Trends Index) is then assigned to the keyword, standardizing it from 0 to 100, where 100 represents the highest share of the term over a time series.

* The maximum value of the index is set to be 100. For example, if one data point is 50 and another data point is 100, this means that the number of searches satisfying the condition was half as large for the first data point as for the second data point. The scaling is done separately for each request, but you can compare up to 5 items per request. A score of 0 means that there was not enough data for this term.

* Google classifies search queries into about 30 categories at the top level and about 250 categories at the second level using a natural language classification engine.

* If you choose a time period that is 3 months or shorter you get daily data, otherwise you get weekly data.
If the time period is 3 years or longer, the monthly data is plotted, otherwise it is weekly data.
Categories are helpful when there is ambiguity in the search term.

* If Google Trends shows that a search term has decreased through time, this does not necessarily mean that there are fewer searches now than there were previously! It means that there are fewer searches, as a percent of all searches, then there were previously.
Google Trends has an unreported privacy threshold. If total searches are below that threshold, a 0 will be reported. This means that not enough were made to advance past the threshold. The privacy threshold is based on absolute numbers. Thus, smaller places will more frequently show zeros, as will earlier time periods. If you run into zeros, it may be helpful to use a coarser time period or geography.
Google Trends data is averaged to the nearest integer. If this is a concern, a researcher can pull multiple samples and average them to get a more precise estimate. If you compare two queries, one of which is very popular and the other much less so, the normalization can push the unpopular query to zero. The way to deal with this is to run a separate request for each query. The normalized magnitude of the queries will no longer be comparable, but the growth rate comparison will still be meaningful.

* Google Trends data is cached each day. Even though it comes from a sample, the same request made on the same day will report data from the same sample. A researcher who wants to average multiple samples must wait a day to get a new sample.
* It is worth emphasizing that the sampling generally gives reasonably precise estimates.
Searches made by very few people: Trends only shows data for popular terms, so search terms with low volume appear as "0".
Duplicate searches: Trends eliminates repeated searches from the same person over a short period of time. (Seth mentiones it at one of the “Talks at Google” talks too.)

* Special characters: Trends filters out queries with apostrophes and other special characters.

# Google Trends uses the following conventions to refine searches:
* + means “or.” If you type Lakers+Celtics, the results will be searches 149 that include either the word Lakers or the word Celtics.
* - means to exclude a word. If you type jobs - steve, results will be searches that include jobs but do not include steve.
* A space means “and”. If you type Lakers Celtics, the results will be searches that include both the word Lakers and the word Celtics. The order does not matter.
* Quotes force a phrase match. If you type ‘‘Lakers Celtics’’, results will be searches that include the exact phrase Lakers Celtics.

# What does the Python script actually do?

* It reads your CSV file with all your keywords you would want to check the slope for.
* It then split your keywords list into chunks of five keywords as you cannot check more than five at a time.
* Checks the indexes for the terms in the past five years for the UK region.
* It calculates the last and the previous years, and calculates the slope using indexes found for these years.
* You will end up with a CSV file that will contain your original keyword list in the column A and their slope values in the column next to it.

Based on the information from the “Guide to Google Data”, I compiled a list of keywords with relatively high search volumes and also sorted them descendingly so that the search volumes in each of the group with five keywords are not spread too widely from each other.

How can we use the calculated search interest in your next keyword research?
It’s great to have a way of calculating search interest over time using Pytrens, but the calculated values would be more powerful if we can use them in combination with other metrics such as search volume and keyword difficulty. My next step here would be to add these metrics to the keywords in question together with the calculated search interest, and visualise all data in a meaningful way in Data Studio.
