#!/usr/bin/env python3
"""
Test runner for RealPlanner backend tests
"""
import sys
import os
import subprocess

def run_tests():
    """Run all tests in the tests directory"""
    print("🧪 Running RealPlanner backend tests...")
    print("=" * 50)
    
    # Get the current directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(test_dir)
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run the optimization test
    print("Testing route optimization...")
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join(test_dir, "test_optimization.py")
        ], capture_output=True, text=True, cwd=backend_dir)
        
        if result.returncode == 0:
            print("✅ Route optimization test passed!")
            print(result.stdout)
        else:
            print("❌ Route optimization test failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False
    
    print("\n🎉 All tests completed successfully!")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 