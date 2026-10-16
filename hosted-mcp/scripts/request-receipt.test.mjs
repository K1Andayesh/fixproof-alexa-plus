import assert from "node:assert/strict";
import test from "node:test";
import { makeRequestReceipt, readRequestReceipt } from "../lib/request-receipt.ts";

const original = {
  request_id: "retry-1",
  case_id: "fictional-case",
  revision: 1,
  observation: "Original fictional observation",
};
const caseRecord = { id: "fictional-case", revision: 2 };

test("an identical operation and payload replays its stored result", async () => {
  const body = await makeRequestReceipt("record_outcome", original, caseRecord);
  assert.deepEqual(await readRequestReceipt(body, "record_outcome", { ...original }), {
    kind: "match",
    case_record: caseRecord,
  });
});

test("the same request ID cannot be reused with changed input", async () => {
  const body = await makeRequestReceipt("record_outcome", original, caseRecord);
  assert.deepEqual(await readRequestReceipt(body, "record_outcome", { ...original, observation: "Changed" }), {
    kind: "mismatch",
  });
});

test("the same request ID cannot cross tool boundaries", async () => {
  const body = await makeRequestReceipt("record_outcome", original, caseRecord);
  assert.deepEqual(await readRequestReceipt(body, "ask_fixproof", original), { kind: "mismatch" });
});

test("legacy unbound receipts fail closed", async () => {
  assert.deepEqual(await readRequestReceipt(JSON.stringify(caseRecord), "record_outcome", original), { kind: "legacy" });
});
