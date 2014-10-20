Anatomy
===========================
Anatomy is a linear anonymization algorithm base on lossy join, proposed by Xiao et. al. Xiao in his papers[1]. Anatomy anonymize dataset by breaking direct correlation between QID and SA (publish QID and SA in separated tables). To our knowledge, Anatomy is the fastest algorithm, which preserve good data utility at the same time. Although Xiao et. al. gave the pseudocode in his papers, the original source code is not available. You can find the Java implement in Anonymization Toolbox[2].

This repository is an *open source python implement* for Anatomy. I implement this algorithm in python for further study.

### Motivation 
Researches on data privacy have lasted for more than ten years, lots of great papers have been published. However, only a few open source projects are available on Internet [2-3], most open source projects are using algorithms proposed before 2004! Fewer projects have been used in real life. Worse more, most people even don't hear about it. Such a tragedy! 

I decided to make some effort. Hoping these open source repositories can help researchers and developers on data privacy (privacy preserving data publishing).

## For more information:
[1]  LeFevre, Kristen, David J. DeWitt, and Raghu Ramakrishnan. Mondrian multidimensional k-anonymity. Data Engineering, 2006. ICDE'06. Proceedings of the 22nd International Conference on. IEEE, 2006.

==========================
by Qiyuan Gong
qiyuangong@gmail.com

2014-09-11

[1] Xiao, X. & Tao, Y. Anatomy: simple and effective privacy preservation Proceedings of the 32nd international conference on Very large data bases, VLDB Endowment, 2006, 139-150 

[2] [UTD Anonymization Toolbox](http://cs.utdallas.edu/dspl/cgi-bin/toolbox/index.php?go=home)

[3] [ARX- Powerful Data Anonymization](https://github.com/arx-deidentifier/arx)
