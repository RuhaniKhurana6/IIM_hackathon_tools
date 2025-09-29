const inMemoryQueue = [];

export function publishEvent(type, payload) {
  inMemoryQueue.push({ type, payload, ts: Date.now() });
}

export function drainQueue() {
  const items = [...inMemoryQueue];
  inMemoryQueue.length = 0;
  return items;
}

export function getRecentTransactions(limit = 50) {
  // naive mapping: turn queued events into transactions for demo
  return inMemoryQueue.slice(-limit).map(e => ({
    source: e.type,
    merchant: e.payload?.merchant ?? null,
    amount: Number(e.payload?.amount ?? 0),
    method: e.payload?.method ?? null,
    ts: e.ts,
  }));
}