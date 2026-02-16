"""
Script to generate complete dataset
Run this first!
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.generators.network_simulator import generate_complete_dataset

def main():
    print("=" * 60)
    print("🛡️  CyberIntent-AI Dataset Generator")
    print("=" * 60)
    
    # Generate dataset
    df = generate_complete_dataset(
        num_normal_users=25,
        num_attackers=5,
        events_per_user=200
    )
    
    # Save to data folder
    output_path = 'data/sample_logs.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\n✅ Complete! Dataset saved to: {output_path}")
    print("\n🚀 Next step: Run 'python scripts/train_models.py'")

if __name__ == "__main__":
    main()
