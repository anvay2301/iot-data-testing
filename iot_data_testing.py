"""
IoT Data Quality Testing & Validation System
Author: Anvay Pandey
Description: Automated testing system to validate IoT sensor data quality
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Sample IoT Sensor Data
sensor_data = {
    'sensor_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008'],
    'temperature': [25.5, 28.3, None, 150.0, 22.1, -50.0, 30.2, 26.8],
    'humidity': [60, 65, 70, 55, None, 80, 62, 68],
    'timestamp': ['2025-01-15 10:00', '2025-01-15 10:05', '2025-01-15 10:10', 
                  '2025-01-15 10:15', '2025-01-15 10:20', '2025-01-15 10:25',
                  '2025-01-15 10:30', '2025-01-15 10:35']
}

def load_data():
    """Load sensor data into pandas DataFrame"""
    df = pd.DataFrame(sensor_data)
    print("=" * 70)
    print("IOT DATA QUALITY TESTING SYSTEM")
    print("=" * 70)
    print("\n📊 Sensor Data Loaded:")
    print(df)
    print("\n" + "=" * 70)
    return df

def test_missing_values(df):
    """Test Case 1: Check for missing values in sensor data"""
    print("\n🔍 TEST 1: Missing Value Detection")
    print("-" * 70)
    missing = df.isnull().sum()
    print(missing)
    
    if missing.sum() > 0:
        print("\n❌ TEST FAILED: Missing values detected")
        missing_sensors = df[df.isnull().any(axis=1)]['sensor_id'].tolist()
        print(f"   Affected Sensors: {missing_sensors}")
        return False
    else:
        print("\n✅ TEST PASSED: No missing values")
        return True

def test_temperature_range(df):
    """Test Case 2: Validate temperature readings (0-50°C)"""
    print("\n🔍 TEST 2: Temperature Range Validation (0-50°C)")
    print("-" * 70)
    invalid = df[(df['temperature'] < 0) | (df['temperature'] > 50)]
    
    if len(invalid) > 0:
        print("❌ TEST FAILED: Invalid temperature readings")
        for _, row in invalid.iterrows():
            print(f"   Sensor {row['sensor_id']}: {row['temperature']}°C")
        return False
    else:
        print("✅ TEST PASSED: All temperatures valid")
        return True

def test_humidity_range(df):
    """Test Case 3: Validate humidity readings (0-100%)"""
    print("\n🔍 TEST 3: Humidity Range Validation (0-100%)")
    print("-" * 70)
    invalid = df[(df['humidity'] < 0) | (df['humidity'] > 100)]
    
    if len(invalid) > 0:
        print("❌ TEST FAILED: Invalid humidity readings")
        for _, row in invalid.iterrows():
            print(f"   Sensor {row['sensor_id']}: {row['humidity']}%")
        return False
    else:
        print("✅ TEST PASSED: All humidity values valid")
        return True

def test_duplicates(df):
    """Test Case 4: Check for duplicate sensor IDs"""
    print("\n🔍 TEST 4: Duplicate Sensor ID Detection")
    print("-" * 70)
    duplicates = df[df.duplicated(subset=['sensor_id'], keep=False)]
    
    if len(duplicates) > 0:
        print("❌ TEST FAILED: Duplicate sensor IDs found")
        print(duplicates)
        return False
    else:
        print("✅ TEST PASSED: No duplicates")
        return True

def test_outliers(df):
    """Test Case 5: Detect outliers using statistical analysis"""
    print("\n🔍 TEST 5: Outlier Detection (Temperature)")
    print("-" * 70)
    temp_clean = df['temperature'].dropna()
    mean = np.mean(temp_clean)
    std = np.std(temp_clean)
    
    print(f"Mean Temperature: {mean:.2f}°C")
    print(f"Standard Deviation: {std:.2f}°C")
    
    outliers = df[np.abs(df['temperature'] - mean) > (2 * std)]
    
    if len(outliers) > 0:
        print("\n⚠️  WARNING: Outliers detected")
        for _, row in outliers.iterrows():
            print(f"   Sensor {row['sensor_id']}: {row['temperature']}°C")
        return False
    else:
        print("\n✅ TEST PASSED: No outliers")
        return True

def generate_report(results):
    """Generate final test report"""
    print("\n" + "=" * 70)
    print("📋 FINAL TEST REPORT")
    print("=" * 70)
    
    total_tests = len(results)
    passed = sum(results)
    failed = total_tests - passed
    success_rate = (passed / total_tests) * 100
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    print("\n📊 Data Quality Score: {:.1f}%".format(success_rate))
    
    if success_rate >= 80:
        print("✅ RESULT: Data quality is GOOD")
    elif success_rate >= 60:
        print("⚠️  RESULT: Data quality needs IMPROVEMENT")
    else:
        print("❌ RESULT: Data quality is POOR")
    
    print("=" * 70)

def main():
    """Main execution function"""
    # Load data
    df = load_data()
    
    # Run all tests
    results = []
    results.append(test_missing_values(df))
    results.append(test_temperature_range(df))
    results.append(test_humidity_range(df))
    results.append(test_duplicates(df))
    results.append(test_outliers(df))
    
    # Generate report
    generate_report(results)

if __name__ == "__main__":
    main()
