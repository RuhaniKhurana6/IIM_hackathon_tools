export function computeGauge(transactions = [], limits = { monthly: 1 }) {
  const total = transactions.reduce((sum, t) => sum + (Number(t.amount) || 0), 0);
  const monthly = limits.monthly || 1;
  const percent = Math.min(100, Math.round((100 * total) / monthly));
  const status = percent < 70 ? 'green' : percent < 90 ? 'orange' : 'red';
  return { percent, status, monthly_limit: monthly, spend: total };
}