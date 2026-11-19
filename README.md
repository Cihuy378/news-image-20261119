# The World in One Day — Thursday, 19 November 2026

A make.fun `news-image-20261119` entry: one 1024×1024 newspaper front page
that sums up the world's news of **Thursday, 19 November 2026** — 30 verified
stories, every one reported on that day.

## The front page

**Leads**

1. **Shenzhen — Trump, Xi and Putin meet** for the first trilateral of the
   three sitting presidents, at the APEC summit; nuclear arms reduction is on
   the agenda, with a Trump–Putin bilateral to follow. (Reuters, Le Monde)
2. **GTA VI launches** at midnight local time on PS5 and Xbox — 9.69 million
   pre-orders worth $942m, Metacritic 99, eight Game Awards nominations.
   (People, Sensor Tower, The Escapist)
3. **Anthropic lists on Nasdaq as ANT** — 825m shares at $70–$78, priced
   above $80 by one report, raising up to $64bn at a ~$1.4tn valuation, the
   biggest IPO ever and the first standalone AI lab to go public.
   (Motley Fool, Wall Street Journal, Nasdaq)
4. **Berlin — the Coalition of the Willing meets** with Witkoff and Kushner
   present, as Europe fears Shenzhen could settle Ukraine's fate without it.
   (Reuters)

**The Gulf war** — coalition forces intercept two Houthi drones aimed at
Riyadh and a cruise missile targeting the capital; Saudi Arabia says the
danger has passed in three southern cities; Hormuz war-risk insurance hits
$64m; Saudis prepare for a Yemen campaign lasting into 2027; Trump warns
Iran could pay dearly over a dirty-bomb plan. (Saudi Gazette, Reuters)

**Also today** — Israel threatens more land seizures; Cyclone Akvan brings
21cm of rain to India's Andhra coast; a cocaine and pills seizure in eastern
Libya; France's justice minister says Mélenchon could win the presidency;
Carney recalibrates Canada's China ties; US senators warn AI cyber threats
are outpacing defences; Myanmar's military-backed president rethinks ASEAN
ties; Saudi PIF is named the top sovereign wealth fund brand for a third
year; Trump claims a major Philippines trade pact; a Stockholm vigil honours
children killed in Gaza; Delhi journalists tell the Supreme Court "we are
journalists, not reel makers"; a panel is planned for India's professional
leagues; Ben Duckett hits 133 in the 3rd ODI; a sunken LPG tanker off
Bulgaria was hit by projectiles; India and Japan review defence ties in
Tokyo; tougher rules are proposed for US employment green cards; Peltola's
Alaska win seals a 56–44 Senate majority; Microsoft is in talks to sell AI
services to ByteDance; oil prices fall; US–China barriers keep rising.

## How the image was made

- `compose.py` (Python 3, Pillow) draws the whole page: masthead, headlines,
  decks, briefs, rules and five small flat icons (globe, gamepad, chart,
  flag, storm) — all text is rendered by this script, so the finished image
  carries no garbled AI text. The script is deterministic: no network, no
  clock, no randomness.
- `assets/` holds four editorial illustrations generated for this entry
  (summit table, Vice City, IPO, Brandenburg Gate). They contain no text;
  every word on the page comes from `compose.py`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png`, byte for byte.

Rebuild the image: `python3 compose.py` — then test the entry program with
`mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`.

## Sources

Reuters, Associated Press, AFP, Bloomberg, CNBC, Wall Street Journal, India
Meteorological Department, People, Sensor Tower, Saudi Gazette, Le Monde,
Motley Fool, Nasdaq. Every story was verified as reported on 19 November
2026; stories dated 18 November or earlier were excluded.

## License

MIT — see `LICENSE`.
