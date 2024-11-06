import sys
import argparse
import requests
from junitparser import JUnitXml, TestCase, TestSuite, Skipped, Error, Element
import os
from os import path
import shutil
import socket
import time

def restartArSim() -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    while not connected:
        try:
            s.connect(('127.0.0.1',4003))
            connected = True
        except Exception as e:
            print (e)
            pass #Do nothing, just try again
    print('Connected to ArSim')
    s.settimeout(2)

    maxRetries = 400
    while True:
        maxRetries -= 1
        if (maxRetries <= 0):
            print('ArSim did not start')
            return False
        try:
            s.send(b'<Status Command="10"/>')
            data = s.recv(1024).decode("utf-8")
            if '<AR status SERVCIE Command="98"/>' in data:
                print('ArSim in service mode')
                break
            time.sleep(0.5)
        except Exception as e:
            print(e)
            pass
    
    s.send(b'<Restart Command="2"/>')
    while True:
        maxRetries -= 1
        if (maxRetries <= 0):
            print('ArSim did not start')
            return False
        try:
            s.send(b'<Status Command="10"/>')
            data = s.recv(1024).decode("utf-8")
            print(data)
            if '<AR status RUN Command="99"/>' in data:
                s.close()
                print('ArSim started')
                return True
            time.sleep(0.5)
        except Exception as e:
            print(e)
            pass

def readTests(port) -> []:
    print('reading the available unit tests')
    resp = requests.get(f'http://127.0.0.1:{port}/WsTest/')
    if (resp.status_code != requests.codes.ok):
        return []
    print('found these tests available')
    availableTests = []
    for test in resp.json()['itemList']:
        availableTests.append(test['device'])
        print(f'{test["device"]} {test["description"]}')
    return availableTests

def cleanTestDir(directory):
    print('cleaning the test results directory')
    contents = [path.join(directory, i) for i in os.listdir(directory)]
    [os.remove(i) if path.isfile(i) or path.islink(i) else shutil.rmtree(i) for i in contents]

class CustomElement(Element):
    _tag = 'system-out'
    @property
    def text(self):
        return self._elem.text

    @text.setter
    def text(self, value: str):
        self._elem.text = value

def runTest(name, output, port) -> bool:
    print(f'running test{name}')
    try:
        resp = requests.get(f'http://127.0.0.1:{port}/WsTest/{name}')
        if (resp.status_code != requests.codes.ok):
            print('invalid response ' + str(resp.status_code))
            return False
    except Exception as e:
        #restartArSim()
        f = JUnitXml()
        s = TestSuite(name)
        c = TestCase("ArSim In Service Mode", name)
        c.result = [Error('ArSim In Service Mode', '')]
        s.failures += 1
        s.add_testcase(c)
        f.add_testsuite(s)
        f.write(path.join(output, f'{name}.xml'))
        return False

    xml = JUnitXml.fromstring(resp.text.replace('encoding="utf-8"', ''))
    results = []
    failed = False
    for suite in xml:
        f = JUnitXml()
        s = TestSuite(suite.name)
        for p in suite.properties():
            s.add_property(p.name, p.value)
            if (p.name == 'TotalAssertsFailures'):
                results.append({suite.name, p.value})
                if (int(p.value) > 0):
                    failed = True
        for ts in suite.testsuites():
            for case in ts:
                #print(f'adding {case}')
                s.add_testcase(case)
                for custom in case.iterchildren(CustomElement):
                    print(custom.text)
            s.tests += s.tests
            s.failures += s.failures
        f.add_testsuite(s)
        if (s.tests > 0):
            f.write(path.join(output, f'{suite.name}.xml'))
    return failed

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='test to run', dest='testName', required=True)
    parser.add_argument('-o', '--output', help='directory to store the results', dest='output', required=False, default='TestResults')
    parser.add_argument('-p', '--port', help='port number that ArSim is running the webserver on', dest='port', required=False, default=80)
    args = parser.parse_args()
    availableTests = readTests(args.port)

    if (path.isdir(f'{args.output}') == False):
        os.mkdir(f'{args.output}')

    cleanTestDir(args.output)
    failedTests = []
    if (args.testName == 'all'):
        for t in availableTests:
            print(f'running test {t}')
            if (runTest(t, args.output, args.port) == True):
                failedTests.append(t)
    elif (args.testName in availableTests):
        if (runTest(args.testName, args.output, args.port) == True):
            failedTests.append(args.testName)

    for t in failedTests:
        print(f'{t} test failed')

    # use the junit command in jenkins to parse the results, so that the results can conditionally fail the build
    #sys.exit(0 if len(failedTests) == 0 else 1)
    return

if __name__ == '__main__':
    main()
