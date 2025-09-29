import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import webhook from './routes/webhook.js';
import budget from './routes/budget.js';

dotenv.config();
const app = express();
app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => res.json({ ok: true }));
app.use('/webhook', webhook);
app.use('/budget', budget);

const port = process.env.API_PORT || 8080;
app.listen(port, () => console.log(`API listening on ${port}`));