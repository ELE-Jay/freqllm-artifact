# Security-Level Latency Sensitivity

Latency is in seconds. Lower is better.

Parameters: CKKS, multiplicative depth = 24, scaling modulus size = 50, first modulus size = 60, logical slot capacity = 32768.
Security levels use conservative ring dimensions: λ=128 -> N=65536, λ=192 -> N=131072, λ=256 -> N=262144.
Primitive scaling: additions scale with N; rotations, multiplications, and bootstrapping scale with N log N.

## GPT-2 Small

### 32 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 1243.6 | 1025.3 | 1252.1 | 643.5 | 1.95x |
| 192 | 131072 | 2639.8 | 2176.3 | 2642.4 | 1365.8 | 1.93x |
| 256 | 262144 | 5585.0 | 4604.0 | 5561.2 | 2889.3 | 1.92x |

### 64 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 2388.0 | 1951.3 | 2166.7 | 1177.6 | 1.84x |
| 192 | 131072 | 5069.3 | 4142.1 | 4578.8 | 2499.7 | 1.83x |
| 256 | 262144 | 10725.2 | 8763.2 | 9648.5 | 5288.3 | 1.82x |

### 128 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 4412.7 | 3658.5 | 3479.4 | 1732.4 | 2.01x |
| 192 | 131072 | 9368.3 | 7766.5 | 7354.5 | 3677.4 | 2.00x |
| 256 | 262144 | 19822.2 | 16432.0 | 15500.5 | 7780.0 | 1.99x |

## GPT-2 Medium

### 32 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 2487.2 | 2050.5 | 2793.6 | 1286.9 | 2.17x |
| 192 | 131072 | 5279.7 | 4352.5 | 5888.3 | 2731.6 | 2.16x |
| 256 | 262144 | 11169.9 | 9208.0 | 12378.8 | 5778.6 | 2.14x |

### 64 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 4775.9 | 3902.6 | 4676.7 | 2355.1 | 1.99x |
| 192 | 131072 | 10138.5 | 8284.2 | 9871.9 | 4999.3 | 1.97x |
| 256 | 262144 | 21450.3 | 17526.4 | 20781.1 | 10576.6 | 1.96x |

### 128 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 11694.2 | 9682.9 | 8923.4 | 4512.2 | 1.98x |
| 192 | 131072 | 24827.2 | 20555.7 | 18859.5 | 9578.6 | 1.97x |
| 256 | 262144 | 52531.7 | 43491.2 | 39744.4 | 20265.4 | 1.96x |

## GPT-2 Large

### 32 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 6470.3 | 5259.7 | 6655.0 | 3542.6 | 1.88x |
| 192 | 131072 | 13734.4 | 11164.0 | 14050.9 | 7519.8 | 1.87x |
| 256 | 262144 | 29056.3 | 23617.5 | 29583.8 | 15909.1 | 1.86x |

### 64 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 10829.9 | 8865.0 | 9702.1 | 5215.1 | 1.86x |
| 192 | 131072 | 22989.9 | 18817.7 | 20493.3 | 11070.4 | 1.85x |
| 256 | 262144 | 48640.1 | 39811.1 | 43164.6 | 23421.0 | 1.84x |

### 128 tok
| λ | Ring dim | EncryptedLLM | PolyTransformer | THOR | FreqLLM | FreqLLM speedup vs THOR |
|---:|---:|---:|---:|---:|---:|---:|
| 128 | 65536 | 22236.8 | 18465.5 | 16483.9 | 8560.2 | 1.93x |
| 192 | 131072 | 47208.5 | 39199.4 | 34837.4 | 18171.4 | 1.92x |
| 256 | 262144 | 99886.7 | 82935.7 | 73414.3 | 38444.6 | 1.91x |

