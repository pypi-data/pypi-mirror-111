import os
import time
import json
import sys

logerObj = {}


def mkdir(path):
    if not os.path.isdir(os.path.dirname(path)):
        mkdir(os.path.dirname(path))
    if not os.path.isdir(path):
        os.mkdir(path)


class loger():
    __startAt = None
    __taskId = None
    # ��־��ŵ�·��
    __logPath = None
    # ��ʱ��־
    __tmpPath = None
    # ��ʵ��־���·��
    __reaLogPath = None
    # �ָ����
    __SEPARATOR = "<=========>"
    # ���÷���ֵ���·��
    __realResultPath = None

    def __init__(self, taskId):
        self.__taskId = taskId
        self.__logPath = sys.path[0] + "/runtime" + "/" + taskId + "/"
        mkdir(self.__logPath)
        self.__tmpPath = self.__logPath + "tmp.log"
        self.__reaLogPath = self.__logPath + "runtime.log"
        self.__reaLogPath = self.__logPath + "runtime.log"
        self.__realResultPath = self.__logPath + "result.log"
        # ����ϴε��õĽ�� ��������´˽�� �����ӽڵ�ش������Ľڵ�
        if os.path.isfile(self.__realResultPath):
            os.unlink(self.__realResultPath)
        self.flushTmpLog()

    # �����ʱ���� д��������־
    def flushTmpLog(self):
        if os.path.isfile(self.__tmpPath):
            logString = open(self.__tmpPath, encoding="utf-8").read()
            logString = logString + self.__SEPARATOR
            with open(self.__reaLogPath, "a") as f:
                f.write(logString + '\n')
            os.unlink(self.__tmpPath)

    # д����־
    def write(self, content):
        with open(self.__tmpPath, 'a') as f:
            f.write(content + "\n")
        return self

    # ������ֵд�뵽�ļ���
    def writeRes(self, content):
        with open(self.__realResultPath, "w") as f:
            f.write(json.dumps(content))
        return self

    @staticmethod
    def instance(taskId):
        if (taskId in logerObj.keys()):
            return logerObj[taskId]
        obj = loger(taskId)
        logerObj[taskId] = obj
        return obj
