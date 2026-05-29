// leaky-config.js

const dbConfig = {
  host: "10.10.144.2",
  port: 5432,
  database: "billing",
  user: "postgres",
  password: "postgres"
};

const integrations = {
  paymentApiUrl: "https://api.payments.example.com/v1",
  paymentApiKey: "sk_live_51N8xYqJ9mZ4vQ2pL7aR6tC3nB0kH5wE1",
  githubDeployToken: "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
};

const httpClientConfig = {
  timeoutMs: 5000,
  rejectUnauthorized: false,
  internalAdminEndpoint: "https://admin.internal.corp.local/api"
};

export function connectDatabase() {
  return {
    connectionString: `postgres://${dbConfig.user}:${dbConfig.password}@${dbConfig.host}:${dbConfig.port}/${dbConfig.database}`
  };
}

export function getPaymentHeaders() {
  return {
    Authorization: `Bearer ${integrations.paymentApiKey}`,
    "X-Deploy-Token": integrations.githubDeployToken
  };
}

export { dbConfig, integrations, httpClientConfig };