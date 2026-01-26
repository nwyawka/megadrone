# JP Security - Concept of Operations (CONOPS)

**Classification:** UNCLASSIFIED // PROPRIETARY
**Version:** 1.0 DRAFT
**Date:** January 2026
**Author:** JP Security

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Mission and Objectives](#2-mission-and-objectives)
3. [Operational Environment](#3-operational-environment)
4. [Organization and Command Structure](#4-organization-and-command-structure)
5. [Operational Phases](#5-operational-phases)
6. [Platform Employment](#6-platform-employment)
7. [Intelligence Operations](#7-intelligence-operations)
8. [Communications Architecture](#8-communications-architecture)
9. [Coordination with Authorities](#9-coordination-with-authorities)
10. [Logistics and Sustainment](#10-logistics-and-sustainment)
11. [Rules of Engagement](#11-rules-of-engagement)
12. [Training Requirements](#12-training-requirements)
13. [Risk Management](#13-risk-management)

---

## 1. Executive Summary

JP Security conducts persistent maritime surveillance operations in the Gulf of Mexico using a multi-domain unmanned systems approach. Operations integrate aerial (VA-), surface (VS-), and subsurface (VSS-) platforms to detect, track, and support interdiction of illicit maritime activity.

**Core Capability:** Provide actionable intelligence to federal law enforcement agencies (USCG, CBP) through persistent surveillance, vessel identification, and threat assessment.

**Operational Model:** Self-funded operations with compensation tied to successful vessel interdiction. Team deploys to forward operating locations (Key West) for rotational operations.

---

## 2. Mission and Objectives

### 2.1 Mission Statement

Conduct persistent maritime domain awareness operations in the Gulf of Mexico to detect, identify, track, and report vessels engaged in illicit activity, supporting federal law enforcement interdiction efforts.

### 2.2 Primary Objectives

1. **Detection:** Identify vessels of interest through multi-domain sensor coverage
2. **Identification:** Confirm vessel identity, flag state, registration, and activity
3. **Tracking:** Maintain custody of vessels of interest until handoff to authorities
4. **Assessment:** Provide close-range threat assessment prior to interdiction
5. **Support:** Provide real-time intelligence support during boarding operations

### 2.3 Secondary Objectives

1. Build operational track record for government contracting opportunities
2. Develop and validate unmanned systems for maritime surveillance
3. Establish relationships with federal agencies (USCG, CBP, DHS)
4. Generate revenue through successful interdiction support

### 2.4 Success Metrics

| Metric | Target |
|--------|--------|
| Vessels detected per patrol | TBD |
| Positive identification rate | >90% |
| Track custody maintained | >95% |
| Successful interdiction support | TBD |
| Platform availability | >80% |

---

## 3. Operational Environment

### 3.1 Area of Operations

**Primary AO:** Gulf of Mexico, Florida Straits, Caribbean approaches

```
GULF OF MEXICO OPERATIONAL AREA

                    ┌─────────────────────────────────────┐
                    │          GULF OF MEXICO             │
                    │                                     │
      Texas ────────┤                                     │
                    │         ★ Patrol Areas              │
                    │                                     │
                    │                    ┌────────────────┤──── Florida
                    │                    │   ★            │
                    │                    │  Key West      │
                    └────────────────────┴────────────────┘
                              │
                              │  Florida Straits
                              │
                    ══════════════════════════════
                              CUBA
```

**Key Locations:**
- **Home Base:** TBD (shore facility for VS-1 operations)
- **Forward Operating Location:** Key West, FL
- **Testing Locations:** Outer Banks NC, Maryland

### 3.2 Threat Environment

| Threat Type | Description | Indicators |
|-------------|-------------|------------|
| **Go-fast boats** | High-speed vessels, 30-50 ft, carrying contraband | High speed, erratic course, night operations |
| **Semi-submersibles** | Low-profile vessels, difficult to detect | Minimal freeboard, slow speed, specific routes |
| **Fishing vessel cover** | Legitimate vessels used for smuggling | Unusual patterns, rendezvous behavior |
| **Motherships** | Larger vessels supporting smaller craft | Offshore loitering, multiple small craft contact |

### 3.3 Environmental Factors

| Factor | Impact | Mitigation |
|--------|--------|------------|
| **Weather** | Limits air operations, affects sensors | Multiple platform redundancy, weather holds |
| **Sea state** | Affects VS-1 operations, USV recovery | Operating limits defined, safe harbor procedures |
| **Currents** | Affects VSS-1 navigation, drift | DVL navigation, current modeling |
| **Visibility** | Affects visual identification | Thermal/IR sensors, radar |

---

## 4. Organization and Command Structure

### 4.1 Team Organization

```
JP SECURITY ORGANIZATION

                    ┌─────────────────┐
                    │   LEADERSHIP    │
                    │    (O'Neil)     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  OPERATIONS   │   │    INTEL      │   │   BUSINESS    │
│    (TBD)      │   │    (TBD)      │   │    (TBD)      │
└───────────────┘   └───────────────┘   └───────────────┘
```

### 4.2 Core Team (Current)

| Name | Role | Key Responsibilities |
|------|------|---------------------|
| O'Neil | Lead | Overall direction, platform development, comms |
| Brown | Operations | Field ops, firearms, intel contacts |
| Boza | Maritime | Boat operations, marina contacts, federal liaison |
| Devlin | TBD | TBD |

### 4.3 Planned Expansion

| Phase | Timeline | Personnel |
|-------|----------|-----------|
| Phase 1 | Feb 2026 | Introduce Waller |
| Phase 2 | Apr 2026 | Full team rollout (Hartley, Cieglo, others) |
| Phase 3 | May 2026 | Corporate retreat, role finalization |

### 4.4 Field Team Structure

**Typical Deployment Team:**
- Team Lead (1)
- Drone Operator (1-2)
- Analyst (1) - may be remote
- Boat Operator (1) - Boza or designated

---

## 5. Operational Phases

### 5.1 Phase Overview

```
OPERATIONAL SEQUENCE

┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ PHASE 1  │──►│ PHASE 2  │──►│ PHASE 3  │──►│ PHASE 4  │──►│ PHASE 5  │
│ DETECT   │   │ IDENTIFY │   │  TRACK   │   │ INTERDICT│   │ SUPPORT  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
  VS-1 AIS      VA-1/2 ISR     All platforms   Authority     VA-5R ISR
  VSS-1 Hydro   VA-5R close    handoff coord   boarding      Real-time
  VA-2 radar    Visual ID                      JP Security   intel feed
                                               supports
```

### 5.2 Phase 1: Detection

**Objective:** Identify vessels of interest within the AO

**Methods:**
- VS-1 picket vessel AIS monitoring (passive)
- VS-1 radar surveillance (active)
- VSS-1S acoustic monitoring (passive)
- VA-2/VA-4 long-range aerial patrol
- Shore-based monitoring (Starlink data feed)

**Triggers for Phase 2:**
- Vessel without AIS in monitored area
- Vessel exhibiting suspicious behavior
- Acoustic signature matching threat profile
- Intelligence tip or tasking from authorities

**Output:** Initial detection report with position, course, speed, preliminary assessment

### 5.3 Phase 2: Identification

**Objective:** Positively identify vessel and assess threat level

**Methods:**
- VA-1/VA-2 medium-range ISR overflight
- VA-5R close-range inspection (500m-2km standoff)
- Visual identification (hull number, flag, name)
- Thermal/IR imaging for personnel count
- Photographic documentation

**Information Required:**
| Data Point | Source | Priority |
|------------|--------|----------|
| Vessel name | Visual/camera | High |
| Hull number | Visual/camera | High |
| Flag state | Visual/camera | High |
| Vessel type | Visual/camera | High |
| Personnel count | Thermal/visual | Medium |
| Cargo visible | Visual/camera | Medium |
| Vessel condition | Visual | Low |

**Output:** Vessel identification report with imagery, assessment of threat level

### 5.4 Phase 3: Track

**Objective:** Maintain continuous custody of vessel of interest

**Methods:**
- VA-2/VA-4 persistent overhead coverage
- VS-1 surface tracking (radar, visual)
- Handoff coordination between platforms
- Position reporting to authorities

**Track Custody Requirements:**
- Position update minimum every 15 minutes
- Predicted course and speed
- Estimated time to key waypoints (territorial waters, ports)

**Output:** Continuous track data feed to authorities and operations center

### 5.5 Phase 4: Interdiction

**Objective:** Support authority boarding operation

**Note:** JP Security does not conduct interdiction. Federal authorities (USCG, CBP) execute all interdiction operations.

**JP Security Role:**
- Provide real-time vessel position to boarding team
- Conduct final pre-boarding threat assessment (VA-5R)
- Provide overwatch during approach
- Document interdiction for evidence/records

**Coordination:**
- Handoff to USCG/CBP at designated point
- Maintain comms with boarding team
- Provide requested intelligence support

### 5.6 Phase 5: Boarding Support

**Objective:** Provide intelligence support during boarding operation

**Methods:**
- VA-5R overhead for situational awareness
- Real-time video feed to command element (if requested)
- Personnel tracking on vessel
- Early warning of other vessel approach

**Post-Boarding:**
- Document seized vessel/cargo
- Provide imagery for evidence package
- Debrief with authorities
- Update intelligence databases

---

## 6. Platform Employment

### 6.1 Platform Roles

| Platform | Primary Role | Secondary Role |
|----------|--------------|----------------|
| **VA-1/VA-2** | Medium-range ISR | Identification, tracking |
| **VA-4** | Long-endurance patrol | Persistent tracking, Starlink relay |
| **VA-5R** | Close-range assessment | Boarding support, overwatch |
| **VS-1D/S** | Picket surveillance | AIS monitoring, platform mothership |
| **VSS-1I** | Hull inspection | Subsurface search |
| **VSS-1S** | Acoustic monitoring | Early warning |

### 6.2 Integrated Operations

```
MULTI-DOMAIN INTEGRATION

                    VA-4 (Long Endurance)
                    8-12 hr patrol
                         │
                         │ Wide area search
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
    VA-1/VA-2                       VS-1 Picket
    Medium ISR                      Surface monitoring
         │                               │
         │ ID pass                       │ AIS/radar
         │                               │
         ▼                               ▼
      VA-5R ◄─────── Target ───────► VSS-1S
      Close ISR      handoff         Acoustic detect
         │
         │ Pre-boarding assessment
         │
         ▼
    Authority Boarding
    (USCG/CBP)
```

### 6.3 Platform Availability

| Platform | Qty Planned | Summer 2026 Ready |
|----------|-------------|-------------------|
| VA-1 or VA-2 | 1 | Target |
| VA-5R | 1 | Target |
| VS-1D | 1 | Development |
| VSS-1I | 1 | Development |

### 6.4 Deployment from VS-1

VS-1 serves as a mothership for smaller platforms:

```
VS-1 PLATFORM DEPLOYMENT

┌─────────────────────────────────────────┐
│              VS-1 PICKET                │
│                                         │
│   ┌─────────┐  ┌─────────┐  ┌────────┐ │
│   │  VA-5R  │  │ VSS-1I  │  │ Comms  │ │
│   │ (deck)  │  │ (stern) │  │ (mast) │ │
│   └─────────┘  └─────────┘  └────────┘ │
│                                         │
│   Launch/recover aerial and subsurface  │
│   platforms for extended operations     │
└─────────────────────────────────────────┘
```

---

## 7. Intelligence Operations

### 7.1 Intelligence Cycle

```
        ┌─────────────┐
        │  PLANNING   │
        │  & DIRECTION│
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐         ┌─────────────┐
        │ COLLECTION  │────────►│ PROCESSING  │
        └─────────────┘         └──────┬──────┘
               ▲                       │
               │                       ▼
        ┌──────┴──────┐         ┌─────────────┐
        │DISSEMINATION│◄────────│  ANALYSIS   │
        └─────────────┘         └─────────────┘
```

### 7.2 Collection Sources

| Source | Type | Platform | Data |
|--------|------|----------|------|
| AIS | SIGINT | VS-1 | Vessel ID, position, course |
| Radar | Active | VS-1, VA-4 | Non-cooperative tracks |
| EO/IR | IMINT | VA-1/2/5R | Imagery, video |
| Acoustic | Passive | VSS-1S | Vessel signatures |
| Open Source | OSINT | Shore | Vessel databases, news |

### 7.3 Analyst Role

**Location:** Shore-based (remote) or forward deployed

**Responsibilities:**
- Monitor incoming sensor feeds
- Correlate multi-source data
- Produce vessel identification reports
- Maintain vessel database
- Coordinate with authorities
- Brief operations team

**Shifts:** TBD (based on operational tempo)

### 7.4 Information Security

- All operational data encrypted in transit (Starlink, cellular)
- Vessel database access controlled
- Imagery stored securely
- OPSEC protocols for communications
- Need-to-know basis for sensitive information

---

## 8. Communications Architecture

### 8.1 Communications Overview

```
COMMUNICATIONS ARCHITECTURE

┌──────────────────────────────────────────────────────────────────┐
│                        STARLINK                                   │
│                    (Primary backbone)                             │
└───────────────────────────┬──────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
    ┌─────────┐       ┌─────────┐       ┌─────────┐
    │  VS-1   │       │  VA-4   │       │  Shore  │
    │ Picket  │       │ Relay   │       │  Base   │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                  │
    ┌────┴────┐       ┌────┴────┐            │
    │ VA-5R   │       │ Field   │            │
    │ VSS-1   │       │ Team    │            │
    └─────────┘       └─────────┘            │
                                             │
                                    ┌────────┴────────┐
                                    │    Analyst      │
                                    │    (Remote)     │
                                    └─────────────────┘
```

### 8.2 Communication Methods

| Method | Use Case | Range | Security |
|--------|----------|-------|----------|
| **Starlink** | Primary data/video | Global | Encrypted |
| **Cellular** | Backup, shore comms | Coastal | Encrypted app |
| **VHF Marine** | Emergency, authority coord | 20-50 nm | Unencrypted |
| **GMRS** | Team tactical | 5-25 mi | Unencrypted |
| **Ham (HF)** | Emergency backup | Long range | Unencrypted |

### 8.3 Frequency Plan

| Service | Frequency/Channel | Use |
|---------|-------------------|-----|
| VHF Ch 16 | 156.800 MHz | Distress, calling |
| VHF Ch 22A | 157.100 MHz | USCG liaison |
| GMRS Ch 1 | 462.5625 MHz | Team primary |
| GMRS Ch 2 | 462.5875 MHz | Team alternate |
| Ham 2m | TBD | Emergency backup |

### 8.4 Call Signs and Procedures

**Call Signs:** TBD

**Check-in Schedule:**
- Routine: Every 4 hours
- Operations: Every hour
- Active tracking: Every 15 minutes

**Emergency Procedures:**
- MAYDAY: VHF Ch 16
- Platform loss: Immediate report to operations
- Comms loss: RTB after 1 hour

---

## 9. Coordination with Authorities

### 9.1 Agency Relationships

| Agency | Role | Contact Method |
|--------|------|----------------|
| **USCG Sector Key West** | Primary interdiction | VHF, phone |
| **CBP Air and Marine** | Interdiction, intel sharing | Phone, liaison |
| **JIATF-South** | Strategic intel | TBD |
| **DEA** | Intel sharing | TBD |

### 9.2 Reporting Procedures

**Suspicious Activity Report (SAR):**
- Position, course, speed
- Vessel description
- Observed activity
- Imagery if available
- Assessed threat level

**Report Timeline:**
- Immediate: High-confidence threat vessel
- Priority: Suspicious activity
- Routine: End of patrol summary

### 9.3 Legal Framework

JP Security operates as a private entity providing intelligence support:
- No law enforcement authority
- No authority to stop, board, or detain
- Operates in public waters under normal maritime rights
- Provides information to authorities who determine action

---

## 10. Logistics and Sustainment

### 10.1 Forward Operating Location - Key West

**Facilities Required:**
- Boat slip/mooring (Boza coordinates)
- Equipment storage
- Team housing
- Vehicle parking

**Rotation Schedule:**
- Summer 2026: 1-2 rotations planned
- Duration: TBD (1-2 weeks per rotation)

### 10.2 Equipment Transport

**Method:** O'Neil drives to Key West

**Equipment Transported:**
- VA-1/VA-2 fixed-wing platform
- VA-5R quad platform
- Ground control station
- Batteries, chargers, spares
- Communications equipment
- Personal kit

### 10.3 Platform Maintenance

| Platform | Maintenance Interval | Location |
|----------|---------------------|----------|
| VA-1/VA-2 | Pre/post flight | Field |
| VA-5R | Pre/post flight | Field |
| VS-1 | Weekly, post-patrol | Shore facility |
| VSS-1 | Post-dive, monthly | Shore facility |

### 10.4 Supply Chain

**Critical Spares (deploy with):**
- Propellers (all platforms)
- Batteries (charged spares)
- Motor/ESC (one per platform type)
- Basic repair kit

**Resupply:**
- Batteries: Local recharge or ship
- Fuel (VS-1): Local marina
- Parts: Overnight ship if critical

---

## 11. Rules of Engagement

### 11.1 General Principles

1. **Safety First:** Personnel and platform safety paramount
2. **Legal Compliance:** All operations within applicable law
3. **No Direct Action:** JP Security does not interdict, board, or detain
4. **Observe and Report:** Primary mission is intelligence collection
5. **Escalation:** Contact authorities for any threat situation

### 11.2 Platform Employment Rules

| Situation | Action | Authority |
|-----------|--------|-----------|
| Vessel of interest detected | Continue monitoring, report | Operator |
| Close approach requested | Minimum 500m standoff | Team Lead |
| Vessel takes evasive action | Maintain track, report | Operator |
| Vessel displays weapons | Withdraw, report immediately | Immediate |
| Platform threatened | Withdraw, report | Immediate |
| Authority requests support | Provide within capability | Team Lead |

### 11.3 Standoff Distances

| Platform | Minimum Standoff | Notes |
|----------|------------------|-------|
| VA-1/VA-2 | 500m | Higher for armed vessels |
| VA-5R | 500m | Close approach only with authority present |
| VS-1 | 1 nm | Surface vessel vulnerable |
| VSS-1 | N/A | Subsurface, not visible |

### 11.4 Weapons Policy

- Team members with valid CWL may carry personal firearms
- Brown designated firearms resource
- Firearms for personal defense only
- No offensive weapons on platforms (except VA-5S, future)
- Firearms secured when not on person

---

## 12. Training Requirements

### 12.1 Required Certifications

| Certification | Required For | Who |
|---------------|--------------|-----|
| FAA Part 107 | Drone operations | All pilots |
| Florida Boater Safety | FL waters | All boat operators |
| USCG OUPV | Paid operations | Boza (verify) |
| FCC GMRS | Radio operations | O'Neil (complete) |
| Florida CWL | Concealed carry | Brown, others |

### 12.2 Training Program

| Training | Frequency | Attendees |
|----------|-----------|-----------|
| Platform operations | Pre-deployment | All operators |
| Emergency procedures | Quarterly | All |
| Communications | Pre-deployment | All |
| First aid/safety | Annual | All |
| Intel analysis | Initial + quarterly | Analysts |

### 12.3 Proficiency Requirements

| Skill | Standard | Evaluation |
|-------|----------|------------|
| Drone flight | 5 hrs/quarter | Log review |
| Boat operations | 10 hrs/quarter | Log review |
| Emergency procedures | Pass scenario | Quarterly exercise |

---

## 13. Risk Management

### 13.1 Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Platform loss (crash/sink) | Medium | Medium | Redundancy, insurance |
| Personnel injury | Low | High | Training, safety protocols |
| Detection by target | Medium | Low | Standoff distances |
| Equipment failure | Medium | Medium | Spares, redundancy |
| Weather impacts | High | Medium | Forecasting, holds |
| Legal/liability | Low | High | Legal review, insurance |
| Hostile action | Low | High | Standoff, withdrawal |

### 13.2 Emergency Procedures

**Platform Loss:**
1. Mark last known position
2. Attempt recovery if safe
3. Report to operations
4. Document for insurance
5. Continue mission if able

**Medical Emergency:**
1. Stabilize patient
2. Contact USCG (VHF 16) or 911
3. Evacuate to nearest medical facility
4. Document incident

**Hostile Action:**
1. Immediately withdraw all platforms
2. Contact USCG
3. Document incident
4. Abort mission
5. Debrief

### 13.3 Insurance Requirements

- General liability
- Marine operations coverage
- Equipment/hull coverage
- Professional liability
- Workers compensation (if employees)

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| AIS | Automatic Identification System |
| AO | Area of Operations |
| CBP | Customs and Border Protection |
| CONOPS | Concept of Operations |
| CWL | Concealed Weapons License |
| DVL | Doppler Velocity Log |
| EO/IR | Electro-Optical/Infrared |
| GMRS | General Mobile Radio Service |
| IMINT | Imagery Intelligence |
| ISR | Intelligence, Surveillance, Reconnaissance |
| JIATF | Joint Interagency Task Force |
| RTB | Return to Base |
| SAR | Suspicious Activity Report |
| SIGINT | Signals Intelligence |
| USCG | United States Coast Guard |
| USV | Unmanned Surface Vehicle |
| UUV | Unmanned Underwater Vehicle |
| VTOL | Vertical Take-Off and Landing |

### Appendix B: References

- Hardware specifications: `/hardware/README.md`
- VS-1 Picket: `/hardware/vs1_picket/README.md`
- VSS-1 Submersible: `/hardware/vss1_submersible/README.md`
- VA-5 Strike: `/hardware/va5_strike/README.md`
- TODO List: `/docs/TODO.md`

### Appendix C: Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 DRAFT | Jan 2026 | JP Security | Initial draft |

---

*This document is UNCLASSIFIED // PROPRIETARY*
*Distribution limited to JP Security personnel*
*Version controlled in MegaDrone repository*
