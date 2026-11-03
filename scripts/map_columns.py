"""Phase 3: propose a mapping from every source column to a canonical field, for human review.

Reads reports/schemas.json (from profile_files.py). For each column in each distinct layout it proposes
<entity>.<field> (entity = person | company | source), checks the proposal against the profiled data type,
and assigns a confidence. Nothing is dropped: unmapped columns stay in raw JSONB as extra attributes.

Outputs:
  reports/column_mapping.csv   one row per (schema, column) -> review this (filter needs_review = yes)
  reports/column_mapping.md    coverage per canonical field, top unmapped headers, review queue
  docs/canonical_fields.md     the canonical field dictionary

Usage: python3 -I scripts/map_columns.py
"""
import csv
import json
import os
import re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")

# (pattern on normalized header, field, confidence cap[, transform template]). First match wins. Tried on the
# full header, then on the header with its entity prefix ("company ", "person ", ...) removed.
# "entity:field" pins the entity. Transform templates use named groups, e.g. "kind=work;position={n}".
RULES = [
    # --- numbered / typed contact columns (before the generic email/phone rules)
    (r"^(?:work )?email (?P<n>\d)$", "email", None, "kind=work;position={n}"),
    (r"^direct email (?P<n>\d)$", "email", None, "kind=direct;position={n}"),
    (r"^(?:work )?email (?P<n>\d) status$", "email_status", None, "kind=work;position={n}"),
    (r"^direct email (?P<n>\d) status$", "email_status", None, "kind=direct;position={n}"),
    (r"^email (?P<n>\d) (?:validation|total ai)$", "email_status", None, "position={n}"),
    (r"^personal email (?:validation|total ai)$", "email_status", None, "kind=personal"),
    (r"^phone (?P<n>\d)$", "phone", None, "position={n}"),
    (r"^first phone$", "phone", None, "position=1"),
    # --- abbreviated company columns (LinkedIn 945K export): c = company
    (r"^cphone$", "company:phone", None), (r"^clinkedin$", "company:linkedin_url", None),
    (r"^cfacebook$", "company:facebook_url", None), (r"^cx$", "company:twitter_url", "medium"),
    (r"^ccity$", "company:city", None), (r"^cstate$", "company:state", None),
    (r"^ccountry$", "company:country", None), (r"^cpostalcode$", "company:postal_code", None),
    (r"^companysize$", "company:employee_range", None), (r"^foundedyear$", "company:founded_year", None),
    (r"^managementlevel$", "seniority", None), (r"^postalcode$", "postal_code", None),
    # --- funding facts (core.company_funding)
    (r"^(total funding|funding total|totalfunding)$", "funding:total_funding_raw", None),
    (r"^(latest funding|last funding type)$", "funding:last_funding_type", None),
    (r"^latest funding amount$", "funding:last_funding_amount_usd", None),
    (r"^(last raised at|last funding at)$", "funding:last_funding_at", None),
    (r"^num funding rounds$", "funding:num_funding_rounds", None),
    (r"^num investors$", "funding:num_investors", None),
    (r"^num exits$", "funding:num_exits", None),
    (r"^num acquisitions$", "funding:num_acquisitions", None),
    (r"^listed stock symbol$", "funding:stock_symbol", None),
    (r"^operating status$", "funding:operating_status", None),
    # --- email verification results (core.email_verifications, attached to the row's primary email)
    (r"^zb status$", "verification:status", None, "provider=zerobounce"),
    (r"^zb sub status$", "verification:sub_status", None, "provider=zerobounce"),
    (r"^(zb mx found|mx found|mx accepts mail)$", "verification:mx_found", None),
    (r"^(zb smtp provider|smtp provider)$", "verification:smtp_provider", None),
    (r"^is deliverable$", "verification:is_deliverable", None),
    (r"^is disposable$", "verification:is_disposable", None),
    (r"^is role account$", "verification:is_role_account", None),
    (r"^is catch all$", "verification:is_catch_all", None),
    (r"^(tech used)$", "technologies", None),
    (r"^(team size)$", "employee_range", None),
    (r"^(linked url|li profile url)$", "linkedin_url", None),
    (r"^facebook profile$", "facebook_url", None),
    # --- source PDL short keys: meaning inferred from value shapes only -> capped at medium
    (r"^n$", "full_name", "medium"), (r"^e$", "email", "medium"), (r"^t$", "phone", "medium"),
    (r"^a$", "location_raw", "medium"), (r"^liid$", "linkedin_username", "medium"),
    # --- names
    (r"^(full ?name|contact full name|contact name|contact person|person name|name unanalyzed downcase|owner name)$", "full_name", None),
    (r"^(first ?name|first|fname|given name|first name unanalyzed|furst name)$", "first_name", None),
    (r"^(last ?name|last|lname|surname|family name|last name unanalyzed)$", "last_name", None),
    (r"^(middle ?name|middle initial|middle)$", "middle_name", None),
    # --- job
    (r"^(job ?title|title|position|designation|job)$", "job_title", None),
    (r"^(title normalized|primary title normalized for faceting)$", "job_title_normalized", None),
    (r"^seniority$", "seniority", None),
    (r"^(departments?|functions?|detailed function|sub role|job function)$", "department", None),
    (r"^(job start date|start date)$", "job_start_date", None),
    # --- email
    (r"^(emails?|e ?mail|e ?mail address|primary email|work email|business email|corporate email)$", "email", None),
    (r"^(personal emails?|secondary email|other emails?)$", "secondary_email", None),
    (r"^generic email$", "company:email", None),
    (r"^(email status|email status cd|email confidence|extrapolated email confidence|email verification|verified)$", "email_status", None),
    # --- phone
    (r"^(corporate phone|company phone|office phone|main phone|business phone|comp phone)$", "company:phone", None),
    (r"^(phones?|phone numbers?|telephones?|tel|telephone|work direct phone|direct phone|sanitized phone|contact phone)$", "phone", None),
    (r"^(mobile|mobile phone|cell|cell phone|mobile number)$", "mobile_phone", None),
    (r"^home phone$", "home_phone", None),
    (r"^other phone$", "other_phone", None),
    (r"^phone type$", "phone_type", None),
    # --- social
    (r"^(linkedin|linkedin url|linkedin profile|linkedin link|linkedin profile url|pers linkedin)$", "linkedin_url", None),
    (r"^(linkedin username|linkedin id)$", "linkedin_username", None),
    (r"^(twitter|twitter url|twitter username|twitter handle)$", "twitter_url", None),
    (r"^(facebook|facebook url|facebook username)$", "facebook_url", None),
    (r"^(github|github url|github username)$", "github_url", None),
    (r"^(instagram|instagram url)$", "instagram_url", None),
    (r"^(youtube|youtube url|youtube channel url)$", "youtube_url", None),
    (r"^(linkedin connections|num linkedin connections)$", "linkedin_connections", None),
    # --- company
    (r"^(company size|employee range|employees range|size range|number of employees range)$", "employee_range", None),
    (r"^(employees|employee|number of employees|num employees|employee count|employees count|headcount|estimated num employees|size)$", "employee_count", None),
    (r"^(revenue|reveneu|annual revenue|sales revenue usd|sales revenue|revenue range|estimated revenue)$", "revenue", None),
    (r"^(founded|year founded|founded year|founded date|founded on|founding year)$", "founded_year", None),
    (r"^(website|web address|url|homepage|site|web|website url)$", "website", None),
    (r"^(domain|domain name|primary domain)$", "domain", None),
    (r"^(industry|industries|primary industry)$", "industry", None),
    (r"^(sub industry|industry 2|secondary industry)$", "sub_industry", None),
    (r"^(vertical|category|categories|sector|naics|sic|naics code|sic code)$", "category", None),
    (r"^(technologies|technology|tech stack|installed apps|technologies used)$", "technologies", None),
    (r"^(keywords|tags|specialties|specialities)$", "keywords", None),
    (r"crunchbase", "crunchbase_url", None),
    (r"^(logo|logo url)$", "logo_url", None),
    (r"^(description|short description|about|about us|meta description|overview)$", "description", None),
    (r"^name$", "name", None),
    # --- person extras
    (r"^(summary|job summary|bio|headline)$", "headline", None),
    (r"^(skills)$", "skills", None), (r"^(interests)$", "interests", None),
    (r"^(gender|sex)$", "gender", None),
    (r"^(birth date|birth year|dob|date of birth)$", "birth_date_raw", None),
    (r"^(inferred salary|salary)$", "salary", None),
    (r"^years experience$", "years_experience", None),
    # --- location (shared)
    (r"^(address|street|street address|mailing address|address 1|address line 1|full address|location street address)$", "address", None),
    (r"^(address line 2|address 2|location address line 2)$", "address_line2", None),
    (r"^(city|locality|primary city|town|location city|location locality)$", "city", None),
    (r"^(region|location region)$", "state", "medium"),
    (r"^(state|province|primary state|location state|state code)$", "state", None),
    (r"^(country|countries|location country|country code|country name)$", "country", None),
    (r"^(zip|zip code|postal code|postcode|zipcode|location postal code|postal)$", "postal_code", None),
    (r"^(metro|location metro)$", "metro", None),
    (r"^(continent|location continent)$", "continent", None),
    (r"^(location|location name|full location|geo|location geo|location geojson|hq location|headquarters|"
     r"location state with country|location city with state or country)$", "location_raw", None),
    # --- provenance
    (r"^(id|index|uuid|record id)$", "source:record_id", None),
    (r"^(created at|last updated|updated at|research date|vacuumed at|date added|scraped at)$", "source:observed_at", None),
]
RULES = [(re.compile(r[0]), r[1], r[2], r[3] if len(r) > 3 else None) for r in RULES]

PREFIX = re.compile(r"^(person|contact|company|organization|org|comp)\s+(.+)$")
PREFIX_ENTITY = {"person": "person", "contact": "person", "company": "company", "organization": "company",
                 "org": "company", "comp": "company"}

PERSON_ONLY = {"full_name", "first_name", "last_name", "middle_name", "job_title", "job_title_normalized", "seniority",
               "department", "job_start_date", "secondary_email", "email_status", "mobile_phone", "home_phone",
               "other_phone", "linkedin_username", "linkedin_connections", "headline", "skills", "interests",
               "gender", "birth_date_raw", "salary", "years_experience"}
COMPANY_ONLY = {"name", "website", "domain", "employee_range", "employee_count", "revenue", "founded_year",
                "sub_industry", "category", "technologies", "crunchbase_url", "logo_url", "description"}
PII = {"full_name", "first_name", "last_name", "middle_name", "email", "secondary_email", "phone", "mobile_phone",
       "home_phone", "other_phone", "linkedin_url", "linkedin_username", "twitter_url", "facebook_url",
       "github_url", "instagram_url", "address", "address_line2", "postal_code", "gender", "birth_date_raw", "salary"}
EXPECT = {"email": {"email", "json"}, "secondary_email": {"email", "json"}, "phone": {"phone", "int", "json"},
          "mobile_phone": {"phone", "int"}, "home_phone": {"phone", "int"}, "other_phone": {"phone", "int"},
          "website": {"url", "domain"}, "domain": {"domain", "url"}, "founded_year": {"int", "date"},
          "employee_count": {"int", "float"}, "linkedin_url": {"url", "domain", "text"},
          "birth_date_raw": {"date", "int"}, "source:observed_at": {"date"}}
DATA_TYPES = {"email", "phone", "url", "int", "float", "date"}


def norm(h):
    h = (h or "").lower().replace("#", "")
    return re.sub(r"[^a-z0-9]+", " ", h).strip()


def match(h):
    for rx, field, cap, tmpl in RULES:
        m = rx.search(h)
        if m:
            return field, cap, (tmpl.format(**m.groupdict()) if tmpl else "")
    return None, None, ""


def map_column(header, person_schema):
    """-> (entity, field, confidence cap, transform, reason)"""
    h = norm(header)
    field, cap, transform = match(h)
    prefix_entity = None
    if not field:
        m = PREFIX.match(h)
        if m:
            prefix_entity = PREFIX_ENTITY[m.group(1)]
            field, cap, transform = match(m.group(2))
    if not field:
        return None, None, None, "", "no rule matched"
    if ":" in field:  # rule pins the entity (company:phone, funding:..., verification:...)
        entity, field = field.split(":")
        return entity, field, cap, transform, "entity fixed by rule"
    if prefix_entity:
        return prefix_entity, field, cap, transform, f"entity from '{h.split()[0]}' prefix"
    if field in PERSON_ONLY:
        return "person", field, cap, transform, "person-only field"
    if field in COMPANY_ONLY:
        return "company", field, cap, transform, "company-only field"
    entity = "person" if person_schema else "company"
    return entity, field, cap, transform, f"shared field -> {entity} (dataset kind)"


OVERRIDES = os.path.join(ROOT, "config", "mapping_overrides.csv")


def load_overrides():
    """Reviewed decisions for columns the rules got wrong or were unsure about (see config/mapping_overrides.csv)."""
    if not os.path.exists(OVERRIDES):
        return []
    return list(csv.DictReader(open(OVERRIDES, newline="")))


def find_override(overrides, header, archives):
    for o in overrides:
        if o["source_header"] == header and (not o["archive_contains"] or o["archive_contains"] in archives):
            return o
    return None


def is_person_schema(headers):
    for h in headers:
        n = norm(h)
        # Only name columns make a dataset person-level ("contact_email" alone is a company's contact).
        if n.startswith("person ") or n == "n":
            return True
        f, _, _ = match(n)
        if f in ("full_name", "first_name", "last_name"):
            return True
    return False


def confidence(field, cap, col, entity, person_schema):
    t = col.get("inferred_type", "empty")
    # Older cached profiles typed '+1 315-... (spreadsheet quote prefix) as text; their samples were still
    # masked from the real values, so masked shapes tell us what the column really holds.
    samples = col.get("samples") or []
    if samples and all(re.fullmatch(r"\*\*\*\d{2}", v) for v in samples):
        t = "phone"
    elif samples and all(re.fullmatch(r"\w\*\*\*@\S+", v) for v in samples):
        t = "email"
    level, why = "high", []
    if t == "empty" or not col.get("non_empty"):
        level, why = "medium", ["column empty in sample"]
    elif field in EXPECT and t not in EXPECT[field]:
        level, why = "low", [f"data looks like '{t}', expected {sorted(EXPECT[field])}"]
    if entity == "person" and field in PERSON_ONLY and not person_schema:
        level, why = "low", why + ["person field in a dataset without person names"]
    order = ["low", "medium", "high"]
    if cap and order.index(cap) < order.index(level):
        level, why = cap, why + ["meaning inferred from value shapes, header not descriptive"]
    return level, "; ".join(why)


def main():
    schemas = json.load(open(os.path.join(REPORTS, "schemas.json")))
    out_rows = []
    coverage = defaultdict(lambda: {"schemas": 0, "rows": 0, "headers": Counter()})
    unmapped = defaultdict(lambda: {"schemas": 0, "rows": 0})
    kinds = Counter()
    overrides = load_overrides()
    used_overrides = set()
    for s in schemas:
        headers = s["header"]
        no_header = sum(1 for h in headers if h and h.strip() and _looks_like_data(h)) >= 2
        person_schema = is_person_schema(headers)
        kinds["person" if person_schema else "company/other"] += s["est_rows"]
        cols = {c["index"]: c for c in s.get("columns", [])}
        counted = set()
        for i, h in enumerate(headers):
            col = cols.get(i, {})
            if no_header:
                entity, field, cap, transform, reason = None, None, None, "", "file has no header row (first row is data)"
            else:
                entity, field, cap, transform, reason = map_column(h, person_schema)
            level, why = confidence(field, cap, col, entity, person_schema) if field else ("unmapped", "")
            archives = " | ".join(a.replace("Copy of ", "")[:45] for a in s["archives"])
            target = f"{entity}.{field}" if field else ""
            # review decision: explicit override > policy by confidence
            # Overrides only settle columns the rules were unsure about; never touch an agreeing (high) mapping.
            o = find_override(overrides, h, archives) if level == "low" else None
            if o:
                used_overrides.add((o["source_header"], o["archive_contains"]))
                status = "rejected" if o["decision"] == "reject" else "approved"
                target = "" if o["decision"] == "reject" else (o["to_target"] or target)
                transform = o["transform"] or transform
                note, decided_by = o["note"], "override"
            elif level == "high":
                status, note, decided_by = "approved", "header and data agree", "rule"
            elif level == "medium":
                status, note, decided_by = "approved", "policy: header match accepted (" + why + ")", "policy"
            elif level == "unmapped":
                status, note, decided_by = "approved", "no canonical field: kept in extra (jsonb)", "policy"
            else:
                status, note, decided_by = "proposed", "needs a decision", "rule"
            if target:
                entity, field = target.split(".", 1)
                if target not in counted:  # several columns can map to one target; count the layout once
                    counted.add(target)
                    coverage[target]["schemas"] += 1
                    coverage[target]["rows"] += s["est_rows"]
                coverage[target]["headers"][h] += 1
            else:
                unmapped[norm(h) or "(blank)"]["schemas"] += 1
                unmapped[norm(h) or "(blank)"]["rows"] += s["est_rows"]
            out_rows.append({
                "schema_id": s["schema_id"], "dataset_kind": "person" if person_schema else "company/other",
                "files": s["files"], "est_rows": s["est_rows"],
                "archives": archives,
                "example_file": s["example"][-80:], "col_index": i, "source_header": h,
                "inferred_type": col.get("inferred_type", ""), "fill_pct": col.get("fill_pct", ""),
                "samples_masked": " || ".join(col.get("samples", []))[:150],
                "target": target, "transform": transform,
                "pii": "yes" if target and entity == "person" and field in PII else "",
                "confidence": level, "reason": "; ".join(x for x in (reason, why) if x),
                "review_status": status, "decided_by": decided_by, "review_note": note,
            })

    path = os.path.join(REPORTS, "column_mapping.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(sorted(out_rows, key=lambda r: (-r["est_rows"], r["schema_id"], r["col_index"])))

    conf = Counter(r["confidence"] for r in out_rows)
    review = Counter(r["review_status"] for r in out_rows)
    unused = [o for o in overrides if (o["source_header"], o["archive_contains"]) not in used_overrides]
    total_rows = sum(s["est_rows"] for s in schemas)
    L = ["# Column mapping (Phase 3)", "",
         "Generated from header names + profiled data types, plus reviewed decisions in "
         "`config/mapping_overrides.csv`. Columns without a canonical field are not dropped: they are stored in "
         "the record's `extra` jsonb under their original header.", "",
         f"Layouts: {len(schemas)} | Columns: {len(out_rows)} | "
         + " | ".join(f"{k}: {conf[k]}" for k in ("high", "medium", "low", "unmapped")), "",
         "Review status: " + " | ".join(f"{k}: {v}" for k, v in review.most_common())
         + (f" | unused overrides: {len(unused)}" if unused else ""), "",
         f"Rows in person-level datasets: ~{kinds['person']:,} ({100 * kinds['person'] / max(total_rows, 1):.0f}%) | "
         f"company/other: ~{kinds['company/other']:,}", "",
         "## Canonical field coverage (estimated rows that will have this field)", "",
         "| Target | PII | Layouts | Est. rows | Source headers (top) |", "|---|---|---:|---:|---|"]
    for t, c in sorted(coverage.items(), key=lambda kv: -kv[1]["rows"]):
        top = ", ".join(f"`{h}`" for h, _ in c["headers"].most_common(5))
        L.append(f"| {t} | {'yes' if t.startswith('person.') and t.split('.')[1] in PII else ''} | {c['schemas']} | {c['rows']:,} | {top} |")
    L += ["", "## Top unmapped headers (kept as extra attributes unless a rule is added)", "",
          "| Normalized header | Layouts | Est. rows |", "|---|---:|---:|"]
    for h, c in sorted(unmapped.items(), key=lambda kv: -kv[1]["rows"])[:80]:
        L.append(f"| {h[:60]} | {c['schemas']} | {c['rows']:,} |")
    L += ["", "## Decisions on low-confidence columns (config/mapping_overrides.csv)", "",
          "| Source header | Archive | Decision | Target | Transform | Why |", "|---|---|---|---|---|---|"]
    seen = set()
    for r in sorted([r for r in out_rows if r["decided_by"] == "override"], key=lambda r: -r["est_rows"]):
        k = (r["source_header"], r["target"], r["review_status"])
        if k in seen:
            continue
        seen.add(k)
        L.append(f"| `{r['source_header']}` | {r['archives'][:40].replace('|', '/')} | {r['review_status']} | {r['target'] or '(extra)'} | "
                 f"{r['transform']} | {r['review_note']} |")
    pending = [r for r in out_rows if r["review_status"] == "proposed"]
    if pending:
        L += ["", f"## Still needing a decision ({len(pending)})", ""]
        L += [f"- `{r['source_header']}` -> {r['target']} ({r['archives'][:60]}): {r['reason']}" for r in pending[:50]]
    open(os.path.join(REPORTS, "column_mapping.md"), "w").write("\n".join(L) + "\n")

    write_field_doc()
    print(f"wrote {path} ({len(out_rows)} columns); confidence " + ", ".join(f"{k}={v}" for k, v in conf.items())
          + "; review " + ", ".join(f"{k}={v}" for k, v in review.items()) + f"; unused overrides={len(unused)}")


def _looks_like_data(h):
    h = h.strip()
    if "***" in h:  # masked email/phone
        return True
    return bool(re.match(r"^(https?://|www\.)|^[^@\s]+@|^-?\d[\d.,\s-]*$", h))


def write_field_doc():
    fields = sorted({r[1] for r in RULES})
    L = ["# Canonical fields (draft)", "",
         "Target fields used by `scripts/map_columns.py`. Entity is decided per column: an explicit header prefix "
         "(`company`, `organization`, `person`, `contact`...) wins; otherwise person-only / company-only fields go "
         "to that entity, and shared fields (email, phone, city, linkedin_url...) go to `person` in datasets that "
         "contain person names and to `company` otherwise.", "",
         "| Field | Scope | PII |", "|---|---|---|"]
    for f in fields:
        if ":" in f:
            scope, name = f.split(":")
        else:
            name = f
            scope = "person" if f in PERSON_ONLY else "company" if f in COMPANY_ONLY else "shared"
        L.append(f"| {name} | {scope} | {'yes' if name in PII else ''} |")
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    open(os.path.join(ROOT, "docs", "canonical_fields.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
