<!--
Web version of Lecture 4 (EN). Built into web/L4.html by lectures/common/build_web_lecture.py (format: see its docstring).
Frame hashes: python3 build_web_lecture.py 4 --frames
-->

## @intro

An energy company that buys or sells power every day does not lose money because prices are high; it loses money because tomorrow's price differs from the price it budgeted today. A supplier that buys 100 megawatts (MW) flat on the Romanian day-ahead market, Piața pentru Ziua Următoare (PZU), loses 2,400 euro (EUR) for every EUR per megawatt-hour (EUR/MWh) that the price rises above its budget. This lecture asks how large that loss can be on a bad day, how often a bad day comes, and how a company should turn the answer into limits, cash buffers and bank guarantees.

The two standard answers are value-at-risk (VaR), a high quantile of tomorrow's loss, and expected shortfall (ES), the average loss beyond that quantile. Lecture 1 promised to show why the normal curve understates crisis days; here we do it on real prices. We estimate VaR and ES in four ways on Romanian day-ahead prices from 1 Jan 2015 to 31 Oct 2026, check every method day by day over almost ten years (backtesting), and then follow the same quantiles into exchange margins, the day-ahead guarantee required by the market operator and position limits in MW.

The data are real and downloaded: the day-ahead base prices of Romania and of the Germany–Luxembourg zone, the Romanian load, the Brent crude oil futures and the Dutch gas price. The lecture ends with a case study of the price rise of autumn 2026, in which the danger turned out to be cash, not the daily VaR.

@goals
- **Measure** the price risk of an energy position with VaR and ES, defined as quantiles of the loss distribution, and explain why the normal curve understates crisis days.
- **Estimate** VaR and ES in four ways on Romanian prices: historical simulation, normal and Student-t curves, filtered historical simulation and extreme value theory.
- **Check** a risk model after the fact with the Kupiec and Christoffersen tests, the Basel traffic light and a test for ES.
- **Turn** quantiles into decisions: position limits, exchange margins and the day-ahead guarantee, for a supplier, a producer and a trader.

# Price risk: losses, quantiles, VaR and ES

The risk of an energy position sits in the daily change of the price, and VaR and ES are two ways of summarising the bad tail of that change. This section defines the loss, the two risk measures and shows on Romanian data why a limit built on the normal curve fails.

## Data sources: prices and positions analysed {h=1ca32c42}

The main series is the day-ahead base price of Romania (RO) on the PZU, run by the Romanian electricity and gas market operator (OPCOM), with the price of the Germany–Luxembourg bidding zone (DE-LU) from the EPEX SPOT power exchange (EPEX) for comparison. Both come from the European Network of Transmission System Operators for Electricity (ENTSO-E) through energy-charts.info, the data portal of the Fraunhofer Institute for Solar Energy Systems (ISE), at daily and hourly frequency. The Romanian load, from ENTSO-E (Transelectrica data), gives the hourly shape of a supplier's portfolio. Two further series show how risk turns into cash: the front-month Brent crude oil futures, a margined contract, from Yahoo Finance (BZ=F), and the monthly gas price at the Dutch Title Transfer Facility (TTF), from the World Bank Pink Sheet.

The data run from 1 Jan 2015 to 31 Oct 2026, the last complete month, and were downloaded on 4 Nov 2026. The daily price is the mean of the delivery day in Central European Time (CET). Five missing days of the Romanian price stay missing, and the changes next to them are not computed. The backtest covers every day from 1 Jan 2017 to 31 Oct 2026, 3,587 valid days, and each forecast is made only with data up to the previous day, as a risk desk would have to do.

## Daily price changes before and after 2021 {h=e8618855}

The variable that drives the loss is the change of the daily base price, $X_t=P_t-P_{t-1}$, in EUR/MWh, where $P_t$ is the base price of day $t$. Power prices can be negative, so the lecture works with changes in euro rather than with log returns, which are not defined for a negative price.

The chart shows that the size of these changes is not stable. Until 2021 the daily changes are small; with the energy crisis they become violent, and they stay larger than before afterwards. The largest rise in the sample is 260.77 EUR/MWh, on 11 Jul 2022, and the largest fall is −166.59 EUR/MWh, on 24 Dec 2021. For a position of 100 MW flat, that is 2,400 MWh per day, every EUR/MWh of change moves the result of the day by 2,400 EUR.

@practice a supplier that buys 100 MW flat on the PZU and budgets at yesterday's price loses 2,400 EUR for every EUR/MWh of rise.

@chart price_changes
Daily change of the Romanian day-ahead base price, in EUR/MWh, 2015–2026.

## Value-at-risk is a quantile of tomorrow's loss {h=53e7565e}

VaR is the loss that is exceeded only on a small, chosen share of days, for example one day in a hundred. For a buyer of $Q$ MW flat, the loss of day $t$ and its VaR are

$$ L_t = Q\cdot 24\cdot X_t, \qquad \text{VaR}_{\alpha,t}=\min\{\ell:\ \Pr(L_t\le \ell\mid\mathcal F_{t-1})\ge\alpha\} $$ {#eq:var}

where $L_t$ is the loss in EUR, $Q$ the position in MW (for 100 MW flat, $Q\cdot 24$ = 2,400 MWh per day), $X_t$ the price change in EUR/MWh, $\alpha$ the confidence level, 0.95 or 0.99, and $\mathcal F_{t-1}$ the information available up to day $t-1$, that is the prices known at 12:00 CET, the gate closure of the auction. VaR is therefore the $\alpha$-quantile of the loss, conditional on what is known when the bid is placed.

On the last 365 days of Romanian data, the 99% quantile of $X_t$ is 86.63 EUR/MWh, which gives a VaR$_{0.99}$ of 207,922 EUR for 100 MW; the 95% quantile is 50.39 EUR/MWh. What VaR does not say is how large the loss is on the worst 1% of days. It is a threshold, not an average, and for the size of the bad days we need ES.

@practice the desk reports the 99% VaR every morning, before bidding at 12:00 CET.

## Expected shortfall: the average loss beyond VaR {h=9451eaf6}

ES answers the question: when a bad day comes, how large is the loss on average? It is the mean of the loss beyond VaR, or equivalently the average of all VaRs above the level $\alpha$:

$$ \text{ES}_{\alpha,t}=\E\big[L_t\mid L_t\ge \text{VaR}_{\alpha,t}\big]=\frac{1}{1-\alpha}\int_{\alpha}^{1}\text{VaR}_{u,t}\,du $$ {#eq:es}

where $u$ runs over the confidence levels above $\alpha$. ES is a coherent risk measure (Artzner et al., 1999): in particular it is subadditive,

$$ \text{ES}(L_1+L_2)\le\text{ES}(L_1)+\text{ES}(L_2) $$ {#eq:subadd}

where $L_1$ and $L_2$ are the losses of two positions, so diversification never adds risk. VaR may break this property (Acerbi and Tasche, 2002). This is why the Fundamental Review of the Trading Book (FRTB), the Basel market-risk rules, uses ES at 97.5% instead of VaR at 99% (BCBS, 2019).

On the last 365 days, VaR$_{0.975}$ is 61.96 EUR/MWh and ES$_{0.975}$ is 86.91 EUR/MWh, the mean of the 10 worst days. For 100 MW in Romania and 100 MW in Germany–Luxembourg, the 99% VaRs are 86.63 and 91.76 EUR/MWh separately but 150.77 together: with a correlation of 0.55 between the two price changes, the joint risk is smaller than the sum.

@practice size the cash buffer with ES, not with VaR.

## Large price rises are far more frequent than the normal curve allows {h=45610e07}

If price changes followed a normal curve, extreme days would be extremely rare. They are not. The excess kurtosis of $X_t$ is 12.0 in Romania and 12.1 in Germany–Luxembourg, against 0 for a normal curve: the distribution has a narrow centre and long tails.

The count of large rises makes the point concrete. Rises above 3 standard deviations occurred on 52 days, while the normal curve expects 5.8 over the same sample. The largest rise is 10.1 standard deviations: under normality, such a day would come once in more than $10^{20}$ years. The chart compares the observed distribution of changes with the normal curve fitted to the same mean and standard deviation, for both bidding zones.

@practice a limit built on the normal curve understates how often a crisis day comes (Lecture 1).

@chart tails
Distribution of daily price changes in Romania and Germany–Luxembourg, 2015–2026, against the normal curve with the same mean and standard deviation.

## A normal-curve limit set in 2020 was breached 19 times more often than planned in 2021–2022 {h=4f2a0395}

A static limit assumes that tomorrow's risk looks like the past; in a crisis it does not. Consider the limit a risk manager would have set at the end of 2020 from the normal curve:

$$ \ell_{0.99}=\hat\mu+z_{0.99}\,\hat\sigma, \qquad z_{0.99}=2.326 $$ {#eq:normlim}

where $\hat\mu$ and $\hat\sigma$ are the mean and standard deviation of $X_t$ in 2015–2020 and $z_{0.99}$ is the 99% quantile of the standard normal distribution. A correct limit is exceeded on 1% of days.

Estimated on 2,182 days of 2015–2020, $\hat\sigma$ is 10.21 and the limit is 23.77 EUR/MWh. Already within 2015–2020 it was breached 45 times against 21.8 expected, because of the fat tails. Afterwards the failure became dramatic: 139 breaches in 2021–2022 against 7.3 expected, and 226 in 2023–2026 against 14.0 expected, 16 times more. The limit did not move when volatility moved, so it measured a market that no longer existed.

@practice a limit must move with volatility; the next section shows four ways to make it move.

# Estimating VaR and ES: four methods

There are many ways to estimate a quantile of tomorrow's loss, and on the same day and the same data they give different answers. This section presents historical simulation, the normal and Student-t curves, filtered historical simulation and extreme value theory, then compares them on October 2026 and through the 2021–2022 crisis.

## Historical simulation with a one-year window {h=a3ead1e5}

Historical simulation (HS) assumes no distribution: it sorts the last 365 daily changes and reads the quantile directly; the 4th largest change is the 99% VaR. Formally,

$$ \widehat{\text{VaR}}^{\text{HS}}_{\alpha,t}=\hat q_{\alpha}\big(X_{t-W},\dots,X_{t-1}\big), \qquad \widehat{\text{ES}}^{\text{HS}}_{\alpha,t}=\text{mean of }\{X_s\ge\widehat{\text{VaR}}^{\text{HS}}_{\alpha,t}\} $$ {#eq:hs}

where $W$ = 365 days is the window, $\hat q_\alpha$ the empirical quantile of the changes in the window, and $X_s$ the changes of the window that lie at or above the VaR.

On October 2026, HS gives a VaR$_{0.99}$ of 86.63 and an ES$_{0.975}$ of 87.59 EUR/MWh. Over the backtest 2017–2026 it was exceeded on 2.04% of days, not on 1%. Its weakness is speed: a new regime needs months to fill the window, and a crisis day counts with full weight for 365 days, then drops out at once, so the VaR jumps down on a fixed date that has nothing to do with the market.

@practice HS is the default in many energy companies, and it lags the market.

## Parametric VaR: normal and Student-t distributions {h=f0b6fe6f}

The parametric approach fits a curve to the last year of changes and reads its quantile. The normal curve has two parameters; the Student-t curve adds a third, the degrees of freedom, which makes its tails fatter:

$$ \text{VaR}^{N}_{\alpha}=\mu+\sigma z_\alpha, \qquad \text{ES}^{N}_{\alpha}=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha} $$ {#eq:normal}

$$ \text{VaR}^{t}_{\alpha}=m+s\,t_{\nu,\alpha}, \qquad \text{ES}^{t}_{\alpha}=m+s\,\frac{g_\nu(t_{\nu,\alpha})}{1-\alpha}\cdot\frac{\nu+t_{\nu,\alpha}^2}{\nu-1} $$ {#eq:student}

where $\mu$ and $\sigma$ are the mean and standard deviation, $z_\alpha$ and $\varphi$ the quantile and density of the standard normal distribution, $m$, $s$ and $\nu$ the location, scale and degrees of freedom of the Student-t curve, estimated by maximum likelihood estimation (MLE), and $t_{\nu,\alpha}$ and $g_\nu$ the Student-t quantile and density. The ES formulas are derived in Appendix A.

On October 2026 the normal curve gives VaR$_{0.99}$ 69.64 and ES$_{0.975}$ 69.98 EUR/MWh; the Student-t gives 76.66 and 80.05. In the backtest the normal 99% VaR was exceeded on 3.21% of days and the Student-t on 1.98%, against a target of 1%. The t curve fixes part of the tail but not the centre: at 95% it is too narrow, with 8.75% of days above it.

@practice the normal VaR is the easiest to explain and the most dangerous to trust.

## Filtered historical simulation: past shocks rescaled to current volatility {h=ac347b8e}

Filtered historical simulation (FHS) combines the two previous ideas. It divides past changes by their volatility to obtain standardised shocks, then rescales those shocks by today's volatility, so that the shape of the tail comes from history and the scale from the present (Barone-Adesi, Giannopoulos and Vosper, 1999):

$$ e_t=X_t-\mu_{d(t)}, \quad \sigma_t^2=\omega+a\,e_{t-1}^2+b\,\sigma_{t-1}^2, \quad z_t=e_t/\sigma_t $$ {#eq:fhs-garch}

$$ \text{VaR}^{\text{FHS}}_{\alpha,t}=\mu_{d(t)}+\sigma_t\,\hat q_\alpha(z) $$ {#eq:fhs-var}

where $\mu_{d(t)}$ is the mean change of that weekday (prices fall at weekends), $e_t$ the change net of that mean, $\sigma_t$ the generalised autoregressive conditional heteroskedasticity (GARCH) volatility of Lecture 3 (Bollerslev, 1986) with parameters $\omega$, $a$ and $b$, refitted every 21 days on 730 days, $z_t$ the standardised shock and $\hat q_\alpha(z)$ the empirical quantile of the shocks. ES is $\sigma_t$ times the mean of the shocks $z$ above $\hat q_\alpha(z)$.

On the Romanian data the GARCH(1,1) volatility ranges from 4.06 EUR/MWh (29 Mar 2021) to 100.86 EUR/MWh (12 Jul 2022). In October 2026, the FHS VaR$_{0.99}$ is 67.50 EUR/MWh. In the backtest, the 99% VaR was exceeded on 1.51% of days, and the 95% VaR on 5.58%, with a Kupiec $p$-value of 0.120: the first method so far that passes at 95%.

@practice FHS raises the limit within days of a volatility jump; HS needs months.

## Extreme value theory: model only the tail, with a generalised Pareto curve {h=266e05a9}

Extreme value theory (EVT) models only the tail. Above a high threshold, the excesses of almost any distribution follow the same two-parameter curve, the generalised Pareto distribution (GPD) (Pickands, 1975):

$$ \Pr(Z-u\le y\mid Z>u)\approx 1-\Big(1+\frac{\xi y}{\beta}\Big)^{-1/\xi} $$ {#eq:gpd}

$$ \text{VaR}_\alpha=u+\frac{\beta}{\xi}\Big[\Big(\frac{n}{N_u}(1-\alpha)\Big)^{-\xi}-1\Big], \quad \text{ES}_\alpha=\frac{\text{VaR}_\alpha+\beta-\xi u}{1-\xi} $$ {#eq:evt}

where $Z$ is the standardised shock, $y$ the excess over the threshold, $u$ the threshold, chosen by the peaks-over-threshold (POT) method as the 90% quantile of $z$, $N_u$ the number of the $n$ residuals that exceed it, $\xi$ the shape (tail heaviness) and $\beta$ the scale of the GPD, both estimated by MLE. The result is then multiplied by $\sigma_t$ as in FHS (McNeil and Frey, 2000); the derivation is in Appendix B.

On raw changes, with the threshold at the 95% quantile, $\hat\xi$ = 0.164: a heavy tail, in which moments above order 6.1 do not exist. After the GARCH filter, the median $\hat\xi$ is 0.011: the filter absorbs most of the tail. In the backtest the 99% EVT VaR was exceeded on 1.37% of days, the best of the five methods.

@practice use EVT for the one-in-ten-years day that no window contains.

## Above the threshold the Pareto curve fits the data; the normal curve does not {h=7fccae5f}

The chart shows the tail of the GARCH-filtered changes over the 730 days before 31 Oct 2026 together with the fitted Pareto curve and the normal curve. At the last refit, on 11 Oct 2026, the estimates are $\hat\xi$ = 0.182 and $\hat\beta$ = 0.569. Above the threshold the Pareto curve follows the observed points, while the normal curve falls off far too quickly.

The shape parameter is not stable: $\hat\xi$ was positive in 53% of the refits, so the standardised tail is sometimes heavy and sometimes not (Balkema and de Haan, 1974; McNeil and Frey, 2000). This is one reason to refit the model regularly rather than fix a tail shape once.

@practice a 4-sigma day is rare but not impossible; the normal curve calls it impossible.

@chart gpd_tail
Tail of the GARCH-filtered Romanian price changes over the 730 days before 31 Oct 2026, with the fitted generalised Pareto curve and the normal curve.

## VaR and ES on the same day by five methods {h=78223520}

The table gives the mean of the 31 forecasts made for October 2026. The first three columns are in EUR/MWh; the last two are in thousand EUR for 100 MW flat, 2,400 MWh per day.

| Method | VaR 0.95 | VaR 0.99 | ES 0.975 | VaR 0.99, kEUR | ES 0.975, kEUR |
|---|---|---|---|---|---|
| HS | 50.38 | 86.63 | 87.59 | 208 | 210 |
| Normal | 49.33 | 69.64 | 69.98 | 167 | 168 |
| Student-t | 45.77 | 76.66 | 80.05 | 184 | 192 |
| FHS | 36.22 | 67.50 | 67.44 | 162 | 162 |
| EVT | 35.66 | 64.33 | 68.54 | 154 | 164 |

The same position, on the same day, has a 99% VaR between 154 and 208 thousand EUR depending on the method. The gap is not noise. HS and Student-t still carry the volatile days of the past year in their window, while FHS and EVT use today's volatility, which in October 2026 was below the yearly average. Choosing a method is therefore a risk decision in its own right.

@practice report two methods side by side and explain the gap.

## In the crisis FHS adapted within days; HS and the normal VaR lagged {h=3890e828}

The difference between methods matters most in a crisis. Between 1 Jul 2021 and 30 Jun 2023, 730 days, a correct 99% VaR should have been exceeded 7.3 times. The counts were 28 for HS, 45 for the normal curve, 29 for the Student-t, 19 for FHS and 17 for EVT. No method was right, but the filtered ones, which follow the GARCH volatility, adapted within days, while HS and the normal VaR waited for their windows to fill with crisis days.

@practice in a crisis, a model that reacts within days protects the cash.

@chart var_paths
Daily price changes in Romania and the 99% VaR forecasts of the five methods, 1 Jul 2021 to 30 Jun 2023, with the exceedances marked.

## The square-root-of-time rule overstates the 10-day risk {h=f54b9c24}

Regulators and many companies scale a one-day VaR to ten days by multiplying it by $\sqrt{10}$ = 3.16. The rule assumes that daily changes are independent, like a random walk. Power prices are not: they revert to a level set by fuel costs and the weekly calendar.

Measured directly, the 10-day 99% quantile is 1.72 times the 1-day one in Romania and 1.75 times in Germany–Luxembourg, not 3.16. The variance ratio at 10 days is 0.33, where 1 would mean a random walk. The autocorrelation of $X_t$ is −0.076 at lag 1, a mild reversal, and 0.474 at lag 7, the weekly pattern (Weron, 2014). The chart compares the empirical quantile at each horizon with the square-root scaling.

@practice for a 10-day horizon, measure 10-day changes directly; multiplying by √10 wastes capital.

@chart horizon
Empirical 99% quantile of price changes over horizons up to 10 days, in Romania and Germany–Luxembourg, against the square-root-of-time scaling of the 1-day quantile.

# Backtesting VaR and ES

A VaR is a promise about how often losses will exceed it, and the promise can be checked after the fact. This section counts exceedances with the Kupiec test, checks their timing with the Christoffersen test and the Basel traffic light, and tests ES with the Acerbi–Székely statistic, over 3,587 days.

## Kupiec test of the exceedance frequency {h=75883790}

A 99% VaR promises to be exceeded on 1% of days. The Kupiec (1995) test counts the exceedances and tests whether their share differs from that promise:

$$ I_t=\mathbf 1\{L_t>\text{VaR}_{\alpha,t}\}, \qquad x=\textstyle\sum_{t=1}^{n}I_t, \qquad \hat p=x/n $$ {#eq:hit}

$$ \text{LR}_{uc}=-2\ln\frac{(1-p)^{n-x}\,p^{x}}{(1-\hat p)^{n-x}\,\hat p^{\,x}}\ \sim\ \chi^2_1 $$ {#eq:kupiec}

where $I_t$ is the exceedance indicator (1 if the loss exceeds the VaR, 0 otherwise), $n$ the number of days, $x$ the number of exceedances, $\hat p$ their observed share and $p=1-\alpha$ the promised share. $\text{LR}_{uc}$ is the likelihood ratio (LR) test of unconditional coverage; under the null hypothesis it follows a $\chi^2$ distribution with one degree of freedom, and the model is rejected at 5% if $\text{LR}_{uc}$ exceeds 3.84.

For the 99% VaR on 3,587 days, 35.9 exceedances are expected. The normal VaR had 115, with $\text{LR}_{uc}$ = 111.5; FHS had 54, with $\text{LR}_{uc}$ = 8.0; EVT had 49, with $p$ = 0.037. The power of the test depends on the sample: with one year at 99% we expect only 2–3 exceedances, and the test can hardly reject anything; ten years of daily data make it sharp.

@practice ask for the exceedance count before you trust anyone's VaR.

## Christoffersen test of independent exceedances {h=d0331e9c}

A good model is not surprised twice in a row: an exceedance today should not make one tomorrow more likely. Christoffersen (1998) tests this by comparing two conditional probabilities:

$$ \pi_{01}=\Pr(I_t=1\mid I_{t-1}=0), \qquad \pi_{11}=\Pr(I_t=1\mid I_{t-1}=1) $$ {#eq:markov}

$$ \text{LR}_{ind}=-2\ln\frac{(1-\hat\pi)^{n_{00}+n_{10}}\hat\pi^{\,n_{01}+n_{11}}}{(1-\hat\pi_{01})^{n_{00}}\hat\pi_{01}^{\,n_{01}}(1-\hat\pi_{11})^{n_{10}}\hat\pi_{11}^{\,n_{11}}}\sim\chi^2_1 $$ {#eq:christoffersen}

where $\pi_{01}$ is the probability of an exceedance after a quiet day, $\pi_{11}$ the probability of an exceedance after an exceedance, $n_{ij}$ the number of days with $I_{t-1}=i$ and $I_t=j$, $\hat\pi$ the overall share of exceedances and $\hat\pi_{01}$, $\hat\pi_{11}$ the estimated conditional shares. The null hypothesis is $H_0$: $\pi_{01}=\pi_{11}$. The joint test of coverage and independence is $\text{LR}_{cc}$ = $\text{LR}_{uc}$ + $\text{LR}_{ind}$, distributed as $\chi^2_2$.

On the 99% VaR the independence $p$-values are 0.682 for HS, 0.868 for the normal VaR and 0.199 for FHS. No method fails: exceedances rarely fall on consecutive days. But they do cluster in months. The normal VaR was exceeded on 7.26% of days in 2021–2022 and on 2.33% in 2017–2020. A first-order test, which only looks at yesterday, misses this; the traffic light, which looks at a 250-day window, sees it.

@practice look at the timing of exceedances, not only at their number.

## Over ten years only the filtered methods pass at 95%; at 99% every method has too many exceedances {h=af97dd5d}

The table collects the backtest of all five methods on Romania, 1 Jan 2017 to 31 Oct 2026. The expected shares are 5% and 1% of 3,587 days, that is 35.9 exceedances at 99%. "Red days" is the share of days whose last 250 days held 10 or more exceedances (next block); the same table for Germany–Luxembourg is in Appendix D.

| Romania | 95%: share | Kupiec p | 99%: count | share, % | Kupiec p | Christoffersen p | red days, % |
|---|---|---|---|---|---|---|---|
| HS | 6.16 | 0.002 | 73 | 2.04 | <0.001 | 0.682 | 16.7 |
| Normal | 7.36 | <0.001 | 115 | 3.21 | <0.001 | 0.868 | 29.5 |
| Student-t | 8.75 | <0.001 | 71 | 1.98 | <0.001 | 0.630 | 18.3 |
| FHS | 5.58 | 0.120 | 54 | 1.51 | 0.005 | 0.199 | 6.2 |
| EVT | 5.55 | 0.139 | 49 | 1.37 | 0.037 | 0.244 | 2.8 |

At 95% only FHS and EVT pass the Kupiec test, with $p$-values of 0.120 and 0.139. At 99% every method is rejected, but the gap is very different: the normal VaR is exceeded on 3.21% of days and spends 29.5% of days in the red zone, while EVT is exceeded on 1.37% and is red on 2.8% of days. No method captures the 99% tail of power prices fully.

@practice accept a model at 95%, but hold extra capital for the 99% tail that none of them captures fully.

## The Basel traffic light: the normal VaR spent 30% of days in the red zone {h=4c01f005}

The Basel Committee on Banking Supervision (BCBS, 1996) judges a 99% VaR by the count of exceedances in the last 250 days: green for 0–4, yellow for 5–9 and red for 10 or more. A correct model is green with probability 89.2% and red with probability 0.025%, so a red zone is strong evidence that the model is wrong.

The chart follows the zone of each method day by day through the backtest. The normal VaR spent almost a third of the days in the red zone; HS was red on 16.7% of days, FHS on 6.2% and EVT on 2.8%. The red periods are concentrated in the crisis years, which is the clustering in months that the Christoffersen test did not detect.

@practice yellow means recalibrate, red means stop using the model for limits.

@chart traffic
Basel traffic-light zone of each method's 99% VaR (count of exceedances in the last 250 days), Romania, backtest 2017–2026.

## Exceedance rates by method in 2021–2022 and since 2023 {h=fba97d02}

Splitting the backtest into three periods shows where the failures come from. The table gives the share of days above the 99% VaR, in percent, for Romania and Germany–Luxembourg.

| 99% VaR, % of days | RO 17–20 | RO 21–22 | RO 23–26 | DE-LU 17–20 | DE-LU 21–22 | DE-LU 23–26 |
|---|---|---|---|---|---|---|
| HS | 1.58 | 4.93 | 1.00 | 1.16 | 3.84 | 1.07 |
| Normal | 2.33 | 7.26 | 2.00 | 2.40 | 5.89 | 2.07 |
| Student-t | 1.30 | 4.66 | 1.29 | 1.37 | 3.97 | 1.29 |
| FHS | 1.37 | 2.88 | 0.93 | 1.44 | 2.47 | 1.36 |
| EVT | 1.24 | 2.47 | 0.93 | 1.51 | 2.19 | 1.07 |

In the crisis even FHS was exceeded on 2.88% of days in Romania: the gas shock moved the whole distribution, not only its scale. After the crisis the picture changes: since 2023, FHS and EVT are at 0.93%, HS at 1.00% and only the normal VaR stays far off, at 2.00%. A model that looks good on calm years tells little about its behaviour in a crisis.

@practice test every model on 2021–2022 before you trust it in a crisis.

## Backtesting ES: the size of losses beyond VaR {h=061813ec}

ES cannot be checked by counting, because it is a statement about the size of the losses beyond VaR. Acerbi and Székely (2014) divide each exceedance loss by its ES forecast; if ES is right, these ratios average 1:

$$ Z_2=\frac{1}{T(1-\alpha)}\sum_{t=1}^{T}\frac{L_t\,I_t}{\text{ES}_{\alpha,t}}-1, \qquad \E_{H_0}[Z_2]=0 $$ {#eq:z2}

where $T$ is the number of days, $\alpha$ = 0.975, $I_t$ the exceedance of VaR$_{0.975}$, $L_t$ the loss and $\text{ES}_{\alpha,t}$ the ES forecast. A positive $Z_2$ means that ES was too small. The $p$-value comes from 2,000 paths simulated from each model (Appendix C).

| Z2 | all | p | 2021–22 | p | 2023–26 | p |
|---|---|---|---|---|---|---|
| HS | 0.628 | <0.001 | 2.694 | <0.001 | −0.026 | 0.761 |
| Normal | 1.425 | <0.001 | 4.170 | <0.001 | 0.697 | <0.001 |
| Student-t | 0.908 | <0.001 | 2.910 | <0.001 | 0.329 | 0.052 |
| FHS | 0.335 | 0.004 | 1.164 | <0.001 | −0.083 | 0.759 |
| EVT | 0.279 | 0.009 | 1.183 | <0.001 | −0.114 | 0.722 |

Every ES was too small in the crisis, the normal one by the widest margin. Since 2023, FHS, EVT and HS pass. Because a 97.5% ES rests on only about 9 tail days a year, its comparison needs several years of data (Pele and Mazurencu-Marinescu-Pele, 2026).

@practice judge ES on several years, never on one quarter (about 9 tail days a year).

## AIDA 2026: a conformal shift measures and corrects the miscalibration of VaR {h=ce542221}

At the AIDA conference (Bucharest University of Economic Studies, 4 June 2026), D. T. Pele presented joint work with V. Bolovăneanu, A. T. Ginavar, S. Lessmann and W. K. Härdle on recalibrating VaR forecasts ([slides](https://github.com/danpele/EMQA/blob/main/resources/aida2026/pele_conformal_tail_risk.pdf); the paper is submitted). The method needs a single number. Each day the score $s_t=\hat q_t-r_t$ compares the forecast quantile with the realised return and is positive on an exceedance day; $\hat q_V$ is the 99% quantile of past scores, and the corrected VaR is the VaR plus $\hat q_V$. The shift is either fixed on a calibration sample (an audit) or rolled over the last 250 days (for daily use). The work applies it to the 1% VaR of 10 models, foundation models, GARCH-type models and HS, on 24 assets including oil and gas, 240 pairs in all, and judges the result with the Kupiec and Christoffersen tests and the traffic light of this section.

As a diagnosis, $\hat q_V$ ranges from −0.007, for a model that is too prudent, to +0.102, for a model with no usable tail signal, and it explains 53.4% (partial $R^2$) of the gain in quantile score. As a repair, the green-zone pairs rise from 63/240 (26.2%) raw to 203/240 (84.6%) with the fixed shift and 234/240 (97.5%) with the rolling shift. The exceedance rate is restored, but their clustering is not, so the Christoffersen test keeps its role. The link to this lecture is direct: Kupiec says whether VaR fails, $\hat q_V$ says by how much, and the widening $\hat c_t$ of the day-ahead guarantee in the next section is the same one-parameter shift.

@practice after a failed backtest, widen VaR by the conformal shift and keep testing for clusters.

# Margins, guarantees and position limits

The quantiles of the previous sections become cash and limits in three places: the margins of an exchange, the guarantee of the day-ahead market and the position limits of a trading desk. This section shows how each is computed and why a well-hedged company can still run out of cash.

## Exchange margins: initial margin as a VaR, variation margin paid daily {h=4408bce8}

A clearing house holds a deposit that covers a 99% two-day loss and settles gains and losses in cash every evening:

$$ \text{IM}_t=K F_t\,\hat q_{0.99}\big(|r^{(2)}|\big), \qquad \text{VM}_t=n K(F_t-F_{t-1}) $$ {#eq:margin}

where $\text{IM}_t$ is the initial margin (IM) and $\text{VM}_t$ the variation margin (VM), both set by the central counterparty (CCP), $F_t$ the futures price, $K$ = 1,000 barrels per Brent lot, $r^{(2)}$ the two-day return, $\hat q_{0.99}$ its empirical 99% quantile in absolute value and $n$ the number of lots sold (positive) or bought (negative).

The rules come from the European Market Infrastructure Regulation (EMIR) and its regulatory technical standards (RTS), Delegated Regulation 153/2013. For futures, the margin must cover 99% of losses over a 2-day liquidation period, on at least 12 months of data (Art. 24–26). Article 28 adds anti-procyclicality (APC) tools: a 25% buffer, a 25% weight on stressed observations, or a floor computed on 10 years. On the Intercontinental Exchange (ICE) Brent contract, a position of 100 lots sold faced its largest one-day VM of 0.88 million United States dollars (USD) on 16 Sep 2019.

@practice a hedged producer gains on the physical sale later, but pays the margin today.

## Margin calls and liquidity shortfalls of hedged energy companies in 2022 {h=85f6d45d}

The European Central Bank (ECB) described what happened in November 2022. TTF gas futures reached 227 EUR/MWh on 7 March 2022, about 12 times the level of early 2021. By mid-2022 about twice as much initial margin was posted as in late 2021. The firms hurt were mostly utilities and producers that had sold forward: hedgers, not speculators. Their physical position gained value, but the gain would arrive only at delivery, while the margin had to be paid in cash immediately.

The European Union (EU) responded with Delegated Regulation (EU) 2022/2311, which accepted public guarantees as collateral until 29 November 2023. In Romania the same mechanism works on the day-ahead market: OPCOM accepts a buy order at a positive price only up to the participant's guarantee, usually a bank letter (OPCOM, 2025).

@practice the risk that sinks a hedged company is liquidity, not the price itself.

## Margins are procyclical: in 2026 the Brent margin rose 2.7-fold in two months {h=a33069fc}

A margin computed from the last 12 months of returns rises exactly when the market becomes volatile, which is when cash is scarcest. The chart recomputes the Brent initial margin per lot from the front-month futures. In early 2026 Brent rose from 72.48 USD on 27 Feb 2026 to 118.35 USD on 31 Mar 2026. With 12 months of history, the IM went from 5,970 to 16,313 USD per lot, ×2.73; with a floor computed on data since 2015, it rose only ×2.07.

The floor also protects better: losses beyond the IM occurred on 1.80% of days with 12 months of history and on 0.66% with the floor, against a target of 1%. The anti-procyclicality tools of EMIR are therefore not only a matter of stability for the clearing house; they also make the margin a better 99% quantile.

@practice plan your cash for the margin a crisis would demand, not for today's margin.

@chart brent_im
Brent front-month price and the initial margin per lot computed with 12 months of history and with a floor since 2015, trading days 2016–2026.

## The day-ahead guarantee is set from a quantile forecast of tomorrow's price {h=f7f8d9be}

To be sure its order clears, a supplier bids up to a high price, and the guarantee must cover price times volume. The guarantee therefore rests on a high quantile of tomorrow's price, forecast with quantile regression (QR) (Koenker and Bassett, 1978) and widened with a conformal correction (Romano et al., 2019):

$$ G_t\ \ge\ Q\cdot 24\cdot \hat q_{\tau,t}, \qquad \hat q_{\tau,t}=\beta_0+\beta_1P_{t-1}+\beta_2P_{t-7}+\textstyle\sum_j\delta_jD_{j,t} $$ {#eq:guarantee}

$$ \tilde q_{\tau,t}=\hat q_{\tau,t}+\hat c_t, \qquad \hat c_t=\hat q_\tau\big(P_s-\hat q_{\tau,s},\ s=t-365,\dots,t-1\big) $$ {#eq:conformal}

where $G_t$ is the guarantee in EUR, $Q$ the position in MW, $\hat q_{\tau,t}$ the QR forecast of the $\tau$-quantile of the price, estimated on the last 365 days as in quantile regression averaging (QRA) of Lecture 2, $\beta_0$, $\beta_1$, $\beta_2$ and $\delta_j$ its coefficients, $P_{t-1}$ and $P_{t-7}$ the prices one day and one week earlier, $D_{j,t}$ weekday dummies, $\tilde q_{\tau,t}$ the widened quantile and $\hat c_t$ the conformal correction, the $\tau$-quantile of the past forecast errors.

With $\tau$ = 0.99 over 2017–2026, the price stayed below the forecast on 96.90% of days with plain QR, 98.47% with the widened QR and 98.49% with FHS. For 100 MW flat the guarantee costs 0.371 million EUR per day on average, and the widening adds 7.5%. The amount depends strongly on the regime: 0.172 million EUR per day in 2017–2020 and 0.649 in 2021–2022.

@practice size the bank line behind the guarantee on the crisis quantile, before the crisis.

## Heavier tails bring the 99% quantile close to its nominal coverage {h=4b1190e2}

The chart compares, through the backtest, the share of days on which the price stayed below each 99% forecast. The Kupiec $p$-values at 99% are below 0.001 for plain QR, 0.003 for the widened QR and 0.005 for FHS: the conformal correction moves the coverage close to its promise, though not quite to it. At 95% the widened QR passes, with $p$ = 0.053, as Lecture 2 suggested for the tails (Nowotarski and Weron, 2018).

@practice a forecast used for collateral must be calibrated in the tail, not only accurate on average.

@chart coverage
Coverage of the 99% quantile forecast of the Romanian day-ahead price for plain QR, the widened QR and FHS, backtest 2017–2026.

## A position limit in MW should shrink when VaR grows {h=1fb3d4bd}

The board sets a daily risk budget in EUR; the desk divides it by today's VaR per MW:

$$ Q^{\max}_t=\frac{B}{24\cdot\text{VaR}^{\text{FHS}}_{0.99,t}} $$ {#eq:limit}

where $B$ is the daily VaR budget, here 250,000 EUR (an assumption for the example), $\text{VaR}^{\text{FHS}}_{0.99,t}$ the FHS 99% VaR in EUR/MWh and $Q^{\max}_t$ the maximum open flat position in MW.

With the FHS 99% VaR on Romanian data, the median VaR of 2019 was 20.27 EUR/MWh, which allows 514 MW. On 12 Jul 2022 the VaR was 245.80 and the limit only 42 MW. On 31 Oct 2026 the VaR was 53.15 and the limit 196 MW. A fixed MW limit lets the money at risk grow with volatility; a fixed EUR budget keeps it constant and forces the position to shrink when the market becomes dangerous.

@practice set limits in EUR of VaR and convert them to MW every day.

# Price risk for suppliers and producers

A supplier and a producer face the same price but opposite tails, and a supplier's monthly bill adds the shape of its load. This section measures the supplier's monthly cash-flow-at-risk, compares the two tails and summarises case study C4 on systemic and energy-specific risks.

## A supplier's monthly cost-at-risk under the normal distribution {h=46817159}

A supplier prices next month at this month's cost; the risk is a jump of the load-weighted price. The cost overrun and its quantile are

$$ \bar P^{L}_m=\frac{\sum_h P_hL_h}{\sum_h L_h}, \qquad o_m=\frac{\bar P^{L}_m}{\bar P^{L}_{m-1}}-1, \qquad \text{CFaR}_{0.95}=\hat q_{0.95}(o_m) $$ {#eq:cfar}

where $P_h$ is the hourly price, $L_h$ the Romanian load in hour $h$ (the shape of the portfolio), $\bar P^{L}_m$ the load-weighted price of month $m$, $o_m$ the cost overrun from one month to the next and the cash-flow-at-risk (CFaR) its quantile. Amounts in EUR are for a portfolio of 100 MW on average.

Over 140 months, from Mar 2015 to Oct 2026, the normal 99% limit estimated on 2015–2020 is an overrun of +50.5%. It was exceeded 3 times since 2021, against 0.7 expected. The worst month was Nov 2024, with +86.6%, or 5.96 million EUR. Empirically, on all months, the CFaR$_{0.95}$ is +39.9%, i.e. 2.84 million EUR, and the ES$_{0.95}$ is +60.2%, i.e. 6.49 million EUR.

@practice price a fixed retail offer with an ES-based premium, or hedge it forward (Lecture 5).

## Since 2021 the normal 99% monthly limit was exceeded 3 times (0.7 expected) {h=6769c270}

The chart shows the monthly overrun of the load-weighted cost since March 2015 together with the normal 99% limit computed in 2020. The red bars are the months that exceed the limit. The largest overrun came in Nov 2024, after the summer of 2024, and not during the 2022 crisis: a supplier's monthly risk depends on the jump from one month to the next, not on the level of the price.

@practice re-estimate the monthly limit every quarter and stress it with the 2022 months.

@chart supplier_month
Monthly overrun of the load-weighted power cost in Romania, Mar 2015 to Oct 2026, with the normal 99% limit computed in 2020; months above the limit in red.

## Loss tails: the supplier's tail is heavier than the producer's {h=fdcdce2f}

A supplier loses when the price rises, a producer when it falls:

$$ L^{\text{buyer}}_t=+Q\,24\,X_t, \qquad L^{\text{seller}}_t=-Q\,24\,X_t $$ {#eq:twotails}

where $L^{\text{buyer}}_t$ is the loss of the buyer (the supplier), $L^{\text{seller}}_t$ that of a producer selling spot, $Q$ the position in MW and $X_t$ the price change. There is one distribution of $X_t$ but two tails: the upper one for the supplier and the lower one for the producer. Because prices jump up more than down, the skewness of $X_t$ is 1.02.

On daily data, 1 Jan 2015 to 31 Oct 2026, the 99% quantile of the change (the supplier's risk) is +88.21 EUR/MWh and the 1% quantile (the producer's risk) is −70.74 EUR/MWh. The ES$_{0.975}$ is 91.29 for the supplier against 74.92 for the producer. On the monthly base price the asymmetry persists: the 95% quantile of the change is +42.4% and the 5% quantile −32.3%.

@practice the producer's price risk is smaller, but a dry year adds volume risk (next slide).

## Case study C4: a systemic risk meter and two risks specific to energy companies {h=637b758c}

Case study C4 builds on a paper from our group (Toma, Dima, Grecu, Pele and Lessmann, 2026). The paper uses 100 European energy companies over 2016–2026 and estimates 5% quantile regressions with the least absolute shrinkage and selection operator (LASSO); the mean penalty across firms is the Energy Financial Risk Meter (EFRM). The EFRM captures the shocks of 2020 and 2022, and together with the ECB's Composite Indicator of Systemic Stress (CISS) it predicts volatile months with an area under the curve (AUC) of 0.731.

Our replication on three Romanian companies, OMV Petrom, Romgaz and Nuclearelectrica, gives an AUC of 0.38, against 0.61 for past volatility: a systemic meter needs many firms, as in the paper. The case study adds two risks specific to energy companies. The price–volume premium of the household profile, the extra cost of buying more power in the expensive hours, was 5.2% of the base price in 2025. A hydro fleet that sold its median output forward would have had to buy back the missing volume in the dry year 2022 at a cost of 394 million EUR.

@practice put the systemic meter, the price–volume premium and the dry-year cost on one dashboard.

## AIDA 2026: systemic tail risk in EU energy broke upward in July 2021 {h=0bdfd8d7}

At the AIDA conference (3 June 2026), F.-M. Toma presented the paper behind case study C4 ([slides](https://github.com/danpele/EMQA/blob/main/resources/aida2026/toma_energy_financial_risk_meter.pdf); paper: [doi:10.2139/ssrn.6985301](https://doi.org/10.2139/ssrn.6985301)). The work uses 100 European energy firms from April 2016 to March 2026. For each firm the 5% quantile of the return is regressed by LASSO on the returns of the other 99 firms, oil and gas futures and stock indices; the EFRM is the mean LASSO penalty, so a higher value means that more links are needed to explain the tail, i.e. more systemic exposure.

The monthly EFRM has two breaks: February 2020, at the start of the pandemic, and July 2021, during the run-up of gas prices, seven months before the invasion of Ukraine. Geopolitical risk moved the EFRM only after the invasion, by +1.52 percentage points in a time-varying model. The effect of the EFRM on Stoxx 600 stocks has since become about 60% weaker, while its effect on 5-year credit default swaps stayed positive. Out of sample, the EFRM together with the CISS predicts volatile months with an AUC of 0.731, against 0.708 for the EFRM alone and 0.673 for the CISS alone.

@practice a firm's own VaR cannot see contagion; read a sector meter next to it.

## AIDA 2026: the tail risk of carbon-heavy firms predicts the low-carbon premium {h=67a4b6e0}

At the AIDA conference (5 June 2026), Prof. Wolfgang Karl Härdle presented joint work with R. Wang and L. Zhang ([slides](https://github.com/danpele/EMQA/blob/main/resources/aida2026/wang_carbon_risk_dynamics.pdf); paper: [doi:10.2139/ssrn.5757742](https://doi.org/10.2139/ssrn.5757742)). The starting point is the carbon premium puzzle. Risk compensation says that high-carbon firms should earn more, because investors demand a higher return for their transition risk; a preference for green assets says that low-carbon firms should earn more. The work uses Chinese stocks from July 2014 to February 2025: the 50 largest high-carbon and the 50 largest low-carbon firms, chosen from the top and bottom 30% by CO$_2$ emissions per unit of revenue. For each firm the 5% quantile of the return is regressed by LASSO on the other firms and on macroeconomic factors, including the volatility of carbon prices, over a 63-day window, exactly as for the EFRM of the previous section. The carbon risk dynamic indicator (CARDI) is the Financial Risk Meter (FRM), the mean LASSO penalty $\lambda$, of the high-carbon firms divided by that of the low-carbon firms.

The high-risk regimes of CARDI coincide with unexpected or early-stage climate-policy events. Both hypotheses of the puzzle hold, depending on CARDI: a rising CARDI predicts a higher factor-adjusted low-carbon premium in the next month, with a coefficient of 0.022 at the 5% quantile over 118 months, while ratios built from connectedness, extreme downside co-movement or conditional VaR do not predict it. A strategy that is long low-carbon and short high-carbon only when CARDI rises earned 115.84% cumulatively over 2015–2024, with a Sharpe ratio of 0.72, against 89.03% and 0.49 for holding the same position all the time. For an energy company, the ratio says which side of the sector carries the tail risk.

@practice in an oil and gas firm, watch CARDI: when it rises, investors favour low-carbon peers.

# Case study: the price rise of autumn 2026

In 2026 the Romanian price doubled between June and October without a single violent day. This case study shows that the VaR models passed their tests while the cash needs of a supplier doubled, and ends with a checklist for a risk desk.

## Case study: in 2026 the price doubled gradually, without jumps {h=9dfaa9e6}

The monthly mean of the day-ahead price was 122.99 EUR/MWh in June 2026 and 239.32 in October, with a peak of 323.76 EUR/MWh on 29 Oct 2026. The rise came gradually, through many moderate daily changes rather than a few jumps. Over the 153 days of the period, a correct 99% VaR should have been exceeded 1.5 times; FHS was exceeded 2 times, HS once and the normal VaR 3 times. By the standard of the daily VaR, nothing alarming happened.

@practice a slow rise passes the VaR tests and still drains cash: watch the price level too.

@chart case2026
Romanian day-ahead base price and the 99% VaR forecasts, 1 Jun to 31 Oct 2026, with the exceedances marked.

## Case study: market risk and liquidity needs in 2026 {h=f7460c47}

Market risk barely moved. The FHS 99% VaR was 61.64 EUR/MWh in June and 67.50 in October, and the ES test since 2023 does not reject FHS ($Z_2$ = −0.083). Cash needs, however, doubled. The day-ahead guarantee for 100 MW, computed from the widened 99% quantile, rose from 0.416 to 0.776 million EUR per day. Orders would have exceeded the guarantee limit on 3 days, and on 6 without the widening.

The supplier's monthly bill for 100 MW rose by +25.1% in August (2.38 million EUR), +16.2% in September (1.86 million) and +34.0% in October (4.68 million). Each month stayed below the 99% limit of +50.5%, but three overruns came in a row, and their cost accumulates. The drivers were external: the TTF gas price rose from 44.94 to 86.81 EUR/MWh between June and October, Brent averaged 108.34 USD in October and the Germany–Luxembourg price 169.48 EUR/MWh.

@practice a risk report needs a liquidity line next to VaR: guarantees, margins and the cumulative monthly overrun.

## A risk desk checklist for energy prices {h=3b42433e}

The lecture can be condensed into four steps for a risk desk.

- **Measure.** Define the position and the sign of the loss, buyer or seller. Use only data known at gate closure. Report VaR and ES from two methods, one of them filtered (FHS or EVT).
- **Check.** Run the Kupiec and Christoffersen tests and the traffic light on several years, including 2021–2022. Use $Z_2$ for ES, and never rank models on a few tail days.
- **Decide.** Set limits in EUR of VaR, converted daily to MW. Size guarantees and credit lines from calibrated high quantiles. Keep a cash buffer for the margin a crisis would demand.
- **Report.** In EUR and in MW, by month, with the liquidity next to the market risk.

@practice Assignment 2 (Task 5) applies this checklist to the cash flow of your own role.

# Wrap-up

The wrap-up tests the main ideas with five short questions, summarises the lecture and points to the research of our group and to further reading.

## Self-assessment questions {h=a1f237cd}

1. Your 99% one-day VaR for 100 MW is 162 thousand EUR. What does it promise, and what does it not say? Answer: on about 1 day in 100 the loss should exceed it. It says nothing about how large the loss is on those days, which is what ES (162 thousand EUR at 97.5%) measures.
2. Over the last 250 days your 99% VaR was exceeded 7 times. What zone is it in, and what does Kupiec say? Answer: the yellow zone (5–9). The Kupiec test gives $\text{LR}_{uc}$ = 5.50 and $p$ = 0.019, so the model is rejected at 5%. Recalibrate it, for example by moving from HS to FHS, and keep watching.
3. Your chief financial officer computes the 10-day VaR as $\sqrt{10}$ times the 1-day VaR. Is that prudent or wasteful for power? Answer: wasteful. Power prices revert, and the empirical 10-day 99% quantile is only 1.72 times the 1-day one in Romania, not 3.16.
4. You sold 100 lots of Brent to hedge your production, and today the price rises by 5 USD per barrel. What happens tonight? Answer: you pay a variation margin of 100 × 1,000 × 5 = 500,000 USD in cash. The physical oil you sell later is worth more, but the cash leaves today.
5. Your 99% quantile forecast of tomorrow's price was exceeded on 111 days out of 3,585. What do you do? Answer: widen the tail with a conformal correction from recent errors. Coverage rises from 96.90% to 98.47% for 7.5% more guarantee.

## Wrap-up {h=fa9ea138}

VaR is a quantile of tomorrow's loss and ES the mean of the loss beyond it. On power prices the normal curve fails, the filtered methods, FHS and EVT, come closest to their promise, and none was right in 2021–2022. The same quantiles set position limits, exchange margins and the day-ahead guarantee. The 2026 case study shows that liquidity, not VaR, is the first casualty of a price rise. The next lecture turns to hedging with derivatives (Lecture 5).

## Research from our group on energy risk {h=db4c4f8e}

Three recent papers from our group, at the Bucharest University of Economic Studies and the Romanian Academy, Institute for Economic Forecasting, address the topics of this lecture. Their findings are those stated in the papers; the numbers on the other slides come from our own data.

- **Energy Financial Risk Meter** (Toma, Dima, Grecu, Pele and Lessmann, 2026). The paper builds a systemic-risk indicator for the EU energy sector from LASSO quantile regressions on 100 companies; the indicator captures the 2020 and 2022 shocks (case study C4).
- **Foundation models for VaR and ES** (Jheng, Tak, Găman, Mazurencu-Marinescu-Pele and Pele, 2026). The paper uses ten daily return series from five Central and Eastern European (CEE) markets, including Romania, out of sample in 2018–2025. It applies three pre-trained time-series models, without fine-tuning, against classical benchmarks, and evaluates them with the Kupiec, Christoffersen and Acerbi–Székely tests and the Basel traffic light. The best raw model has a green-zone rate of 90%, which rises to 96.7% after a rolling conformal calibration, the highest of all models.
- **How precise is an ES comparison?** (Pele and Mazurencu-Marinescu-Pele, 2026). The paper turns the $(n\alpha)^{-1/2}$ precision limit of ES into four practical diagnostics, including a sample-size rule. On global financial assets it finds that about one in five pairwise ES comparisons cannot be trusted at regulatory tail levels.

## Further reading and resources {h=b6d305d6}

- **McNeil, Frey and Embrechts**, *Quantitative Risk Management*, 2nd edition: VaR, ES, EVT and backtesting.
- **Christoffersen**, *Elements of Financial Risk Management*, 2nd edition: FHS and backtests, with exercises.
- **ECB**, Financial stability risks from energy derivatives markets (2022): [ecb.europa.eu](https://www.ecb.europa.eu/pub/financial-stability/fsr/special/html/ecb.fsrart202211_01~173476301a.en.html).
- **This course**: code, data and notebooks on [github.com/danpele/EMQA](https://github.com/danpele/EMQA); the notebook reproduces every chart and number of this lecture.
- **Assignment 2**, Task 5: VaR and ES of your role's cash flow, with backtests.
- **OPCOM**, the day-ahead guarantee procedure: [opcom.ro](https://www.opcom.ro).

# Appendix

The appendix gives the derivations behind the ES formulas of the normal, Student-t and generalised Pareto curves, the backtests in full and the backtest table for Germany–Luxembourg.

## Appendix A: ES of the normal and Student-t distributions {h=df09226c}

For the normal curve, ES is the mean of the loss above the quantile:

$$ \text{ES}^{N}_\alpha=\frac{1}{1-\alpha}\int_{z_\alpha}^{\infty}(\mu+\sigma z)\varphi(z)\,dz=\mu+\sigma\frac{\varphi(z_\alpha)}{1-\alpha} $$ {#eq:app-normal}

where $z$ is the standard normal variable, $\varphi$ its density, $z_\alpha$ its $\alpha$-quantile and $\mu$, $\sigma$ the mean and standard deviation. The step uses $\int_{c}^{\infty}z\varphi(z)\,dz=\varphi(c)$, because the derivative of $\varphi$ is $-z\varphi$. At $\alpha$ = 0.975, ES$^N$ = $\mu$ + 2.338$\sigma$, almost equal to VaR$^N_{0.99}$ = $\mu$ + 2.326$\sigma$: this is why FRTB could swap one for the other.

For the Student-t curve,

$$ \text{ES}^{t}_\alpha=m+s\,\frac{g_\nu(t_{\nu,\alpha})}{1-\alpha}\cdot\frac{\nu+t_{\nu,\alpha}^{2}}{\nu-1}, \quad \nu>1 $$ {#eq:app-t}

where $m$, $s$ and $\nu$ are the location, scale and degrees of freedom and $t_{\nu,\alpha}$, $g_\nu$ the quantile and density of the standard Student-t. It follows from $\int_c^\infty x\,g_\nu(x)\,dx=g_\nu(c)\,(\nu+c^2)/(\nu-1)$. For $\nu\le 1$ the mean, hence ES, does not exist. We fit $(m,s,\nu)$ by MLE every day and keep $\nu$ at least 2.2 so that the variance exists (McNeil, Frey and Embrechts, 2015).

## Appendix B: VaR and ES from the generalised Pareto tail {h=285a10aa}

By the Pickands–Balkema–de Haan theorem, for a high threshold $u$ the excesses over $u$ are approximately GPD for almost all distributions. The tail probability above $u$ is then

$$ \Pr(Z>z)\approx\frac{N_u}{n}\Big(1+\xi\frac{z-u}{\beta}\Big)^{-1/\xi}, \quad z>u $$ {#eq:app-tail}

where $N_u/n$ is the share of the $n$ observations above $u$, $\xi$ the shape and $\beta$ the scale. Setting $\Pr(Z>\text{VaR}_\alpha)=1-\alpha$ and solving gives

$$ \text{VaR}_\alpha=u+\frac{\beta}{\xi}\Big[\Big(\frac{n(1-\alpha)}{N_u}\Big)^{-\xi}-1\Big] $$ {#eq:app-var}

For the GPD the mean excess over a level $v$ above $u$ is linear in $v$, provided $\xi<1$:

$$ \E[Z-v\mid Z>v]=\frac{\beta+\xi(v-u)}{1-\xi} \quad\Rightarrow\quad \text{ES}_\alpha=\frac{\text{VaR}_\alpha+\beta-\xi u}{1-\xi} $$ {#eq:app-es}

The sign of $\xi$ classifies the tail: $\xi>0$ is a heavy tail, $\xi=0$ an exponential tail and $\xi<0$ a bounded tail. Conditional EVT applies these formulas to the standardised shocks $z_t=e_t/\sigma_t$ and then sets VaR$_t=\mu_{d(t)}+\sigma_t\,$VaR$^z_\alpha$, where VaR$^z_\alpha$ is the GPD quantile of the shocks (McNeil and Frey, 2000).

## Appendix C: the three backtests in full {h=fff23875}

**Kupiec and Christoffersen.** Under $H_0$ each $I_t$ is an independent Bernoulli($p$) variable, and $\text{LR}_{uc}$ compares the promised share $p$ with the observed $\hat p$. $\text{LR}_{ind}$ compares a first-order Markov chain with independence. The joint statistic $\text{LR}_{cc}$ = $\text{LR}_{uc}$ + $\text{LR}_{ind}$ follows $\chi^2_2$, with a 5% critical value of 5.99.

**Basel traffic light.** For a correct model, the number of exceedances in 250 days is $x\sim$ Binomial(250, 0.01). Then $\Pr(x\le4)$ = 89.22%, $\Pr(5\le x\le9)$ = 10.76% and $\Pr(x\ge10)$ = 0.025% (BCBS, 1996).

**Acerbi–Székely test.** When VaR and ES are correct, $\E[L_tI_t]=(1-\alpha)\text{ES}_t$, so $\E[Z_2]=0$. $Z_2$ mixes a VaR error, a wrong count of $I_t$, with an ES error, a wrong size of the tail losses; ES alone is not elicitable (Gneiting, 2011), so it is tested together with VaR. Our $p$-value comes from 2,000 simulated paths, each day drawn from that model's predictive distribution: the window for HS, $\mu+\sigma z^*$ for FHS, where $z^*$ is a resampled shock, and the GPD above $u$ for EVT (Acerbi and Székely, 2014).

## Appendix D: the same backtest for Germany–Luxembourg {h=272601fd}

The backtest for the Germany–Luxembourg zone covers 1 Jan 2017 to 31 Oct 2026, 3,591 days, with the same methods and windows as for Romania.

| DE-LU | 95%: share | Kupiec p | 99%: count | share | Kupiec p | Chr. p | red, % | Z2 | p |
|---|---|---|---|---|---|---|---|---|---|
| HS | 6.38 | <0.001 | 60 | 1.67 | <0.001 | 0.998 | 9.2 | 0.529 | <0.001 |
| Normal | 6.66 | <0.001 | 107 | 2.98 | <0.001 | 0.332 | 16.3 | 1.250 | <0.001 |
| Student-t | 8.33 | <0.001 | 67 | 1.87 | <0.001 | 0.174 | 9.0 | 0.617 | 0.001 |
| FHS | 5.82 | 0.028 | 58 | 1.62 | <0.001 | 0.948 | 2.7 | 0.305 | 0.009 |
| EVT | 5.93 | 0.013 | 53 | 1.48 | 0.007 | 0.811 | 0.7 | 0.283 | 0.007 |

The ranking is the same as in Romania: the normal VaR is the worst and the filtered methods are the best.
