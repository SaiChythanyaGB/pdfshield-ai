# PDFShield AI — PDF Malware Detection + Adversarial Robustness Lab

Academic project for **Data Science for Security (ADS23704A)**.

## 1. Project title
**PDFShield AI: Explainable PDF Malware Detection and Adversarial Robustness Analysis Using Machine Learning**

## 2. Problem statement
PDF files can contain active content and structural features that may be abused for malicious behavior. The project builds a defensive static-analysis classifier that predicts whether a PDF is benign or malicious from extracted structural features, then evaluates how sensitive the model is to controlled feature-space perturbations.

## 3. Syllabus mapping
- Module 1: malware analysis and ML-based malware detection.
- Module 2: PDF feature extraction and feature engineering.
- Module 5: adversarial ML, evasion attacks, decision-time attacks, and attacks on PDF malware classifiers.

## 4. Safety boundary
The application performs static analysis only. It does not execute PDF JavaScript, embedded files, shell commands, or malware. The adversarial lab modifies feature vectors in memory rather than generating or modifying real malicious files.

## 5. Dataset
Recommended primary dataset: **CIC-Evasive-PDFMal2022**. The Canadian Institute for Cybersecurity describes 10,025 records: 5,557 malicious and 4,468 benign, with static PDF features and an evasive subset. See the official page: https://www.unb.ca/cic/datasets/pdfmal-2022.html

A newer optional benchmark is **RIT-PDFMal-2026**, which provides 24,337 included samples and 42 extracted features. See https://github.com/Mo-Alani/RIT-PDFMal-2026

Do not commit malware samples to Git. Prefer the extracted feature CSV for model training.

## 6. Expected dataset layout
Create:

```text
data/
  processed/
    PDFMalware2022.csv
```

The training script searches for a label column named one of: `Label`, `label`, `class`, `Class`, `target`, `Target`.

The label convention is normalized to:
- 0 = Benign
- 1 = Malicious

## 7. Setup on macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 8. Train

```bash
python -m ml.train --csv data/processed/PDFMalware2022.csv
```

The trained model is written to:

```text
models/pdf_malware_rf.joblib
models/pdf_malware_rf.json
```

## 9. Evaluate

```bash
python -m ml.evaluate --csv data/processed/PDFMalware2022.csv --model models/pdf_malware_rf.joblib
```

For a proper academic evaluation, use a held-out test set rather than reporting performance on the same data used for training.

## 10. Run the application

```bash
streamlit run app/main.py
```

## 11. Project workflow

```text
                 PDF file
                    |
                    v
          Safe static feature extraction
                    |
                    v
              Feature vector
                    |
                    v
            Random Forest model
                    |
            +-------+-------+
            |               |
         Benign         Malicious
            |               |
            +-------+-------+
                    |
                    v
            Risk indicators
                    |
                    v
          Feature-space robustness
                 experiment
```

## 12. Evaluation metrics
Use:
- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

For security, pay particular attention to **recall for the malicious class** and the false-negative count. Do not claim a model is secure based on accuracy alone.

## 13. Adversarial experiment
The included lab is deliberately feature-space based. It asks: "How does the classifier's malicious probability change when selected numerical features are systematically perturbed?"

This is a teaching experiment and **not** evidence that an actual PDF can be changed in the same way. In the report, explicitly state this limitation.

## 14. Suggested report chapters
1. Introduction
2. Problem Statement
3. Objectives
4. Literature/Dataset Review
5. Proposed Methodology
6. Feature Engineering
7. Machine Learning Model
8. System Architecture
9. Implementation
10. Experimental Evaluation
11. Adversarial Robustness Experiment
12. Results and Discussion
13. Limitations
14. Future Enhancement
15. Conclusion
16. References

## 15. Viva questions to prepare
1. Why is PDF malware detection a cybersecurity problem?
2. What is static analysis?
3. Why is machine learning useful here?
4. What are the PDF structural features?
5. Why Random Forest?
6. Why is recall important for malware detection?
7. What is an evasion attack?
8. What is a black-box attack?
9. What is the difference between a real adversarial PDF and this feature-space experiment?
10. What are false positives and false negatives?
11. Why should malicious samples never be executed by the web application?
12. What limitations does the model have?

## 16. Important academic honesty note
Do not invent accuracy numbers. Train the model on the chosen dataset, record the actual test-set metrics, and use those numbers in the report and presentation.
