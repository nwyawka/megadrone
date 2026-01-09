#!/usr/bin/env python3
"""
OpenVSP Python API Setup Script
Adds OpenVSP Python module to system path

Author: MegaDrone Project
Date: January 8, 2026
"""

import sys
import os

# Path to OpenVSP Python API
OPENVSP_PATH = "/Users/matthewoneil/OpenVSP-3.46.0-MacOS"
OPENVSP_PYTHON_API = os.path.join(OPENVSP_PATH, "python")

def setup_openvsp_path():
    """Add OpenVSP Python API to system path"""
    
    # Check if OpenVSP is installed
    if not os.path.exists(OPENVSP_PATH):
        raise FileNotFoundError(
            f"OpenVSP not found at {OPENVSP_PATH}\n"
            "Please verify installation location"
        )
    
    # Check for Python API
    if not os.path.exists(OPENVSP_PYTHON_API):
        print(f"Warning: Python API not found at {OPENVSP_PYTHON_API}")
        print("Looking for alternative locations...")
        
        # Try alternate locations
        alt_paths = [
            os.path.join(OPENVSP_PATH, "vspscript"),
            os.path.join(OPENVSP_PATH, "lib"),
            os.path.join(OPENVSP_PATH, "Resources"),
        ]
        
        for path in alt_paths:
            if os.path.exists(path):
                print(f"Found Python API at: {path}")
                sys.path.insert(0, path)
                return path
        
        # If still not found, add main directory
        print(f"Using main OpenVSP directory: {OPENVSP_PATH}")
        sys.path.insert(0, OPENVSP_PATH)
        return OPENVSP_PATH
    
    # Add to Python path
    sys.path.insert(0, OPENVSP_PYTHON_API)
    print(f"Added OpenVSP Python API to path: {OPENVSP_PYTHON_API}")
    return OPENVSP_PYTHON_API

def test_openvsp_import():
    """Test if OpenVSP module can be imported"""
    try:
        import openvsp as vsp
        print("✓ OpenVSP module imported successfully")
        print(f"  OpenVSP Version: {vsp.GetVSPVersion()}")
        return True
    except ImportError as e:
        print("✗ Failed to import OpenVSP module")
        print(f"  Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify OpenVSP is installed at:")
        print(f"   {OPENVSP_PATH}")
        print("2. Check if Python API exists in OpenVSP directory")
        print("3. Try running OpenVSP GUI to verify installation")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("OpenVSP Python API Setup")
    print("=" * 60)
    
    # Setup path
    api_path = setup_openvsp_path()
    
    print("\nPython Path:")
    for i, path in enumerate(sys.path[:5]):
        print(f"  [{i}] {path}")
    
    print("\n" + "=" * 60)
    print("Testing OpenVSP Import")
    print("=" * 60 + "\n")
    
    # Test import
    success = test_openvsp_import()
    
    if success:
        print("\n✓ Setup complete! OpenVSP API is ready to use.")
    else:
        print("\n✗ Setup incomplete. Please check installation.")
        sys.exit(1)
