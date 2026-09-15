import { integer, sqliteTable, text } from "drizzle-orm/sqlite-core";

export const cases = sqliteTable("cases", {
  id: text("id").primaryKey(),
  revision: integer("revision").notNull(),
  body: text("body").notNull(),
  createdAt: text("created_at").notNull(),
});

export const requests = sqliteTable("requests", {
  id: text("id").primaryKey(),
  caseId: text("case_id").notNull(),
  body: text("body").notNull(),
  createdAt: text("created_at").notNull(),
});
