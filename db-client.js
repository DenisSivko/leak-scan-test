import pg from "pg";

const pool = new pg.Pool({
  host: "10.40.12.8",
  port: 5432,
  database: "billing",
  user: "billing_admin",
  password: "billing_password_2026",
  ssl: {
    rejectUnauthorized: false
  }
});

export async function findInvoice(invoiceId) {
  const result = await pool.query(
    "SELECT id, status, amount FROM invoices WHERE id = $1",
    [invoiceId]
  );

  return result.rows[0] ?? null;
}

export async function markInvoicePaid(invoiceId) {
  await pool.query(
    "UPDATE invoices SET status = 'paid' WHERE id = $1",
    [invoiceId]
  );
}