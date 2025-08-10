import { NextResponse } from "next/server";

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID;

export async function POST(request: Request) {
  try {
    const { message } = await request.json();

    if (!message) {
      return NextResponse.json({ error: "Message is required" }, { status: 400 });
    }
    if (TELEGRAM_BOT_TOKEN && TELEGRAM_CHAT_ID) {
      const telegramApiUrl = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 50000); 

      try {
        const telegramResponse = await fetch(telegramApiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            chat_id: TELEGRAM_CHAT_ID,
            text: `🚨 Alert from Novaledger 🚨\n\n${message}`,
            parse_mode: "Markdown",
          }),
          signal: controller.signal, 
        });

        clearTimeout(timeoutId);

        if (!telegramResponse.ok) {
          const errorData = await telegramResponse.json();
          console.error("[Telegram Alert] Failed to send message:", errorData);
          throw new Error(errorData.description || `Telegram API error: ${telegramResponse.status}`);
        } else {
          console.log("[Telegram Alert] Message sent successfully.");
        }
      } catch (error: any) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
          console.error("[Telegram Alert] Request timed out:", error.message);
          throw new Error("Telegram API request timed out.");
        }
        throw error;
      }
    } else {
      console.warn("[Alerting] Telegram credentials not configured. Alert not sent.");
    }

    return NextResponse.json({ success: true, message: "Alert processing initiated" });

  } catch (error) {
    console.error("[Alert API] General error:", error);
    const errorMessage =
      error instanceof Error
        ? error.message
        : "An unknown error occurred while sending the alert";
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}