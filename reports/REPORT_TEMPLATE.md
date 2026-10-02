# PDFShield AI
## Explainable PDF Malware Detection and Adversarial Robustness Analysis Using Machine Learning

### Abstract
[Write 150–250 words after completing experiments. Include problem, dataset, features, model, evaluation and key result.]

### 1. Introduction
PDF is a widely used document format. Its support for active and embedded content creates a security-analysis problem. This project investigates whether static PDF features can be used by a supervised ML classifier to distinguish benign and malicious PDFs.

### 2. Problem Statement
Develop a defensive ML system that analyzes PDF structure without executing embedded content and predicts whether a file is benign or malicious. Evaluate model sensitivity using a controlled feature-space adversarial robustness experiment.

### 3. Objectives
- Extract security-relevant static PDF features.
- Train a supervised binary classifier.
- Evaluate using accuracy, precision, recall, F1 and ROC-AUC.
- Visualize security-relevant indicators.
- Conduct a safe feature-space robustness experiment.

### 4. Dataset
[Insert exact dataset name/version, source, number of rows, class distribution and citation.]

### 5. Methodology
PDF → static feature extraction → preprocessing → train/test split → Random Forest → evaluation → robustness experiment.

### 6. Feature Engineering
[Describe file size, pages, encryption, objects, streams, JavaScript/action indicators, embedded files, XFA, RichMedia, etc.]

### 7. Model
[Describe Random Forest and why it is appropriate for mixed nonlinear feature interactions.]

### 8. Results
[Insert actual metrics and confusion matrix from `ml.evaluate`.]

### 9. Adversarial Robustness
[Describe the controlled feature-space experiment and clearly state that it is not equivalent to creating a valid evasive PDF.]

### 10. Limitations
- Static analysis cannot observe runtime behavior.
- Dataset bias may affect generalization.
- False positives and false negatives are possible.
- Feature-space perturbations are an abstraction.
- A research classifier is not a replacement for antivirus/sandboxing.

### 11. Future Work
- Compare Random Forest, SVM and gradient boosting.
- Add calibrated probabilities.
- Use a held-out external dataset.
- Add explainability such as SHAP.
- Build an isolated sandbox only if appropriate institutional safety controls exist.

### 12. Conclusion
[Write after results are available. Do not claim more than the evidence supports.]
