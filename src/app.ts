import cookieParser from "cookie-parser";
import express from "express";
import * as Sentry from "@sentry/node";
import { env } from "./config/env";
import { authRouter } from "./routes/auth";
import { usersRouter } from "./routes/users";

export const app = express();

if (env.sentryDsn) {
  Sentry.init({
    dsn: env.sentryDsn,
    tracesSampleRate: 0.1
  });
}

app.use(express.json());
app.use(cookieParser());

app.get("/healthz", (_req: express.Request, res: express.Response) => {
  res.json({ status: "ok" });
});

app.use("/api/v1/auth", authRouter);
app.use("/api/v1/users", usersRouter);

app.use((error: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error(error);
  res.status(500).json({ message: "Internal Server Error" });
});
