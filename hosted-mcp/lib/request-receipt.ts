const RECEIPT_VERSION = "fixproof-request-receipt-1";

type RequestReceipt<T> = {
  receipt_version: typeof RECEIPT_VERSION;
  operation: string;
  input_sha256: string;
  case_record: T;
};

function sortForDigest(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortForDigest);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0)
        .map(([key, item]) => [key, sortForDigest(item)]),
    );
  }
  return value;
}

async function sha256(value: unknown) {
  const canonical = JSON.stringify(sortForDigest(value));
  const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(canonical));
  return Array.from(new Uint8Array(hash), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

export async function makeRequestReceipt<T>(operation: string, input: unknown, caseRecord: T) {
  const receipt: RequestReceipt<T> = {
    receipt_version: RECEIPT_VERSION,
    operation,
    input_sha256: await sha256({ operation, input }),
    case_record: caseRecord,
  };
  return JSON.stringify(receipt);
}

export async function readRequestReceipt<T>(body: string, operation: string, input: unknown): Promise<
  | { kind: "match"; case_record: T }
  | { kind: "mismatch" }
  | { kind: "legacy" }
> {
  const parsed = JSON.parse(body) as Partial<RequestReceipt<T>>;
  if (parsed.receipt_version !== RECEIPT_VERSION || !parsed.case_record) return { kind: "legacy" };
  const inputSha256 = await sha256({ operation, input });
  if (parsed.operation !== operation || parsed.input_sha256 !== inputSha256) return { kind: "mismatch" };
  return { kind: "match", case_record: parsed.case_record };
}
