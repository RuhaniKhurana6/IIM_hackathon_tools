import { Router } from 'express';
import { computeGauge } from '../services/localGauge.js';
const r = Router();

r.get('/gauge', async (req, res) => {
  // Placeholder: use last events + user limits
  const transactions = [];
  const limits = { monthly: 50000 };
  const gauge = computeGauge(transactions, limits);
  res.json(gauge);
});

export default r;