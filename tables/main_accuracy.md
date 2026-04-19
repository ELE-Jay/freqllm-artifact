# Main Accuracy Table

| Scale | Method | SST2 | WiC | PIQA | ARC-E | SIQA | MNLI | HellaSwag | ANLI-R1 | Avg. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Small | Plaintext GPT-2 | 0.492 | 0.495 | \textbf{0.589} | \textbf{0.378} | \textbf{0.365} | 0.324 | \textbf{0.269} | \textbf{0.379} | \textbf{0.412} |
|   | PolyTransformer | 0.480 | \textbf{0.500} | 0.519 | 0.272 | 0.326 | \textbf{0.354} | 0.261 | 0.334 | 0.381 |
|   | EncryptedLLM | \textbf{0.509} | \textbf{0.500} | 0.543 | 0.257 | 0.330 | \textbf{0.354} | 0.257 | 0.334 | 0.386 |
|   | FreqGPT | 0.491 | \textbf{0.500} | 0.536 | 0.269 | 0.336 | 0.319 | 0.262 | 0.329 | 0.380 |
| Medium | Plaintext GPT-2 | 0.493 | \textbf{0.500} | \textbf{0.541} | 0.261 | 0.341 | \textbf{0.354} | 0.260 | 0.334 | 0.386 |
|   | PolyTransformer | 0.491 | \textbf{0.500} | 0.511 | 0.262 | 0.336 | \textbf{0.354} | \textbf{0.261} | 0.334 | 0.381 |
|   | EncryptedLLM | \textbf{0.513} | \textbf{0.500} | 0.534 | \textbf{0.272} | \textbf{0.348} | 0.351 | 0.258 | \textbf{0.335} | \textbf{0.389} |
|   | FreqGPT | 0.508 | \textbf{0.500} | 0.516 | 0.260 | 0.344 | \textbf{0.354} | 0.259 | 0.334 | 0.384 |
| Large | Plaintext GPT-2 | 0.494 | \textbf{0.500} | \textbf{0.525} | \textbf{0.267} | 0.336 | 0.341 | \textbf{0.261} | 0.329 | 0.382 |
|   | PolyTransformer | \textbf{0.509} | \textbf{0.500} | 0.517 | 0.264 | 0.331 | \textbf{0.354} | 0.260 | 0.334 | \textbf{0.384} |
|   | EncryptedLLM | 0.505 | 0.486 | 0.513 | 0.243 | \textbf{0.342} | 0.330 | 0.261 | \textbf{0.337} | 0.377 |
|   | FreqGPT | \textbf{0.509} | \textbf{0.500} | 0.515 | 0.256 | 0.341 | 0.318 | 0.261 | 0.333 | 0.379 |
