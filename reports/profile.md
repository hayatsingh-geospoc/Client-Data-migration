# Data profile (Phase 2, sampled)

Row counts are **estimates** from a sample (bytes ratio) unless the whole file fit in the sample. Exact counts need a full streaming pass.

Files profiled: 6641 | Distinct column layouts (schemas): 436

## Status

| Kind | Status | Files |
|---|---|---:|
| delimited | ok | 5828 |
| xlsx | ok | 769 |
| macos_junk | skipped | 30 |
| nested_archive | expanded | 5 |
| delimited | empty | 5 |
| document | skipped_non_data | 2 |
| ndjson | ok | 1 |
| xlsx | empty | 1 |

## Per archive

| Archive | Files | Schemas | Est. rows | Encodings | Malformed rows (sample) | PII types | Errors | Deferred |
|---|---:|---:|---:|---|---:|---|---:|---:|
| Copy of People Datalabs Database 415,821,844.zip | 418 | 1 | 593,747,796 | utf-8-sig:418 | 0 | (json fields), name/addr/social | 0 | 0 |
| Copy of Entire Linkedin Database 434,832,484.zip | 200 | 1 | 368,714,150 | utf-8-sig:200 | 1521 | email, name/addr/social, phone | 0 | 0 |
| Copy of Entire Apollo Database 99,311,285.zip | 41 | 18 | 105,416,091 | utf-8-sig:41 | 77 | email, name/addr/social, phone | 0 | 0 |
| Copy of High Quality B2B Leads 31,457,250.zip | 30 | 2 | 31,125,281 | utf-8-sig:30 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of USA Database Business Leads 9,979,021.zip | 2195 | 120 | 10,313,261 | utf-8-sig:1892, cp1252:4 | 15535 | email, name/addr/social, phone | 0 | 0 |
| Copy of The Ultimate Ecommerce 7,797,171.zip | 21 | 1 | 8,947,985 | utf-8-sig:21 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Company Using X Technology - 10,135,706.zip | 82 | 1 | 4,072,512 | utf-8-sig:82 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Almost Full Crunchbase Database 2,807,492.zip | 59 | 1 | 2,791,423 | utf-8-sig:29 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Seamless Database 1,547,199.zip | 582 | 10 | 1,629,904 | utf-8-sig:580 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Seamless Database 1,547,199.zip :: Seamless Database 1,547,199/Seamless Search-20250129T145500Z-001.zip | 583 | 8 | 1,603,758 | utf-8-sig:581 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Pitchbook 2025-06-21.zip | 349 | 109 | 1,108,731 | utf-8-sig:343 | 65 | email, phone | 0 | 0 |
| Copy of Pitchbook 2025-09-14.zip :: Pitchbook/Pitchbook-20250621T054827Z-1-001.zip | 349 | 109 | 1,108,731 | utf-8-sig:343 | 65 | email, phone | 0 | 0 |
| Copy of Real Estate Agents 830K | 2 | 2 | 1,006,277 | utf-8-sig:1 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of LinkedIn - 945,237.zip | 9 | 2 | 759,045 | utf-8-sig:9 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Fresh Apollo Leads 1,232,352.zip | 19 | 3 | 612,075 | utf-8-sig:19 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of NinjaLeads Database 238,702.zip | 731 | 19 | 439,745 | utf-8-sig:365, cp1252:4 | 490 | email, name/addr/social, phone | 0 | 0 |
| Copy of AG-AgTech Leads 103,322.zip | 115 | 35 | 399,865 | utf-8-sig:115 | 424 | email, name/addr/social, phone | 0 | 0 |
| Copy of LeadRocks Database 341,632.zip | 642 | 121 | 341,645 | utf-8-sig:577 | 15053 | email, name/addr/social, phone | 0 | 0 |
| Copy of Instagram - 843,613.zip | 64 | 1 | 331,642 | utf-8-sig:64 | 0 | email, phone | 0 | 0 |
| Copy of Seamless Database 1,547,199.zip :: Seamless Database 1,547,199/Seamless Search-20250129T145500Z-001.zip :: Seamless Search/coache, consultants, over 80k year.zip | 1 | 1 | 254,903 | utf-8-sig:1 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Seamless Database 1,547,199.zip :: Seamless Database 1,547,199/coache, consultants, over 80k year.zip | 1 | 1 | 254,903 | utf-8-sig:1 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Apollo Software Development Leads 111,582.zip | 12 | 8 | 222,825 | utf-8-sig:11, cp1252:1 | 2 | email, name/addr/social, phone | 0 | 0 |
| Copy of Clutch.co Database 194,257.zip | 17 | 10 | 143,415 | utf-8-sig:17 | 0 |  | 0 | 0 |
| Copy of Phone Leads 321,562.zip | 6 | 2 | 112,348 | utf-8-sig:6 | 0 | email, phone | 0 | 0 |
| Copy of Getlanka Database 24,404.zip | 71 | 23 | 84,737 | utf-8-sig:57, cp1252:13, utf-8 (with invalid bytes):1 | 12 | email, name/addr/social, phone | 0 | 0 |
| Copy of Seamless Database 1,547,199.zip :: Seamless Database 1,547,199/Seamless Search-20250129T145500Z-001.zip :: Seamless Search/Miner, Mining Engineer, Underground Miner, Driller, Blaster, Mine Operator.zip | 1 | 1 | 36,100 | utf-8-sig:1 | 0 | email, name/addr/social, phone | 0 | 0 |
| Copy of Chrunchbase Database 24,060.zip | 7 | 7 | 16,187 | utf-8-sig:7 | 0 |  | 0 | 0 |
| Copy of Pitchbook 2025-09-14.zip | 34 | 81 | 0 |  | 0 | email, name/addr/social, phone | 0 | 0 |

## Largest schemas (by estimated rows)

- `565235b167` — 62 cols, 205 files, ~369,371,834 rows, archives: Entire Linkedin Database 434,832, Seamless Database 1,547,199.zip, Seamless Database 1,547,199.zip , Seamless Database 1,547,199.zip , Seamless Database 1,547,199.zip , Seamless Database 1,547,199.zip   
  columns: Full name, Industry, Job title, Sub Role, Industry 2, Emails, Mobile, Phone numbers, Company Name, Company Industry, Company Website, Company Size, Company Founded, Location, Locality, Metro, Region, Skills, First Name, Middle Initial, Middle Name, Last Name, Birth Year, Birth Date, Gender …
- `11238dbe3a` — 6 cols, 417 files, ~287,203,769 rows, archives: People Datalabs Database 415,821  
  columns: a, e, liid, linkedin, n, t
- `56638e757e` — 39 cols, 1 files, ~100,383,780 rows, archives: Entire Apollo Database 99,311,28  
  columns: person_name, person_first_name_unanalyzed, person_last_name_unanalyzed, person_name_unanalyzed_downcas, person_title, person_functions, person_seniority, person_email_status_cd, person_extrapolated_email_conf, person_email, person_phone, person_sanitized_phone, person_email_analyzed, person_linkedin_url, person_detailed_function, person_title_normalized, primary_title_normalized_for_f, sanitized_organization_name_un, person_location_city, person_location_city_with_stat, person_location_state, person_location_state_with_cou, person_location_country, person_location_postal_code, job_start_date …
- `50cc0879bf` — 17 cols, 25 files, ~26,038,123 rows, archives: High Quality B2B Leads 31,457,25, USA Database Business Leads 9,97  
  columns: First Name, Middle Name, Last Name, Title, Company Name, Mailing Address, Primary City, Primary State, ZIP Code, Country, Phone, Web Address, Email, Revenue, Employee, Industry, Sub Industry
- `6db856ead1` — 17 cols, 14 files, ~14,524,333 rows, archives: High Quality B2B Leads 31,457,25  
  columns: First Name, Middle Name, Last Name, Title, Company Name, Mailing Address, Primary City, Primary State, ZIP Code, Country, Phone, Web Address, Email, Reveneu, Employee, Industry, Sub Industry
- `7f77cd06e6` — 140 cols, 21 files, ~8,947,985 rows, archives: The Ultimate Ecommerce 7,797,171  
  columns: domain, about_us_url, aliases, android_app_id, brands_page_url, categories, city, cluster_domains, combined_followers, common_crawl_centrality, common_crawl_pagerank, company_ids, company_location, contact_page_url, country_code, created, currency, description, domain_count, domain_tld1, domain_url, emails, employee_count, estimated_monthly_pageviews, estimated_monthly_sales …
- `7c2907d353` — 51 cols, 1 files, ~4,777,264 rows, archives: Entire Apollo Database 99,311,28  
  columns: organization_id, organization_name, organization_revenue_in_thousa, organization_retail_location_c, organization_public_symbol, organization_linkedin_company_, organization_founded_year, organization_alexa_ranking, organization_num_current_emplo, organization_relevant_keywords, organization_relevant_keywords, organization_industries, organization_linkedin_specialt, organization_angellist_markets, organization_yelp_categories, organization_keywords, organization_linkedin_industry, organization_linkedin_specialt, organization_angellist_market_, organization_short_description, organization_seo_description, organization_website_url, organization_angellist_url, organization_facebook_url, organization_twitter_url …
- `3c002e9df4` — 11 cols, 82 files, ~4,072,512 rows, archives: Company Using X Technology - 10,  
  columns: Domain, Sales Revenue USD, Employees, Company, Vertical, Telephones, Emails, City, State, Zip, Country
- `cb2490d7b5` — 41 cols, 29 files, ~2,791,423 rows, archives: Almost Full Crunchbase Database   
  columns: id, created_at, name, short_description, semrush_global_rank, semrush_visits_latest_month, num_investors, funding_total, num_exits, num_funding_rounds, last_funding_type, last_funding_at, num_acquisitions, apptopia_total_apps, apptopia_total_downloads, contact_email, phone_number, facebook, linkedin, twitter, num_investments, num_lead_investments, num_lead_investors, listed_stock_symbol, company_type …
- `d6e4c4381e` — 147 cols, 461 files, ~1,338,181 rows, archives: Seamless Database 1,547,199.zip, Seamless Database 1,547,199.zip   
  columns: Research Date, Contact Full Name, First Name, Middle Name, Last Name, Title, Department, Seniority, Company Name, Company Name - Cleaned, Website, List, Primary Email, Intel, Contact LI Profile URL, Email 1, Email 1 Validation, Email 1 Total AI, Email 2, Email 2 Validation, Email 2 Total AI, Email 3, Email 3 Validation, Email 3 Total AI, Email 4 …
- `724cc79605` — 53 cols, 274 files, ~1,095,276 rows, archives: Seamless Database 1,547,199.zip, Seamless Database 1,547,199.zip   
  columns: Research Date, Contact Full Name, First Name, Middle Name, Last Name, Title, Department, Seniority, Company Name - Cleaned, Website, List, Contact LI Profile URL, Email 1, Email 1 Validation, Email 1 Total AI, Email 2, Email 2 Validation, Email 2 Total AI, Personal Email, Personal Email Validation, Personal Email Total AI, Contact Phone 1, Company Phone 1, Contact Phone 2, Company Phone 2 …
- `793fdafb4a` — 13 cols, 681 files, ~891,025 rows, archives: NinjaLeads Database 238,702.zip, USA Database Business Leads 9,97  
  columns: Id, Business Name, Number of Employees, Contact Person, Corporate Email, Generic Email, Website, Phone, Phone Type, Street Address, Zip Code, State, City
- `029ff407f6` — 14 cols, 1 files, ~876,999 rows, archives: Real Estate Agents 830K  
  columns: Agency_Name, First_Name, Last_Name, Full_Name, email_address, Address, City, State, ZIPCode, Phone_Number, Fax_Number, Website, , 
- `7373fb0041` — 18 cols, 17 files, ~587,881 rows, archives: Fresh Apollo Leads 1,232,352.zip  
  columns: First Name, Last Name, Title, Comp name, Website, Email, Phone, Comp Phone, Employees, Pers Linkedin, Comp Linkedin, Facebook, Twitter, Country, Industry, Tech Used, Keywords, SEO Description
- `f79aba5579` — 145 cols, 399 files, ~561,107 rows, archives: Seamless Database 1,547,199.zip, Seamless Database 1,547,199.zip   
  columns: Research Date, Contact Full Name, First Name, Middle Name, Last Name, Title, Department, Seniority, Company Name, Company Name - Cleaned, Website, List, Primary Email, Intel, Contact LI Profile URL, Email 1, Email 1 Validation, Email 1 Total AI, Email 2, Email 2 Validation, Email 2 Total AI, Email 3, Email 3 Validation, Email 3 Total AI, Email 4 …
- `cac4b72a9b` — 32 cols, 5 files, ~527,220 rows, archives: LinkedIn - 945,237.zip  
  columns: first name, last name, title, department, managementlevel, industry, city, state, country, postalcode, linkedin, email, phone, cphone, website, company, companysize, languages, clinkedin, cfacebook, cx, description, keywords, technologies, revenue …
- `22b9502030` — 23 cols, 64 files, ~507,072 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, entity-hover 4, entity-hover href 4, ellipsis 15
- `970f6c0b48` — 9 cols, 64 files, ~331,642 rows, archives: Instagram - 843,613.zip  
  columns: Username, Name, Bio, Category, FollowerCount, FollowingCount, Website, Email, Phone
- `162ef2f659` — 66 cols, 10 files, ~253,432 rows, archives: AG-AgTech Leads 103,322.zip, Entire Apollo Database 99,311,28  
  columns: First Name, Last Name, Title, Company, Company Name for Emails, Email, Email Status, Seniority, Departments, First Phone, Work Direct Phone, Home Phone, Mobile Phone, Corporate Phone, Other Phone, Stage, # Employees, Industry, Keywords, Person Linkedin Url, Website, Company Linkedin Url, Facebook Url, Twitter Url, City …
- `d8f74a9321` — 31 cols, 4 files, ~231,825 rows, archives: LinkedIn - 945,237.zip  
  columns: first name, last name, title, department, managementlevel, industry, city, state, country, postalcode, linkedin, email, phone, cphone, website, company, companysize, languages, clinkedin, cfacebook, cx, description, keywords, technologies, revenue …
- `746ba7a688` — 23 cols, 16 files, ~205,498 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis href, ellipsis 6, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, entity-hover 4, entity-hover href 4, ellipsis 14, ellipsis 15
- `89cd161875` — 23 cols, 6 files, ~158,316 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis 7, ellipsis href, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, ellipsis 15, ellipsis 16, entity-hover 4, entity-hover href 4
- `85c1947c5e` — 22 cols, 44 files, ~158,002 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, entity-hover 4, entity-hover href 4
- `25c8342d97` — 23 cols, 34 files, ~130,390 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, entity-hover 4, entity-hover href 4, ellipsis 14, ellipsis 15
- `1aa143fae3` — 12 cols, 1 files, ~129,278 rows, archives: Real Estate Agents 830K  
  columns: Email, COMPANY, ADDRESS, CITY, STATE, ZIPCODE, PHONE_NUMBER, FAX_NUMBER, SIC_CODE, SIC_DESCRIPTION, WEB_ADDRESS, Email-Domain
- `04a382a378` — 23 cols, 44 files, ~123,710 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, ellipsis 15, entity-hover 4, entity-hover href 4
- `3f13b684c1` — 52 cols, 15 files, ~122,433 rows, archives: Apollo Software Development Lead, Getlanka Database 24,404.zip  
  columns: First Name, Last Name, Title, Company, Company Name for Emails, Email, Email Status, Seniority, Departments, First Phone, Work Direct Phone, Home Phone, Mobile Phone, Corporate Phone, Other Phone, Stage, # Employees, Industry, Keywords, Person Linkedin Url, Website, Company Linkedin Url, Facebook Url, Twitter Url, City …
- `63ac3d6b56` — 8 cols, 1047 files, ~113,519 rows, archives: USA Database Business Leads 9,97  
  columns: Name, URL, Query, Rating, Reviews, Phone, Address, Website
- `68a22cc6e3` — 59 cols, 24 files, ~87,519 rows, archives: AG-AgTech Leads 103,322.zip, Seamless Database 1,547,199.zip  
  columns: Research Date, Contact Full Name, First Name, Middle Name, Title, Last Name, Department, Seniority, Company Name - Cleaned, Website, List, Contact LI Profile URL, Email 1, Email 1 Validation, Email 1 Total AI, Email 2, Email 2 Validation, Email 2 Total AI, Personal Email, Personal Email Validation, Personal Email Total AI, Contact Phone 1, Company Phone 1, Contact Phone 2, Company Phone 2 …
- `d979242217` — 23 cols, 6 files, ~85,586 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, entity-hover 4, entity-hover href 4, ellipsis 15, ellipsis 16
- `b3c1c7f112` — 5 cols, 5 files, ~84,220 rows, archives: Phone Leads 321,562.zip  
  columns: name, phone, email, website, category
- `d89543bae7` — 23 cols, 14 files, ~78,574 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 4, ellipsis 5, ellipsis 7, ellipsis 8, ellipsis href, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, ellipsis 15, ellipsis 16, entity-hover 4, entity-hover href 4, ellipsis 17
- `3278aa8080` — 54 cols, 8 files, ~74,387 rows, archives: Seamless Database 1,547,199.zip, Seamless Database 1,547,199.zip   
  columns: name, phone, email, email_host, website, category, address, city, region, zip, country, google_rank, facebook, instagram, twitter, linkedin, googlestars, googlereviewscount, yelpstars, yelpreviewscount, facebookstars, facebookreviewscount, facebookpixel, googlepixel, criteopixel …
- `d9251bde90` — 23 cols, 6 files, ~73,228 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis 7, ellipsis href, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, ellipsis 15, entity-hover 4, entity-hover href 4, ellipsis 16
- `21a321b224` — 22 cols, 2 files, ~71,964 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis 7, ellipsis href, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, entity-hover 4, entity-hover href 4, ellipsis 16
- `7be260d962` — 24 cols, 2 files, ~71,546 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis 7, ellipsis href, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, ellipsis 14, ellipsis 15, entity-hover 4, entity-hover href 4, ellipsis 16, ellipsis 17
- `8c8f602c66` — 84 cols, 10 files, ~71,405 rows, archives: AG-AgTech Leads 103,322.zip, Entire Apollo Database 99,311,28  
  columns: First Name, Last Name, Title, Company, Company Name for Emails, Email, Email Status, Seniority, Departments, First Phone, Work Direct Phone, Home Phone, Mobile Phone, Corporate Phone, Other Phone, Stage, # Employees, Industry, Keywords, Person Linkedin Url, Website, Company Linkedin Url, Facebook Url, Twitter Url, City …
- `0c3cb9059e` — 30 cols, 2 files, ~66,273 rows, archives: AG-AgTech Leads 103,322.zip, Entire Apollo Database 99,311,28  
  columns: First Name, Last Name, Title, Company, Company Name for Emails, Email, Email Status, Seniority, Departments, First Phone, Work Direct Phone, Home Phone, Mobile Phone, Corporate Phone, Other Phone, Stage, # Employees, Industry, Website, Company Linkedin Url, Facebook Url, Twitter Url, City, State, Country …
- `23bcc83fd5` — 70 cols, 17 files, ~62,650 rows, archives: Apollo Software Development Lead, Getlanka Database 24,404.zip  
  columns: First Name, Last Name, Title, Company, Company Name for Emails, Email, Email Status, Seniority, Departments, First Phone, Work Direct Phone, Home Phone, Mobile Phone, Corporate Phone, Other Phone, Stage, # Employees, Industry, Keywords, Person Linkedin Url, Website, Company Linkedin Url, Facebook Url, Twitter Url, City …
- `dbeb6bb207` — 23 cols, 18 files, ~61,046 rows, archives: Pitchbook 2025-06-21.zip, Pitchbook 2025-09-14.zip :: Pitc  
  columns: entity-hover, entity-hover href, entity-hover 2, entity-hover 3, entity-hover href 3, ellipsis, ellipsis 2, ellipsis 3, ellipsis 4, ellipsis 5, ellipsis 6, ellipsis href, ellipsis 7, ellipsis 8, ellipsis 9, ellipsis 10, ellipsis 11, ellipsis 12, ellipsis 13, entity-hover 4, entity-hover href 4, ellipsis 15, ellipsis 16
