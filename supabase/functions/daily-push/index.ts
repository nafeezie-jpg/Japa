// Now You Have Landed: sends the daily "Today's Landing is ready" nudge.
// Runs every hour from a database schedule and only notifies players whose local time matches their saved hour (10am).
import webpush from "npm:web-push@3.6.7";
import { createClient } from "npm:@supabase/supabase-js@2";

const MESSAGES = [
  "A new country and new surprises are waiting. Can you beat today's players?",
  "Home is calling again. Today's Landing is ready.",
  "Your streak is waiting. Five minutes, one new landing.",
  "New day, new landing. Will you send the money or switch off your phone?",
];

Deno.serve(async (req) => {
  if (req.headers.get("x-cron-secret") !== Deno.env.get("CRON_SECRET")) {
    return new Response("Not allowed", { status: 401 });
  }
  webpush.setVapidDetails("mailto:nafeezie@gmail.com", Deno.env.get("VAPID_PUBLIC")!, Deno.env.get("VAPID_PRIVATE")!);
  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

  const now = new Date();
  const utcMinutes = now.getUTCHours() * 60 + now.getUTCMinutes();
  const body = MESSAGES[Math.floor(now.getTime() / 864e5) % MESSAGES.length];
  const { data: subs, error } = await db.from("push_subs").select("*");
  if (error) return new Response(error.message, { status: 500 });

  let sent = 0;
  const gone: string[] = [];
  for (const s of subs ?? []) {
    const localHour = Math.floor((((utcMinutes + s.tz) % 1440) + 1440) % 1440 / 60);
    if (localHour !== s.hour) continue;
    try {
      await webpush.sendNotification(
        { endpoint: s.endpoint, keys: { p256dh: s.p256dh, auth: s.auth } },
        JSON.stringify({ title: "Today's Landing is ready ✈️", body, url: "/?source=push" }),
      );
      sent++;
    } catch (e) {
      const code = (e as { statusCode?: number }).statusCode;
      if (code === 404 || code === 410) gone.push(s.endpoint);   // the player turned notifications off
    }
  }
  if (gone.length) await db.from("push_subs").delete().in("endpoint", gone);
  return new Response(JSON.stringify({ sent, removed: gone.length }), { headers: { "Content-Type": "application/json" } });
});
