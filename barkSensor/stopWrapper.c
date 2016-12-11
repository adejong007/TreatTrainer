  #include <stdlib.h>
  #include <sys/types.h>
  #include <unistd.h>
  #include <iostream>
  #include <fstream>

  int main (int argc, char *argv[])
  {
     setuid (0);

     /* WARNING: Only use an absolute path to the script to execute,
      *          a malicious user might fool the binary and execute
      *          arbitary commands if not.
      * */

    std::ofstream messages;
    messages.open("/var/www/html/messages.sh");
    messages << "barkstop=True"<<std::endl;

     return 0;
   }
