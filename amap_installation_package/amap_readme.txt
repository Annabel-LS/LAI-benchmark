Software Name: aMAP
Version: 1.6
Date: 06/01/2014
--------------------

Copyright
--------------------
All Rights Reserved. No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

Development Environment
--------------------
JDK 1.7.0
Microsoft Windows 7 64-bit

Compile & Run
--------------------
1. Download latest JDK and make sure JDK binary folder is added to the system PATH.
2. Compile source code and build the jar package by executing the following batch file: build.bat.
3. Run the software with the following command: java -jar amap.jar sample_config.xml.
4. aMAP can be run on all platforms supporting Java.

Inputs
--------------------
All necessary inputs information can be customized in the configuration file (the only parameter of program).
1. positionCount - how many records for single hyplotype
2. populations - information of one sample file for analysis and multiple reference files
	a. id - population id
	b. type - sample or reference
	c. ordinal - population ordinal, will be used in the results
	d. fileName - population file name
3. outputDir - output directory name
4. minWinSize - the minimum window size to scan
5. winStep - the step to increase window size for different scans
6. maxWinSize - the maximum window size to scan

Data Format
--------------------
aMAP supports HapMap data format. The population data can be downloaded from the following link.
http://www.sanger.ac.uk/resources/downloads/human/hapmap3.html
Example:
rsID	position_b36	NA17970_A	NA17970_B	NA17977_A	NA17977_B	NA17981_A	NA17981_B	NA17993_A	NA17993_B	NA18101_A	NA18101_B
rs10458597	554484	C	C	C	C	C	C	C	C	C	C
rs2185539	556738	C	C	C	C	C	C	C	C	C	C
rs11240767	718814	C	C	C	C	C	C	C	C	C	C
rs12564807	724325	A	A	A	A	A	A	A	A	A	A
rs3131972	742584	G	G	A	G	A	G	G	G	A	G
rs3131969	744045	G	G	A	A	A	G	G	G	A	G
rs3131967	744197	C	C	T	C	C	C	C	C	T	C
rs1048488	750775	T	T	T	T	T	T	T	T	C	T
rs12562034	758311	G	A	A	A	A	G	A	A	G	A
rs12124819	766409	A	A	A	A	A	A	A	A	A	A
rs4040617	769185	A	A	A	A	A	A	A	A	G	A
rs2905036	782343	T	T	T	T	T	T	T	T	T	T
rs4245756	789326	C	C	C	C	C	C	C	C	C	C
rs4970383	828418	C	A	C	A	A	C	A	A	C	C
rs4475691	836671	C	C	C	C	C	C	C	C	C	C
rs1806509	843817	A	A	A	A	A	A	A	A	C	C
rs7537756	844113	A	A	A	A	A	A	A	A	A	A
rs6694982	847691	A	A	A	A	A	A	A	A	A	A
rs13302982	851671	G	A	A	A	A	G	A	A	A	G
rs4040604	852987	T	G	G	G	G	T	G	G	G	T

Outputs
--------------------
The results will be output to output directory as Excel CSV file, one haplotype result per column. The value is the ordinal of each reference population defined in configuration file. 'o' (other) means the program cannot find match in given reference populations.

example:
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,0,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,1,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1
1,1,1,o,1,1,1,1,1,1

