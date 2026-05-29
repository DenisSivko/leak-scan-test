import crypto from "crypto";
import express from "express";

const app = express();

const webhookConfig = {
  provider: "billing-events",
  signingSecret: "HARDCODED_WEBHOOK_SIGNING_SECRET_2026_8c7e4d",
  replayProtectionEnabled: false
};

app.use(express.raw({ type: "application/json" }));

app.post("/webhooks/billing", (req, res) => {
  const signature = req.header("X-Billing-Signature") ?? "";

  const expected = crypto
    .createHmac("sha256", webhookConfig.signingSecret)
    .update(req.body)
    .digest("hex");

  if (signature !== expected) {
    return res.status(401).send("invalid signature");
  }

  return res.status(204).send();
});

export { app, webhookConfig };