# India Voice AI Agents: Market Map and Investment Memo

An early-stage investor's view of Indian voice AI agents: who is building what, where the money has gone, what the unit economics of a voice-agent platform look like, what a seed investment needs to return, and what to ask in technical diligence.

I built and ran a production voice AI calling agent at Tru Estate (1 lakh+ calls a day), so the cost and latency questions below come from operating one, not only from reading about them.

**Data:** `data/companies.csv` holds 10 companies. Every funding figure and metric comes from a public announcement linked in the file. Prices come from Bolna's public pricing page. Anything marked **ESTIMATE** or **SCENARIO** is my calculation on stated assumptions, not a reported number.

![summary](results/summary.png)

## Market map

| Layer | What it does | Companies | Latest disclosed round |
|---|---|---|---|
| **Infrastructure** | Telephony and customer-engagement rails that voice agents run on | Exotel | $40M Series D (Jan 2022) |
| **Models + platform** | Own speech and language models (STT, TTS, LLM) for Indian languages, plus an agent platform on top | Sarvam AI, Smallest.ai, Gnani.ai, Navana.ai | $234M (Sarvam, Series B first close, Jun 2026), $13M (Smallest.ai, Series A, 2026), $10M (Gnani, Series B, Mar 2026), INR 40 crore, about $4.5M (Navana, Series A, Sep 2026) |
| **Orchestration** | Self-serve tooling to build, deploy and monitor agents; routes each call across third-party models | Bolna | $6.3M seed (Jan 2026) |
| **Applications** | Agents and suites sold for a business outcome: lead qualification, collections, renewals, support, analytics | Uniphore, Ringg AI, Skit.ai, Vodex | $260M (Uniphore, Series F, Oct 2025), $10M (Ringg, Series A extension, Aug 2026), $23M (Skit, Series B, Sep 2021), $2M (Vodex, seed, Apr 2024) |

**Why these 10:** the best-known funded companies in each layer, with a public announcement for the latest round. They cover every layer from telephony to end applications, and six of the ten raised in 2026. It is a map, not a census; see Limitations.

## Key findings

| Area | Finding | Investment read |
|---|---|---|
| Where the money went | The 10 latest rounds total **$603M**. Two rounds, Uniphore and Sarvam, take **82%**; the median of the other eight is **$10M**. **6 of the 10** latest rounds closed in 2026. | Big cheques go to scaled platforms; the rest of the market is still at seed and Series A sizes, where an early fund can enter |
| Traction | Bolna went from 1.5K to **200K+ calls a day** with **1,050+ paying customers**; Sarvam reports **2M+ interactions a day**; Navana, **100M+ minutes** served; Exotel reported **$50M ARR** at its 2022 round (all company figures). | Demand is real; the open question is who keeps the margin |
| Unit economics | Bolna's public price is **4.2–6.0 US cents a minute** for STT + LLM + TTS. To keep a **50%** gross margin on the AI stack, the stack must cost under **2.1–3.0c** a minute; for **70%**, under **1.3–1.8c**. | Orchestration margins depend on falling model prices, which the platform does not control |
| Cost-down lever (SCENARIO) | At the lowest public price (4.2c), cutting an assumed 3.5c stack cost by **75%** lifts margin from **17% to 79%**. | Whoever owns cost and latency (own models, routing, caching) owns the margin; ask every founder for their cost per minute |
| Revenue size (ESTIMATE) | 200K calls a day at 1–3 minutes a call and 4.2–6.0c a minute implies **$3.1M–13.1M** of annualised AI-stack revenue for Bolna. Revenue is not disclosed. | Sizes the business from public numbers; confirm with the founder's real minutes and price mix |
| Valuation | Sarvam's round: **$234M at $1.5B post-money**, so a **$1.27B pre-money** and **15.6% dilution**. Uniphore raised **$260M at a flat $2.5B**, the same post-money as its 2022 round, so existing holders' stake value fell **10.4%**. | Even a sector leader can raise flat; entry price matters |
| Returns (SCENARIO) | A **$1M seed cheque at a $30M post-money** owns **3.3%**, diluted to **1.9%** by exit. Returning **10x** needs a **$522M exit**, or about **$52M ARR** at a 10x revenue multiple: **4–17x** Bolna's estimated revenue today. | A seed bet here must believe in a path to $50M+ ARR; that sets the bar for diligence |

The full margin grid (stack cost 0.5–5.0c against the three public price points) is in `results/margin_grid.csv`.

## Valuation and returns model

**Reported rounds.** For a round with a disclosed valuation:

- pre-money = post-money − new money
- dilution to existing holders = new money ÷ post-money
- value change for existing holders = this round's pre-money ÷ the previous round's post-money − 1

| Round | New money | Post-money | Pre-money | Dilution |
|---|---|---|---|---|
| Sarvam AI, Series B first close (Jun 2026) | $234M | $1.5B | $1.27B | 15.6% |
| Uniphore, Series F (Oct 2025) | $260M | $2.5B (flat on 2022) | $2.24B | 10.4% |

**Seed returns (SCENARIO).** Where:

- C = cheque size ($1M), P = seed post-money valuation
- d_i = dilution in each later round, M = target return multiple (10x), k = exit revenue multiple (10x)

the model computes:

- ownership at entry = C ÷ P
- ownership at exit = C ÷ P × Π(1 − d_i)
- exit value needed = M × C ÷ ownership at exit
- ARR needed = exit value needed ÷ k

Later dilution: Series A 20% and ESOP top-ups 5% (assumptions); Series B 15.6% and Series C 10.4% (set to the real Sarvam and Uniphore rounds). Together the later rounds leave the seed investor with **57%** of the entry stake.

| Seed post-money (P) | Ownership at entry | Ownership at exit | Exit needed for 10x | ARR needed at 10x revenue |
|---|---|---|---|---|
| $20M | 5.0% | 2.9% | $348M | $35M |
| $30M | 3.3% | 1.9% | $522M | $52M |
| $40M | 2.5% | 1.4% | $696M | $70M |

## Investment view

1. **Model layer: a capital game.** Owning Indian-language speech models gives cost and latency control and a sovereignty story (Gnani's IndiaAI Mission selection, Navana's on-premise models for regulated banks). It also needs large rounds and compute. For a seed or Series A fund, entry is hardest here.
2. **Orchestration layer: fast growth, margin risk.** Self-serve platforms grow quickly but resell other providers' models. The bet is that routing, evals and observability become the product, and that model prices keep falling faster than the platform's own prices.
3. **Application layer: outcome pricing.** Selling "renewals recovered" or "leads qualified" instead of minutes can protect margin, as long as the agent beats a human team on cost per outcome. Customer concentration and integration depth (CRM, telephony, payments) decide defensibility. Uniphore's flat round is a reminder that scale alone does not guarantee a markup.
4. **Infrastructure layer: the toll road.** Telephony providers such as Exotel earn on every call whichever agent wins, but their growth depends on minutes moving from human agents to AI agents.

## Technical diligence checklist

| Area | What to ask or check |
|---|---|
| Latency | End-to-end response time (p50 and p95) on a real phone line, not in a demo; where the time goes across STT, LLM and TTS |
| Languages | Word error rate by language and accent; Hinglish and code-mixed speech; noisy lines |
| Model choices | Own models vs third-party APIs; cost per minute today and the plan to lower it; dependence on a single provider |
| Data pipelines | How call recordings and transcripts are stored, labelled and fed back into prompts or models; consent and data residency |
| Evals and observability | How a bad call is detected; which KPIs are tracked per call (containment, transfer to a human, task success); how a fix is tested before release |
| Infrastructure | Concurrency limits, telephony partners, uptime, fallbacks when a model provider fails |
| Reliability and safety | Guardrails on what the agent can promise; handling of payments and personal data; compliance with telecom rules on automated calls |

## Questions for founders

1. What is your fully loaded cost per minute today, and what was it 6 months ago?
2. What share of your revenue comes from the top 5 customers?
3. Which provider would hurt most if it raised prices or failed, and how fast could you switch?
4. What is your p95 latency and word error rate on your three biggest languages?
5. How do you price: per minute, per call or per outcome? What happens to gross margin as customers scale?

## Method

- **Market map:** companies grouped by the layer they mainly sell. Funding = latest disclosed round only, not total raised, so totals understate cumulative funding.
- **Gross margin** = 1 − (AI stack cost per minute ÷ price per minute). Price and cost both exclude telephony and platform fees, which Bolna bills separately.
- **Revenue triangulation** = calls a day × minutes a call × price a minute × 365.
- **Currency:** Navana's INR 40 crore round is converted at INR 88 per US dollar (an assumption; reports of the USD amount differ).

## Limitations

- 10 companies, chosen as well-known funded players in each layer; not a complete census (Tracxn lists about 30 Indian voice AI startups).
- Skit.ai's and Exotel's latest disclosed rounds are from 2021 and 2022, and Uniphore is now headquartered in the US (founded in Chennai).
- Company metrics (calls, customers, ARR) are self-reported in announcements and not independently verified.
- The AI stack cost per minute is not public for any company, so margins are shown as a grid of scenarios, not as one figure.
- One price list (Bolna) anchors the economics; enterprise contracts are usually negotiated lower.
- The returns model uses assumed seed valuations, an assumed 10x revenue multiple at exit, and ignores liquidation preferences, which would lower a seed investor's payout in a small exit.

## Outputs

- `results/results.json`: every number in this README
- `results/margin_grid.csv`: gross margin by stack cost and price
- `results/summary.png`: the four charts above

## Run it

```bash
pip install pandas numpy matplotlib
python run_analysis.py   # writes everything in results/
```

## Sources

Links for every company row are in `data/companies.csv` (BusinessToday, Inc42, YourStory, Business Standard, Entrepreneur India, and the Smallest.ai and Bolna company pages). Prices: bolna.ai/pricing, read in November 2026.
