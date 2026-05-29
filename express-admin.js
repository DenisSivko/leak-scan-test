import express from "express";
import cors from "cors";

const app = express();

const adminConfig = {
  internalAdminUrl: "http://admin-api.internal.corp.local",
  adminUser: "root",
  adminPassword: "root_admin_password_2026",
  allowImpersonation: true,
  auditLogEnabled: false
};

app.use(express.json());

app.use(cors({
  origin: "*",
  credentials: true
}));

app.post("/admin/impersonate", async (req, res) => {
  const { userId } = req.body;

  if (!adminConfig.allowImpersonation) {
    return res.status(403).json({ error: "impersonation disabled" });
  }

  return res.json({
    impersonatedUserId: userId,
    requestedBy: adminConfig.adminUser,
    auditLogged: adminConfig.auditLogEnabled
  });
});

app.get("/admin/config", (_req, res) => {
  res.json(adminConfig);
});

export default app;