# Operating_Systems_II
Creating an Intrusion Detection System

------Obtaining the KDD Preprocessor----

Please use the installation script to build the pre-processor when the respository is cloned.

The repository can be found at:
https://github.com/AI-IDS/kdd99_feature_extractor

----------------------------------------

Source Location for Java Wireshark compatibility:
https://sourceforge.net/projects/jnetpcap/postdownload

You should be able to import the Java code to use the file. However you need the jnetpcap.dll to be installed in the right directory. Please see the release notes below.

---------------Taken from JNetPcap Installation---------
== Installation Instructions ==

To install the library unzip the binary platform-dependent package into any
directory, or install the RPM package on unix based systems into its default
directories. There are 2 parts to setting up environment for jNetPcap.

  *) Win32 Dependency: jNetPcap requires WinPcap 3.1 or greater installed. 
                       WinPcap version 4.0.1 or greater is recommended, but not 
                       neccessary. (http://winpcap.org)
                       
  *) FC notes: main files of interest from linux RPM package are installed 
                  in the following locations:
  
     - /usr/lib/libjnetpcap.so
     - /usr/share/java/jnetpcap-1.3.a1.jar 
     - /usr/share/doc/jnetpcap-1.3.a1 = contains RELEASE notes and javadocs

  *) Debian notes: main files of interest from linux deb package are installed 
                  in the following locations:
  
     - /usr/lib/libjnetpcap.so
     - /usr/share/java/jnetpcap-1.3.a1.jar 
     - /usr/share/doc/jnetpcap-1.3.a1 = contains RELEASE notes and javadocs

  1) Add supplied jnetpcap-version.jar file to your build system's CLASSPATH.
     The jar file is found at the root of the installation directory in zip 
     files and in /usr/share/java on linux systems.
  
  2) Setup native jnetpcap dynamically loadable library. This varies between
     operating systems.
     
     * On Win32 systems do only one of the following
     
       - copy the jnetpcap.dll library file, found at root of jnetpcap's
         installation directory to one of the window's system folders. This
         could be \windows or \windows\system32 directory.
         
       - add the jNetPcap's installation directory to system PATH variable. This
         is the same variable used access executables and scripts.
         
       - Tell Java VM at startup exactly where to find jnetpcap.dll by setting
         a java system property 'java.library.path' such as:
           c:\> java -Djava.library.path=%JNETPCAP_HOME%
           
       - You can change working directory into the root of jnetpcap's 
         installation directory.
         
     * On unix based systems, use one of the following
       - add /usr/lib directory to LD_LIBRARY_PATH variable as java JRE does not
         look in this directory by default
       
       - Tell Java VM at startup exactly where to find jnetpcap.dll by setting
         a java system property 'java.library.path' such as:
           shell > java -Djava.library.path=$JNETPCAP_HOME
           
       - You can change working directory into the root of jnetpcap's 
         installation directory.
         
     * For further trouble shooting information, please see the following link:
       (http://jnetpcap.wiki.sourceforge.net/Troubleshooting+native+library)