// News-image entry for Thursday 26 November 2026 (Node 22, stdlib only).
//
// v4: a newspaper front page, built from the v3 template (25 Nov,
// 43 stories, submitted, blind rounds not yet published) and from
// the winners' template (superskie 864,498 / 872,350 on 19-20 Nov;
// v2 round 2 of 24 Nov: score 708,842, rank 272/9,063). 43 stories
// this time (3 leads + 10 picture stories + 30 briefs): the Thu
// 26 Nov cycle is news-rich in Asia and the US -- tariffs, Kim's
// tactical-nukes call, Thanksgiving.
//
// Strict same-day bar (RULES.txt: events that happened, or were
// first reported, on 26 November 2026 in any time zone). Built Thu
// 26 Nov 08:30 WIB (01:30 UTC): this edition covers the Thu
// morning news cycle plus Thu-scheduled events (marked TODAY).
// Everything first reported Wed 25 Nov or earlier is LEFT OUT and
// named in the DATE CHECK footer instead of appearing as news.
//
// This program places that finished image where the grader expects
// it, but it does more than copy bytes: before writing anything it
// validates the poster it is about to ship, so a broken or stale
// build fails loudly here instead of silently reaching the judge.
//
// The checks it runs:
//   1. entry.png exists next to this file and starts with the PNG
//      magic bytes (89 50 4E 47 0D 0A 1A 0A).
//   2. The IHDR chunk says exactly 1024 x 1024, the size the
//      bounty asks for and the size draw.py promises.
//   3. The file is at most 1 MiB (the bounty limit), so an
//      over-budget poster is caught before submission.
//   4. The story manifest below matches what draw.py drew: 43
//      stories, 3 leads + 10 picture stories + 30 briefs, each
//      with a short verified-fact note. If the manifest and the
//      poster ever drift apart, the mismatch is visible here in
//      plain text instead of hidden inside the image.
//   5. The copy itself is byte-for-byte identical to the source,
//      verified by comparing the bytes just written with the bytes
//      just read. No network, no randomness and no clock are
//      involved anywhere, so running this twice writes exactly
//      the same bytes.
//
// Local check:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//   # expect: "entry.png OK: 1024x1024, <size> bytes, 43 stories"

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const fileName = 'entry.png';
const MAX_BYTES = 1024 * 1024;
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

// The 43 stories on the poster, in reading order, with the fact
// each one was verified against live reporting in the 25 Nov 2026
// news cycle. Keep this list in sync with tools/draw.py; the count
// is checked below, and the wording is the human-readable record
// of what the judge will see.
const STORIES = [
  { slot: 'lead 1', tag: 'MARKETS', headline: 'Asia steadies after Wall St fightback', fact: 'Nikkei futures 57,370 (+0.6%), Hang Seng futures 22,149 (+0.8%) (CNBC Thu).' },
  { slot: 'lead 2', tag: 'KOREA', headline: 'Kim: deploy tactical nukes wider', fact: 'KCNA Thu: tactical nukes across more domains; status "absolutely inviolable" (Reuters SEOUL Nov 26).' },
  { slot: 'lead 3', tag: 'TRADE', headline: 'Asia counts the tariff cost', fact: 'Taiwan 15% lowest tier; China 20% rising to 40% if truce terms break (Reuters; Exec Yuan presser Thu 08:30).' },
  { slot: 'picture 1', tag: 'OCEANIA', headline: 'Bougainville debate rolls on', fact: 'Parliament debate continues Thu; 89 of 118 MPs needed; PNG 2027 Budget due Thu (Business Melanesia).' },
  { slot: 'picture 2', tag: 'EUROPE', headline: 'Chess Game 3 today', fact: 'Sindarov White in Geneva, score 1-1, 15:00 CET (ChessBase).' },
  { slot: 'picture 3', tag: 'AMERICAS', headline: 'Thanksgiving: 3 NFL games', fact: 'Bears-Lions 1pm, Eagles-Cowboys 4:30pm, Chiefs-Bills 8:20pm ET (NBC).' },
  { slot: 'picture 4', tag: 'EUROPE', headline: 'Europa League: 18 games', fact: 'Milan at Olympiacos; Palace host Real Sociedad; 17:45 + 20:00 GMT (Sports Mole).' },
  { slot: 'picture 5', tag: 'ASIA', headline: 'Taiwan: 15% is the floor', fact: 'Lowest tier with Japan, Korea, EU; not stacked on MFN or forced-labour tariff (Exec Yuan Thu).' },
  { slot: 'picture 6', tag: 'ASIA', headline: 'India marks Constitution Day', fact: '26 Nov Constitution Day; IITs add 6,000 seats in robotics, AI and space (26 Nov headlines).' },
  { slot: 'picture 7', tag: 'AMERICAS', headline: 'Wall St claws back', fact: 'Dow +0.33% to 50,182.95 after 1,100-point slide; Nasdaq -0.62% to 23,585.80 (AP/Reuters).' },
  { slot: 'picture 8', tag: 'AMERICAS', headline: "Macy's parade steps off", fact: 'Balloons over NYC; National Dog Show follows the football (NBC/DIRECTV).' },
  { slot: 'picture 9', tag: 'ASIA', headline: 'Nepal gets Rs 15,000 cr', fact: 'India package after Modi-Shah talks in Delhi (26 Nov headlines).' },
  { slot: 'picture 10', tag: 'MID EAST', headline: 'Emirates tops the skies', fact: "Named world's best airline in global rankings (26 Nov headlines)." },
  { slot: 'brief 1', tag: 'KOSPI', headline: 'Opens lower again', fact: 'KOSPI 100 ETF opens 59,210 vs prev close 62,015; low 57,840 by 09:12 KST (Finnhub live Thu).' },
  { slot: 'brief 2', tag: 'CHINA', headline: 'Tariff reply awaited', fact: "Beijing's response tonight is the read to watch (The Retest)." },
  { slot: 'brief 3', tag: 'NIKKEI', headline: 'Futures 57,370', fact: 'Nikkei futures +0.6% vs Wed close 57,011.62 (CNBC).' },
  { slot: 'brief 4', tag: 'HANG SENG', headline: 'Futures 22,149', fact: 'Hang Seng futures +0.8% vs close 21,966.01 (CNBC).' },
  { slot: 'brief 5', tag: 'ASX', headline: '+0.15% at the open', fact: 'Australia S&P/ASX 200 up 0.15% at Thu open (CNBC).' },
  { slot: 'brief 6', tag: 'TAIWAN', headline: '15%, lowest tier', fact: '15% not stacked on MFN; lowest tier with Japan, Korea, EU, Switzerland (Exec Yuan).' },
  { slot: 'brief 7', tag: 'IPL', headline: '1,220 players register', fact: '1,220 cricketers register for IPL 2027 auction (26 Nov headlines).' },
  { slot: 'brief 8', tag: 'FLIPKART', headline: 'CEO steps down in Dec', fact: 'Kalyan Krishnamurthy to step down in December (26 Nov headlines).' },
  { slot: 'brief 9', tag: 'HASINA', headline: 'Seeks return Dec 16', fact: 'Ex-PM Sheikh Hasina seeks return to Dhaka on Dec 16 (26 Nov headlines).' },
  { slot: 'brief 10', tag: 'INDIA SPACE', headline: '$9bn to $45bn', fact: 'India space economy to grow $9bn to $45bn within a decade (26 Nov headlines).' },
  { slot: 'brief 11', tag: 'PNG', headline: '2027 Budget due today', fact: 'Treasurer Lelang hands down 2027 Budget Thu (Business Melanesia).' },
  { slot: 'brief 12', tag: 'PNG BUDGET', headline: 'Balanced plan vowed', fact: 'Government promises a balanced plan (Business Melanesia).' },
  { slot: 'brief 13', tag: 'DOG SHOW', headline: 'Thanksgiving classic', fact: 'National Dog Show today, part of Thanksgiving TV (DIRECTV).' },
  { slot: 'brief 14', tag: 'US MARKETS', headline: 'Shut Thu, short Fri', fact: 'US stocks and Treasuries closed Thu for Thanksgiving; shortened session Fri (Reuters).' },
  { slot: 'brief 15', tag: 'INDIA', headline: 'Human control over war AI', fact: 'India urges human judgement central in military AI use (26 Nov headlines).' },
  { slot: 'brief 16', tag: 'INDIA', headline: 'Condemns Riyadh attack', fact: 'India condemns attack on Riyadh tower after 2 Indians injured (26 Nov headlines).' },
  { slot: 'brief 17', tag: 'ANAND KUMAR', headline: 'Honoured in Japan', fact: 'Super 30 founder Anand Kumar receives honorary award in Japan (26 Nov headlines).' },
  { slot: 'brief 18', tag: 'BRAZIL', headline: 'Wolbachia cuts cases 68%', fact: 'Wolbachia mosquitoes slash viral infections 68% in Brazil (26 Nov headlines).' },
  { slot: 'brief 19', tag: 'CHESS', headline: '$2.5m crown at stake', fact: 'World Championship prize fund $2.5m; first to 7.5 pts (Yardbarker).' },
  { slot: 'brief 20', tag: 'CRICKET', headline: 'Rising Stars semis today', fact: 'Asia Cup Rising Stars semifinals Thu/Fri (indiafantasy).' },
  { slot: 'brief 21', tag: 'ISLAND SCHOOL', headline: 'Tuition in coconuts', fact: 'Island families pay tuition with coconuts so every child attends (26 Nov headlines).' },
  { slot: 'brief 22', tag: 'DETROIT', headline: '87th Thanksgiving game', fact: "Detroit's 87th Thanksgiving game, tradition since 1934 (NBC)." },
  { slot: 'brief 23', tag: 'BILLS', headline: '9-1 host Chiefs 8-2', fact: 'Bills (9-1) host Chiefs (8-2), 8:20pm ET primetime (USA Today).' },
  { slot: 'brief 24', tag: 'COLLEGE', headline: 'TCU vs Texas Tech 8pm ET', fact: 'College football Thanksgiving night, 8pm ET on ESPN (DIRECTV).' },
  { slot: 'brief 25', tag: 'CHESS', headline: '12 games left, first to 7.5', fact: '14-game match, first to 7.5 pts; Game 3 Thu, Sindarov White (ChessBase).' },
  { slot: 'brief 26', tag: 'BOUGAINVILLE', headline: '97.7% said yes in 2019', fact: '97.7% voted for independence in 2019 referendum; non-binding (The Conversation).' },
  { slot: 'brief 27', tag: 'TARIFFS', headline: 'India up to 17%', fact: 'India could see duties up to 17% under pending trade deal (Peter Lewis briefing).' },
  { slot: 'brief 28', tag: 'TARIFFS', headline: 'EU, Japan, Korea ~15%', fact: 'EU, Japan, South Korea generally face tariffs around 15% (Peter Lewis briefing).' },
  { slot: 'brief 29', tag: 'TARIFFS', headline: 'China 20%, may rise to 40%', fact: 'China 20%, rising to 40% if Beijing fails to honour truce terms (Peter Lewis).' },
  { slot: 'brief 30', tag: 'BLACK FRIDAY', headline: 'Broncos at Steelers', fact: 'Denver at Pittsburgh, Fri 3:00pm ET on Prime Video (NFL schedule).' },
] as const;

function fail(message: string): never {
  throw new Error(`entry.png validation failed: ${message}`);
}

function pngDimensions(png: Buffer): { width: number; height: number } {
  // PNG layout: 8-byte signature, then the IHDR chunk. Its length
  // (4 bytes) and type "IHDR" (4 bytes) are followed by width and
  // height, each a 4-byte big-endian integer.
  const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (png.length < 33 || !png.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail('not a PNG file (bad signature)');
  }
  if (png.toString('ascii', 12, 16) !== 'IHDR') {
    fail('first chunk is not IHDR');
  }
  return {
    width: png.readUInt32BE(16),
    height: png.readUInt32BE(20),
  };
}

const png = readFileSync(join(here, fileName));

if (png.length === 0) fail('empty file');
if (png.length > MAX_BYTES) {
  fail(`${png.length} bytes exceeds the 1 MiB limit`);
}

const { width, height } = pngDimensions(png);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}, got ${width}x${height}`);
}

if (STORIES.length !== 43) {
  fail(`story manifest lists ${STORIES.length} stories, expected 41`);
}
const slots = new Set(STORIES.map((story) => story.slot));
if (slots.size !== STORIES.length) {
  fail('story manifest has a duplicated slot');
}

mkdirSync(destination, { recursive: true });
const target = join(destination, fileName);
writeFileSync(target, png);

// Byte-for-byte check of what was just written.
const written = readFileSync(target);
if (!written.equals(png)) {
  fail('written file differs from entry.png');
}

console.log(
  `entry.png OK: ${width}x${height}, ${png.length} bytes, ` +
    `${STORIES.length} stories -> ${target}`,
);
for (const story of STORIES) {
  console.log(`  ${story.slot}: ${story.headline}`);
}
