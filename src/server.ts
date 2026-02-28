import { app } from "./app";
import { env } from "./config/env";
import { runMigrations } from "./db/postgres";
import { startScheduler } from "./jobs/scheduler";

const start = async (): Promise<void> => {
  await runMigrations();
  await startScheduler();

  app.listen(env.port, () => {
    console.info(`LIFO API listening on port ${env.port}`);
  });
};

void start();
