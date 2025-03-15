
from datetime import datetime, timedelta
import calendar

class SmartMeetingScheduler:
    def __init__(self):
        self.working_hours = (9, 17)  
        self.meetings = {}  
        self.public_holidays = {"2025-01-01", "2025-12-25"}  
    
    def is_working_day(self, date):
        weekday = date.weekday()
        return weekday < 5 and date.strftime("%Y-%m-%d") not in self.public_holidays
    
    def get_available_slots(self, user, date):
        if not self.is_working_day(date):
            return []
        
        meetings = self.meetings.get(user, {}).get(date.strftime("%Y-%m-%d"), [])
        all_slots = [(hour, hour + 1) for hour in range(self.working_hours[0], self.working_hours[1])]
        
        available_slots = [slot for slot in all_slots if slot not in meetings]
        return available_slots
    
    def schedule_meeting(self, user, date, start_hour, end_hour):
        if not self.is_working_day(date):
            return "Cannot schedule on weekends or holidays."
        
        if start_hour < self.working_hours[0] or end_hour > self.working_hours[1]:
            return "Meeting time outside working hours."
        
        meetings = self.meetings.setdefault(user, {}).setdefault(date.strftime("%Y-%m-%d"), [])
        if any(start_hour < m_end and end_hour > m_start for m_start, m_end in meetings):
            return "Meeting overlaps with an existing one."
        
        meetings.append((start_hour, end_hour))
        meetings.sort()
        
        available_slots = self.get_available_slots(user, date)
        scheduled_meetings = self.view_meetings(user)
        
        return f"Meeting scheduled successfully.\nAvailable slots: {available_slots}\nScheduled meetings: {scheduled_meetings}" 
    
    def view_meetings(self, user):
        return self.meetings.get(user, {})
    
scheduler = SmartMeetingScheduler()
date = datetime(2025, 3, 18)
print(scheduler.schedule_meeting("Alice", date, 10, 11))
