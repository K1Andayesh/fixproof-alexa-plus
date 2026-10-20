const test = require('node:test');
const assert = require('node:assert/strict');
const { digestEvidence, verify } = require('./verify_judge_suite_report.cjs');

function report() {
  return {
    schema_version: 'fixproof-judge-suite-v1',
    tools_discovered: 5,
    cases: ['streaks', 'scope', 'retry'].map((id) => {
      const evidence = { case_id: `fictional-${id}`, reported_issue: `${id} proof` };
      const fingerprint = digestEvidence(evidence);
      return {
        id,
        result: 'passed',
        evidence,
        evidence_integrity: {
          algorithm: 'sha256',
          canonicalization: 'fixproof-sorted-json-v1',
          covers: 'evidence',
          authorship_proof: false,
          digest: fingerprint,
        },
        fingerprint,
        browser_recomputation: 'matched',
      };
    }),
  };
}

test('a complete suite report independently verifies all three evidence objects', () => {
  assert.equal(verify(report()), 3);
});

test('a changed evidence field fails verification', () => {
  const changed = report();
  changed.cases[1].evidence.reported_issue = 'changed after export';
  assert.throws(() => verify(changed), /fingerprint mismatch/);
});
