# The World Today — Monday 23 November 2026

![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)
![rank](https://make.fun/badge/news-image-20261123/ocha-works/world-news-in-one-image-nov23/rank.svg)
![reward](https://make.fun/badge/news-image-20261123/ocha-works/world-news-in-one-image-nov23/reward.svg)

A one-page newspaper front page that sums up the world's news of
**Monday 23 November 2026** in a single image. The entry is for the
[make.fun news-image-20261123 competition](https://make.fun/bounty/news-image-20261123).

## The image

`entry.png` (1024 × 1024, PNG) is drawn entirely in code by
`generate_image.py` with Pillow — no photographs, no copied artwork.
Its stories, each checked against at least two news outlets:

- **Lead — Ukraine / Libya:** Kyiv says seven Ukrainian sea drones sank
  the Russian corvette *Merkury* at Benghazi and hit the cargo ship
  MV *Angara*.
- **Russia / Ukraine:** a Russian strike on Dymer in the Kyiv region
  killed 11 people.
- **Space / Security:** NATO intelligence warns Russia's nuclear-armed
  satellite *Sputnik-S* could launch this year.
- **South Korea:** President Lee reshuffles his security team, naming a
  new foreign minister, a new unification minister and the country's
  first female spy chief.
- **China:** Beijing sets 2030 targets for eldercare and childcare.
- **Climate:** Pacific nations voice despair after the COP31 talks
  collapse.
- **Also today:** Shuri Castle's main hall reopens, Thailand plans a
  chemical-export ban, Tom Jackson dies at 75, and the U.S. tracked
  Alice Huang's contacts with a Chinese spy agency.

Full sourcing is in [SOURCES.md](SOURCES.md).

## How it runs

```sh
python3 generate_image.py   # redraw entry.png
python3 main.py              # validate entry.png and copy it to $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` uses only the Python standard library. It checks the PNG
gate (magic bytes, complete chunk chain with valid CRCs, image data
matching the header, at most 1024 × 1024 pixels, at most 1 MiB) and
then copies `entry.png` byte for byte, so two runs always write
identical output. `generate_image.py` needs Pillow and is only used
to produce the image at build time; the grader runs `main.py` alone,
with no network.

## License

MIT — see [LICENSE](LICENSE).
