# Investment Memo: Bolna (Series A)

*Independent analysis from public sources, written as an analyst memo for an investment committee. I have no relationship with Bolna. Numbers marked **SCENARIO** are my assumptions; every other figure comes from a public source listed at the end. All figures are as reported in January 2026, when the seed round was announced.*

## Recommendation

**Proceed to full diligence for a Series A cheque; do not issue a term sheet yet.**

Bolna has real pull: calls grew from 1.5K to 200K+ a day in about eight months. But the public numbers do not yet show whether those calls turn into durable revenue at a healthy margin. Three questions have to clear first (see "Conditions to invest").

## The company

| | |
|---|---|
| What it does | Self-serve and enterprise platform to build, deploy and monitor voice AI agents; routes each call to a suitable speech and language model; 10+ Indian languages |
| Founded | 2024, Bengaluru; founders Maitreya Wagh (CEO) and Prateek Sachan (CTO); Y Combinator, Fall 2025 |
| Funding | $6.3M seed (Jan 2026), led by General Catalyst, with Y Combinator, Blume Ventures and others; valuation not disclosed |
| Traction | 200K+ calls a day (from 1.5K in May 2025); 1,050+ paying customers; ARR about **$0.7M**; 75% of revenue self-serve; 2 enterprises paying, 4 in pilot |
| Customers | Spinny, Snabbit, Varun Beverages; mostly small and mid-sized businesses |
| Price | 4.2–6.0 US cents a minute for STT + LLM + TTS; $500 pilot plan |
| Team | 9 forward-deployed engineers, adding 2–3 a month |

## Thesis: why it could be big

1. **Model-agnostic orchestration.** Customers can switch speech and language models as better or cheaper ones appear. If model prices keep falling, Bolna keeps more of each minute without locking customers to one provider.
2. **Indian-language demand.** 30–40% of call volume is outside English and Hindi. Collections, onboarding, support and recruitment calls in regional languages are a large, under-automated market.
3. **Self-serve distribution.** 1,050+ paying customers in under two years with a small team suggests low customer acquisition cost.
4. **Forward-deployed engineers for enterprises.** This is the path from $56 a month customers to six-figure contracts.

## The key diligence finding: calls do not equal revenue

At list price, 200K calls a day should produce far more revenue than Bolna reports.

- **List-price estimate:** calls a day × minutes a call × price a minute × 365 = **$3.1M–13.1M** a year for 1–3 minute calls.
- **Reported ARR:** about **$0.7M**, **4–19x lower**.
- **Revenue per call** = ARR ÷ (calls a day × 365) = $0.7M ÷ (200K × 365) ≈ **1.0 cent**.
- **Billed minutes per call** = revenue per call ÷ price a minute ≈ **0.16–0.23 minutes**, or about 10–14 seconds.

So either most calls are very short or unanswered (common in outbound calling), many minutes are billed below list price (for example through bring-your-own-key plans or free credits), or call volume grew faster than the ARR figure was updated. Each explanation has a different meaning for the business, and the founders need to show which one it is.

**Revenue per customer** = $0.7M ÷ 1,050 ≈ **$667 a year, or about $56 a month**. The base is broad but shallow, which is why the enterprise motion matters.

## Unit economics

Gross margin on the AI stack = 1 − (AI cost per minute ÷ price per minute).

- At the lowest public price (4.2c), a 50% margin needs AI cost under **2.1c a minute**; at 6.0c, under **3.0c**.
- **SCENARIO:** if the AI cost is 3.5c today, margin is 17%; cutting that cost 75% lifts it to 79%. Cost per minute, and its trend, is the single most important number to collect in diligence.

## Valuation and returns (SCENARIO)

Assumptions: a **$5M** cheque; the round priced at **25x ARR** at the time of the raise; later dilution of 15.6% (Series B) and 10.4% (Series C), the real dilution in Sarvam's and Uniphore's latest rounds, plus 5% for ESOP top-ups. That leaves the investor with 72% of the entry stake.

Where C = cheque, P = post-money valuation, d_i = dilution in each later round:

- ownership at exit = C ÷ P × Π(1 − d_i)
- exit needed for a return of M times = M × C ÷ ownership at exit

| ARR at the raise | Post-money | Ownership at entry | At exit | Exit for 5x | Exit for 10x |
|---|---|---|---|---|---|
| $2M | $50M | 10.0% | 7.2% | $348M | $696M |
| $3M | $75M | 6.7% | 4.8% | $522M | $1.04B |
| $5M | $125M | 4.0% | 2.9% | $870M | $1.74B |

In the middle case, a 5x return needs a **$522M exit**: about **$52M ARR** at a 10x revenue multiple, roughly **75x** the reported ARR. That is the bar Bolna must clear to be a fund-returning Series A investment.

## Risks

| Risk | Why it matters | What would reduce it |
|---|---|---|
| Revenue per call | 1 cent a call may mean most volume earns little | Billed minutes per call and revenue by plan, month by month |
| Margin dependence | Reselling third-party models; a provider price rise squeezes margin | Cost per minute trend; share of minutes on cheaper or own models |
| Competition | Global platforms (Vapi, LiveKit) and Indian model builders (Sarvam, Gnani) moving into agents | Win rates against named rivals; Indian-language quality benchmarks |
| Self-serve churn | 75% of revenue from small customers who can leave easily | Monthly logo and revenue retention by cohort |
| Enterprise conversion | Only 2 enterprises paying, 4 in pilot | Pilot-to-paid conversion and contract sizes |
| Regulation | Telecom rules on automated and promotional calls | Consent handling, call registration, compliance record |

## Conditions to invest

1. **Revenue quality:** billed minutes per call and revenue per call explained and stable, with net revenue retention above 100% for the self-serve base.
2. **Margin:** blended gross margin on the AI stack of 50% or more, with a falling cost per minute.
3. **Enterprise proof:** at least half of the enterprise pilots converted to paid contracts, with a clear path to the ARR the returns table needs.

## Questions for the founders

1. What is your billed minutes per call, and how much call volume is unanswered or under 10 seconds?
2. What is your blended cost per minute today, and what was it six months ago?
3. What is monthly net revenue retention for self-serve customers who joined in 2025?
4. Of the four enterprise pilots, which convert, at what contract size, and when?
5. If your largest model provider doubled its price, what would happen to gross margin, and how fast could you switch?

## Sources

- Bolna newsroom, seed round announcement (Jan 2026): https://www.bolna.ai/newsroom/bolna-bags-63-million-seed-funding-led-by-general-catalyst-to-build-indias-voice-ai-platform
- TechCrunch, "Bolna nabs $6.3 million from General Catalyst…" (20 Jan 2026): https://techcrunch.com/2026/01/20/bolna-nabs-6-3-million-from-general-catalyst-for-its-india-focused-voice-orchestration-platform/
- Bolna pricing page, bolna.ai/pricing (read Nov 2026)
- Sarvam AI and Uniphore rounds: links in `data/companies.csv`

The numbers in this memo are produced by `run_analysis.py` and stored in `results/results.json` under `bolna_deal`.
