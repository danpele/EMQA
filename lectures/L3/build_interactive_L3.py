"""Build the interactive page of Lecture 3 (Volatility): interactive/L3.html (EN) and interactive/L3_ro.html (RO).

Inputs (interactive/L3_data.js) are computed here from data/clean (Romanian daily base price, 2019 to the cut-off), with the same
definitions as lectures/L3/analysis_L3.py (log and EUR/MWh daily changes, OLS mean equation with AR(1..7) and day-of-week dummies,
GARCH(1,1)-t and GJR(1,1)-t estimates from L3_numbers.json), plus the saved rolling GARCH-t forecasts of the Quantlet
EMQA_L3_case_band. The page logic is in interactive/L3.js. Run: python3 lectures/L3/build_interactive_L3.py [--no-data]
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'common'))
import interactive_common  # noqa: E402
from interactive_common import slider, select, play, charts, rnd, csv, ql_dir  # noqa: E402

K = 3

# (anchor, chart file / Quantlet, section key, id prefix)
BLOCKS = [('clustering', 'acf_clust', 'meas', 'cl'),
          ('fat-tails', 'tails', 'meas', 'ft'),
          ('garch-filter', 'cond_vol', 'garch', 'gf'),
          ('half-life', 'halflife', 'garch', 'hl'),
          ('news-impact', 'nic', 'garch', 'ni'),
          ('forecast-band', 'case_band', 'case', 'fb')]

SECTIONS = {
 'en': dict(meas='Measuring volatility', garch='The GARCH family', case='Case study: Romanian power in 2026'),
 'ro': dict(meas='Măsurarea volatilității', garch='Modelele din familia GARCH',
            case='Studiu de caz: prețul energiei electrice din România în 2026'),
}

L = {
 'en': dict(h1='Lecture 3 · Volatility',
   note='The slide of the lecture is on the left, the same figure on the right, recomputed in your browser from the course data '
        '(data/clean) when you move a control. The ▶ button moves the main parameter step by step. Under each figure: a readout, '
        'a question for the room and the Quantlet with the code of the chart. GARCH = generalised autoregressive conditional '
        'heteroskedasticity; the shocks are the residuals of the mean equation of the lecture (constant, AR(1..7) and day-of-week dummies).',
   src='Romanian day-ahead daily base price: OPCOM PZU via energy-charts.info (Fraunhofer ISE), 2019-01-01 to the cut-off of the lecture. '
       'Shocks: residuals of the OLS (ordinary least squares) mean equation on the daily log change (%) or the daily change in EUR/MWh. '
       'Model parameters: maximum-likelihood estimates of lectures/L3/analysis_L3.py. Market half-lives: GARCH(1,1)-t on Brent, EUA '
       '(EU emission allowances) and OMV Petrom (SNP) returns. Test-year forecasts: Quantlet EMQA_L3_case_band.'),
 'ro': dict(h1='Cursul 3 · Volatilitate',
   note='În stînga este slide-ul din curs, în dreapta aceeași figură, recalculată în browser din datele cursului (data/clean) cînd '
        'modificați un control. Butonul ▶ modifică parametrul principal pas cu pas. Sub fiecare figură: o sinteză numerică, o întrebare '
        'pentru sală și Quantlet-ul cu codul figurii. GARCH = heteroscedasticitate condiționată autoregresivă generalizată; șocurile sînt '
        'reziduurile ecuației mediei din curs (constantă, AR(1..7) și variabile dummy pentru ziua săptămînii).',
   src='Prețul zilnic de bază pentru ziua următoare în România: OPCOM PZU, prin energy-charts.info (Fraunhofer ISE), 2019-01-01 pînă '
       'la data-limită a cursului. Șocuri: reziduurile ecuației mediei estimate prin OLS (metoda celor mai mici pătrate) pe variația '
       'zilnică logaritmică (%) sau pe variația zilnică în EUR/MWh. Parametrii modelelor: estimații de verosimilitate maximă din '
       'lectures/L3/analysis_L3.py. Timpii de înjumătățire pentru piețe: GARCH(1,1)-t pe randamentele Brent, EUA (certificatele de emisii '
       'ale UE) și OMV Petrom (SNP). Prognozele din anul de test: Quantlet-ul EMQA_L3_case_band.'),
}


def widgets(lang):
    ro = lang == 'ro'
    unit = [('pct', 'Variația în % (logaritmică)' if ro else 'Change in % (log)'), ('eur', 'Variația în EUR/MWh' if ro else 'Change in EUR/MWh')]
    return {
     'clustering': (select('cl-u', 'Unitatea șocurilor' if ro else 'Unit of the shocks', unit, 'pct')
                    + slider('cl-L', 'Laguri afișate (zile)' if ro else 'Lags shown (days)', 10, 60, 5, 30)
                    + slider('cl-y', 'Începutul eșantionului' if ro else 'Start of the sample', 2019, 2025, 1, 2019) + play('cl'),
                    charts('cl-e', 'cl-e2')),
     'fat-tails': (slider('ft-nu', 'Gradele de libertate ale repartiției Student-t, ν' if ro else 'Degrees of freedom of the Student-t, ν', 2.5, 30, 'any', 4.27)
                   + slider('ft-k', 'Pragul |z| > k' if ro else 'Threshold |z| > k', 2, 6, 0.5, 4) + play('ft'), charts('ft-chart', cls='one')),
     'garch-filter': (select('gf-u', 'Unitatea șocurilor' if ro else 'Unit of the shocks', unit, 'pct')
                      + slider('gf-a', 'α (reacția la șocul de ieri)' if ro else 'α (reaction to yesterday\'s shock)', 0, 0.5, 'any', 0.3081)
                      + slider('gf-b', 'β (memoria varianței)' if ro else 'β (memory of the variance)', 0, 0.99, 'any', 0.4378)
                      + play('gf'), charts('gf-chart', cls='one')),
     'half-life': (slider('hl-p', 'Persistența α + β' if ro else 'Persistence α + β', 0.5, 0.999, 0.001, 0.746)
                   + slider('hl-h', 'Orizontul afișat (zile)' if ro else 'Horizon shown (days)', 20, 250, 10, 120) + play('hl'),
                   charts('hl-chart', cls='one')),
     'news-impact': (select('ni-u', 'Unitatea șocurilor' if ro else 'Unit of the shocks', unit, 'pct')
                     + slider('ni-g', 'γ (efectul suplimentar al unei scăderi)' if ro else 'γ (extra effect of a fall)', -0.3, 0.6, 'any', 0.2245)
                     + slider('ni-a', 'α' if ro else 'α', 0, 0.5, 'any', 0.179) + play('ni'), charts('ni-chart', cls='one')),
     'forecast-band': (select('fb-m', 'Prognoza volatilității' if ro else 'Volatility forecast',
                              [('garch', 'GARCH(1,1)-t, reestimat zilnic' if ro else 'GARCH(1,1)-t, re-estimated daily'),
                               ('hist30', 'Istoric pe 30 de zile, normală' if ro else '30-day historical, normal')], 'garch')
                       + slider('fb-c', 'Nivelul de acoperire al benzii (%)' if ro else 'Coverage of the band (%)', 50, 99, 1, 90) + play('fb'),
                       charts('fb-chart', cls='one')),
    }


QA = {
 'en': {
  'clustering': ('The daily shocks of the Romanian price are almost uncorrelated, yet the lecture speaks of volatility clustering. Where is the clustering?',
                 'In the squared shocks. On the full sample the first-order autocorrelation of the % shocks is 0.001, but that of the squared shocks '
                 'is 0.133, and the Ljung–Box statistic for ten lags rises from 13.8 (p = 0.18) to 120.0. Large moves, of either sign, follow large '
                 'moves: the size of a shock is predictable even when its sign is not. Switch to EUR/MWh: the squared shocks are far more '
                 'autocorrelated (Ljung–Box 1,519.5), because the price level itself moved from about 40 to over 400 EUR/MWh.'),
  'fat-tails': ('After dividing each % shock by its GARCH-t volatility, 17 of the 2,853 standardised shocks exceed 4 in absolute value. How many would a normal distribution give?',
                'About 0.18, i.e. none: the normal tail beyond 4 standard deviations has probability 6.3 × 10⁻⁵. Even after GARCH removes the '
                'clustering, the tails stay fat; the estimated Student-t, with ν = 4.27 degrees of freedom, expects 12.7. Move ν: with a small ν the Student-t '
                'curve reaches the far bins of the histogram, with ν above 30 it is close to the normal.'),
  'garch-filter': ('For the % shocks the GARCH(1,1)-t estimates are α = 0.31 and β = 0.44. What happens to the conditional volatility if we keep α and raise β to 0.68?',
                   'With the long-run variance held at its estimate, the persistence α + β rises from 0.75 to 0.99: shocks die out slowly, the '
                   'path becomes smooth and stays high for weeks after a spike, and the half-life of a shock grows from 2.4 days to about 58 '
                   'days. The Student-t log-likelihood in the readout falls: the data prefer the faster decay. In EUR/MWh the estimate itself '
                   'is persistent (α + β = 0.994, half-life 113.5 days), because the level of the price drives the size of the changes.'),
  'half-life': ('Brent has a GARCH persistence of 0.973, Romanian power in % of 0.746. How long does it take for half of a volatility shock to fade?',
                'Half-life = ln 0.5 / ln(α + β): 25.6 trading days (about five weeks) for Brent and 2.4 days for Romanian power in %. A shock to the '
                'volatility of a daily auction fades in days, one to oil volatility in weeks. EUA (EU emission allowances, 0.992, 82.8 trading days) '
                'and Romanian power in EUR/MWh (0.994, 113.5 days) are the most persistent. Near α + β = 1 a small change of persistence moves the half-life a lot.'),
  'news-impact': ('In the GJR-GARCH-t model of the % shocks, γ = 0.22 > 0. Does tomorrow\'s volatility react more to a price fall or to a price rise of the same size?',
                  'To a fall. GJR (Glosten–Jagannathan–Runkle) adds γ·ε² on the days when the shock is negative. With the estimates, a shock of '
                  '−2 standard deviations (−39.7%) gives a next-day σ of 30.3%, a shock of +2 standard deviations 23.7%. For the EUR/MWh shocks '
                  'the estimate is γ = −0.13: there a rise of the price increases volatility more than a fall, as rises of the level come with larger '
                  'changes. Set γ = 0 to recover the symmetric GARCH curve.'),
  'forecast-band': ('On the test year, a 90% band built from the daily GARCH-t forecast leaves out 38 of 365 days (10.4%). Is the band well calibrated?',
                    'Roughly: 10.4% outside against 10% nominal. The 30-day historical volatility with a normal quantile also leaves out 38 days '
                    '(10.4%) at 90%, but its band reacts late to new shocks and drops abruptly when a large shock leaves the 30-day window. Change '
                    'the coverage: at high coverage the normal quantile is too narrow for fat tails. At 99% the historical band leaves out 13 days '
                    '(3.6%), the GARCH-t band 4 days (1.1%); at 95%, 8.2% against 6.3%.'),
 },
 'ro': {
  'clustering': ('Șocurile zilnice ale prețului din România sînt aproape necorelate, totuși cursul vorbește despre gruparea volatilității. Unde este gruparea?',
                 'În pătratul șocurilor. Pe tot eșantionul, autocorelația de ordinul întîi a șocurilor în % este 0,001, dar cea a pătratului '
                 'șocurilor este 0,133, iar statistica Ljung–Box pentru zece laguri crește de la 13,8 (p = 0,18) la 120,0. Mișcările mari, de '
                 'orice semn, urmează după mișcări mari: mărimea unui șoc este previzibilă, chiar dacă semnul său nu este. Treceți la EUR/MWh: '
                 'pătratele șocurilor sînt mult mai autocorelate (Ljung–Box 1.519,5), deoarece nivelul prețului a urcat de la circa 40 la peste 400 EUR/MWh.'),
  'fat-tails': ('După împărțirea fiecărui șoc în % la volatilitatea sa GARCH-t, 17 dintre cele 2.853 de șocuri standardizate depășesc 4 în valoare absolută. Cîte ar da o repartiție normală?',
                'Circa 0,18, adică niciunul: coada normalei dincolo de 4 abateri standard are probabilitatea 6,3 × 10⁻⁵. Chiar după ce GARCH '
                'elimină gruparea, cozile rămîn groase; repartiția Student-t estimată, cu ν = 4,27 grade de libertate, se așteaptă la 12,7. Mutați ν: cu un ν mic, '
                'curba Student-t ajunge în clasele îndepărtate ale histogramei, cu ν peste 30 este apropiată de normală.'),
  'garch-filter': ('Pentru șocurile în %, estimațiile GARCH(1,1)-t sînt α = 0,31 și β = 0,44. Ce se întîmplă cu volatilitatea condiționată dacă păstrăm α și ridicăm β la 0,68?',
                   'Cu varianța de lungă durată fixată la estimația ei, persistența α + β crește de la 0,75 la 0,99: șocurile se sting încet, '
                   'traiectoria devine netedă și rămîne ridicată săptămîni întregi după un salt, iar timpul de înjumătățire al unui șoc crește '
                   'de la 2,4 zile la circa 58 de zile. Log-verosimilitatea Student-t din sinteză scade: datele preferă o stingere mai rapidă. În '
                   'EUR/MWh, chiar estimația este persistentă (α + β = 0,994, timp de înjumătățire 113,5 zile), deoarece nivelul prețului determină mărimea variațiilor.'),
  'half-life': ('Brent are persistența GARCH 0,973, iar energia electrică din România, în %, 0,746. În cît timp se stinge jumătate dintr-un șoc de volatilitate?',
                'Timpul de înjumătățire = ln 0,5 / ln(α + β): 25,6 zile de tranzacționare (circa cinci săptămîni) pentru Brent și 2,4 zile pentru '
                'energia electrică din România, în %. Un șoc al volatilității unei licitații zilnice se stinge în cîteva zile, unul al volatilității '
                'țițeiului în săptămîni. EUA (certificatele de emisii ale UE, 0,992, 82,8 zile de tranzacționare) și energia electrică din România '
                'în EUR/MWh (0,994, 113,5 zile) sînt cele mai persistente. Lîngă α + β = 1, o mică schimbare a persistenței mută mult timpul de înjumătățire.'),
  'news-impact': ('În modelul GJR-GARCH-t al șocurilor în %, γ = 0,22 > 0. Reacționează volatilitatea de mîine mai mult la o scădere sau la o creștere de aceeași mărime a prețului?',
                  'La o scădere. GJR (Glosten–Jagannathan–Runkle) adaugă γ·ε² în zilele cu șoc negativ. Cu estimațiile din curs, un șoc de −2 '
                  'abateri standard (−39,7%) dă un σ de a doua zi de 30,3%, iar un șoc de +2 abateri standard 23,7%. Pentru șocurile în EUR/MWh, '
                  'estimația este γ = −0,13: acolo o creștere a prețului mărește volatilitatea mai mult decît o scădere, deoarece creșterile '
                  'nivelului vin cu variații mai mari. Fixați γ = 0 pentru a regăsi curba simetrică GARCH.'),
  'forecast-band': ('În anul de test, o bandă de 90% construită din prognoza zilnică GARCH-t lasă în afară 38 din 365 de zile (10,4%). Este banda bine calibrată?',
                    'Aproximativ: 10,4% în afară, față de 10% nominal. Volatilitatea istorică pe 30 de zile, cu o cuantilă normală, lasă și ea în '
                    'afară 38 de zile (10,4%) la 90%, dar banda ei reacționează tîrziu la șocurile noi și scade brusc cînd un șoc mare iese din '
                    'fereastra de 30 de zile. Schimbați acoperirea: la o acoperire mare, cuantila normală este prea îngustă pentru cozi groase. La '
                    '99%, banda istorică lasă în afară 13 zile (3,6%), banda GARCH-t 4 zile (1,1%); la 95%, 8,2% față de 6,3%.'),
 },
}

TEXT_JS = {
 'en': r"""window.LK_TEXT = {
 unit: { pct: '%', eur: 'EUR/MWh' }, lag: 'Lag (days)', acf: 'Autocorrelation',
 e: 'Shocks ε_t', e2: 'Squared shocks ε_t²', band: '95% band if no autocorrelation',
 cl: (y0, n, a1, a2, q1, q2) => `Sample ${y0} to the cut-off, ${window.EMQAI.cnt(n, 'day', 'days')}: ρ₁(ε) = ${a1}, ρ₁(ε²) = ${a2}. Ljung–Box Q(10): ${q1} for the shocks, ${q2} for the squared shocks (5% critical value 18.3).`,
 z: 'Standardised shock z_t', dens: 'Density (log scale)', hist: 'GARCH-standardised shocks, Romania (%)', normal: 'Normal', stud: nu => `Student-t, ν = ${nu}`,
 ft: (k, n, N, en, et) => `|z| > ${k}: ${n} of ${N} shocks observed; expected ${en} under the normal, ${et} under the Student-t.`,
 sig: u => `Conditional volatility σ_t (${u})`, roll: '30-day rolling standard deviation', garch: 'GARCH(1,1), filter in the browser',
 gf: (a, b, p, hl, s, om) => `α = ${a}, β = ${b}: persistence ${p}, half-life ${hl}; long-run σ = ${s} (held at its estimate, ω = ${om}).`,
 gf2: (ll, ll0, mx, md) => `Student-t log-likelihood ${ll} (at the estimates: ${ll0}). Highest σ_t: ${mx} on ${md}.`,
 days: x => `${x} days`, inf: 'infinite (no mean reversion)',
 left: '% of the shock left', after: 'Days after the shock',
 you: 'Your persistence',
 hl2: (p, h, d10) => `Persistence ${p}: half-life ${h} days; 10 days after the shock ${d10} of it is left.`,
 shock: u => `Shock ε_(t−1), ${u}`, next: u => `Next-day σ_t, ${u}`, fall: 'GJR: price fell yesterday', rise: 'GJR: price rose yesterday', sym: 'Symmetric GARCH (γ = 0)',
 ni: (u, s2, dn, up, r) => `Shock of ±2 standard deviations (±${s2} ${u}): next-day σ ${dn} after a fall, ${up} after a rise (ratio ${r}).`,
 ni2: (p) => `Persistence α + γ/2 + β = ${p}; ω and β are held at their estimates and yesterday's variance at the long-run level.`,
 price: 'Daily base price (EUR/MWh)', bandL: c => `${c}% band, set on t−1`, outside: 'Outside the band',
 fb: (c, n, N, sh, w) => `${c}% band: ${n} of ${N} days outside (${sh}, nominal ${window.EMQAI.nf(100 - c, 0)}%); mean width ±${w} EUR/MWh.`,
 fb2: (a, b) => `Outside the band before 1 May 2026: ${a}; from 1 May 2026: ${b}.`
};
""",
 'ro': r"""window.LK_TEXT = {
 unit: { pct: '%', eur: 'EUR/MWh' }, lag: 'Lagul (zile)', acf: 'Autocorelația',
 e: 'Șocurile ε_t', e2: 'Pătratul șocurilor ε_t²', band: 'Banda de 95% în lipsa autocorelației',
 cl: (y0, n, a1, a2, q1, q2) => `Eșantion din ${y0} pînă la data-limită, ${window.EMQAI.cnt(n, 'zi', 'zile')}: ρ₁(ε) = ${a1}, ρ₁(ε²) = ${a2}. Ljung–Box Q(10): ${q1} pentru șocuri, ${q2} pentru pătratul șocurilor (valoarea critică la 5%: 18,3).`,
 z: 'Șocul standardizat z_t', dens: 'Densitatea (scară logaritmică)', hist: 'Șocuri standardizate cu GARCH, România (%)', normal: 'Normală', stud: nu => `Student-t, ν = ${nu}`,
 ft: (k, n, N, en, et) => `|z| > ${k}: ${n} din ${N} șocuri observate; așteptate ${en} sub repartiția normală, ${et} sub Student-t.`,
 sig: u => `Volatilitatea condiționată σ_t (${u})`, roll: 'Abaterea standard mobilă pe 30 de zile', garch: 'GARCH(1,1), filtru calculat în browser',
 gf: (a, b, p, hl, s, om) => `α = ${a}, β = ${b}: persistența ${p}, timpul de înjumătățire ${hl}; σ de lungă durată = ${s} (fixat la estimația sa, ω = ${om}).`,
 gf2: (ll, ll0, mx, md) => `Log-verosimilitatea Student-t ${ll} (la estimații: ${ll0}). Cel mai mare σ_t: ${mx} pe ${md}.`,
 days: x => `${x} zile`, inf: 'infinit (fără revenire la medie)',
 left: '% rămas din șoc', after: 'Zile după șoc',
 you: 'Persistența aleasă',
 hl2: (p, h, d10) => `Persistența ${p}: timpul de înjumătățire ${h} zile; la 10 zile după șoc mai rămîne ${d10} din el.`,
 shock: u => `Șocul ε_(t−1), ${u}`, next: u => `σ_t de a doua zi, ${u}`, fall: 'GJR: prețul a scăzut ieri', rise: 'GJR: prețul a crescut ieri', sym: 'GARCH simetric (γ = 0)',
 ni: (u, s2, dn, up, r) => `Șoc de ±2 abateri standard (±${s2} ${u}): σ de a doua zi ${dn} după o scădere, ${up} după o creștere (raportul ${r}).`,
 ni2: (p) => `Persistența α + γ/2 + β = ${p}; ω și β sînt fixați la estimațiile lor, iar varianța de ieri la nivelul de lungă durată.`,
 price: 'Prețul zilnic de bază (EUR/MWh)', bandL: c => `Banda de ${c}%, stabilită în t−1`, outside: 'În afara benzii',
 fb: (c, n, N, sh, w) => `Banda de ${c}%: ${n} din ${N} zile în afară (${sh}, nominal ${window.EMQAI.nf(100 - c, 0)}%); lățimea medie ±${w} EUR/MWh.`,
 fb2: (a, b) => `În afara benzii înainte de 1 mai 2026: ${a}; de la 1 mai 2026: ${b}.`
};
""",
}


# ---------------------------------------------------------------- data (real course data only)
def data():
    import numpy as np
    import pandas as pd
    from arch import arch_model

    NUM = json.load(open(os.path.join(HERE, 'L3_numbers.json'), encoding='utf-8'))
    PD = csv('power_da_prices_daily_cet.csv', parse_dates=['date_cet']).set_index('date_cet')
    raw_last = PD['RO'].dropna().index.max()
    END = pd.Timestamp(((raw_last + pd.Timedelta(days=1)).to_period('M').to_timestamp() - pd.Timedelta(days=1)).date())
    CAL = pd.date_range('2019-01-01', END, freq='D')
    P = PD['RO'].reindex(CAL)
    R = {'pct': 100 * np.log(P.where(P > 0)).diff(), 'eur': P.diff()}

    def mean_fit(y, lags=7):          # analysis_L3.mean_fit: constant + AR(1..7) + six day-of-week dummies, OLS
        X = pd.DataFrame({f'L{k}': y.shift(k) for k in range(1, lags + 1)}, index=y.index)
        for j in range(1, 7):
            X[f'D{j}'] = (y.index.dayofweek == j).astype(float)
        X.insert(0, 'const', 1.0)
        df = pd.concat([y.rename('y'), X], axis=1).dropna()
        b = np.linalg.lstsq(df.drop(columns='y').values, df['y'].values, rcond=None)[0]
        return pd.Series(df['y'].values - df.drop(columns='y').values @ b, index=df.index)

    out = {'end': str(END.date())}
    E = {u: mean_fit(R[u]) for u in R}
    for u, e in E.items():
        assert len(pd.date_range(e.index[0], e.index[-1])) == len(e), 'shocks not contiguous'
        g = NUM['garch'][u]
        nu = g['garch_t']['nu']
        const = math.lgamma((nu + 1) / 2) - math.lgamma(nu / 2) - 0.5 * math.log(math.pi * (nu - 2))
        out[u] = {'t0': str(e.index[0].date()), 'e': rnd(e.values, 3),
                  'garch': {k: g['garch_t'][k] for k in ('omega', 'alpha', 'beta', 'nu', 'll', 'pers', 'hl', 'uvar')},
                  'gjr': {k: g['gjr_t'][k] for k in ('omega', 'alpha', 'gamma', 'beta', 'nu')}, 'tconst': const}
    # GARCH(1,1)-t standardised shocks (%): the estimated model of the lecture
    res = arch_model(E['pct'].values, mean='Zero', vol='GARCH', p=1, q=1, dist='t', rescale=False).fit(disp='off', show_warning=False)
    out['z'] = rnd(res.std_resid, 3)
    out['z_nu'] = round(float(res.params['nu']), 4)
    out['facts'] = NUM['facts']
    # half-lives of other markets (GARCH(1,1)-t, each over its own sample)
    out['xm'] = {k: {'pers': NUM['xm'][k]['pers'], 'hl': NUM['xm'][k]['hl']} for k in ('RO_pct', 'RO_eur', 'BRENT', 'EUA', 'SNP')}
    # test-year rolling one-day forecasts (Quantlet EMQA_L3_case_band) and the prices around them
    F = pd.read_csv(os.path.join(ql_dir(3, 'case_band'), 'garch_t_rolling_eur.csv'), parse_dates=['date'])
    out['fb'] = {'date': F['date'].dt.strftime('%Y-%m-%d').tolist(), 'p': rnd(P.reindex(F['date']).values, 2),
                 'p1': rnd(P.shift(1).reindex(F['date']).values, 2), 'yhat': rnd(F['yhat'].values, 3), 'e': rnd(F['e'].values, 3),
                 'garch': rnd(F['garch'].values, 3), 'hist30': rnd(F['hist30'].values, 3), 'nu': rnd(F['nu'].values, 4)}
    return out


if __name__ == '__main__':
    interactive_common.build(sys.modules[__name__])
