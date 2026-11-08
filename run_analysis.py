"""India voice AI agents: market map, unit economics and a revenue triangulation, for an early-stage investment memo.
Inputs: data/companies.csv (every row sourced from public announcements, links in the file) and Bolna's public
per-minute prices. Everything marked ESTIMATE or SCENARIO is a calculation on stated assumptions, not a reported figure.
python run_analysis.py"""
import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = {}
c = pd.read_csv("data/companies.csv")

# ---------- 1. market map ----------
L = c.groupby("layer").agg(companies=("company", "size"), latest_rounds_usd_m=("round_usd_m", "sum"))
R["market_map"] = dict(companies=len(c), layers=L.reset_index().to_dict("records"),
                       latest_rounds_total_usd_m=float(c.round_usd_m.sum()),
                       sarvam_share_of_total=float(c.round_usd_m[c.company == "Sarvam AI"].sum() / c.round_usd_m.sum()),
                       rounds_in_2026=int(c.round_date.astype(str).str.startswith("2026").sum()))
excl = c[c.company != "Sarvam AI"]
R["market_map"]["median_round_excl_sarvam_usd_m"] = float(excl.round_usd_m.median())

# ---------- 2. unit economics per minute (SCENARIO) ----------
# Revenue: Bolna's public prices per minute, which bundle speech-to-text, the LLM and text-to-speech
# (telephony and a platform fee are billed on top, so they are left out of both price and cost here).
PRICES = {"Pay-as-you-go (6.0c)": 0.060, "Pilot, $300 (4.6c)": 0.046, "Pilot, $500 (4.2c)": 0.042}
# Cost: the provider's own cost of the AI stack per minute is not public, so it is a range to test.
COSTS = np.round(np.arange(0.005, 0.0501, 0.005), 3)
grid = pd.DataFrame({k: [1 - cost / p for cost in COSTS] for k, p in PRICES.items()}, index=[f"{x*100:.1f}c" for x in COSTS])
R["unit_economics"] = dict(
    gross_margin_grid={i: {k: round(float(v), 3) for k, v in row.items()} for i, row in grid.iterrows()},
    max_stack_cost_for_50pct_margin_c={k: p * 0.5 * 100 for k, p in PRICES.items()},
    max_stack_cost_for_70pct_margin_c={k: round(p * 0.3 * 100, 2) for k, p in PRICES.items()})
# cost-down scenario: what a 75% cut in stack cost does to margin at the lowest public price
p, before = 0.042, 0.035
after = before * 0.25
R["unit_economics"]["cost_down_scenario"] = dict(price_c=4.2, stack_cost_before_c=3.5, stack_cost_after_c=round(after * 100, 3),
                                                 margin_before=1 - before / p, margin_after=1 - after / p,
                                                 note="SCENARIO: stack cost before the cut is an assumption")

# ---------- 3. revenue triangulation for one company (ESTIMATE) ----------
# Bolna reports 200K+ calls a day; revenue is not disclosed. Annualised AI revenue = calls/day x minutes/call x price x 365.
calls = 200_000
tri = {f"{m} min/call": {k: calls * m * pr * 365 / 1e6 for k, pr in PRICES.items()} for m in [1, 2, 3]}
R["revenue_triangulation"] = dict(calls_per_day=calls, annualised_usd_m=tri,
                                  low=min(min(v.values()) for v in tri.values()), high=max(max(v.values()) for v in tri.values()),
                                  note="ESTIMATE: minutes per call and the price mix are assumptions; enterprise contracts may price lower")

# ---------- charts ----------
fig, ax = plt.subplots(1, 3, figsize=(14, 4.4))
o = c.sort_values("round_usd_m")
cols = {"Models + platform": "#0052CC", "Orchestration": "#E07A2F", "Applications": "#9AA5AD"}
ax[0].barh(o.company, o.round_usd_m, color=[cols[x] for x in o.layer]); ax[0].set_xscale("log")
for i, (v, dte) in enumerate(zip(o.round_usd_m, o.round_date)): ax[0].text(v * 1.1, i, f"${v:g}M ({dte})", va="center", fontsize=8)
ax[0].set_xlim(3, 2000); ax[0].set_xlabel("Latest disclosed round (USD million, log scale)")
ax[0].set_title("Latest rounds: blue = models, orange = orchestration,\ngrey = applications", fontsize=10)
im = ax[1].imshow(grid.to_numpy() * 100, aspect="auto", cmap="RdYlGn", vmin=-20, vmax=100)
ax[1].set_xticks(range(len(PRICES))); ax[1].set_xticklabels([k.split(" (")[0] + "\n" + k.split("(")[1].rstrip(")") for k in PRICES], fontsize=8)
ax[1].set_yticks(range(len(grid))); ax[1].set_yticklabels(grid.index, fontsize=8); ax[1].set_ylabel("AI stack cost per minute (scenario)")
for i in range(len(grid)):
    for j in range(len(PRICES)): ax[1].text(j, i, f"{grid.iloc[i, j]*100:.0f}%", ha="center", va="center", fontsize=7)
ax[1].set_title("Gross margin on the AI stack, by price and cost", fontsize=10)
lo = [tri[f"{m} min/call"]["Pilot, $500 (4.2c)"] for m in [1, 2, 3]]; hi = [tri[f"{m} min/call"]["Pay-as-you-go (6.0c)"] for m in [1, 2, 3]]
x = np.arange(3)
ax[2].bar(x - .2, lo, .4, color="#9AA5AD", label="at 4.2c/min"); ax[2].bar(x + .2, hi, .4, color="#0052CC", label="at 6.0c/min")
for i in range(3): ax[2].text(i - .2, lo[i] + .2, f"${lo[i]:.1f}M", ha="center", fontsize=8); ax[2].text(i + .2, hi[i] + .2, f"${hi[i]:.1f}M", ha="center", fontsize=8)
ax[2].set_xticks(x); ax[2].set_xticklabels(["1 min/call", "2 min/call", "3 min/call"]); ax[2].legend(fontsize=8)
ax[2].set_ylabel("Annualised AI revenue (USD million, estimate)"); ax[2].set_title("Bolna at 200K calls/day: revenue range", fontsize=10)
for a in (ax[0], ax[2]): a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("results/summary.png", dpi=150)

grid.to_csv("results/margin_grid.csv")
json.dump(R, open("results/results.json", "w"), indent=2)
print(json.dumps({k: R[k] for k in ["market_map"]}, indent=2)); print(json.dumps(R["unit_economics"]["cost_down_scenario"], indent=2))
print("triangulation", round(R["revenue_triangulation"]["low"], 2), round(R["revenue_triangulation"]["high"], 2))
print(R["unit_economics"]["max_stack_cost_for_50pct_margin_c"], R["unit_economics"]["max_stack_cost_for_70pct_margin_c"])
