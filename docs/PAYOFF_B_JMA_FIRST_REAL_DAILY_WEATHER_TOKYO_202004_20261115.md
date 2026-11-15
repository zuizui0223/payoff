# First real JMA daily weather source: Tokyo, April 2020

**2026-11-15 | PR #356 | official source run https://github.com/zuizui0223/payoff/actions/runs/43667417814 | 91 tests passed**

Official original page: https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2020&month=4&day=&view=

- Source HTML: 36,939 bytes, SHA-256 `09ba492a8d03c97dedfe9b28cdca54221a27ae617eb4efc1f5b1d84ae5b4a3cd`
- 30 distinct original daily observation rows successfully read (2020-04-01 to 2020-04-30).
- **Real displayed daily temperature**: 30 numeric days; mean of daily means **12.803 °C**, mean of daily highs **18.163 °C**, mean of daily lows **7.873 °C**.
- **Real displayed daily relative humidity**: 30 numeric days, mean **65.767%**.
- **Real displayed mean wind speed**: 30 numeric days, mean **3.220 m/s**.
- **Real displayed sunshine duration**: 30 numeric days, sum **213.4 h**.
- **Displayed precipitation**: 17 numeric days totaling **296.5 mm**; **13 original cells are `--`**, whose source missing/zero semantics have **not** been certified. **Do not call 296.5 mm the monthly precipitation total.** A source legend is needed before treating `--` as zero or missing.
- The page is a public HTML display, not the official downloadable CSV with original per-variable quality and homogeneity numbers. The original source station ID `47662` must still be mapped to the historical 3-digit phenology station ID and its valid date.
- **No weather–phenology station-year matched regression was fitted**, and there is no NDVI/biomass fit.

This is the first measured daily meteorology read for PAYOFF-B Japan, beyond synthetic weather import tests. Next: certify precipitation dash semantics and source station identity, obtain official CSV with quality and homogeneity numbers for the same month, then align the 30/60/90-day pre-event window with an actual original JMA phenology event at the same source station/year. Expand only after the one-station real join passes.
