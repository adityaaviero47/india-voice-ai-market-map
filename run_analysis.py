"""India voice AI agents: market map, unit economics, a revenue triangulation and a valuation / VC returns model,
for an early-stage investment memo.
Inputs: data/companies.csv (every row sourced from a public announcement, link in the file) and Bolna's public
per-minute prices. Everything marked ESTIMATE or SCENARIO is a calculation on stated assumptions, not a reported figure.
python run_analysis.py"""
import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = {}
c = pd.read_csv("data/companies.csv")

# ---------- 1. market map ----------
total = c.round_usd_m.sum()
L = c.groupby("layer").agg(companies=("company", "size"), latest_rounds_usd_m=("round_usd_m", "sum"))
L["share"] = L.latest_rounds_usd_m / total
top2 = c.nlargest(2, "round_usd_m")
rest = c.drop(top2.index)
R["market_map"] = dict(companies=len(c), layers=L.reset_index().to_dict("records"), latest_rounds_total_usd_m=float(total),
                       top2=list(top2.company), top2_share=float(top2.round_usd_m.sum() / total),
                       median_round_excl_top2_usd_m=float(rest.round_usd_m.median()),
                       rounds_in_2026=int(c.round_date.astype(str).str.startswith("2026").sum()))

# ---------- 2. unit economics per minute (SCENARIO) ----------
# Revenue: Bolna's public prices per minute, which bundle speech-to-text, the LLM and text-to-speech
# (telephony and a platform fee are billed on top, so they are left out of both price and cost here).
PRICES = {"Pay-as-you-go (6.0c)": 0.060, "Pilot, $300 (4.6c)": 0.046, "Pilot, $500 (4.2c)": 0.042}
# Cost: the provider's own cost of the AI stack per minute is not public, so it is a range to test.
COSTS = np.round(np.arange(0.005, 0.0501, 0.005), 3)
# gross margin = 1 - cost per minute / price per minute
grid = pd.DataFrame({k: [1 - cost / p for cost in COSTS] for k, p in PRICES.items()}, index=[f"{x*100:.1f}c" for x in COSTS])
R["unit_economics"] = dict(
    gross_margin_grid={i: {k: round(float(v), 3) for k, v in row.items()} for i, row in grid.iterrows()},
    max_stack_cost_for_50pct_margin_c={k: round(p * 0.5 * 100, 2) for k, p in PRICES.items()},
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

# ---------- 4. valuation, dilution and VC returns ----------
# 4a. reported rounds with a disclosed post-money valuation
#     pre-money = post-money - new money; dilution to existing holders = new money / post-money
v = c.dropna(subset=["valuation_usd_m"])
R["valuation"] = {r.company: dict(round=r.latest_round, new_money_usd_m=r.round_usd_m, post_money_usd_m=r.valuation_usd_m,
                                  pre_money_usd_m=r.valuation_usd_m - r.round_usd_m, dilution=r.round_usd_m / r.valuation_usd_m)
                  for r in v.itertuples()}
# Uniphore's Series F was flat on its 2022 Series E post-money of $2.5B: existing holders' stake value changes by pre / previous post - 1
R["valuation"]["Uniphore"]["previous_post_money_usd_m"] = 2500
R["valuation"]["Uniphore"]["value_change_for_existing_holders"] = R["valuation"]["Uniphore"]["pre_money_usd_m"] / 2500 - 1
# 4b. SCENARIO: a $1M seed cheque, diluted by later rounds; exit value needed for a 10x return
#     ownership at entry = cheque / post-money; ownership at exit = entry x product of (1 - dilution of each later round)
#     exit needed = target multiple x cheque / ownership at exit; ARR needed = exit needed / exit revenue multiple
CHEQUE, TARGET, EXIT_MULT = 1.0, 10, 10
LATER = {"Series A": 0.20, "Series B": 0.156, "Series C": 0.104, "ESOP top-ups": 0.05}   # B and C set to Sarvam's and Uniphore's real dilution
keep = float(np.prod([1 - x for x in LATER.values()]))
ret = {}
for post in [20, 30, 40]:
    own0 = CHEQUE / post
    own1 = own0 * keep
    exit_needed = TARGET * CHEQUE / own1
    ret[f"seed post-money ${post}M"] = dict(entry_ownership=own0, exit_ownership=own1, exit_needed_usd_m=exit_needed,
                                            arr_needed_usd_m_at_10x=exit_needed / EXIT_MULT)
R["vc_returns"] = dict(assumptions=dict(cheque_usd_m=CHEQUE, target_multiple=TARGET, exit_revenue_multiple=EXIT_MULT, later_dilution=LATER),
                       ownership_kept_after_later_rounds=keep, scenarios=ret,
                       note="SCENARIO: seed post-money values and the Series A and ESOP dilution are assumptions; "
                            "Series B and C dilution use the real Sarvam and Uniphore rounds")
mid = ret["seed post-money $30M"]
R["vc_returns"]["growth_needed_vs_bolna_estimate"] = dict(arr_needed_usd_m=mid["arr_needed_usd_m_at_10x"],
                                                          vs_low=mid["arr_needed_usd_m_at_10x"] / R["revenue_triangulation"]["low"],
                                                          vs_high=mid["arr_needed_usd_m_at_10x"] / R["revenue_triangulation"]["high"])

# ---------- 5. deal memo numbers: Bolna (see MEMO_BOLNA.md) ----------
# Reported: ARR about $0.7M and 200K+ calls a day (TechCrunch and Bolna, Jan 2026); 1,050+ paying customers.
ARR, CUST = 0.7, 1050
rev_per_call = ARR * 1e6 / (calls * 365)                       # revenue per call = ARR / (calls a day x 365)
billed_min = {k: rev_per_call / pr for k, pr in PRICES.items()}  # billed minutes per call = revenue per call / price per minute
B = dict(reported_arr_usd_m=ARR, calls_per_day=calls, revenue_per_call_usd=rev_per_call,
         implied_billed_minutes_per_call=billed_min,
         triangulation_vs_reported=dict(low=R["revenue_triangulation"]["low"] / ARR, high=R["revenue_triangulation"]["high"] / ARR),
         arr_per_paying_customer_usd=ARR * 1e6 / CUST, mrr_per_paying_customer_usd=ARR * 1e6 / CUST / 12)
# SCENARIO: a $5M cheque into a Series A, priced at 25x ARR at the time of the raise
A_CHEQUE, A_MULT = 5.0, 25
later_a = {k: LATER[k] for k in ["Series B", "Series C", "ESOP top-ups"]}
keep_a = float(np.prod([1 - x for x in later_a.values()]))
series_a = {}
for arr_at_raise in [2, 3, 5]:
    post = arr_at_raise * A_MULT
    own_exit = A_CHEQUE / post * keep_a
    series_a[f"ARR ${arr_at_raise}M at raise"] = dict(post_money_usd_m=post, entry_ownership=A_CHEQUE / post, exit_ownership=own_exit,
                                                      exit_for_5x_usd_m=5 * A_CHEQUE / own_exit, exit_for_10x_usd_m=10 * A_CHEQUE / own_exit,
                                                      arr_needed_for_5x_at_10x_revenue_usd_m=5 * A_CHEQUE / own_exit / EXIT_MULT)
B["series_a_scenario"] = dict(assumptions=dict(cheque_usd_m=A_CHEQUE, price_as_multiple_of_arr=A_MULT, later_dilution=later_a),
                              ownership_kept_after_later_rounds=keep_a, cases=series_a,
                              note="SCENARIO: ARR at the raise and the 25x ARR price are assumptions")
mid_a = series_a["ARR $3M at raise"]
B["series_a_scenario"]["growth_needed_vs_reported_arr_for_5x"] = mid_a["arr_needed_for_5x_at_10x_revenue_usd_m"] / ARR
R["bolna_deal"] = B

# ---------- charts ----------
fig, ax = plt.subplots(2, 2, figsize=(14, 9.5))
ax = ax.ravel()
o = c.sort_values("round_usd_m")
cols = {"Models + platform": "#0052CC", "Orchestration": "#E07A2F", "Applications": "#9AA5AD", "Infrastructure": "#2E8B57"}
ax[0].barh(o.company, o.round_usd_m, color=[cols[x] for x in o.layer]); ax[0].set_xscale("log")
for i, (val, dte) in enumerate(zip(o.round_usd_m, o.round_date)): ax[0].text(val * 1.1, i, f"${val:g}M ({dte})", va="center", fontsize=8)
ax[0].set_xlim(1, 3000); ax[0].set_xlabel("Latest disclosed round (USD million, log scale)")
ax[0].set_title("Latest rounds: blue = models, green = infrastructure,\norange = orchestration, grey = applications", fontsize=10)
ax[1].imshow(grid.to_numpy() * 100, aspect="auto", cmap="RdYlGn", vmin=-20, vmax=100)
ax[1].set_xticks(range(len(PRICES))); ax[1].set_xticklabels([k.split(" (")[0] + "\n" + k.split("(")[1].rstrip(")") for k in PRICES], fontsize=8)
ax[1].set_yticks(range(len(grid))); ax[1].set_yticklabels(grid.index, fontsize=8); ax[1].set_ylabel("AI stack cost per minute (scenario)")
for i in range(len(grid)):
    for j in range(len(PRICES)): ax[1].text(j, i, f"{grid.iloc[i, j]*100:.0f}%", ha="center", va="center", fontsize=7)
ax[1].set_title("Gross margin on the AI stack, by price and cost", fontsize=10)
lo = [tri[f"{m} min/call"]["Pilot, $500 (4.2c)"] for m in [1, 2, 3]]; hi = [tri[f"{m} min/call"]["Pay-as-you-go (6.0c)"] for m in [1, 2, 3]]
x = np.arange(3)
ax[2].bar(x - .2, lo, .4, color="#9AA5AD", label="at 4.2c/min"); ax[2].bar(x + .2, hi, .4, color="#0052CC", label="at 6.0c/min")
for i in range(3): ax[2].text(i - .2, lo[i] + .2, f"${lo[i]:.1f}M", ha="center", fontsize=8); ax[2].text(i + .2, hi[i] + .2, f"${hi[i]:.1f}M", ha="center", fontsize=8)
ax[2].axhline(ARR, color="#C0392B", lw=1.5, ls="--", label=f"reported ARR, Jan 2026 (${ARR}M)")
ax[2].set_xticks(x); ax[2].set_xticklabels(["1 min/call", "2 min/call", "3 min/call"]); ax[2].legend(fontsize=8)
ax[2].set_ylabel("Annualised AI revenue (USD million)")
ax[2].set_title("Bolna at 200K calls/day: list-price estimate vs reported ARR", fontsize=10)
names = list(ret); ex = [ret[n]["exit_needed_usd_m"] for n in names]
ax[3].bar(range(3), ex, color="#0052CC", width=.5)
for i, n in enumerate(names):
    ax[3].text(i, ex[i] + 12, f"${ex[i]:.0f}M exit\n(ARR ${ret[n]['arr_needed_usd_m_at_10x']:.0f}M at 10x)\n{ret[n]['exit_ownership']*100:.2f}% owned at exit", ha="center", fontsize=8)
ax[3].set_xticks(range(3)); ax[3].set_xticklabels([n.replace("seed post-money ", "Seed post-money\n") for n in names], fontsize=8)
ax[3].set_ylim(0, max(ex) * 1.3); ax[3].set_ylabel("Exit value needed (USD million)")
ax[3].set_title("Scenario: exit value a $1M seed cheque needs to return 10x", fontsize=10)
for a in (ax[0], ax[2], ax[3]): a.spines[["top", "right"]].set_visible(False)
plt.tight_layout(); plt.savefig("results/summary.png", dpi=150)

grid.to_csv("results/margin_grid.csv")
json.dump(R, open("results/results.json", "w"), indent=2, default=float)
print(json.dumps({k: R[k] for k in ["market_map", "valuation", "vc_returns"]}, indent=2, default=float))
print("triangulation", round(R["revenue_triangulation"]["low"], 2), round(R["revenue_triangulation"]["high"], 2))
