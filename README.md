# Anatomize

Anatomize is a linear anonymization algorithm base on Anatomy, proposed by Xiao et. al.[1]. Anatomy anonymize dataset by breaking direct correlation between QID and SA (publish QID and SA in separated tables). To our knowledge, Anatomize is the fastest algorithm, which preserve good data utility at the same time. Although Xiao et. al. gave the pseudocode in his paper, the original source code is not available. You can find the Java implementation in Anonymization Toolbox[2].

This repository is an **open source python implementation for Anatomize**. I implement this algorithm in python for further study.



### Motivation

Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [2-3], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy! 

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing).


### Usage:

My Implementation is based on Python 2.7 (not Python 3.0). Please make sure your Python environment is collectly installed. You can run Anatomy in following steps: 

1) Download (or clone) the whole project. 

2) Run "anonymized.py" in root dir with CLI.



	# run Mondrian with default l(l=10)

	python anonymizer.py 

	

	# run Mondrian with l=20

	python anonymized.py 20



## For more information:

[1] X. Xiao, Y. Tao. Anatomy: simple and effective privacy preservation Proceedings of the 32nd international conference on Very large data bases, VLDB Endowment, 2006, 139-150 

[2] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/cgi-bin/toolbox/index.php?go=home)

[3] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)

==========================

by Qiyuan Gong

qiyuangong@gmail.com

2014-09-11