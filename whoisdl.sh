#!/bin/bash -
#===============================================================================
#whoisdl v0.1 - Copyright 2018 James Slaughter,
#This file is part of whoisdl v0.1.

#whoisdl v0.1 is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#whoisdl v0.1 is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with whoisdl v0.1.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================
#------------------------------------------------------------------------------
#
# Execute whoisdl on top of an Ubuntu-based Linux distribution.
#
#------------------------------------------------------------------------------

__ScriptVersion="whoisdl-v0.1-1"
LOGFILE="/home/scalp/whoisdl/whoisdl.log"
WHOISDL_DIR="/home/scalp/whoisdl"
DAY=`date --date="-1 day" +"%Y-%m-%d"`
KEYWORD_FILE="/home/scalp/whoisdl/keywords.txt"

echoerror() {
    printf "${RC} [x] ${EC}: $@\n" 1>&2;
}

echoinfo() {
    printf "${GC} [*] ${EC}: %s\n" "$@";
}

echowarn() {
    printf "${YC} [-] ${EC}: %s\n" "$@";
}

usage() {
    echo "usage"
    exit 1
}

initialize() {
  echoinfo "--------------------------------------------------------------------------------" >> $LOGFILE
  echoinfo "Running whoisdl.sh version $__ScriptVersion on `date`" >> $LOGFILE
  echoinfo "--------------------------------------------------------------------------------" >> $LOGFILE

  echoinfo "---------------------------------------------------------------"
  echoinfo "Running whoisdl.sh version $__ScriptVersion on `date`"
  echoinfo "---------------------------------------------------------------"
}

download_whois_list() {
  #Pull newly registered whois domains from whoisds.com
  echoinfo "Pulling newly registered whois domains from whoisds.com from yesterday..."
  echoinfo "Pulling newly registered whois domains from whoisds.com from yesterday..." >> $LOGFILE
  wget -q "https://whoisds.com/whois-database/newly-registered-domains/$DAY.zip/nrd" --output-document "/tmp/$DAY.zip"
  ERROR=$?
  unzip -q "/tmp/$DAY.zip" -d "/tmp/" 
  chmod a+w "/tmp/domain-names.txt"
  mkdir "$WHOISDL_DIR/$DAY"
  chmod a+w "$WHOISDL_DIR/$DAY"
  mkdir "$WHOISDL_DIR/$DAY/output/"
  chmod a+w "$WHOISDL_DIR/$DAY/output/"
  mv "/tmp/domain-names.txt" "$WHOISDL_DIR/$DAY/domain-names$DAY.csv"
  rm "/tmp/$DAY.zip"

  echoinfo "Details logged to $LOGFILE."

  if [ $ERROR -ne 0 ]; then
    return 1
  fi

  return 0
}


pipe_to_whoisdl_python() {
 
  #Now that the domain list has been downloaded, pipe to python to do text manipulation
  echoinfo "Piping program execution to Python component..."
  echoinfo "Piping program execution to Python component..." >> $LOGFILE
  echo $(/opt/whoisdl/whoisdl.py --domainlist $WHOISDL_DIR/$DAY/domain-names$DAY.csv --outputdir $WHOISDL_DIR/$DAY/output) >> $LOGFILE
}

zip_package() {
  echoinfo "Zipping output package..."
  echoinfo "Zipping output package..." >> $LOGFILE
  zip -rj domain-namesA$DAY.zip $WHOISDL_DIR/$DAY/*
}

wrap_up() {
  echoinfo "--------------------------------------------------------------------------------" >> $LOGFILE
  echoinfo "Program complete on `date`" >> $LOGFILE
  echoinfo "--------------------------------------------------------------------------------" >> $LOGFILE

  echoinfo "---------------------------------------------------------------"
  echoinfo "Program complete on `date`"
  echoinfo "---------------------------------------------------------------"
}

#Function calls
initialize
download_whois_list
pipe_to_whoisdl_python
#zip_package
wrap_up
