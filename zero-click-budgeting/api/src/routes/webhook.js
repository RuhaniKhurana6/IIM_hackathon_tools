import { Router } from 'express';
import { publishEvent } from '../services/eventPublisher.js';
const r = Router();

r.post('/sms', (req, res) => { publishEvent('sms', req.body); res.status(202).json({ queued: true }); });
r.post('/upi', (req, res) => { publishEvent('upi', req.body); res.status(202).json({ queued: true }); });
r.post('/receipt', (req, res) => { publishEvent('receipt', req.body); res.status(202).json({ queued: true }); });

export default r;