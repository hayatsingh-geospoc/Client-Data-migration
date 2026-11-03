# Canonical fields (draft)

Target fields used by `scripts/map_columns.py`. Entity is decided per column: an explicit header prefix (`company`, `organization`, `person`, `contact`...) wins; otherwise person-only / company-only fields go to that entity, and shared fields (email, phone, city, linkedin_url...) go to `person` in datasets that contain person names and to `company` otherwise.

| Field | Scope | PII |
|---|---|---|
| address | shared | yes |
| address_line2 | shared | yes |
| birth_date_raw | person | yes |
| category | company |  |
| city | shared |  |
| city | company |  |
| country | company |  |
| email | company | yes |
| employee_range | company |  |
| facebook_url | company | yes |
| founded_year | company |  |
| linkedin_url | company | yes |
| phone | company | yes |
| postal_code | company | yes |
| state | company |  |
| twitter_url | company | yes |
| continent | shared |  |
| country | shared |  |
| crunchbase_url | company |  |
| department | person |  |
| description | company |  |
| domain | company |  |
| email | shared | yes |
| email_status | person |  |
| employee_count | company |  |
| employee_range | company |  |
| facebook_url | shared | yes |
| first_name | person | yes |
| founded_year | company |  |
| full_name | person | yes |
| last_funding_amount_usd | funding |  |
| last_funding_at | funding |  |
| last_funding_type | funding |  |
| num_acquisitions | funding |  |
| num_exits | funding |  |
| num_funding_rounds | funding |  |
| num_investors | funding |  |
| operating_status | funding |  |
| stock_symbol | funding |  |
| total_funding_raw | funding |  |
| gender | person | yes |
| github_url | shared | yes |
| headline | person |  |
| home_phone | person | yes |
| industry | shared |  |
| instagram_url | shared | yes |
| interests | person |  |
| job_start_date | person |  |
| job_title | person |  |
| job_title_normalized | person |  |
| keywords | shared |  |
| last_name | person | yes |
| linkedin_connections | person |  |
| linkedin_url | shared | yes |
| linkedin_username | person | yes |
| location_raw | shared |  |
| logo_url | company |  |
| metro | shared |  |
| middle_name | person | yes |
| mobile_phone | person | yes |
| name | company |  |
| other_phone | person | yes |
| phone | shared | yes |
| phone_type | shared |  |
| postal_code | shared | yes |
| revenue | company |  |
| salary | person | yes |
| secondary_email | person | yes |
| seniority | person |  |
| skills | person |  |
| observed_at | source |  |
| record_id | source |  |
| state | shared |  |
| sub_industry | company |  |
| technologies | company |  |
| twitter_url | shared | yes |
| is_catch_all | verification |  |
| is_deliverable | verification |  |
| is_disposable | verification |  |
| is_role_account | verification |  |
| mx_found | verification |  |
| smtp_provider | verification |  |
| status | verification |  |
| sub_status | verification |  |
| website | company |  |
| years_experience | person |  |
| youtube_url | shared |  |
