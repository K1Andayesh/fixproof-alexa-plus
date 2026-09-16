-- Local D1 only: verify a request receipt follows the immediately preceding CAS update.
CREATE TABLE IF NOT EXISTS _fixproof_cas_probe_case (id TEXT PRIMARY KEY, revision INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS _fixproof_cas_probe_receipt (id TEXT PRIMARY KEY);
DELETE FROM _fixproof_cas_probe_case;
DELETE FROM _fixproof_cas_probe_receipt;
INSERT INTO _fixproof_cas_probe_case (id, revision) VALUES ('fictional', 0);
UPDATE _fixproof_cas_probe_case SET revision = 1 WHERE id = 'fictional' AND revision = 9;
INSERT INTO _fixproof_cas_probe_receipt (id) SELECT 'stale' WHERE changes() = 1;
SELECT COUNT(*) AS stale_receipts FROM _fixproof_cas_probe_receipt;
UPDATE _fixproof_cas_probe_case SET revision = 1 WHERE id = 'fictional' AND revision = 0;
INSERT INTO _fixproof_cas_probe_receipt (id) SELECT 'valid' WHERE changes() = 1;
SELECT COUNT(*) AS valid_receipts FROM _fixproof_cas_probe_receipt;
DROP TABLE _fixproof_cas_probe_receipt;
DROP TABLE _fixproof_cas_probe_case;
