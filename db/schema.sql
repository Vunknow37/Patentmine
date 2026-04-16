CREATE TABLE patents (
    id              TEXT PRIMARY KEY,   -- e.g. US7234567, IN/PCT/2015/123
    source          TEXT,               -- PATENTSVIEW | IPINDIA | EPO | WIPO
    country         TEXT,               -- US, IN, EP, WO, DE, GB...
    title           TEXT,
    abstract        TEXT,
    assignee        TEXT,               -- company or university name
    assignee_type   TEXT,               -- corporate | university | individual
    inventors       TEXT,               -- JSON array
    grant_date      TEXT,
    lapse_date      TEXT,               -- when it entered public domain
    lapse_reason    TEXT,               -- FEE_NOT_PAID | EXPIRED | ABANDONED
    cpc_codes       TEXT,               -- JSON array of CPC codes
    ipc_codes       TEXT,               -- JSON array
    tech_domain     TEXT,               -- human-readable e.g. "Clean Energy"
    citation_count  INTEGER DEFAULT 0,
    paper_title     TEXT,               -- linked OpenAlex paper
    paper_url       TEXT,
    paper_citations INTEGER DEFAULT 0,
    opportunity_score REAL DEFAULT 0,
    startup_opportunity TEXT,
    original_url    TEXT,               -- link back to source
    scraped_at      TEXT
);

CREATE INDEX idx_country ON patents(country);
CREATE INDEX idx_domain ON patents(tech_domain);
CREATE INDEX idx_score ON patents(opportunity_score DESC);
CREATE INDEX idx_lapse ON patents(lapse_date);
CREATE INDEX idx_source ON patents(source);
