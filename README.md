# The Day's News — 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/KaiserHxZ/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/KaiserHxZ/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A one-page newspaper front page summing up the world's news of
Saturday 21 November 2026, drawn entirely in code — no AI-generated
text, so every headline stays crisp and legible.

## The stories

- **Kyiv, Ukraine — War (lead):** Russia's massive overnight strikes hit
  Kyiv — more than 400 drones and 110 missiles fired; three bridges over
  the Dnipro shut; power cut in 11 regions. (AP / BBC)
- **Shenzhen — Diplomacy:** Trump, Xi and Putin's trilateral declaration
  backs UN reform, nuclear-risk talks and more oil; Trump tells Europe's
  allies Putin "wants a deal". (AP / Reuters)
- **Odisha, India — Weather:** Cyclone Akvan weakens after crossing the
  Odisha coast near Gopalpur; more than 300,000 evacuated, no deaths
  reported. (India Meteorological Department / Reuters)
- **Wellington — Sport:** KL Rahul's century lifts India to 255 for 1 on
  Day 3 of the first Test, chasing New Zealand's 368. (Reuters)
- **Virginia, USA — Health:** Virginia's first measles-associated death
  of 2026 — a child under five; 220 cases recorded in the state this
  year. (Virginia Dept. of Health / Reuters)

Also today: Denmark expels Russia's defence attaché; the S&P 500 enters
correction as AI shares slide; GTA VI sets a $3.79bn first-day sales
record.

## How it is built

`draw.py` renders `entry.png` (1024×1024) with Pillow: masthead, date,
headlines, decks and all pictograms are drawn in code with DejaVu fonts.
`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png` at grade time, so both grader runs write identical
bytes.

Run locally:

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
