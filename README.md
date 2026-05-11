# 🛡️ Phantom Sentinel: Multi-Modal Deepfake Detective (SaaS)

![Version](https://img.shields.io/badge/version-1.0.0_MVP-blue)
![Frontend](https://img.shields.io/badge/frontend-Streamlit-FF4B4B)
![Framework](https://img.shields.io/badge/framework-Multi--Agent_Debate-orange)

An enterprise-grade SaaS platform designed for high-concurrency, multi-modal Deepfake detection and logical evidence tracing. Specially optimized for V2A (Video-to-Audio) and A2V cross-modal consistency analysis.

## 📌 Web UI Demonstration

*(Internal Dev Snapshot - UI Core)*
![Product Demo](./demo_ui.png) 

## ⚙️ System Architecture

Unlike traditional black-box classification models, Phantom Sentinel relies on a highly token-intensive **Multi-Agent Red-Blue Teaming** architecture:
1. **Decomposition Agent**: Extracts dense temporal features from uploaded media.
2. **Detective Agent (CoT)**: Performs millisecond-level causal alignment (e.g., matching visual fingering with acoustic pitch).
3. **Red-Blue Debate Protocol**: Triggers high-frequency internal debate to eliminate LLM hallucinations and finalize the judicial-level evidence chain.

## 🚀 Extreme Token Consumption (MiMo Plan Required)

This repository contains the frontend MVP implementation (`app.py`). **The backend reasoning engine requires massive Context Window capabilities.** A single media analysis task consumes over **100,000+ tokens** due to the extensive temporal text descriptions and multi-round agent debates. 

We are actively applying for the **Xiaomi MiMo 100T Plan** to migrate our core inference endpoints and support production-scale concurrency for our upcoming beta release.
