# ERD — leads database (v0.2)

Renders on GitHub / VS Code / Cursor (Mermaid). Source of truth: `database/schema.sql`.

## Provenance (catalog)

```mermaid
erDiagram
    DATASETS ||--o{ ARCHIVES : contains
    ARCHIVES ||--o{ ARCHIVES : "nested zip"
    ARCHIVES ||--o{ FILES : contains
    LAYOUTS ||--o{ FILES : "header layout"
    LAYOUTS ||--o{ COLUMN_MAPPINGS : "column -> target"
    FILES ||--o| FILES : "duplicate_of"
    FILES ||--o{ IMPORT_BATCHES : "import runs"
    IMPORT_BATCHES ||--o{ REJECTED_ROWS : "unparseable rows"
    IMPORT_BATCHES ||--o{ TRANSFORM_ERRORS : "bad values"

    DATASETS {
        smallint id PK
        text name
        date data_as_of
        smallint priority
    }
    ARCHIVES {
        int id PK
        smallint dataset_id FK
        int parent_archive_id FK
        text path
    }
    LAYOUTS {
        int id PK
        text fingerprint
        text_arr headers
    }
    FILES {
        int id PK
        int archive_id FK
        int layout_id FK
        text member_path
        date data_as_of
        int duplicate_of_file_id FK
        text load_status
    }
    COLUMN_MAPPINGS {
        int layout_id PK
        smallint column_index PK
        text target
        text transform
        text review_status
    }
    IMPORT_BATCHES {
        bigint id PK
        int file_id FK
        text status
        bigint last_row_committed
    }
    REJECTED_ROWS {
        bigint id PK
        int file_id FK
        bigint row_number
        text reason
        text raw_line
    }
    TRANSFORM_ERRORS {
        bigint id PK
        int file_id
        bigint row_number
        text target
        text bad_value
    }
```

Every core record points back to its source row with (dataset_id, file_id, sheet_name, row_number);
the original files stay on Google Drive.

## Core layer

```mermaid
erDiagram
    FILES ||--o{ PERSON_RECORDS : "source row"
    FILES ||--o{ COMPANY_RECORDS : "source row"
    PEOPLE ||--o{ PERSON_RECORDS : "merged from"
    COMPANIES ||--o{ COMPANY_RECORDS : "merged from"
    COMPANIES ||--o{ PEOPLE : employs
    COMPANY_RECORDS ||--o{ PERSON_RECORDS : "employer in same row"

    PERSON_RECORDS ||--o{ RECORD_EMAILS : has
    COMPANY_RECORDS ||--o{ RECORD_EMAILS : has
    EMAIL_ADDRESSES ||--o{ RECORD_EMAILS : "same email"
    RECORD_EMAILS ||--o{ EMAIL_VERIFICATIONS : verified

    PERSON_RECORDS ||--o{ RECORD_PHONES : has
    COMPANY_RECORDS ||--o{ RECORD_PHONES : has
    PHONE_NUMBERS ||--o{ RECORD_PHONES : "same phone"

    PERSON_RECORDS ||--o{ RECORD_PROFILES : has
    COMPANY_RECORDS ||--o{ RECORD_PROFILES : has
    PROFILE_URLS ||--o{ RECORD_PROFILES : "same profile"

    COMPANY_RECORDS ||--o{ COMPANY_RECORD_CATEGORIES : tagged
    CATEGORIES ||--o{ COMPANY_RECORD_CATEGORIES : ""
    COMPANY_RECORDS ||--o{ COMPANY_RECORD_TECHNOLOGIES : uses
    TECHNOLOGIES ||--o{ COMPANY_RECORD_TECHNOLOGIES : ""
    COMPANY_RECORDS ||--o| COMPANY_FUNDING : funding

    LOCATIONS ||--o{ PERSON_RECORDS : ""
    LOCATIONS ||--o{ COMPANY_RECORDS : ""

    PEOPLE {
        bigint id PK
        text full_name
        text job_title
        bigint company_id FK
        int record_count
    }
    COMPANIES {
        bigint id PK
        text name
        text domain
        text linkedin_url
        int record_count
    }
    PERSON_RECORDS {
        smallint dataset_id PK
        bigint id PK
        int file_id FK
        bigint row_number
        timestamptz observed_at
        bigint person_id FK
        bigint company_record_id FK
        text first_name
        text last_name
        text job_title
    }
    COMPANY_RECORDS {
        smallint dataset_id PK
        bigint id PK
        int file_id FK
        bigint row_number
        timestamptz observed_at
        bigint company_id FK
        text name
        text domain
        jsonb extra
    }
    EMAIL_ADDRESSES {
        bigint id PK
        text email UK
        text domain
    }
    RECORD_EMAILS {
        bigint id PK
        bigint email_address_id FK
        text email_kind
        smallint position
    }
    PHONE_NUMBERS {
        bigint id PK
        text phone UK
        bool is_e164
    }
    PROFILE_URLS {
        bigint id PK
        text platform
        text url UK
    }
```

`MATCH_CANDIDATES` (dedup review queue) links pairs of person records or company records; it has no FK
because one table serves both entity types.

All source-level tables (`*_records`, `record_*`, `email_verifications`, `company_funding`, `company_record_*`)
are partitioned by `dataset_id`.
