#!/usr/bin/env python3
"""
Utility script to remove debug breakpoints from route_optimization_api.py
Run this script when you're done debugging to clean up the code
"""
import re
import os

def remove_debug_breakpoints():
    """Remove debug breakpoints from route_optimization_api.py"""
    
    file_path = "app/services/route_optimization_api.py"
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove debug breakpoints
    original_content = content
    
    # Remove pdb import and set_trace lines
    content = re.sub(r'# BREAKPOINT:.*\n\s*import pdb; pdb\.set_trace\(\)\s*# Debug breakpoint - remove in production\n', '', content)
    
    # Remove standalone pdb.set_trace() lines
    content = re.sub(r'\s*import pdb; pdb\.set_trace\(\)\s*# Debug breakpoint - remove in production\n', '', content)
    
    # Check if any changes were made
    if content == original_content:
        print("✅ No debug breakpoints found to remove")
        return
    
    # Write the cleaned content back
    with open(file_path, 'w') as f:
        f.write(content)
    
    print("✅ Debug breakpoints removed successfully!")
    print(f"📝 File cleaned: {file_path}")

if __name__ == "__main__":
    remove_debug_breakpoints() 