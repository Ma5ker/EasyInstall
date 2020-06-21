import argparse
import os
import sys
parser = argparse.ArgumentParser()

def parseInit():
    parser.add_argument("-s","--stop", help="stop a container", default=None)
    parser.add_argument("-hn","--hostname", help="the hostname of docker", default=None)
    parser.add_argument("-n","--name", help="the name of docker container", default=None)
    parser.add_argument("-p","--port", help="the port of docker binding to host", default=0,type=int)
    parser.add_argument("-f","--folder",help="the file folder mounted to docker", default=None)



def main():
    parseInit()
    args = parser.parse_args()
    if len(sys.argv)== 1:
        print("Use --help or -h to get help.")
        sys.exit()
    stopcontainer = args.stop
    hostname = args.hostname
    dockername = args.name
    port = args.port
    folder = args.folder

    #停止容器
    if stopcontainer!=None:
        cmd = "docker container stop "+ stopcontainer
        print(cmd)
        os.system(cmd)
        sys.exit()

    cmd = "docker run -d --rm"
    if hostname!=None:
        cmd += " -h "+hostname
    else:
        print("[*]No hostname,will not add it")


    if dockername!= None:
        cmd += " --name "+dockername
    else:
        print("[*]Container name is needed to exec it or you have to attach to it manually.")


    if port!=0:
        cmd += " -p "+str(port)+":"+str(port)
    else:
        print("[*]No port given,will not bind to any port.")


    if folder!=None:
        if  os.path.isdir(folder):
            cmd += " -v "+os.path.realpath(folder)+":/ctf/work"
        else:
            print("[x]File path error,will not copy it into container")
    else:
        print("[x]File path error,will not copy it")

    cmd += " --cap-add=SYS_PTRACE ma5ker/pwndocker"
    print(cmd)
    retcode = os.system(cmd)
    retcode = retcode >> 8
    if retcode!=0:
        print("[x]Creating container error.")
        sys.exit()
    print("[+]Creating container success")
    cmd = "docker exec -it "+dockername+" /bin/bash"
    print(cmd)
    os.system(cmd)

if __name__=="__main__":
    main()

#docker run -d --rm -h ${ctf_name} --name ${ctf_name} -v $(pwd)/${ctf_name}:/ctf/work -p 23946:23946 --cap-add=SYS_PTRACE skysider/pwndocker
#docker exec -it ${ctf_name} /bin/bash