
The code and data are related to the paper ''*Probabilistic Qualitative Spatial Reasoning with Applications to GeoQA*''

# Perquisites

Two spatial reasoning tools, SparQ for conventional reasoning and Probcog for probabilistic reasoning need to be installed:

- Probcog ( Follow the their github repo in https://github.com/opcode81/ProbCog)
- SparQ (Follow their manual in https://www.uni-bamberg.de/fileadmin/sme/SparQ/SparQ-Manual.pdf)


# Materials

This includes codes, data and evidence sets folders for two experiments:

- Code: This folder includes questionGenerator.py and answerExtraction.py for generating synthetic questions and post-processing of inferences from Probcog and SparQ reasoners. Also we have written Python API for Probcog (ProbCog-API.py) and SparQ reasoners (SparQ-API.py).
- Data: This folder shows the chosen 500 place name in Experiment 1 and UK footprints in Experiment 2. 
- Evidence: This hows all spatial configurations defined for two experiments. 

# File Description

Each experiment follows the following steps for generating answers for input questions:

1. Query generation: Generating three types of questions (Finding relation (FR), Finding Features (FF), Yes/no (YN))
2. Answer extraction: Feeding the generated questions in the previous step into the Probcog and SparQ Python APIs ( You have to firstly install these reasoners in your local machine). The output of this step is the generated answers from the reasoners for each question.
3. Evaluation of the answers: Different evaluations of answers are generated from this steps (e.g., accuracy, magnitude of difference in probability values distribution, probability distribution boxplots, etc) 

