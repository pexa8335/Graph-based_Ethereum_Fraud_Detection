export const sendAlert = async (message: string) => {
  try {
    const response = await fetch("/api/send-alert", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Failed to send alert:", errorData.error);
    } else {
      console.log("Alert sent successfully!");
    }
  } catch (error) {
    console.error("Error sending alert:", error);
  }
};