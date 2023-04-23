# Installer image
FROM mcr.microsoft.com/windows/servercore:10.0.14300.1030 AS installer

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]


RUN Invoke-WebRequest -OutFile java.zip https://download.oracle.com/otn-pub/java/jdk/13.0.2+8/d4173c853231432d94f001e99d882ca7/jdk-13.0.2_windows-x64_bin.zip;
CMD [ "Expand-Archive", "java.zip", "-DestinationPath java;" ]
       
	