Subject: Lead database migration – audit complete, database design ready

Hi,

Quick update on the data migration project.

1. Audit completed
- All 23 archives (111 GB zipped, ~424 GB unzipped) have been inventoried and profiled without modifying anything on your Drive. In total that is 28 archives, including 5 zip files nested inside others, with 6,641 data files (CSV, Excel and JSON).
- We found 436 different column layouts across the sources. About 99% of the rows are person-level contacts (name, title, email, phone, LinkedIn); the rest are company data.

2. Duplicates found
- People Data Labs: the 63 GB JSON file and the 417 CSV chunks contain the same records, so it will be imported once (~416M records).
- Copied files: 988 files appear in more than one archive (~5.3 GB). Examples: LeadRocks and NinjaLeads files inside "USA Database Business Leads", AgTech files inside "Entire Apollo", and the Pitchbook and Seamless zips nested inside other archives. Each will be imported once, with a record of every place it appeared.
- Ecommerce: as mentioned earlier, the Shopify folder is a copy of the WooCommerce data.
- Record level: the same person or company appearing across different vendors will be matched during the import (by email, LinkedIn URL and website domain). Uncertain matches will not be merged automatically.

3. Data quality notes
- Some files have shifted columns or repeated header rows inside the data.
- Phone numbers were stored as numbers by Excel, and some cells hold several emails or phones.
- One Pitchbook file is empty.
- Problem values will be logged separately, not silently dropped.
- The "Entire LinkedIn Database" is the oldest source: its own "Last Updated" column shows 2018–2020.

4. Database design (attached)
- A normalized PostgreSQL design: people, companies, emails, phones, social profiles, funding and email verification.
- Every record keeps a reference to its exact source file and row.
- When sources disagree, the most recent source wins. Sources are ranked by data date (attached datasets.csv); all original values are kept.
- The design has been tested on a local PostgreSQL instance.

5. Next steps
1) A pilot import of one dataset ("Fresh Apollo Leads", ~600K rows) to measure import speed and actual storage size.
2) Based on the pilot, a recommendation for the Render PostgreSQL plan. Current rough estimate: 300–500 GB.
3) The full import, run from a cloud server, since the data is too large to process from a laptop.

What we need from you
1) Please review the attached source ranking (datasets.csv). If you know the actual collection date of any dataset, please share it, as it decides which source wins when values conflict.
2) For the full import we will need a cloud server and a Render PostgreSQL database. We can share exact specs after the pilot.
3) Please confirm that you are authorised to store and process the personal contact data in these datasets (names, emails, phone numbers), as it will be hosted in a database.

Attachments:
- schema_design.md – database design and decisions
- erd.md – table diagram
- datasets.csv – source ranking by data date
- file_duplicates.md – duplicate files found

Thanks!
