export function computeGauge(transactions, limits) {
  const monthly = limits?.monthly || 1;
  const total = transactions.reduce((s, t) => s + (Number(t?.amount) || 0), 0);
  const pct = Math.min(100, Math.round((total / monthly) * 100));
  const status = pct < 70 ? 'green' : pct < 90 ? 'orange' : 'red';
  return { percent: pct, status, monthly_limit: monthly, spend: total };
}