# Urdu Story Generation System

This repository contains a full-stack implementation of an Urdu Story Generation system using a **Trigram Language Model** and **Byte-level Byte Pair Encoding (BPE)**.

## Project Overview

The goal of this project is to generate coherent, long-form Urdu children's stories (approx. 600+ tokens) based on a starting prefix. The system uses a statistical language model trained on a large corpus of Urdu text.

### Key Features
- **Byte-level BPE Tokenizer**: A custom implementation with a 1500-token vocabulary that eliminates Out-Of-Vocabulary (OOV) issues.
- **Trigram MLE Model**: A 3-gram language model with **Linear Interpolation** for smoothing.
- **Story Generation Service**: A FastAPI-based backend that supports streaming and standard generation.
- **Premium Frontend**: A modern, responsive web interface for interacting with the AI.

---

## 🏗 Implementation Details

### 1. Tokenization: Byte-level BPE
The tokenizer was implemented from scratch following the standard BPE algorithm but applied at the byte level (UTF-8) to ensure robustness for Urdu script.

**Algorithm Steps Applied:**
1.  **Initialize**: Start with a base vocabulary of 256 bytes (0-255).
2.  **Find Frequent Pairs**: Identify the most frequent pair of bytes/tokens in the training corpus.
3.  **Merge**: Create a new token for the pair and add it to the vocabulary.
4.  **Repeat**: Continue until the target vocabulary size (1500) is reached.
5.  **Inference**:
    - **Encode**: Apply the learned merges in the same order they were discovered.
    - **Decode**: Map token IDs back to byte sequences and decode as UTF-8.

### 2. Language Model: Trigram MLE
The model estimates the probability of the next token based on the previous two tokens.

- **N-gram Counting**: The model counts occurrences of all unigrams, bigrams, and trigrams in the tokenized corpus.
- **Smoothing (Linear Interpolation)**: To handle unseen contexts, the model uses:
  $$P(w_i | w_{i-2}, w_{i-1}) = \lambda_1 P_{MLE}(w_i | w_{i-2}, w_{i-1}) + \lambda_2 P_{MLE}(w_i | w_{i-1}) + \lambda_3 P_{MLE}(w_i)$$
  where $\lambda_1 + \lambda_2 + \lambda_3 = 1$.

### 3. Story Constraints & Formatting
The system is designed to produce high-quality children's content:
- **Length**: Stories are generated to be between **600 and 800 tokens**.
- **Paragraphs**: Automatic logic inserts paragraph breaks (`\n\n`) every **5-6 sentences**.
- **Filtering**: Special markers like `<START>`, `<EOT>`, and internal boundary markers are filtered from the final display.

---

## 🚀 Execution & Tasks Completed

| Task | Status | Details |
| :--- | :--- | :--- |
| **BPE Tokenization** | ✅ Done | Implemented Byte-level logic, lossless space preservation, and ordered merges. |
| **Model Training** | ✅ Done | Trained on full Urdu corpus with 1500 BPE vocabulary. |
| **Interpolation** | ✅ Done | Implemented λ-weighted smoothing for robust generation. |
| **Backend Service** | ✅ Done | FastAPI backend with streaming support and Vercel config. |
| **Frontend UI** | ✅ Done | Modern React frontend with premium rounded aesthetics. |
| **Cloud Deployment** | ✅ Done | Successfully deployed to Vercel (Frontend & Backend). |

---

## 📂 Repository Structure
- `Tokenizer/`: `bpe_tokenizer.py` and trained weights.
- `Model/`: Trigram model implementation and `TriGramModel.ipynb`.
- `services/story-generation-service/`: FastAPI backend implementation.
- `frontend/`: React components and UI logic.
- `PreProcessing/`: Corpus processing scripts.

## 📄 Final Report Summary
All execution steps, from data preprocessing to cloud deployment, have been verified. The system successfully generates long Urdu stories with proper paragraph formatting, meeting all project requirements.

---
**Author**: i23-2082
**Project**: AI-B Assignment (NLP - Urdu Story Generation)
