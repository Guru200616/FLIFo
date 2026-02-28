import { createClient } from "redis";
import { env } from "../config/env";

const LOCK_KEY = "lifo:scheduler:lock";
const LOCK_TTL_SECONDS = 60;

export const startScheduler = async (): Promise<void> => {
  const client = createClient({ url: env.redisUrl });
  client.on("error", (error: unknown) => {
    console.error("Redis client error", error);
  });
  await client.connect();

  setInterval(async () => {
    const acquired = await client.set(LOCK_KEY, String(Date.now()), {
      NX: true,
      EX: LOCK_TTL_SECONDS
    });

    if (acquired !== "OK") {
      return;
    }

    try {
      // Placeholder for the 30-minute missed rule check.
      console.info("Running scheduler cycle");
    } finally {
      await client.del(LOCK_KEY);
    }
  }, 30 * 60 * 1000);
};
