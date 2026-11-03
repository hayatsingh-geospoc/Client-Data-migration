# Dataset recency and ranking

Survivorship rule (decided 2026-10-31): when sources disagree, the value from the dataset with the better (lower) priority wins; priority is assigned by how recent each dataset's data is.

`data_as_of` = date in file/folder names if any, else newest sampled row date, else median file time inside the ZIP. ZIP file times show when the export files were written, which bounds how old the data is; they are not a guarantee of collection date.

| Priority | Dataset | Kind | data_as_of | Basis | Name dates | ZIP file times | Sampled row dates |
|---:|---|---|---|---|---|---|---|
| 1 | Fresh Apollo Leads 1,232,352 | person | 2025-09-24 | median file time inside the ZIP |  | 2025-09-22 .. 2025-09-24 (median 2025-09-24) |  |
| 2 | Phone Leads 321,562 | company | 2025-09-22 | median file time inside the ZIP |  | 2025-09-22 .. 2025-09-28 (median 2025-09-22) |  |
| 3 | Real Estate Agents 830K | person | 2025-09-20 | file/folder names (2 of 2 files dated) | 2025-09-20 .. 2025-09-20 | 2025-09-26 .. 2025-09-26 (median 2025-09-26) |  |
| 4 | Pitchbook 2025-09-14 | person | 2025-09-14 | file/folder names (1 of 34 files dated) | 2025-06-21 .. 2025-09-14 |  |  |
| 5 | The Ultimate Ecommerce 7,797,171 | company | 2025-07-30 | median file time inside the ZIP |  | 2025-07-30 .. 2025-07-30 (median 2025-07-30) |  |
| 6 | LinkedIn - 945,237 | person | 2025-07-06 | median file time inside the ZIP |  | 2025-07-01 .. 2025-07-06 (median 2025-07-06) |  |
| 7 | Company Using X Technology - 10,135,706 | company | 2025-07-02 | median file time inside the ZIP |  | 2025-07-02 .. 2025-07-02 (median 2025-07-02) |  |
| 8 | Instagram - 843,613 | company | 2025-06-29 | median file time inside the ZIP |  | 2025-06-29 .. 2025-06-29 (median 2025-06-29) |  |
| 9 | People Datalabs Database 415,821,844 | person | 2025-06-23 | median file time inside the ZIP |  | 2020-08-03 .. 2025-06-23 (median 2025-06-23) |  |
| 10 | Pitchbook 2025-06-21 | company | 2025-06-21 | file/folder names (0 of 349 files dated) | 2025-06-21 .. 2025-06-21 |  |  |
| 11 | High Quality B2B Leads 31,457,250 | person | 2025-06-16 | median file time inside the ZIP |  | 2025-06-16 .. 2025-06-16 (median 2025-06-16) |  |
| 12 | Clutch.co Database 194,257 | company | 2025-04-28 | median file time inside the ZIP |  | 2025-04-27 .. 2025-06-23 (median 2025-04-28) |  |
| 13 | Seamless Database 1,547,199 | person | 2025-01-29 | file/folder names (1 of 582 files dated) | 2025-01-29 .. 2025-01-29 | 2025-01-30 .. 2025-06-23 (median 2025-06-23) | 2024-04-30 .. 2024-08-30 |
| 14 | AG-AgTech Leads 103,322 | person | 2024-11-21 | file/folder names (31 of 115 files dated) | 2024-08-31 .. 2024-11-21 | 2024-08-31 .. 2025-03-08 (median 2024-09-09) |  |
| 15 | Chrunchbase Database 24,060 | company | 2024-11-21 | file/folder names (6 of 7 files dated) | 2024-08-31 .. 2024-11-21 | 2024-08-31 .. 2024-11-21 (median 2024-08-31) |  |
| 16 | Entire Apollo Database 99,311,285 | person | 2024-09-09 | median file time inside the ZIP |  | 2020-11-18 .. 2024-09-25 (median 2024-09-09) |  |
| 17 | Almost Full Crunchbase Database 2,807,492 | company | 2024-08-26 | median file time inside the ZIP |  | 2024-08-26 .. 2024-08-26 (median 2024-08-26) |  |
| 18 | Getlanka Database 24,404 | person | 2024-07-15 | median file time inside the ZIP |  | 2024-06-29 .. 2024-07-31 (median 2024-07-15) |  |
| 19 | Apollo Software Development Leads 111,582 | person | 2024-06-12 | median file time inside the ZIP |  | 2024-05-28 .. 2025-06-23 (median 2024-06-12) |  |
| 20 | LeadRocks Database 341,632 | person | 2024-03-13 | file/folder names (549 of 642 files dated) | 2022-07-31 .. 2024-03-13 | 2025-06-23 .. 2025-06-23 (median 2025-06-23) |  |
| 21 | USA Database Business Leads 9,979,021 | person | 2023-07-18 | file/folder names (535 of 2195 files dated) | 2022-06-01 .. 2023-07-18 | 2025-09-03 .. 2025-09-03 (median 2025-09-03) |  |
| 22 | NinjaLeads Database 238,702 | person | 2023-03-01 | file/folder names (6 of 731 files dated) | 2022-08-01 .. 2023-03-01 | 2025-06-23 .. 2025-06-23 (median 2025-06-23) |  |
| 23 | Entire Linkedin Database 434,832,484 | person | 2020-12-01 | newest sampled row date (Last Updated) |  | 2025-06-23 .. 2025-06-23 (median 2025-06-23) | 2018-08-20 .. 2020-12-01 |
