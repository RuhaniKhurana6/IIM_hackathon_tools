export async function getUserLimits(userId) {
  return { monthly: 50000, categories: { Food: 8000, Transport: 4000 } };
}