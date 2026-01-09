# MegaDrone Phase 1 - Design Summary

## Executive Summary

MegaDrone Phase 1 is a small fixed-wing electric UAV designed for surveillance missions with the following capabilities:
- **100 km round-trip range** (50 km out + 50 km back)
- **15 minute loiter time** at target
- **0.5 kg camera payload**
- **Hand-launch capable** (stall speed < 10 m/s)
- **50 knot cruise speed**

---

## 1. Mission Profile

| Phase | Distance/Time | Speed | Altitude |
|-------|---------------|-------|----------|
| Hand Launch | - | 10 m/s | Ground |
| Climb | 150 m | 15 m/s | 0 → 150m |
| Cruise Out | 50 km | 25.7 m/s (50 kt) | 150m AGL |
| Loiter | 15 min | 15 m/s (29 kt) | 150m AGL |
| Cruise Back | 50 km | 25.7 m/s (50 kt) | 150m AGL |
| Descent/Landing | - | 12 m/s | 150m → 0 |

**Total Flight Time:** ~81 minutes

---

## 2. Aircraft Configuration

### 2.1 Overall Dimensions

| Parameter | Metric | Imperial |
|-----------|--------|----------|
| **Total Weight** | 1.96 kg | 4.33 lb |
| **Wingspan** | 1.70 m | 5.58 ft |
| **Wing Area** | 0.241 m² | 2.59 ft² |
| **Mean Chord** | 0.142 m | 5.57 in |
| **Fuselage Length** | 0.45 m | 17.7 in |
| **Overall Length** | ~0.75 m | ~29.5 in |

### 2.2 Wing Geometry

| Parameter | Value |
|-----------|-------|
| Aspect Ratio | 12.0 |
| Taper Ratio | 0.70 |
| Root Chord | 0.167 m |
| Tip Chord | 0.117 m |
| Dihedral | 3° |
| Incidence | 2° (root), -1° (tip) |
| Sweep | ~0° (straight LE) |
| Airfoil | Optimized (see Section 4) |

### 2.3 Tail Surfaces

| Surface | Span/Height | Area | Volume Coefficient |
|---------|-------------|------|-------------------|
| Horizontal Tail | 0.35 m | 0.031 m² | 0.5 |
| Vertical Tail | 0.21 m | 0.030 m² | 0.04 |

### 2.4 Weight Breakdown

| Component | Mass (kg) | Percentage |
|-----------|-----------|------------|
| Payload (camera) | 0.500 | 25.5% |
| Battery | 0.651 | 33.2% |
| Structure | 0.589 | 30.0% |
| Avionics | 0.150 | 7.6% |
| Motor | 0.053 | 2.7% |
| Propeller | 0.020 | 1.0% |
| **Total** | **1.963** | **100%** |

---

## 3. Aerodynamic Performance

### 3.1 Design Parameters

| Parameter | Value |
|-----------|-------|
| Wing Loading | 80 N/m² (1.67 lb/ft²) |
| CD0 (parasite) | 0.020 |
| Oswald Efficiency | 0.88 |
| CL_max (no flaps) | 1.4 |

### 3.2 Performance Summary

| Condition | Speed | CL | CD | L/D | Power |
|-----------|-------|-----|-----|-----|-------|
| **Cruise** | 25.7 m/s (50 kt) | 0.53 | 0.023 | 19.5 | 66 W |
| **Loiter** | 15.0 m/s (29 kt) | 0.91 | 0.031 | 21.9 | 21 W |
| **Best L/D** | 16.0 m/s (31 kt) | 0.88 | 0.029 | 21.9 | - |
| **Min Power** | 10.0 m/s (19 kt) | 1.26 | 0.043 | - | 13 W |
| **Stall** | 9.7 m/s (19 kt) | 1.40 | - | - | - |

### 3.3 Reynolds Number

| Condition | Re (based on chord) |
|-----------|---------------------|
| Cruise | 243,000 |
| Loiter | 142,000 |

---

## 4. Airfoil Design

### 4.1 Baseline Comparison

Analyzed at Re = 250,000, Mach = 0.075:

| Airfoil | Max L/D | L/D @ CL=0.5 |
|---------|---------|--------------|
| E387 | 90.9 | 58.7 |
| SD7037 | 80.6 | 64.3 |
| Clark-Y | 79.5 | 53.4 |
| NACA 2412 | 72.1 | 55.2 |

### 4.2 Optimized Airfoil

Using NeuralFoil optimization with CST parameterization:

| Parameter | Value |
|-----------|-------|
| Optimization Target | Max L/D at CL ≈ 0.5 |
| Achieved L/D | **106.3** |
| CD at design point | 0.00565 |
| Improvement vs E387 | +81% |

Optimized airfoil coordinates saved to: `designs/optimized_airfoil.dat`

---

## 5. Propulsion System

### 5.1 Power Requirements

| Phase | Power (shaft) | Power (battery) |
|-------|---------------|-----------------|
| Climb | 53 W | 76 W |
| Cruise | 53 W | 76 W |
| Loiter | 15 W | 21 W |
| Payload | 5 W | 5 W |

*Battery power includes 70% system efficiency (motor × ESC × propeller)*

### 5.2 Energy Budget

| Phase | Duration | Energy (Wh) |
|-------|----------|-------------|
| Climb | 1.2 min | 1.5 |
| Cruise | 64.8 min | 82.0 |
| Loiter | 15.0 min | 5.3 |
| Payload | 81.1 min | 6.8 |
| **Total (shaft)** | | **95.6 Wh** |
| **Total (battery)** | | **117 Wh** |

*Includes 20% reserve*

### 5.3 Battery Specification

| Parameter | Value |
|-----------|-------|
| Capacity | 117 Wh |
| Configuration | 4S LiPo (14.8V nominal) |
| Capacity (mAh) | ~7,900 mAh |
| Mass | 651 g |
| Energy Density | 180 Wh/kg |

### 5.4 Motor Specification

| Parameter | Value |
|-----------|-------|
| Power Rating | 131 W (continuous) |
| Peak Power | ~250 W |
| Mass | 53 g |
| Type | Brushless DC (BLDC) |

---

## 6. Stability & Control

### 6.1 Static Stability

| Parameter | Value | Requirement |
|-----------|-------|-------------|
| Static Margin | ~15% MAC | > 5% |
| dCm/dα | Negative | Must be negative |
| Tail Volume (H) | 0.50 | 0.4-0.7 typical |
| Tail Volume (V) | 0.04 | 0.03-0.05 typical |

### 6.2 Control Surfaces (Preliminary)

| Surface | Chord % | Span % | Deflection |
|---------|---------|--------|------------|
| Ailerons | 25% | 40% | ±25° |
| Elevator | 30% | 100% | ±25° |
| Rudder | 30% | 100% | ±25° |

---

## 7. Construction Notes

### 7.1 Recommended Materials

| Component | Material | Notes |
|-----------|----------|-------|
| Wing Spar | Carbon fiber tube | 12mm OD, 10mm ID |
| Wing Skin | 3D printed + film | PLA/PETG ribs |
| Fuselage | Carbon/fiberglass | Composite layup |
| Tail | 3D printed | Solid core foam |

### 7.2 Structural Requirements

- Wing must support 3G load (5.9 kg)
- Fuselage must carry payload + battery
- Hand launch requires reinforced nose
- Quick-release wing attachment for transport

---

## 8. Files Reference

### Scripts
| File | Purpose |
|------|---------|
| `scripts/drone_sizing.py` | Initial sizing with weight iteration |
| `scripts/aerosandbox_model.py` | AeroSandbox aircraft geometry |
| `scripts/aero_analysis.py` | VLM aerodynamic analysis |
| `scripts/airfoil_optimization.py` | NeuralFoil airfoil optimization |

### Output Files
| File | Contents |
|------|----------|
| `designs/matching_chart.png` | Design space constraints |
| `designs/aerosandbox_model.png` | 3D aircraft visualization |
| `designs/alpha_sweep.png` | Lift curves, drag polar |
| `designs/velocity_sweep.png` | Power required curves |
| `designs/airfoil_comparison.png` | Baseline airfoil comparison |
| `designs/airfoil_optimized.png` | Optimized airfoil results |
| `designs/optimized_airfoil.dat` | Airfoil coordinates |

---

## 9. Next Steps

1. **Integrate Optimized Airfoil** - Update aircraft model with custom airfoil
2. **Structural Analysis** - FEA of wing spar and fuselage
3. **Propeller Design** - Match propeller to motor at cruise RPM
4. **CFD Validation** - High-fidelity aerodynamic verification
5. **Prototype Build** - Manufacturing and assembly
6. **Flight Testing** - Validate performance predictions

---

## 10. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-08 | Initial design release |

---

*Generated with AeroSandbox 4.2.9 and NeuralFoil 0.3.2*
