CREATE TABLE `cases` (
	`id` text PRIMARY KEY NOT NULL,
	`revision` integer NOT NULL,
	`body` text NOT NULL,
	`created_at` text NOT NULL
);
--> statement-breakpoint
CREATE TABLE `requests` (
	`id` text PRIMARY KEY NOT NULL,
	`case_id` text NOT NULL,
	`body` text NOT NULL,
	`created_at` text NOT NULL
);
