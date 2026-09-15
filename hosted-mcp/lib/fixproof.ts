import { env } from "cloudflare:workers";

export type Source = { title: string; url: string; service_url: string; document: string; verified: string; sha256: string };
export type Step = { workflow: "drying" | "food" | "detergent" | "streaks" | "noise" | "rust" | "clouding"; title: string; text: string; pages: number[] };
export type Attempt = { outcome: string; observation: string; recorded_at: string };
export type Citation = { title: string; document: string; page: number; url: string; source_verified: string; content_sha256: string };
export type FixProofCase = {
  id: string; created: string; model: string; verified: boolean; demo: boolean; issue: string;
  workflow: Step["workflow"] | null; status: "Open" | "Handover ready"; revision: number;
  attempts: Record<string, Attempt>; pending: string | null;
  latest_event?: { kind: string; text: string; citations?: Citation[] }; safety_report?: string;
};

const definitions: Record<string, Omit<Step, "pages">> = {
  programme: { workflow: "drying", title: "Check the programme", text: "Check whether the selected programme includes drying. Shortening options can reduce drying performance." },
  rinse_aid: { workflow: "drying", title: "Check rinse aid", text: "Check the rinse aid indicator and dosage. Use the cited pages for filling or adjusting it; use only domestic dishwasher rinse aid." },
  loading: { workflow: "drying", title: "Check pooled water", text: "Where possible, angle items so water can drain from their recesses." },
  waiting: { workflow: "drying", title: "Allow drying to finish", text: "Let the programme finish, then wait 30 minutes before removing the tableware." },
  food_spacing: { workflow: "food", title: "Check spacing and contact", text: "Arrange tableware with enough space for spray jets to reach the surfaces, and avoid points of contact." },
  food_spray_arm: { workflow: "food", title: "Check spray-arm movement", text: "Arrange tableware so it does not block the spray arms from rotating." },
  food_filters: { workflow: "food", title: "Check the filters", text: "Check the filters for residue and clean them under running water as described in the manual." },
  food_programme: { workflow: "food", title: "Check wash intensity", text: "Select a more intensive washing programme for stubborn food remnants." },
  detergent_tray: { workflow: "detergent", title: "Clear the tablet collecting tray", text: "Arrange the top basket so tableware does not obstruct the tablet collecting tray, and keep tableware and fragrance dispensers out of the tray." },
  detergent_position: { workflow: "detergent", title: "Reposition the detergent tablet", text: "Position the detergent tablet transversely in the dispenser rather than vertically." },
  streaks_rinse_setting: { workflow: "streaks", title: "Lower the rinse aid setting", text: "If the rinse aid dosage is set too high, set the rinse aid system to a lower setting." },
  streaks_add_rinse_aid: { workflow: "streaks", title: "Check for rinse aid", text: "If no rinse aid has been added, fill the rinse aid dispenser as described in the manual." },
  streaks_tray: { workflow: "streaks", title: "Clear the tablet collecting tray", text: "Arrange the top basket so tableware does not block the detergent dispenser lid, and keep tableware and fragrance dispensers out of the tablet collecting tray." },
  streaks_prerinse: { workflow: "streaks", title: "Avoid intensive pre-rinsing", text: "Remove only large food remnants before loading; do not pre-rinse the tableware." },
  noise_spray_arm: { workflow: "noise", title: "Check spray-arm clearance", text: "Arrange tableware so the spray arms do not strike it during the wash." },
  noise_load_distribution: { workflow: "noise", title: "Distribute a small load", text: "If a small load lets water jets strike the tub directly, distribute the tableware evenly or add more tableware for the next wash." },
  noise_light_items: { workflow: "noise", title: "Secure light items", text: "Position light items of tableware securely so they do not move about during the wash cycle." },
  rust_resistant_tableware: { workflow: "rust", title: "Use rust-resistant tableware", text: "Use rust-resistant tableware when rust spots appear on cutlery." },
  rust_remove_rusting_items: { workflow: "rust", title: "Keep rusting items out", text: "Do not wash rusting items together with the cutlery." },
  clouding_dishwasher_proof: { workflow: "clouding", title: "Use dishwasher-proof glasses", text: "Use glasses that are dishwasher-proof; long-term wear can otherwise be expected." },
  clouding_steam_phase: { workflow: "clouding", title: "Avoid a lengthy steam phase", text: "Avoid leaving glassware standing in the appliance for a long time after the wash cycle ends." },
  clouding_lower_temperature: { workflow: "clouding", title: "Use a lower-temperature programme", text: "Use a programme with a lower washing temperature." },
  clouding_glass_protection: { workflow: "clouding", title: "Use glass-protection detergent", text: "Use detergent with a glass protection component." },
};

const catalogs = {
  "Bosch SMS6HAI02A/01": {
    source: { title: "Bosch SMS6HAI02A · Australian English user manual", url: "https://media3.bsh-group.com/Documents/9001676154_A.pdf", service_url: "https://www.bosch-home.com.au/en/productservice/SMS6HAI02A-01", document: "9001676154 (010805) 650 V1", verified: "2026-09-15", sha256: "af965b35d3447c81adfc56bf652f75f8da565d47a9d4dc9c1e55030ae521a47c" },
    pages: { programme:[40], rinse_aid:[40,23], loading:[41], waiting:[41], food_spacing:[42], food_spray_arm:[42], food_filters:[42,36,37], food_programme:[42], detergent_tray:[42], detergent_position:[42], streaks_rinse_setting:[44], streaks_add_rinse_aid:[44,23], streaks_tray:[44,27], streaks_prerinse:[45], noise_spray_arm:[48], noise_load_distribution:[48], noise_light_items:[48], rust_resistant_tableware:[45], rust_remove_rusting_items:[45], clouding_dishwasher_proof:[45], clouding_steam_phase:[45], clouding_lower_temperature:[45], clouding_glass_protection:[45] },
  },
  "Bosch SMS6HCI01A/38": {
    source: { title: "Bosch SMS6HCI01A · Australian English user manual", url: "https://media3.bsh-group.com/Documents/9001720311_B.pdf", service_url: "https://www.bosch-home.com.au/en/productservice/SMS6HCI01A-38", document: "9001720311 (050605) 650 A1", verified: "2026-09-15", sha256: "b2bb4608cd266752804e8c02b3e251bb31e6c32f95824e602614b13f83240fc9" },
    pages: { programme:[44], rinse_aid:[44,24,25], loading:[44], waiting:[44], food_spacing:[45], food_spray_arm:[45,39], food_filters:[45,38,39], food_programme:[45], detergent_tray:[46,28], detergent_position:[46], streaks_rinse_setting:[48,25], streaks_add_rinse_aid:[48,24], streaks_tray:[48,28], streaks_prerinse:[48], noise_spray_arm:[52], noise_load_distribution:[52], noise_light_items:[52], rust_resistant_tableware:[49], rust_remove_rusting_items:[49], clouding_dishwasher_proof:[49], clouding_steam_phase:[49], clouding_lower_temperature:[49], clouding_glass_protection:[49] },
  },
  "Bosch SMS6HCI02A/72": {
    source: { title: "Bosch SMS6HCI02A · Australian English user manual", url: "https://media3.bsh-group.com/Documents/9002017246_A.pdf", service_url: "https://www.bosch-home.com.au/en/productservice/SMS6HCI02A-72", document: "9002017246 (050605) 650 V1", verified: "2026-09-15", sha256: "b499156281a114882fd254e11400bc6318db71020eab2c4cfac9848264b4b476" },
    pages: { programme:[41], rinse_aid:[41,23,24], loading:[41,28], waiting:[42], food_spacing:[42], food_spray_arm:[42,37], food_filters:[43,36,37], food_programme:[43], detergent_tray:[43,27,28], detergent_position:[43], streaks_rinse_setting:[45,24], streaks_add_rinse_aid:[45,23], streaks_tray:[45,27,28], streaks_prerinse:[46], noise_spray_arm:[49], noise_load_distribution:[49], noise_light_items:[50], rust_resistant_tableware:[46], rust_remove_rusting_items:[46], clouding_dishwasher_proof:[46], clouding_steam_phase:[46], clouding_lower_temperature:[46], clouding_glass_protection:[46] },
  },
} satisfies Record<string, { source: Source; pages: Record<string, number[]> }>;

export const models = Object.keys(catalogs);
export const outcomes = ["Issue unchanged", "Still wet", "Improved, not resolved", "Not yet tested", "Skipped"] as const;

function database(): D1Database {
  if (!env.DB) throw new Error("The hosted evidence store is unavailable.");
  return env.DB;
}

function clean(value: string, max = 500): string {
  return String(value ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}

export function catalog(model: string) {
  const wanted = clean(model, 100).replace(/\s+/g, "").toUpperCase();
  return Object.entries(catalogs).find(([key]) => key.replace(/\s+/g, "").toUpperCase() === wanted) ?? null;
}

export function stepsFor(model: string): Record<string, Step> {
  const entry = catalog(model);
  if (!entry) return {};
  const pages = entry[1].pages as Record<string, number[]>;
  return Object.fromEntries(Object.entries(definitions).map(([id, step]) => [id, { ...step, pages: [...pages[id]] }])) as Record<string, Step>;
}

export function citationsFor(model: string, pages: number[]): Citation[] {
  const entry = catalog(model);
  if (!entry) return [];
  const source = entry[1].source;
  return pages.map((page) => ({ title: source.title, document: source.document, page, url: `${source.url}#page=${page}`, source_verified: source.verified, content_sha256: source.sha256 }));
}

function classify(text: string): FixProofCase["workflow"] {
  const value = clean(text).toLowerCase();
  if (/food|remnant|dirty|soil/.test(value)) return "food";
  if (/detergent|tablet|powder|residue/.test(value)) return "detergent";
  if (/streak|white coating|limescale/.test(value)) return "streaks";
  if (/knock|rattl|spray arm.*(?:hit|strik)|noise during/.test(value)) return "noise";
  if (/rust|corrosion spot/.test(value)) return "rust";
  if (/irreversible cloud|cloudy|clouding|permanent haze|does not wipe off/.test(value)) return "clouding";
  if (/wet|dry|water/.test(value)) return "drying";
  return null;
}

function hazard(text: string): boolean {
  const value = clean(text).toLowerCase().replace(/\bno\s+(smoke|sparks?|burning|leak(?:ing)?)\b/g, "").replace(/\bsmoke test\b/g, "");
  return /\b(smoke|sparks?|burning|electric shock|leak(?:ing)?)\b/.test(value);
}

function view(caseRecord: FixProofCase) {
  const steps = stepsFor(caseRecord.model);
  const entry = catalog(caseRecord.model);
  const pending = caseRecord.pending ? steps[caseRecord.pending] : undefined;
  const performed = Object.values(caseRecord.attempts).filter((a) => ["Issue unchanged", "Still wet", "Improved, not resolved"].includes(a.outcome)).length;
  return {
    case_id: caseRecord.id, revision: caseRecord.revision, status: caseRecord.status, model: caseRecord.model,
    model_confirmed: caseRecord.verified, fictional_demo: caseRecord.demo, reported_issue: caseRecord.issue, workflow: caseRecord.workflow,
    reference_match: entry ? { supported: true, catalog_model: entry[0], user_confirmed_model: caseRecord.verified, document: entry[1].source.document, source_verified: entry[1].source.verified } : { supported: false },
    recorded_outcomes: caseRecord.attempts,
    evidence_summary: { user_reports_performed: performed, deferred_or_skipped: Object.keys(caseRecord.attempts).length - performed },
    pending_check: caseRecord.pending && pending ? { step_id: caseRecord.pending, ...pending, citations: citationsFor(caseRecord.model, pending.pages) } : null,
    latest_event: caseRecord.latest_event ?? null, safety_report: caseRecord.safety_report ?? null,
  };
}

async function cached(requestId: string): Promise<FixProofCase | null> {
  const row = await database().prepare("SELECT body FROM requests WHERE id = ?").bind(clean(requestId, 100)).first<{ body: string }>();
  return row ? JSON.parse(row.body) as FixProofCase : null;
}

export async function readCase(id: string): Promise<FixProofCase> {
  const row = await database().prepare("SELECT body FROM cases WHERE id = ?").bind(clean(id, 80)).first<{ body: string }>();
  if (!row) throw new Error("Case not found.");
  return JSON.parse(row.body) as FixProofCase;
}

async function saveNew(caseRecord: FixProofCase, requestId: string): Promise<FixProofCase> {
  const now = new Date().toISOString();
  await database().batch([
    database().prepare("INSERT INTO cases (id, revision, body, created_at) VALUES (?, ?, ?, ?)").bind(caseRecord.id, caseRecord.revision, JSON.stringify(caseRecord), now),
    database().prepare("INSERT INTO requests (id, case_id, body, created_at) VALUES (?, ?, ?, ?)").bind(clean(requestId, 100), caseRecord.id, JSON.stringify(caseRecord), now),
  ]);
  return caseRecord;
}

async function saveUpdated(caseRecord: FixProofCase, requestId: string, expectedRevision: number): Promise<FixProofCase> {
  const next = { ...caseRecord, revision: expectedRevision + 1 };
  const now = new Date().toISOString();
  const results = await database().batch([
    database().prepare("UPDATE cases SET revision = ?, body = ? WHERE id = ? AND revision = ?").bind(next.revision, JSON.stringify(next), next.id, expectedRevision),
    database().prepare("INSERT INTO requests (id, case_id, body, created_at) VALUES (?, ?, ?, ?)").bind(clean(requestId, 100), next.id, JSON.stringify(next), now),
  ]);
  if ((results[0].meta?.changes ?? 0) !== 1) throw new Error("This case changed. Read it again before continuing.");
  return next;
}

export async function startCase(input: { request_id: string; reported_issue: string; model: string; model_confirmed: boolean; fictional_demo: boolean }) {
  const requestId = clean(input.request_id, 100);
  const prior = await cached(requestId);
  if (prior) return view(prior);
  if (!input.fictional_demo) throw new Error("The public endpoint accepts fictional evaluation cases only. Do not send real household or personal data.");
  if (!input.model_confirmed) throw new Error("Confirm the exact fictional model identity before starting.");
  const entry = catalog(input.model);
  if (!entry) throw new Error(`Unsupported model. Use one of: ${models.join(", ")}.`);
  const issue = clean(input.reported_issue, 300);
  if (!issue) throw new Error("reported_issue is required.");
  const isHazard = hazard(issue);
  const caseRecord: FixProofCase = {
    id: crypto.randomUUID(), created: new Date().toISOString(), model: entry[0], verified: true, demo: true,
    issue, workflow: classify(issue), status: isHazard ? "Handover ready" : "Open", revision: 0, attempts: {}, pending: null,
    latest_event: isHazard ? { kind: "safety", text: "Stop using the appliance and seek qualified help. No further troubleshooting check was selected." } : { kind: "intro", text: "Fictional case saved. Ask for one source-backed check." },
    ...(isHazard ? { safety_report: issue } : {}),
  };
  return view(await saveNew(caseRecord, requestId));
}

export async function askFixProof(input: { request_id: string; case_id: string; revision: number; user_message: string }) {
  const requestId = clean(input.request_id, 100);
  const prior = await cached(requestId);
  if (prior) return view(prior);
  const caseRecord = await readCase(input.case_id);
  if (caseRecord.revision !== input.revision) throw new Error("This case changed. Read it again before continuing.");
  if (caseRecord.status !== "Open") throw new Error("This case is ready for handover; no further check can be selected.");
  const message = clean(input.user_message, 300);
  if (hazard(message)) {
    caseRecord.status = "Handover ready"; caseRecord.pending = null; caseRecord.safety_report = message;
    caseRecord.latest_event = { kind: "safety", text: "Stop using the appliance and seek qualified help. No further troubleshooting check was selected." };
    return view(await saveUpdated(caseRecord, requestId, input.revision));
  }
  caseRecord.workflow ??= classify(`${caseRecord.issue} ${message}`);
  if (!caseRecord.workflow) {
    caseRecord.latest_event = { kind: "clarification", text: "Is the issue wet tableware, food remnants, detergent residue, removable streaks, knocking or rattling during the wash, rust spots on cutlery, or irreversible glass clouding that does not wipe off?" };
    return view(await saveUpdated(caseRecord, requestId, input.revision));
  }
  const steps = stepsFor(caseRecord.model);
  if (caseRecord.pending && steps[caseRecord.pending]) return view(caseRecord);
  const next = Object.entries(steps).find(([id, step]) => step.workflow === caseRecord.workflow && !caseRecord.attempts[id]);
  if (!next) {
    caseRecord.status = "Handover ready";
    caseRecord.latest_event = { kind: "complete", text: "All bounded checks for this fictional path have an explicit outcome. Prepare the handover." };
  } else {
    caseRecord.pending = next[0];
    caseRecord.latest_event = { kind: "check", text: `${next[1].title}. ${next[1].text}`, citations: citationsFor(caseRecord.model, next[1].pages) };
  }
  return view(await saveUpdated(caseRecord, requestId, input.revision));
}

export async function recordOutcome(input: { request_id: string; case_id: string; revision: number; step_id: string; outcome: string; observation?: string }) {
  const requestId = clean(input.request_id, 100);
  const prior = await cached(requestId);
  if (prior) return view(prior);
  const caseRecord = await readCase(input.case_id);
  if (caseRecord.revision !== input.revision) throw new Error("This case changed. Read it again before continuing.");
  if (caseRecord.pending !== input.step_id) throw new Error("Only the currently pending check can receive an outcome.");
  if (!outcomes.includes(input.outcome as typeof outcomes[number])) throw new Error("Unsupported outcome.");
  caseRecord.attempts[input.step_id] = { outcome: input.outcome, observation: clean(input.observation ?? "", 300), recorded_at: new Date().toISOString() };
  caseRecord.pending = null;
  caseRecord.latest_event = { kind: "outcome", text: `${input.step_id}: ${input.outcome}` };
  return view(await saveUpdated(caseRecord, requestId, input.revision));
}

export function handover(caseRecord: FixProofCase) {
  const entry = catalog(caseRecord.model)!;
  const steps = stepsFor(caseRecord.model);
  const checks = Object.entries(caseRecord.attempts).map(([stepId, attempt]) => ({
    step_id: stepId, title: steps[stepId].title,
    evidence_status: ["Issue unchanged", "Still wet", "Improved, not resolved"].includes(attempt.outcome) ? "user_reports_performed" : "deferred_or_skipped",
    outcome: attempt.outcome, observation: attempt.observation, recorded_at: attempt.recorded_at, citations: citationsFor(caseRecord.model, steps[stepId].pages),
  }));
  const lines = ["# FixProof repair handover", "", "Public MCP evaluation · fictional data only · no diagnosis.", "", `Case: ${caseRecord.id}`, `Status: ${caseRecord.status}`, `Model: ${caseRecord.model}`, "", "## Reported issue", caseRecord.issue, "", "## Recorded checks", ...(checks.length ? checks.flatMap((check) => [`- ${check.title}: ${check.outcome}${check.observation ? ` — ${check.observation}` : ""}`, ...check.citations.map((citation) => `  Source: ${citation.url}`)]) : ["None recorded."]), "", "## Reference provenance", entry[1].source.title, entry[1].source.document, entry[1].source.url, entry[1].source.service_url, ...(caseRecord.safety_report ? ["", "## Safety report", caseRecord.safety_report] : []), "", "## Limits", "No physical inspection was performed. No fault or repair requirement was diagnosed. Deferred or skipped checks do not establish performed work."];
  return {
    case_id: caseRecord.id, revision: caseRecord.revision, status: caseRecord.status, markdown: lines.join("\n"),
    evidence: {
      schema_version: "fixproof-handover-1", case_id: caseRecord.id, case_status: caseRecord.status, reported_issue: caseRecord.issue,
      model: { reported: caseRecord.model, user_confirmed: caseRecord.verified, fictional_demo: caseRecord.demo, catalog_match: true }, reference: { ...entry[1].source }, checks,
      suggested_awaiting_outcome: caseRecord.pending ? { step_id: caseRecord.pending, title: steps[caseRecord.pending].title, citations: citationsFor(caseRecord.model, steps[caseRecord.pending].pages) } : null,
      safety_report: caseRecord.safety_report ?? null,
      limits: ["No physical inspection was performed.", "No fault or repair requirement was diagnosed.", "Deferred or skipped checks do not establish performed work."],
    },
  };
}

export const caseView = view;
