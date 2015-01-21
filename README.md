Anatomy
===========================
Anatomizer is a linear anonymization algorithm base on Anatomy, proposed by Xiao et. al.[1]. Anatomy anonymize dataset by breaking direct correlation between QID and SA (publish QID and SA in separated tables). To our knowledge, Anatomizer is the fastest algorithm, which preserve good data utility at the same time. Although Xiao et. al. gave the pseudocode in his papers, the original source code is not available. You can find the Java implement in Anonymization Toolbox[2].

This repository is an *open source python implement* for Anatomizer. I implement this algorithm in python for further study.

Usage:
	# the variable L for l-diversity
	python anonymizer.py L
	# the anonymizer data is stored in result.

### Attention
In residue-assignmenet setp, the original pseudocode in Xiao's paper suggest to use random. I found it unsufficient. So I try every groups in order. It's much faster, meanwhile making previous groups much larger.


### Motivation 
Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [2-3], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy! 

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing).

## For more information:

[1] X. Xiao, Y. Tao. Anatomy: simple and effective privacy preservation Proceedings of the 32nd international conference on Very large data bases, VLDB Endowment, 2006, 139-150 

[2] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/cgi-bin/toolbox/index.php?go=home)

[3] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)

==========================
by Qiyuan Gong
qiyuangong@gmail.com

2014-09-11
