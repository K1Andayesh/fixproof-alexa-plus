#!/usr/bin/env node

const { createHash } = require('node:crypto');
const { readFileSync } = require('node:fs');

function sortForDigest(value) {
  if (Array.isArray(value)) return value.map(sortForDigest);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value)
        .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
        .map(([key, item]) => [key, sortForDigest(item)]),
    );
  }
  return value;
}

function digestEvidence(evidence) {
  return createHash('sha256').update(JSON.stringify(sortForDigest(evidence))).digest('hex');
}

function verify(report) {
  if (report?.schema_version !== 'fixproof-judge-suite-v1') throw new Error('Unsupported report schema.');
  if (report?.tools_discovered !== 5) throw new Error('The report did not discover the five-tool contract.');
  if (!Array.isArray(report?.cases) || report.cases.length !== 3) throw new Error('The report must contain exactly three proof cases.');
  const expected = ['retry', 'scope', 'streaks'];
  const received = report.cases.map((item) => item.id).sort();
  if (JSON.stringify(received) !== JSON.stringify(expected)) throw new Error('The expected proof case IDs were not present exactly once.');
  for (const item of report.cases) {
    const integrity = item.evidence_integrity;
    if (item.result !== 'passed' || item.browser_recomputation !== 'matched') throw new Error(`${item.id}: proof was not reported as passed and matched.`);
    if (integrity?.algorithm !== 'sha256' || integrity?.canonicalization !== 'fixproof-sorted-json-v1' || integrity?.covers !== 'evidence' || integrity?.authorship_proof !== false) {
      throw new Error(`${item.id}: unsupported evidence-integrity declaration.`);
    }
    const recomputed = digestEvidence(item.evidence);
    if (recomputed !== integrity.digest || recomputed !== item.fingerprint) throw new Error(`${item.id}: evidence fingerprint mismatch.`);
  }
  return report.cases.length;
}

if (require.main === module) {
  const path = process.argv[2];
  if (!path) {
    console.error('Usage: node validation/verify_judge_suite_report.cjs <fixproof-live-judge-suite.json>');
    process.exit(2);
  }
  try {
    const count = verify(JSON.parse(readFileSync(path, 'utf8')));
    console.log(`Verified ${count}/3 FixProof judge-suite evidence fingerprints.`);
  } catch (error) {
    console.error(`Verification failed: ${error instanceof Error ? error.message : String(error)}`);
    process.exit(1);
  }
}

module.exports = { digestEvidence, verify };
