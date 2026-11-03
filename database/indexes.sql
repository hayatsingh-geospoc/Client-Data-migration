-- =============================================================================
-- Secondary indexes — DRAFT v0.2
-- Create AFTER the bulk load (indexing once is far faster than maintaining indexes row by row on ~1B rows).
-- Indexes on partitioned tables cascade to every partition, including ones created later.
-- =============================================================================

-- source records -> canonical entities, exact-row duplicates
CREATE INDEX IF NOT EXISTS person_records_person_idx ON core.person_records (person_id);
CREATE INDEX IF NOT EXISTS person_records_company_record_idx ON core.person_records (dataset_id, company_record_id);
CREATE INDEX IF NOT EXISTS person_records_row_hash_idx ON core.person_records (row_hash);
CREATE INDEX IF NOT EXISTS company_records_company_idx ON core.company_records (company_id);
CREATE INDEX IF NOT EXISTS company_records_row_hash_idx ON core.company_records (row_hash);

-- matching keys
CREATE INDEX IF NOT EXISTS company_records_domain_idx ON core.company_records (domain);
CREATE INDEX IF NOT EXISTS company_records_linkedin_idx ON core.company_records (linkedin_url);
CREATE INDEX IF NOT EXISTS company_records_name_idx ON core.company_records (normalized_name);
CREATE INDEX IF NOT EXISTS person_records_name_idx ON core.person_records (last_name, first_name);
CREATE INDEX IF NOT EXISTS companies_domain_idx ON core.companies (domain);
CREATE INDEX IF NOT EXISTS email_addresses_domain_idx ON core.email_addresses (domain);

-- contact links (both directions)
CREATE INDEX IF NOT EXISTS record_emails_email_idx ON core.record_emails (email_address_id);
CREATE INDEX IF NOT EXISTS record_emails_person_idx ON core.record_emails (dataset_id, person_record_id) WHERE person_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS record_emails_company_idx ON core.record_emails (dataset_id, company_record_id) WHERE company_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS record_phones_phone_idx ON core.record_phones (phone_number_id);
CREATE INDEX IF NOT EXISTS record_phones_person_idx ON core.record_phones (dataset_id, person_record_id) WHERE person_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS record_phones_company_idx ON core.record_phones (dataset_id, company_record_id) WHERE company_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS record_profiles_profile_idx ON core.record_profiles (profile_url_id);
CREATE INDEX IF NOT EXISTS record_profiles_person_idx ON core.record_profiles (dataset_id, person_record_id) WHERE person_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS record_profiles_company_idx ON core.record_profiles (dataset_id, company_record_id) WHERE company_record_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS email_verifications_email_idx ON core.email_verifications (dataset_id, record_email_id);

-- review queue
CREATE INDEX IF NOT EXISTS match_candidates_review_idx ON core.match_candidates (entity, status);
CREATE INDEX IF NOT EXISTS match_candidates_right_idx ON core.match_candidates (right_dataset_id, right_record_id);

-- bookkeeping
CREATE INDEX IF NOT EXISTS import_batches_file_idx ON catalog.import_batches (file_id);
CREATE INDEX IF NOT EXISTS transform_errors_batch_idx ON catalog.transform_errors (import_batch_id);
CREATE INDEX IF NOT EXISTS rejected_rows_batch_idx ON catalog.rejected_rows (import_batch_id);
CREATE INDEX IF NOT EXISTS files_duplicate_idx ON catalog.files (duplicate_of_file_id) WHERE duplicate_of_file_id IS NOT NULL;
