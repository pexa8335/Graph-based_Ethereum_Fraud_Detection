

import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI, Content, Part } from "@google/generative-ai";

const apiKey = process.env.GEMINI_API_KEY;

if (!apiKey) {
    throw new Error("GEMINI_API_KEY is not configured.");
}

const genAI = new GoogleGenerativeAI(apiKey);

// QUAY LẠI MODEL ĐÃ HOẠT ĐỘNG
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" }); 

// Hàm tiện ích để đợi
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function POST(req: NextRequest) {
    try {
        const { message, history } = await req.json();
        if (!message) {
            return NextResponse.json({ error: "Message is required" }, { status: 400 });
        }

        const SYSTEM_PROMPT = `Bạn là Nova Assistant, một trợ lý ảo chuyên gia về tài chính... (giữ nguyên prompt của bạn)`;

        const chatHistory: Content[] = [
            { role: 'user', parts: [{ text: SYSTEM_PROMPT }] },
            { role: 'model', parts: [{ text: "Chào bạn, tôi là Nova Assistant..." }] },
            ...history.map((msg: { role: string, parts: Part[] }) => ({
                role: msg.role,
                parts: msg.parts,
            }))
        ];

        const fullPrompt = [
            ...chatHistory,
            { role: 'user', parts: [{ text: message }] }
        ];

        // === CƠ CHẾ THỬ LẠI VỚI EXPONENTIAL BACKOFF ===
        let result;
        const maxRetries = 5;
        let attempt = 0;
        let backoffDelay = 1000; // Bắt đầu đợi 1 giây

        while (attempt < maxRetries) {
            try {
                result = await model.generateContent({ contents: fullPrompt });
                // Nếu thành công, thoát khỏi vòng lặp
                break; 
            } catch (error: any) {
                // Chỉ thử lại nếu lỗi là do quá tải (503) hoặc lỗi mạng
                // error.cause?.status dùng cho lỗi từ fetch, error.status cho lỗi từ API
                const status = error.status || error.cause?.status;

                if (status === 503 || status === 500 || status === 504) {
                    attempt++;
                    console.warn(`Attempt ${attempt}: Model is overloaded (status ${status}). Retrying in ${backoffDelay}ms...`);
                    if (attempt >= maxRetries) {
                        console.error("Max retries reached. Failing request.");
                        throw error; // Ném lỗi ra ngoài sau khi đã thử hết số lần
                    }
                    await delay(backoffDelay);
                    backoffDelay *= 2; // Tăng thời gian chờ cho lần thử tiếp theo
                } else {
                    // Nếu là lỗi khác (ví dụ 400, 404), không thử lại mà báo lỗi ngay
                    throw error;
                }
            }
        }

        if (!result) {
            throw new Error("AI response could not be generated after multiple retries.");
        }

        const response = result.response;
        const botReply = response.text();

        return NextResponse.json({ reply: botReply });

    } catch (error) {
        console.error("Critical Error in chat API:", error);
        const errorMessage = error instanceof Error ? error.message : "Internal Server Error";
        return NextResponse.json({ error: errorMessage }, { status: 500 });
    }
}