"""
Complete network simulation
Combines normal users and attackers
"""

import pandas as pd
from normal_user import generate_normal_users
from attacker import generate_attackers

def generate_complete_dataset(
    num_normal_users=20,
    num_attackers=3,
    events_per_user=200
):
    """Generate complete network dataset"""
    
    print("🔄 Generating normal user activity...")
    normal_df = generate_normal_users(
        num_users=num_normal_users,
        events_per_user=events_per_user
    )
    
    print("🔄 Generating attack sequences...")
    attack_df = generate_attackers(num_attackers=num_attackers)
    
    # Combine datasets
    complete_df = pd.concat([normal_df, attack_df], ignore_index=True)
    
    # Sort by timestamp
    complete_df = complete_df.sort_values('timestamp').reset_index(drop=True)
    
    # Add event_id
    complete_df.insert(0, 'event_id', range(1, len(complete_df) + 1))
    
    print(f"\n✅ Dataset generated successfully!")
    print(f"   Total events: {len(complete_df)}")
    print(f"   Normal events: {len(complete_df[complete_df['risk_label']==0])}")
    print(f"   Malicious events: {len(complete_df[complete_df['risk_label']==1])}")
    print(f"   Time range: {complete_df['timestamp'].min()} to {complete_df['timestamp'].max()}")
    
    return complete_df


if __name__ == "__main__":
    df = generate_complete_dataset(
        num_normal_users=20,
        num_attackers=5,
        events_per_user=200
    )
    
    output_path = '../sample_logs.csv'
    df.to_csv(output_path, index=False)
    print(f"\n💾 Dataset saved to: {output_path}")
    
    print("\n📊 Sample data:")
    print(df.head(10))
    
    print("\n📈 Statistics:")
    print(df.groupby(['risk_label', 'action']).size().head(20))
