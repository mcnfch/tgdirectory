export interface Schedule {
  [key: string]: string;
}

export const isRestaurantOpen = (schedule: string[]): boolean => {
  try {
    // Get current time in ET
    const now = new Date();
    const et = new Date(now.toLocaleString("en-US", { timeZone: "America/New_York" }));
    const currentDay = et.toLocaleString('en-US', { weekday: 'long' });
    const currentHour = et.getHours();
    const currentMinute = et.getMinutes();
    
    // Find today's schedule
    const todaySchedule = schedule.find((s: string) => s.startsWith(currentDay));
    if (!todaySchedule) return false;
    
    // Parse the hours (e.g., "Monday: 5:00 – 10:00 PM")
    const timeRange = todaySchedule.split(': ')[1];
    if (!timeRange) return false;

    const [openTime, closeTime] = timeRange.split('–').map((t: string) => t.trim());
    if (!openTime || !closeTime) return false;

    // Convert current time to minutes since midnight
    const currentMinutes = currentHour * 60 + currentMinute;

    // Convert opening time to minutes since midnight
    const openMatch = openTime.match(/(\d+):(\d+)\s*(AM|PM)/i);
    if (!openMatch) return false;
    let openHour = parseInt(openMatch[1]);
    const openMinute = parseInt(openMatch[2]);
    if (openMatch[3].toUpperCase() === 'PM' && openHour !== 12) openHour += 12;
    if (openMatch[3].toUpperCase() === 'AM' && openHour === 12) openHour = 0;
    const openMinutes = openHour * 60 + openMinute;

    // Convert closing time to minutes since midnight
    const closeMatch = closeTime.match(/(\d+):(\d+)\s*(AM|PM)/i);
    if (!closeMatch) return false;
    let closeHour = parseInt(closeMatch[1]);
    const closeMinute = parseInt(closeMatch[2]);
    if (closeMatch[3].toUpperCase() === 'PM' && closeHour !== 12) closeHour += 12;
    if (closeMatch[3].toUpperCase() === 'AM' && closeHour === 12) closeHour = 0;
    const closeMinutes = closeHour * 60 + closeMinute;

    return currentMinutes >= openMinutes && currentMinutes <= closeMinutes;
  } catch (error) {
    console.error('Error checking restaurant hours:', error);
    return false;
  }
};
