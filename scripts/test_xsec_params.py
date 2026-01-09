#!/usr/bin/env python3
"""
Test script to discover XSec parameter names for Ellipse cross-sections
"""
import openvsp as vsp

# Clear and create a simple fuselage
vsp.ClearVSPModel()
fuse_id = vsp.AddGeom("FUSELAGE")

# Get XSec surface
xsec_surf = vsp.GetXSecSurf(fuse_id, 0)

# Get first cross-section
xsec = vsp.GetXSec(xsec_surf, 0)

# Change to ellipse (if not already)
vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_ELLIPSE)
xsec = vsp.GetXSec(xsec_surf, 0)

# Get all parameters for this XSec
parm_ids = vsp.GetXSecParmIDs(xsec)

print("="*60)
print(f"XSec ID: {xsec}")
print(f"Number of parameters: {len(parm_ids)}")
print("="*60)

# Print all parameter names and current values
for parm_id in parm_ids:
    parm_name = vsp.GetParmName(parm_id)
    parm_val = vsp.GetParmVal(parm_id)
    parm_group = vsp.GetParmGroupName(parm_id)
    print(f"  {parm_name:30s} = {parm_val:8.3f}  (group: {parm_group})")

print("="*60)

# Try to get specific parameters
print("\nAttempting to get ellipse-specific parameters:")
print("="*60)

# Try various names
param_names_to_try = [
    "Ellipse_Width",
    "Ellipse_Height", 
    "Width",
    "Height",
    "Diameter",
    "Circle_Diameter",
    "Circle_Height",
]

for name in param_names_to_try:
    parm_id = vsp.GetXSecParm(xsec, name)
    if vsp.ValidParm(parm_id):
        val = vsp.GetParmVal(parm_id)
        print(f"  ✓ {name:30s} = {val:.3f}  (VALID)")
    else:
        print(f"  ✗ {name:30s} (not found)")

print("="*60)
