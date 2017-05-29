# All SSH libraries for Python are junk (2011-10-13).
# Too low-level (libssh2), too buggy (paramiko), too complicated
# (both), too poor in features (no use of the agent, for instance)

# Here is the right solution today:

import subprocess
import sys
import paramiko

USER = 'usuario'
HOST = "alu0100699968.iaas.ull.es"
# Ports are handled in ~/.ssh/config since we use OpenSSH
COMMAND = 'cd /home/usuario/stanford-corenlp-full-2016-10-31/ && java -Xmx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -serverProperties StanfordCoreNLP-%s.properties -port %s -timeout 15000 &'
COMMAND_EN = 'cd /home/usuario/stanford-corenlp-full-2016-10-31/ && java -mx2048m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port %s -timeout 15000 &'


def launch_corenlp(lang, port):
    '''print ("%s@%s" % (USER, HOST))
    if lang:
        ssh = subprocess.Popen(["ssh", "%s@%s" % (USER, HOST), COMMAND % (lang, port)],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    else:
        ssh = subprocess.Popen(["ssh", "%s@%s" % (USER, HOST), COMMAND_EN % port],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print >> sys.stderr, "ERROR: %s" % error
    else:
        print result'''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password='')
    if lang:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(COMMAND % (lang, port))
    else:
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(COMMAND_EN % port)
