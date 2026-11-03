# Exact file duplicates (Phase 4a)

Based on CRC-32 + size from ZIP directories (no content downloaded). Same CRC and size => identical file with near certainty. Nested archives were checked separately by name + size (see profile.md).

Files checked: 5,670 (424.4 GiB uncompressed)

Duplicate groups: 827 | redundant copies: 988 | redundant data: 5.27 GiB | redundant rows (est.): ~5,514,078

## Copies shared between archives

| Archive A | Archive B | Identical files | GiB | Est. rows |
|---|---|---:|---:|---:|
| AG-AgTech Leads 103,322 | Entire Apollo Database 99,311,285 | 39 | 0.36 | 255,009 |
| LeadRocks Database 341,632 | USA Database Business Leads 9,979,021 | 459 | 0.08 | 267,364 |
| NinjaLeads Database 238,702 | USA Database Business Leads 9,979,021 | 290 | 0.07 | 363,035 |
| AG-AgTech Leads 103,322 | Seamless Database 1,547,199 | 2 | 0.03 | 37,078 |
| AG-AgTech Leads 103,322 | Chrunchbase Database 24,060 | 7 | 0.01 | 16,187 |

## Copies inside the same archive

| Archive | Redundant copies |
|---|---:|
| LeadRocks Database 341,632 | 12 |
| The Ultimate Ecommerce 7,797,171 | 10 |
| Seamless Database 1,547,199 | 8 |
| Entire Linkedin Database 434,832,484 | 2 |
| Fresh Apollo Leads 1,232,352 | 1 |
