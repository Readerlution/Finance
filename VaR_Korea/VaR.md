**Value-at-Risk Testing**

1. **Introduction**

This experiment’s purpose is to create an artificial portfolio of stocks and assessing risk through use of Value at Risk (VaR) concept. The VaR is to be estimated by historical simulation approach (HSA). The HSA includes basic approach, age-weighted approach, volatility updating approach, and volatility updating + age-weighted approach (combined approach).



1. **Constructing Portfolio**

In this experiment, 10 stocks from the Korean stock markets (KOSPI and KOSDAQ) were selected. For demonstration purposes, initial investment was set to 10 billion won in total. First, the 10 stocks were selected with a focus on battery supplier industry, as they were hotly debated in the media during recent years. The following table lists the 10 stocks selected.

|**Count**|**종목명**|**종목코드**|**Listing**|
| :-: | :-: | :-: | :-: |
|1|POSCO홀딩스|005490|코스피|
|2|나노신소재|121600|코스닥|
|3|LG화학|051910|코스피|
|4|에코프로비엠|247540|코스닥|
|5|천보|278280|코스닥|
|6|삼성SDI|006400|코스피|
|7|코스모화학|005420|코스피|
|8|엠플러스|259630|코스닥|
|9|에이에프더블류|312610|코스닥|
|10|후성|093370|코스피|

Second, adjusted close data for each of the stocks were downloaded through yahoo finance using python packages, such as yfinance, pandas, and pandas-data-reader. Data captures approximately 3 years’ worth, starting from June 1, 2020 to May 31, 2023.

Next, percent changes from each date’s adjusted closing prices (daily returns) were calculated. This gave us 740 data points, for each stock, to work with. Among these data points, first 239 days were used for calculating the Sharpe ratio. For demonstration purposes, risk free rate was assumed to be 2%. The results were as follows.

Sharpe=MeanReturnStock-RiskFreeRateσStock


|**종목명**|**Sharpe Ratio**|
| :-: | :-: |
|POSCO홀딩스|2\.286|
|나노신소재|1\.095|
|LG화학|1\.885|
|에코프로비엠|1\.008|
|천보|1\.314|
|삼성SDI|1\.518|
|코스모화학|0\.654|
|엠플러스|0\.685|
|에이에프더블류|0\.759|
|후성|0\.624|
|**Total**|11\.829|

While it is certainly viable to construct a maximum Sharpe portfolio using optimization techniques, this experiment focused on allocating decent amount of capital to every stock selected. Instead, the formula used to allocate the investments were simply summing all the Sharpe ratios calculated and distribute by each of the stock’s share of the total.

Allocationstock i=Sharpestock ii=1NSharpestock i


|**종목명**|**Allocation (in KRW)**|
| :-: | :-: |
|POSCO홀딩스|1,932,630,764|
|나노신소재|926,081,695|
|LG화학|1,593,867,829|
|에코프로비엠|852,658,936|
|천보|1,110,601,742|
|삼성SDI|1,283,171,838|
|코스모화학|553,192,204|
|엠플러스|578,727,227|
|에이에프더블류|641,661,845|
|후성|527,405,920|
|**Total**|**10,000,000,000**|

1. **HSA VaR Basic Approach**

Last 500 days’ daily returns from our data were used to estimate Value-at-Risk measures. The first method is the basic HAS approach. In this approach, for each date, the portfolio allocation is matched for each stock’s daily return. The portfolio return for each date is therefore,

` `Portfolio returnt=t=1N Ri, t× Allocationi

where subscript t = date and i = specific stock. The portfolio returns are easily calculated in vectorized form by using python pandas package’s dot multiplication with daily returns data frame and allocation data series.

`		`Once the portfolio returns are calculated, basic VaR can be calculated by ranking each return in percentile form. The 1-day basic VaR with 95% confidence is 311, 639,862 won and 1-day basic VaR with 99% confidence is 489,127,583 won in our case. These values represent biggest loss the portfolio may experience in one day, x% of the time, based on historical data.

1. **Age-Weighted Approach**

The age-weighted approach for calculating VaR under HSA, involves giving weight parameter for each of the portfolio returns calculated above by measuring distance from the most recent date to each of the data points. Formula can be seen below.				

weighti=λn-i1-λ1-λn

Where, n = number of days and λ adjusts weight given to past day i. Higher the λ, bigger weight is given to day i and λ < 1 with Σ weight<sub>i</sub> = 1. 

`	`This experiment used λ = .995 as the parameter for weight calculation. Once the weights are calculated for each date, the data can be sorted by portfolio dollar[^1] returns (losses) in ascending order. From the sorted data, 1-day VaR is estimated by cumulatively adding the weight on a rolling basis until the desired confidence level is reached or exceeded the first time. This data point represents the VaR based on historical data with age-weighted scheme. Our portfolio returned 1-day weighted VaR of 313,829,605 won and 524, 180, 519 won at 95% confidence level and 99% confidence level respectively.

1. **Volatility Updating Approach**

HSA of VaR can also consider volatility changes in several ways. From these methods, the GARCH(1,1) model was chosen to measure each day’s volatility estimate. 

σn2=γVL+αμn-12+Βσn-12

σn2=ω+αμn-12+Βσn-12

Where γ+α+Β=1 and α+Β<1. The ω, α, and Β were estimated by utilizing maximum likelihood method (MLE) for optimization.

i=1N[-lnvi-μi2vi]
**
`	`Where N denotes the length of the return series.

The arch package in python was used for the above mentioned optimization of GARCH(1,1) parameters and calculating conditional variances given the parameters for each stock on all available dates, as well as to make 1 day forecast of the volatility after the most recent date.

The conditional volatilities calculated then needs to be scaled by the most recent volatility to use the i th volatility as a scenario for what could happen between today and tomorrow. This provides us the following formula.

Value under ith Scenario=Vn×Vi-1×Vi-Vi-1σn+1σiVi-1

In our experiment, the scaling was done by dividing the most recent volatility by each day’s conditional volatility (scaling factor), then multiplying the actual returns for each day to the scaling factor. 

`	`The volatility adjusted returns are calculated from the above process and by repeating the same procedures to these returns, as we did in the basic approach (i.e., dot multiplication of investment allocations), we can calculate the returns (losses) of the portfolio under volatility updating scheme.

`	`The results of VaR are drawn in the same manner as the basic approach as well. In our portfolio, 1-day volatility updated VaRs were 284,982,679 won and 457,963,652 won for 95% confidence level and 99% confidence level respectively.

1. **Volatility Updating & Age-Weighted (Combined) Approach**

The last method is exactly the same as the age-weighted approach from section 4. The weights are calculated given the weight<sub>i</sub> formula mentioned with the same λ value (0.995). However, the returns (losses) are drawn and sorted from the volatility adjusted returns instead of plain daily returns. The 1-day Combined Approach VaR at 95% confidence level was 275,703,617 won and 1-day Combined Approach VaR at 99% confidence level was 457,963,652 won.

1. **Summary Table**

**\***Denominated in KRW

|**Method**|**95% Confidence**|**99% Confidence**|
| :-: | :-: | :-: |
|Basic|311,640,082|489,127,701|
|Weighted|313,829,599|524,180,381|
|Vol-Adj|284,632,483|457,018,807|
|Combined|275,986,973|457,018,807|

(Table Summarizes VaR estimated given each approach at 95% and 99% confidence level)

1. **Bootstrap Simulation**

Last part of this exercise is to test the bootstrap simulation at the 95% confidence interval for each of the VaR calculated. Bootstrap samples were collected 10,000 times, which provides us with 500 x 10,000 = 5,000,000 data points. The samples are randomly drawn from the original data set of daily dollar returns and volatility adjusted daily dollar returns for the portfolio. Each sample can have repeating dates but will contain 500 days regardless. Every time the random samples are drawn, VaR will be estimated repeatedly in the same way it was estimated for each approach used. This means for each of the VaR originally calculated, there will be 10,000 samples of VaR data stored for our purposes. From these 10,000 VaR data set, we simply find the lower and upper boundary levels by ranking them.

The confidence interval for lower boundary is 2.75% level and upper boundary will be 97.5% in the case of 95% confidence interval. The following table summarizes the results.


|**Method**|**95% VaR Lower**|**95% VaR Upper**|**99% VaR Lower**|**99% VaR Upper**|
| :-: | :-: | :-: | :-: | :-: |
|Basic|268,182,912|347,027,606|376,407,365|586,010,562|
|Weighted|268,182,912|348,080,212|365,550,947|571,178,222|
|Vol-Adj|244,058,724|330,863,830|351,426,445|503,305,940|
|Combined|237,598,494|330,863,830|341,319,857|469,913,799|

`	`By comparing the original VaR table to the bootstrapped confidence levels we can see that each VaR falls within the 95% interval. For example, basic actual 1-day 95% VaR is between the bootstrapped basic interval boundaries.

|**Method**|**95% VaR Lower**|**≤**|**95% VaR Actual**|**≤**|**95% VaR Upper**|
| :-: | :-: | :-: | :-: | :-: | :-: |
|Basic|268,182,912|　|311,640,082|　|347,027,606|
|Weighted|268,182,912|　|313,829,599|　|348,080,212|
|Vol-Adj|244,058,724|　|284,632,483|　|330,863,830|
|Combined|237,598,494|　|275,986,973|　|330,863,830|

1-day VaR 95% confidence level comparison

|**Method**|**99% VaR Lower**|**≤**|**99% VaR Actual**|**≤**|**99% VaR Upper**|
| :-: | :-: | :-: | :-: | :-: | :-: |
|Basic|376,407,365|　|489,127,701|　|586,010,562|
|Weighted|365,550,947|　|524,180,381|　|571,178,222|
|Vol-Adj|351,426,445|　|457,018,807|　|503,305,940|
|Combined|341,319,857|　|457,018,807|　|469,913,799|

1-day day VaR 99% confidence level comparison





[^1]: While I referred it as “dollar” returns, the actual denominations were in Korean Won (KRW) for the entirety of this paper.