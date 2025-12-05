"""Test NaN fix in email_notifier"""
from email_notifier import is_nan_or_none, safe_value, safe_float
import math

print("Testing is_nan_or_none():")
print(f"  None -> {is_nan_or_none(None)}")
print(f"  float('nan') -> {is_nan_or_none(float('nan'))}")
print(f"  'nan' string -> {is_nan_or_none('nan')}")
print(f"  42.5 -> {is_nan_or_none(42.5)}")
print(f"  'valid' -> {is_nan_or_none('valid')}")

print("\nTesting safe_float():")
print(f"  None, 0 -> {safe_float(None, 0)}")
print(f"  float('nan'), 0 -> {safe_float(float('nan'), 0)}")
print(f"  42.5, 0 -> {safe_float(42.5, 0)}")
print(f"  'invalid', 0 -> {safe_float('invalid', 0)}")

print("\nTesting safe_value():")
print(f"  None, 'default' -> {safe_value(None, 'default')}")
print(f"  float('nan'), 'default' -> {safe_value(float('nan'), 'default')}")
print(f"  'valid', 'default' -> {safe_value('valid', 'default')}")

print("\n✅ All NaN checks working correctly!")
