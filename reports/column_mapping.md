# Column mapping (Phase 3)

Generated from header names + profiled data types, plus reviewed decisions in `config/mapping_overrides.csv`. Columns without a canonical field are not dropped: they are stored in the record's `extra` jsonb under their original header.

Layouts: 436 | Columns: 15098 | high: 7770 | medium: 330 | low: 76 | unmapped: 6922

Review status: approved: 15094 | rejected: 4

Rows in person-level datasets: ~805,249,808 (97%) | company/other: ~23,801,500

## Canonical field coverage (estimated rows that will have this field)

| Target | PII | Layouts | Est. rows | Source headers (top) |
|---|---|---:|---:|---|
| person.email | yes | 250 | 808,041,231 | `Work Email #1`, `Direct Email #1`, `Work Email #2`, `Direct Email #2`, `Work Email #3` |
| person.phone | yes | 238 | 805,236,204 | `Phone #1`, `Phone #2`, `Phone #3`, `Phone #4`, `Phone #5` |
| person.linkedin_url | yes | 171 | 762,785,548 | `Linked Url`, `Person Linkedin Url`, `Contact LI Profile URL`, `linkedin`, `Pers Linkedin` |
| person.full_name | yes | 188 | 762,587,929 | `Full Name`, `fullname`, `Contact Person`, `Contact Name`, `Contact Full Name` |
| person.location_raw |  | 127 | 760,688,703 | `Location`, `Contact Location`, `Location Geo`, `a`, `person_location_city_with_state_or_country` |
| person.linkedin_username | yes | 4 | 656,576,631 | `LinkedIn Username`, `liid`, `linkedin_id` |
| person.first_name | yes | 231 | 517,155,014 | `First Name`, `firstname`, `first_name`, `first name`, `FIRST NAME` |
| person.last_name | yes | 213 | 517,140,475 | `Last Name`, `lastname`, `last_name`, `last name`, `LAST NAME` |
| person.city |  | 104 | 516,784,324 | `City`, `city`, `CITY`, `Contact City`, `Primary City` |
| person.state |  | 98 | 516,779,156 | `State`, `state`, `STATE`, `Region`, `Contact State` |
| person.job_title |  | 227 | 516,263,476 | `Job Title`, `Title`, `title`, `TITLE`, `Job title` |
| person.country |  | 64 | 515,608,668 | `Country`, `Contact Country`, `country`, `Location Country`, `Countries` |
| person.postal_code | yes | 45 | 512,860,973 | `Zip Code`, `ZIP CODE`, `ZIP Code`, `Postal Code`, `postalcode` |
| source.observed_at |  | 9 | 475,638,231 | `Research Date`, `Last Updated`, `person_vacuumed_at`, `created_at` |
| person.department |  | 54 | 474,388,654 | `Departments`, `Department`, `Sub Role`, `department`, `person_functions` |
| person.job_start_date |  | 5 | 469,756,642 | `Start Date`, `job_start_date` |
| person.linkedin_connections |  | 3 | 469,756,642 | `Linkedin Connections`, `person_num_linkedin_connections` |
| company.website |  | 207 | 425,994,839 | `Company Website`, `Website`, `website`, `Web Address`, `organization_website_url` |
| company.name |  | 66 | 420,731,488 | `Company Name`, `COMPANY NAME`, `name`, `Name`, `organization_name` |
| person.middle_name | yes | 11 | 413,025,751 | `Middle Name`, `Middle Initial`, `middle_name` |
| person.industry |  | 169 | 412,727,632 | `Industry`, `industry` |
| person.address | yes | 47 | 411,718,148 | `Street Address`, `Address`, `ADDRESS LINE 1`, `Address Line 1`, `Mailing Address` |
| company.employee_range |  | 116 | 411,319,956 | `Team Size`, `Employee`, `Company Size`, `companysize` |
| company.sub_industry |  | 5 | 409,935,585 | `Sub Industry`, `Industry 2` |
| company.facebook_url |  | 128 | 387,418,373 | `Company Facebook`, `facebook`, `organization_facebook_url`, `Company Facebook Url`, `cfacebook` |
| company.city |  | 66 | 387,261,998 | `Company City`, `City`, `city`, `Company Location Locality`, `ccity` |
| company.state |  | 64 | 387,261,998 | `Company State`, `State`, `region`, `Company Location Region`, `state` |
| company.country |  | 53 | 387,132,720 | `Company Country`, `country`, `Company Location Country`, `Country`, `ccountry` |
| company.twitter_url |  | 13 | 386,786,087 | `twitter`, `organization_twitter_url`, `Company Twitter Url`, `cx`, `twitter_url` |
| company.linkedin_url |  | 60 | 386,495,955 | `Company Linkedin Url`, `Company LI Profile Url`, `linkedin`, `Comp Linkedin`, `clinkedin` |
| company.postal_code |  | 21 | 383,370,896 | `Zip Code`, `Zip`, `zip`, `Company Location Postal Code`, `cpostalcode` |
| company.location_raw |  | 8 | 381,411,013 | `Company Location`, `Company Location Name`, `Company Location Geo`, `company_location` |
| company.founded_year |  | 14 | 380,839,054 | `Company Founded Date`, `organization_founded_year`, `Company Founded`, `foundedyear`, `founded_on` |
| company.address |  | 53 | 379,319,875 | `Company Address`, `Address`, `Address Line 1`, `Company Location Street Address`, `address` |
| company.industry |  | 9 | 377,261,505 | `Company Industry`, `organization_industries`, `industry` |
| person.facebook_url | yes | 164 | 371,456,248 | `Facebook Profile`, `Facebook Url`, `Facebook`, `facebook_url`, `Facebook Username` |
| person.twitter_url | yes | 48 | 370,818,122 | `Twitter Url`, `Twitter`, `twitter_url`, `Twitter Username` |
| person.mobile_phone | yes | 47 | 370,251,265 | `Mobile Phone`, `Mobile`, `Contact Mobile Phone` |
| person.headline |  | 5 | 369,752,798 | `Job Summary`, `Summary`, `headline`, `Bio` |
| person.github_url | yes | 5 | 369,421,156 | `github_url`, `Github Url`, `Github Username` |
| person.metro |  | 2 | 369,372,862 | `Metro` |
| person.skills |  | 2 | 369,372,862 | `Skills` |
| person.birth_date_raw | yes | 2 | 369,372,862 | `Birth Year`, `Birth Date` |
| person.gender | yes | 2 | 369,372,862 | `Gender` |
| company.metro |  | 2 | 369,372,862 | `Company Location Metro` |
| company.address_line2 |  | 6 | 369,372,862 | `Address Line 2`, `Company Location Address Line 2` |
| company.continent |  | 2 | 369,372,862 | `Company Location Continent` |
| person.continent |  | 2 | 369,372,862 | `Location Continent` |
| person.address_line2 | yes | 21 | 369,372,862 | `Address Line 2`, `ADDRESS LINE 2`, `Address 2` |
| person.salary | yes | 2 | 369,372,862 | `Inferred Salary` |
| person.years_experience |  | 2 | 369,372,862 | `Years Experience` |
| person.interests |  | 2 | 369,372,862 | `Interests` |
| source.record_id |  | 9 | 108,891,786 | `organization_id`, `id`, `_index`, `_id`, `Id` |
| person.seniority |  | 54 | 105,064,086 | `Seniority`, `seniority`, `managementlevel`, `person_seniority` |
| person.email_status |  | 161 | 104,930,367 | `Work Email #1 Status`, `Direct Email #1 Status`, `Work Email #2 Status`, `Direct Email #2 Status`, `Work Email #3 Status` |
| person.job_title_normalized |  | 1 | 100,383,780 | `person_title_normalized`, `primary_title_normalized_for_faceting` |
| company.revenue |  | 173 | 49,793,035 | `Revenue Range`, `Annual Revenue`, `Revenue`, `REVENUE`, `Company Annual Revenue` |
| company.phone |  | 216 | 27,261,002 | `Company Phone`, `Corporate Phone`, `COMPANY PHONE`, `PHONE_NUMBER`, `Business Phone` |
| company.description |  | 12 | 20,410,972 | `description`, `Company Description`, `meta_description`, `organization_short_description`, `short_description` |
| company.domain |  | 39 | 18,149,363 | `domain`, `organization_domain`, `Domain`, `company_domain`, `org_primary_domain` |
| company.category |  | 10 | 16,462,466 | `category`, `categories`, `Vertical`, `Category`, `SIC_CODE` |
| company.employee_count |  | 64 | 15,320,937 | `# Employees`, `Number of Employees`, `Employees`, `employee_count` |
| company.email |  | 168 | 15,215,423 | `Company Email`, `Email`, `Generic Email`, `email`, `Primary Email` |
| company.keywords |  | 2 | 13,725,249 | `tags`, `organization_keywords` |
| company.technologies |  | 41 | 10,986,122 | `Technologies`, `technologies`, `Tech Used`, `installed_apps` |
| company.instagram_url |  | 4 | 9,037,199 | `instagram`, `instagram_url`, `Instagram` |
| company.youtube_url |  | 1 | 8,947,985 | `youtube`, `youtube_channel_url`, `youtube_url` |
| funding.total_funding_raw |  | 146 | 4,837,844 | `Total Funding`, `totalfunding`, `funding_total` |
| funding.last_funding_type |  | 35 | 3,453,473 | `Latest Funding`, `last_funding_type` |
| funding.last_funding_at |  | 35 | 3,453,473 | `Last Raised At`, `last_funding_at` |
| person.secondary_email | yes | 8 | 3,201,737 | `Personal Email`, `Secondary Email` |
| funding.num_investors |  | 1 | 2,791,423 | `num_investors` |
| funding.num_exits |  | 1 | 2,791,423 | `num_exits` |
| funding.num_funding_rounds |  | 1 | 2,791,423 | `num_funding_rounds` |
| funding.num_acquisitions |  | 1 | 2,791,423 | `num_acquisitions` |
| funding.stock_symbol |  | 1 | 2,791,423 | `listed_stock_symbol` |
| funding.operating_status |  | 1 | 2,791,423 | `operating_status` |
| person.keywords |  | 43 | 2,037,831 | `Keywords`, `keywords` |
| company.linkedin_username |  | 2 | 1,899,288 | `Company LinkedIn ID` |
| person.phone_type |  | 22 | 905,564 | `Phone Type` |
| person.home_phone | yes | 43 | 782,801 | `Home Phone` |
| person.other_phone | yes | 43 | 782,801 | `Other Phone` |
| funding.last_funding_amount_usd |  | 34 | 662,050 | `Latest Funding Amount` |
| verification.is_disposable |  | 33 | 330,389 | `is_disposable` |
| verification.is_role_account |  | 33 | 330,389 | `is_role_account` |
| verification.mx_found |  | 54 | 330,389 | `mx_accepts_mail`, `ZB MX Found` |
| verification.is_catch_all |  | 33 | 330,389 | `is_catch_all` |
| verification.is_deliverable |  | 33 | 330,389 | `is_deliverable` |
| company.crunchbase_url |  | 3 | 48,294 | `organization_crunchbase_url`, `org_crunchbase_url` |
| verification.status |  | 21 | 0 | `ZB Status` |
| verification.sub_status |  | 21 | 0 | `ZB Sub status` |
| verification.smtp_provider |  | 21 | 0 | `ZB SMTP Provider` |
| company.phone_type |  | 1 | 0 | `Phone Type` |
| company.logo_url |  | 1 | 0 | `org_logo_url` |

## Top unmapped headers (kept as extra attributes unless a rule is added)

| Normalized header | Layouts | Est. rows |
|---|---:|---:|
| type | 2 | 105,161,044 |
| score | 2 | 105,161,044 |
| person email analyzed | 1 | 100,383,780 |
| sanitized organization name unanalyzed | 1 | 100,383,780 |
| current organization ids | 1 | 100,383,780 |
| modality | 1 | 100,383,780 |
| prospected by team ids | 1 | 100,383,780 |
| person excluded by team ids | 1 | 100,383,780 |
| relavence boost | 1 | 100,383,780 |
| predictive scores | 1 | 100,383,780 |
| random | 1 | 100,383,780 |
| status | 35 | 9,805,594 |
| notes | 11 | 8,960,785 |
| about us url | 1 | 8,947,985 |
| aliases | 1 | 8,947,985 |
| android app id | 1 | 8,947,985 |
| brands page url | 1 | 8,947,985 |
| cluster domains | 1 | 8,947,985 |
| combined followers | 1 | 8,947,985 |
| common crawl centrality | 1 | 8,947,985 |
| common crawl pagerank | 1 | 8,947,985 |
| company ids | 1 | 8,947,985 |
| contact page url | 1 | 8,947,985 |
| created | 1 | 8,947,985 |
| currency | 1 | 8,947,985 |
| domain count | 1 | 8,947,985 |
| domain tld1 | 1 | 8,947,985 |
| domain url | 1 | 8,947,985 |
| estimated monthly pageviews | 1 | 8,947,985 |
| estimated monthly sales | 1 | 8,947,985 |
| estimated monthly visits | 1 | 8,947,985 |
| estimated yearly sales | 1 | 8,947,985 |
| facebook group | 1 | 8,947,985 |
| facebook group url | 1 | 8,947,985 |
| faq page url | 1 | 8,947,985 |
| favicon url | 1 | 8,947,985 |
| features | 1 | 8,947,985 |
| financing page url | 1 | 8,947,985 |
| has cms | 1 | 8,947,985 |
| headless | 1 | 8,947,985 |
| installed apps count | 1 | 8,947,985 |
| installed apps names | 1 | 8,947,985 |
| ios app id | 1 | 8,947,985 |
| judgeme avgrating | 1 | 8,947,985 |
| judgeme reviews | 1 | 8,947,985 |
| language code | 1 | 8,947,985 |
| last plan | 1 | 8,947,985 |
| last plan changed | 1 | 8,947,985 |
| last platform | 1 | 8,947,985 |
| last platform changed | 1 | 8,947,985 |
| last theme | 1 | 8,947,985 |
| last theme changed | 1 | 8,947,985 |
| linkedin account | 1 | 8,947,985 |
| loox avgrating | 1 | 8,947,985 |
| loox reviews | 1 | 8,947,985 |
| merchant name | 1 | 8,947,985 |
| meta keywords | 1 | 8,947,985 |
| monthly app spend | 1 | 8,947,985 |
| okendo avgrating | 1 | 8,947,985 |
| okendo reviews | 1 | 8,947,985 |
| open graph image url | 1 | 8,947,985 |
| pinterest | 1 | 8,947,985 |
| pinterest followers | 1 | 8,947,985 |
| pinterest followers 30d | 1 | 8,947,985 |
| pinterest followers 90d | 1 | 8,947,985 |
| pinterest posts | 1 | 8,947,985 |
| pinterest url | 1 | 8,947,985 |
| plan | 1 | 8,947,985 |
| platform | 1 | 8,947,985 |
| platform domain | 1 | 8,947,985 |
| platform rank | 1 | 8,947,985 |
| platform rank percentile | 1 | 8,947,985 |
| platform version | 1 | 8,947,985 |
| rank | 1 | 8,947,985 |
| rank percentile | 1 | 8,947,985 |
| retailer url | 1 | 8,947,985 |
| returns page url | 1 | 8,947,985 |
| rio avgrating | 1 | 8,947,985 |
| rio reviews | 1 | 8,947,985 |
| sales channel abound | 1 | 8,947,985 |

## Decisions on low-confidence columns (config/mapping_overrides.csv)

| Source header | Archive | Decision | Target | Transform | Why |
|---|---|---|---|---|---|
| `Employee` | High Quality B2B Leads 31,457,250.zip /  | approved | company.employee_range |  | Values are ranges like '25 - 100', '1K - 10K', not counts |
| `title` | The Ultimate Ecommerce 7,797,171.zip | rejected | (extra) |  | Website page title (e.g. Golden Corral | Endless Buffet), not a job title: kept in extra |
| `Telephones` | Company Using X Technology - 10,135,706. | approved | company.phone | split_list(;);validate_phone | Several numbers in one cell separated by ';' |
| `Corporate Email` | NinjaLeads Database 238,702.zip / USA Da | approved | person.email | email_with_status;kind=work | Values look like 'name@co.com (Accept_all)': email plus verification status in brackets; sometimes several separated by commas. Status goes to record_emails.source_status |
| `Website` | Real Estate Agents 830K | approved | company.website | validate_domain | Column mixes domains with emails/phones; only valid domains/URLs are used, the rest go to transform_errors |
| `Bio` | Instagram - 843,613.zip | approved | person.headline |  | Instagram bio. Accounts may be people or businesses; stored as headline of the account holder |
| `Secondary Email` | AG-AgTech Leads 103,322.zip / Entire Apo | approved | person.email | validate_email;kind=personal;position=2 | Only 0.2% filled, partly by rows whose columns shifted ('Fulfilled by Apollo'); invalid values go to transform_errors |
| `Work Direct Phone` | Apollo Software Development Leads 111,58 | approved | person.phone | validate_phone;kind=direct | ~0.1% filled, by rows whose columns shifted; invalid values go to transform_errors |
| `Home Phone` | Apollo Software Development Leads 111,58 | approved | person.home_phone | validate_phone | ~0.1% filled, shifted rows; invalid values go to transform_errors |
| `Direct Email #4` | LeadRocks Database 341,632.zip / USA Dat | approved | person.email | validate_email;kind=direct;position=4 | Same: repeated header text / shifted rows inside some files |
| `Other Phone` | AG-AgTech Leads 103,322.zip / Entire Apo | approved | person.other_phone | validate_phone | Sparse; invalid values (shifted rows) go to transform_errors |
| `Mobile Phone` | Apollo Software Development Leads 111,58 | approved | person.mobile_phone | validate_phone | ~0.1% filled, shifted rows; invalid values go to transform_errors |
| `Phone #6` | LeadRocks Database 341,632.zip / USA Dat | approved | person.phone | validate_phone;position=6 | Some values are words (shifted rows); only valid phones are used |
| `Direct Email #3` | LeadRocks Database 341,632.zip / USA Dat | approved | person.email | validate_email;kind=direct;position=3 | Some files repeat header text inside data ('Direct Email #2'); only valid emails are used |
| `Direct Email #5` | LeadRocks Database 341,632.zip / USA Dat | approved | person.email | validate_email;kind=direct;position=5 | Same: repeated header text / shifted rows inside some files |
| `Direct Email #6` | LeadRocks Database 341,632.zip / USA Dat | approved | person.email | validate_email;kind=direct;position=6 | Same: repeated header text / shifted rows inside some files |
| `Generic Email` | USA Database Business Leads 9,979,021.zi | approved | company.email | email_with_status;kind=generic | Same 'email (status)' format; a shared/company inbox |
| `Email` | USA Database Business Leads 9,979,021.zi | rejected | (extra) |  | Values are only the part before @ (e.g. 'nwiley'), not full email addresses. Kept in extra, not used as email |
| `Phone` | LeadRocks Database 341,632.zip | approved | person.phone | float_to_digits | Phone numbers stored as numbers by Excel |
| `Title` | Pitchbook 2025-09-14.zip | approved | person.job_title |  | Values are clearly job titles (CEO, Co-Founder...). Person names in these files sit in unlabeled scraped columns: to be identified in the Pitchbook review |
| `Phone Number` | Pitchbook 2025-09-14.zip | rejected | (extra) |  | Values are words, not phone numbers: kept in extra |
| `Company Email` | Pitchbook 2025-09-14.zip | rejected | (extra) |  | Header says email but values look like years (1978, 2009). Possibly founded year, not confirmed: kept in extra, not mapped |
| `org_phone` | Pitchbook 2025-09-14.zip | approved | company.phone | float_to_digits;validate_phone | Mostly numeric phones; a few junk values go to transform_errors |
| `org_founded_year` | Pitchbook 2025-09-14.zip | approved | company.founded_year | float_to_int | 2013.0 -> 2013 |
| `org_sanitized_phone` | Pitchbook 2025-09-14.zip | approved | company.phone | float_to_digits | Phone numbers stored as numbers by Excel |
| `COMPANY EMAIL` | Pitchbook 2025-09-14.zip | approved | company.phone | float_to_digits;validate_phone | Header says email but ~70% of values are phone numbers: mapped as company phone; non-phones go to transform_errors |
| `PHONE_NUMBER` | Pitchbook 2025-09-14.zip | approved | person.phone | float_to_digits | Excel stored phone numbers as numbers (4155550123.0); convert back to digits |
| `COMPANY PHONE` | Pitchbook 2025-09-14.zip | approved | company.phone | validate_phone | Mixed values; non-phones go to transform_errors |
| `PHONE_NUMBER` | Pitchbook 2025-09-14.zip | approved | company.phone | float_to_digits | Excel stored phone numbers as numbers (4155550123.0); convert back to digits |
