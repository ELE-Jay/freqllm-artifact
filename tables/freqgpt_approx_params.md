# Approximation Parameter Table

| Scale | Method | Approximation / architectural parameters |
|---|---|---|
| Small | EncryptedLLM | LN Newton = 16, exp r = 7, Goldschmidt = 14 |
| Small | PolyTransformer | InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7 |
| Small | FreqGPT | PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed |
| Medium | EncryptedLLM | LN Newton = 18, exp r = 7, Goldschmidt = 18 |
| Medium | PolyTransformer | InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7 |
| Medium | FreqGPT | PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed |
| Large | EncryptedLLM | LN Newton = 18, exp r = 7, Goldschmidt = 22 |
| Large | PolyTransformer | InvSqrt deg. = 7, Sigma / GeLU deg. = 7 / 7 |
| Large | FreqGPT | PolyNorm deg. = 2, FreqMixer order = 2, FFT-Linear = yes, Softmax / Division = removed |
