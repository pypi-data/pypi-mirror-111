# -*- coding: utf-8 -*-
"""
Copyright (c) 2015-2021 Stduino.
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file or search www.stduino.com.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""
import subprocess
import os,stat
from function.cores.stdedit import stdinit
from function.conf import res
from function.cores.stdmsg import reso
from shutil import copytree,rmtree,copy2
#调用前先判断是否已经正常安装pio
class PioInstall():
    def __init__(self):
        pass


        #print(self.abs_path)
        #self.pip_fast()

    def pip_fast(self):#all the time
        try:
            if res.msg == "1":  # 中
                target = stdinit.stdenv + "/pip"
                # target="C:/stwork/stdemo2019827/tool/packages/pip2/pip.ini"
                if os.path.exists(target):
                    pass
                else:
                    try:
                        source = stdinit.abs_path + "/tool/packages/pip"
                        # print(source)
                        # target=os.environ["USERPROFILE"] + "/pip/pip.ini"
                        copytree(source, target)
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                    pass
                pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def is_installed_pio(self):#mac 和linux 好像不同
        try:



            target = stdinit.stdenv + "/.stduino/packages/pioenv"  # self.abs_path + "/tool/packages/pioenv/Scripts/pio.exe"
            #print(target)
            if os.path.exists(target):
                return True
            else:
                return False
        except:

            stdinit.std_signal_gobal.stdprintln()


    def is_init_pioenv(self):
        try:
            target = stdinit.stdenv + "/.stduino/packages/pioenv"
            if os.path.exists(target):
                return True
            else:
                return False
        except:
            stdinit.std_signal_gobal.stdprintln()


    def pioenv_init(self):

        try:
            if stdinit.platform_is == "Win":
                cmd = stdinit.abs_path + "/tool/packages/python3/python -m venv " + '"' +stdinit.stdenv + "/.stduino/packages/pioenv"+ '"'

            elif stdinit.platform_is == "Linux":
                cmd = stdinit.abs_path + "/tool/packages/python3/bin/python -m venv " + '"' +stdinit.stdenv + "/.stduino/packages/pioenv"+ '"'

            elif stdinit.platform_is == "Darwin":
                cmd = stdinit.abs_path + "/tool/packages/python3/bin/python -m venv " + '"' + stdinit.stdenv + "/.stduino/packages/pioenv" + '"'

            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            for line in iter(proc.stdout.readline, b''):
                s1 = str(line, encoding='gbk')

                if not subprocess.Popen.poll(proc) is None:
                    if line == "":
                        break
        except:
            stdinit.std_signal_gobal.stdprintln()
    def check_net(self):
        try:
            return stdinit.std_signal_gobal.is_connected()

        except:
            return False


            # if stdinit.platform_is == "Win":
            #     request.urlopen(url="https://www.baidu.com", timeout=3.0)
            #
            #
            # elif stdinit.platform_is == "Linux":
            #     pass
            #
            # elif stdinit.platform_is == "Darwin":
            #     pass

            # print(ret)


    def install_pio(self):
        try:
            if stdinit.platform_is == "Win":
                env_path = '"' + stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip" + '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    s1 = str(line, encoding='gbk')
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/package/manager/_registry.py"
                self.delete_file(regi)
                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py")

            elif stdinit.platform_is == "Linux":
                env_path= '"' +stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip"+ '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    s1 = str(line, encoding='gbk')
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/package/manager/_registry.py"
                self.delete_file(regi)
                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/Lib/site-packages/platformio/ide/ideini.py")

            elif stdinit.platform_is == "Darwin":
                env_path= '"' +stdinit.stdenv + "/.stduino/packages/pioenv/bin/pip"+ '"'
                cmd = env_path + " install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
                for line in iter(proc.stdout.readline, b''):
                    s1 = str(line, encoding='gbk')
                    # print(s1)
                    if not subprocess.Popen.poll(proc) is None:
                        if line == "":
                            break
                proc.stdout.close()  # pioenv\Lib\site-packages\platformio\package\manager
                regi = stdinit.stdenv + "/.stduino/packages/pioenv/lib/python3.8/site-packages/platformio/package/manager/_registry.py"

                self.delete_file(regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdload.py", regi)

                copy2(stdinit.abs_path + "/tool/packages/python3/Scripts/stdini.py",
                      stdinit.stdenv + "/.stduino/packages/pioenv/lib/python3.8/site-packages/platformio/ide/ideini.py")


            # if res.msg == "1":  # 中
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U platformio"
            # else:
            #     cmd = stdinit.stdenv + "/.stduino/packages/pioenv/Scripts/pip install -U platformio"

            copy2(stdinit.abs_path + "/tool/packages/pioboards.json",
                  stdinit.stdenv + "/.stduino/packages/pioenv/pioboards.json")
            copy2(stdinit.abs_path + "/tool/packages/stdpio.ini",
                  stdinit.stdenv + "/.stduino/packages/pioenv/stdpio.ini")


            return True
        except:
            stdinit.std_signal_gobal.stdprintln()





    def pio_install(self):
        try:

            if self.is_installed_pio() == False:

                if self.check_net()==False:
                    return False

                if self.is_init_pioenv() == False:

                    self.pioenv_init()
                    self.install_pio()
                    return True
                else:
                    self.install_pio()
                    return True

            return True
        except:
            stdinit.std_signal_gobal.stdprintln()
            return False

        #self.pip_fast()
        # if os.environ["USERPROFILE"]+"/pip":

        #     pass

    def remove_readonly(self,func, path, _):
        try:
            # "Clear the readonly bit and reattempt the removal"
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except:
            stdinit.std_signal_gobal.stdprintln()


    def delete_file(self,path):
        try:
            if os.path.isdir(path):
                try:
                    rmtree(path, onerror=self.remove_readonly)
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    # self.listwidget.append("Delete error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # self.add_lib_si(python3, 0, "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder")
                    # QMessageBox.warning(self, "Delete error",
                    #                     "Unexpected error:" + "\n 请手动至该文件夹处删除\nPlease manually delete to this folder",
                    #                     QMessageBox.Yes)
                    pass
            else:
                try:
                    os.remove(path)
                except:
                    try:
                        # shutil.rmtree(path, onerror=self.remove_readonly)
                        os.chmod(path, stat.S_IWRITE)
                        os.remove(path)
                    except:
                        stdinit.std_signal_gobal.stdprintln()
                pass
            pass
        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_uninstall(self):
        try:
            if self.is_init_pioenv() == False:
                pass
            else:
                try:
                    self.delete_file(stdinit.stdenv + "/.stduino/packages/pioenv")
                    return True
                except:
                    stdinit.std_signal_gobal.stdprintln()
                    return False

        except:
            stdinit.std_signal_gobal.stdprintln()

    def pio_test(self):
        try:
            print(stdinit.board)
            stdinit.board = "ddds"
        except:
            stdinit.std_signal_gobal.stdprintln()


if __name__ == '__main__':  # main函数
    #PioInstall() langeage 工作目录需在test里进行测试
    pass





