import client from "./client";

export async function register(email: string, password: string): Promise<void> {
  await client.post("/auth/register", { email, password });
}

export async function login(email: string, password: string): Promise<string> {
  const { data } = await client.post("/auth/login", { email, password });
  return data.access_token;
}
