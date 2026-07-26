# FPGA Pipelining Analysis

> **An experimental study of how pipelining affects timing, operating frequency, resource utilization, power consumption, and latency on an FPGA.**

---

## Overview

Pipelining is one of the most fundamental optimization techniques in digital design. Almost every FPGA and processor architecture relies on pipelining to achieve high operating frequencies.

While the concept is frequently explained in textbooks, very few examples actually **measure** its impact.

This repository implements the **same arithmetic datapath** using three different pipeline depths and compares their effect on:

- Maximum Operating Frequency (Fmax)
- Critical Path Delay
- Resource Utilization
- Power Consumption
- Pipeline Latency

The objective is to understand **what pipelining really changes**, what it **does not change**, and the trade-offs involved.

---

# Experiment

The same functionality is implemented in three different ways.

```
8 Inputs

a + b + c + d + e + f + g + h
```

The algorithm remains **identical** in all three implementations.

The **only difference** is the placement of pipeline registers.

---

# Implementations

## 1. Baseline

```
Input Registers
        │
        ▼
 Level-1 Adders
        │
 Level-2 Adders
        │
 Level-3 Adder
        │
        ▼
 Output Register
```

Entire combinational datapath executes within a single clock cycle.

---

## 2. Two-Stage Pipeline

```
Input Registers
        │
        ▼
 Level-1 Adders
        │
 Pipeline Registers
        │
 Level-2 Adders
        │
 Level-3 Adder
        │
        ▼
 Output Register
```

The combinational path is divided into two smaller timing paths.

---

## 3. Three-Stage Pipeline

```
Input Registers
        │
        ▼
 Level-1 Adders
        │
 Pipeline Registers
        │
 Level-2 Adders
        │
 Pipeline Registers
        │
 Level-3 Adder
        │
        ▼
 Output Register
```

Each level of the adder tree has its own pipeline stage.

---

# Experimental Setup

- **Tool:** AMD Vivado
- **Language:** SystemVerilog
- **Target Clock:** 100 MHz (10 ns)
- **Constraint:** Single clock constraint
- **Design:** Balanced Adder Tree
- **Inputs:** Eight 8-bit unsigned numbers
- **Output:** 11-bit sum

---

# Results

| **Metric** | **Baseline** | **2-Stage Pipeline** | **3-Stage Pipeline** |
|:-----------|-------------:|---------------------:|---------------------:|
| Slice LUTs | 38 | 52 | 60 |
| Slice Registers | 75 | 111 | 131 |
| WNS (ns) | 5.259 | 6.619 | 8.320 |
| Critical Path (ns) | 4.741 | 3.381 | 1.680 |
| Calculated Maximum Frequency (MHz) | 211 | 296 | 595 |
| Total On-Chip Power (W) | 0.094 | 0.095 | 0.096 |
| Latency (Clock Cycles) | 1 | 2 | 3 |
---

# Key Observations

### Pipelining significantly improves timing

```
Critical Path

4.741 ns
      ↓
3.381 ns
      ↓
1.680 ns
```

Reducing the critical path directly increases the achievable operating frequency.

---

### Maximum Operating Frequency

```
Baseline          : 211 MHz

2-Stage Pipeline  : 296 MHz

3-Stage Pipeline  : 595 MHz
```

Nearly **3× improvement** was achieved without changing the algorithm.

---

### Area Trade-Off

Adding pipeline stages increases the number of flip-flops.

```
Registers

75

↓

111

↓

131
```

The increase in area is expected because intermediate results must be stored between pipeline stages.

---

### Power Consumption

Although additional registers increase clock activity, the overall power increase remains very small.

```
0.094 W

↓

0.095 W

↓

0.096 W
```

---

### Latency

Increasing pipeline depth increases latency.

```
Baseline          : 1 Clock Cycle

2-Stage Pipeline  : 2 Clock Cycles

3-Stage Pipeline  : 3 Clock Cycles
```

However, once the pipeline is full, **one output is produced every clock cycle**, preserving throughput.

---

# What This Experiment Demonstrates

Many beginners believe:

> "Pipelining makes hardware faster."

This experiment demonstrates something more precise.

Pipelining **does not reduce the amount of computation**.

Instead, it reduces the amount of computation performed **during a single clock period** by inserting registers between combinational logic stages.

As a result:

- Critical path decreases
- Maximum operating frequency increases
- Throughput is maintained
- Latency increases
- Register count increases
- Power increases slightly

---


## Repository Structure

```text
fpga-pipelining-analysis
├── README.md
├── .gitignore
├── constraints/
│   └── baseline.xdc
├── docs/
│   ├── blog/
│   ├── images/
│   └── report/
├── results/
│   ├── baseline/
│   ├── pipeline_2stage/
│   └── pipeline_3stage/
├── rtl/
│   ├── baseline/
│   ├── pipeline_2stage/
│   └── pipeline_3stage/
└── tb/
    ├── baseline/
    ├── pipeline_2stage/
    └── pipeline_3stage/
```

---

# Future Improvements

Potential extensions of this work include:

- Wider datapaths (16-bit, 32-bit, 64-bit)
- DSP-based arithmetic implementation
- Automatic pipeline insertion
- Retiming optimization
- Clock enable vs clock gating
- Low-power FPGA design techniques
- Comparison with DSP slices
- Timing closure analysis

---

# Lessons Learned

This project demonstrates several important FPGA design concepts:

- Register placement directly impacts timing.
- Shorter combinational paths enable higher clock frequencies.
- Pipelining improves throughput but increases latency.
- Higher performance comes at the cost of additional registers.
- Modern FPGA carry chains already provide highly optimized arithmetic implementations.
- Timing reports should always be interpreted together with utilization and power reports to understand the complete design trade-off.

---

## License

This project is intended for learning, experimentation, and educational purposes.

Contributions, suggestions, and improvements are always welcome.