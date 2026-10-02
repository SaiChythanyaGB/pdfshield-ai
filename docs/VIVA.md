# Viva cheat sheet

Q: What is the core problem?
A: Classifying PDFs as benign or malicious using static structural features without executing the document.

Q: Why static analysis?
A: It is safer for a web application because the system can inspect bytes and structure without executing embedded content.

Q: Why Random Forest?
A: It can model nonlinear feature interactions, works well on tabular data, and provides feature importance for interpretation.

Q: Why recall?
A: A false negative means malicious content is classified as benign, which is an important failure mode in security detection.

Q: What is an evasion attack?
A: An adversarial technique that attempts to cause a trained model to misclassify an input at decision time.

Q: Is the adversarial lab generating malware?
A: No. It perturbs numerical feature vectors in memory and does not generate or execute malicious files.

Q: Can the model be 100% accurate?
A: No. Security data changes, distributions shift, and static features are incomplete. The system must be evaluated empirically.
