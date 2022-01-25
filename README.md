# QSR-QA
Python scripts and the required inputs for running Qualitative Spatial Reasoning Question Answering (QSR-QA) System.


The script has four main steps:
1. Query generation for three types of questions.
2. Extracting place semantics based on AllenNLP and DeepPavlov libraries in a triple format of (Place 1, relation, Place 2).
3. Preparing the required inputs for SparQ and ProbCog reasoning (You have to firstly set up these reasonsers in your local machine and then use their corresponding implemented python API to generate answers for each question.)
4. Answer extraction on top of the results obtained in the previous step for all question types.
5. Evaluation of the answers.

If you need more information on how it works, feel free to reach out for any inquries.
mkb6988@gmail.com 
