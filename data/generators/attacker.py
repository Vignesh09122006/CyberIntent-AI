"""
Normal user behavior generator
Simulates legitimate network activity
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class NormalUserGenerator:
    def __init__(self, user_id, base_ip="192.168.1"):
        self.user_id = user_id
        self.base_ip = base_ip
        self.normal_actions = [
            'login', 'file_access', 'email_send', 
            'web_browse', 'file_download', 'logout'
        ]
        
    def generate(self, num_events=200, days=7):
        """Generate normal user activity"""
        events = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            # Normal working hours: 8 AM - 6 PM
            work_start = start_date + timedelta(days=day, hours=8)
            work_end = start_date + timedelta(days=day, hours=18)
            
            # Generate 20-30 events per day
            daily_events = random.randint(20, 30)
            
            for _ in range(daily_events):
                # Random time during work hours
                event_time = work_start + timedelta(
                    seconds=random.randint(0, int((work_end - work_start).total_seconds()))
                )
                
                # Consistent IP (with occasional VPN switch)
                ip_suffix = random.randint(10, 50) if random.random() > 0.95 else 25
                ip_address = f"{self.base_ip}.{ip_suffix}"
                
                # Normal action
                action = random.choice(self.normal_actions)
                
                # High success rate
                status = 'success' if random.random() > 0.05 else 'failed'
                
                events.append({
                    'timestamp': event_time,
                    'user_id': self.user_id,
                    'ip_address': ip_address,
                    'action': action,
                    'status': status,
                    'bytes_transferred': random.randint(1024, 1024*1024),
                    'duration_ms': random.randint(100, 5000),
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'risk_label': 0  # Normal
                })
        
        return pd.DataFrame(events)


def generate_normal_users(num_users=10, events_per_user=200):
    """Generate multiple normal users"""
    all_events = []
    
    for i in range(num_users):
        user_id = f"user_{i+1:03d}"
        generator = NormalUserGenerator(user_id)
        user_events = generator.generate(num_events=events_per_user)
        all_events.append(user_events)
    
    return pd.concat(all_events, ignore_index=True)


if __name__ == "__main__":
    # Test the generator
    df = generate_normal_users(num_users=5, events_per_user=100)
    print(f"Generated {len(df)} normal events")
    print(df.head())
    df.to_csv('data/normal_users.csv', index=False)