import argparse
import hashlib
import json
import sys
import dpkt

from .pcap_extractor.MyEncoder import MyEncoder
from .pcap_extractor.FlowExtractor import FlowExtractor
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.HTTPParser import HTTPParser
from .pcap_extractor.SMTPParser import SMTPParser
from .pcap_extractor.POP3Parser import POP3Parser
from .pcap_extractor.IMAPParser import IMAPParser
from .pcap_extractor.DNSExtractor import DNSExtractor, DNSItem
from .report import Report
from io import BytesIO
from contextlib import closing


class CCTXPcapAnalyser:
    def __init__(self, args):
        self.host = args.host
        self.path = args.path
        self.port = args.port
        self.https = args.https
        self.username = args.username
        self.password = args.password
        self.inputFile = args.pcapfile
        self.outputFile = args.outputfile
        if self.port == -1:
            # 不指定端口，使用默认的80或者443
            if self.https:
                self.port = 443
            else:
                self.port = 80

        self.flowExtractor = FlowExtractor(valueCallback=self.dealStream)
        self.dnsExtractor = DNSExtractor(valueCallback=self.dealDNSRecord)
        self.httpParser = HTTPParser()
        self.smtpParser = SMTPParser()
        self.pop3Parser = POP3Parser()
        self.imapParser = IMAPParser()

        self.report = Report()

    def dealDNSRecord(self, dnsRecord: DNSItem):
        """
        处理每个提取到的 DNS 解析记录
        :param dnsRecord:
        :return:
        """
        self.report.addDNSRecord(dnsRecord, [])

    def dealStream(self, tcpFlow: TCPFlow):
        """
        处理每个提取到的TCP流
        :param tcpFlow:
        :return:
        """
        self.report.addTCPFlow(tcpFlow)
        forwardBytes, reverseBytes = tcpFlow.getAllForwardBytes(), tcpFlow.getAllReverseBytes()
        if tcpFlow.dstPort == 21:
            pass
        elif tcpFlow.srcPort == 20 or tcpFlow.dstPort == 20:
            # 处理 FTP
            data1, data2 = forwardBytes, reverseBytes
            data = data1 if len(data2) == 0 else data2
            if len(data) > 0:
                # md1 = hashlib.md5()
                # md2 = hashlib.md5()
                # md3 = hashlib.md5()
                # with closing(BytesIO(data)) as data:
                #     for line in data.readlines():
                #         md1.update(line)
                #         if line.endswith(b"\r\n"):
                #             md2.update(line[:-2])
                #             md2.update(b'\r')
                #             md3.update(line[:-2])
                #             md3.update(b'\n')
                self.report.addFTP(data, tcpFlow, [])
        elif tcpFlow.dstPort == 143:
            # 处理 IMAP
            for mail in self.imapParser.parse(forwardBytes, reverseBytes):
                self.report.addEmail(mail, tcpFlow, [])
        elif tcpFlow.dstPort == 110:
            for mail in self.pop3Parser.parse(reverseBytes):
                self.report.addEmail(mail, tcpFlow, [])
        elif tcpFlow.dstPort == 25:
            for mail in self.smtpParser.parse(forwardBytes):
                self.report.addEmail(mail, tcpFlow, [])
        elif (len(forwardBytes) == 0 and len(reverseBytes) > 0) or (len(forwardBytes) > 0 and len(reverseBytes) == 0):
            # try to cal file hash for FTP passive mode
            if len(forwardBytes) == 0 and len(reverseBytes) > 0:
                self.report.addFTP(reverseBytes, tcpFlow, [])
            else:
                self.report.addFTP(forwardBytes, tcpFlow, [])
        else:
            # parse http
            for httpData in self.httpParser.parse(forwardBytes, reverseBytes):
                self.report.addHttp(httpData, tcpFlow, [])

    def start(self):
        """
        Start to parse pcap file
        :return:
        """
        # print(f'{"https" if self.https else "http"}://{self.host}{self.path}')

        # TODO: 参数检查
        with open(self.inputFile, 'rb') as pcap:
            packets = dpkt.pcap.Reader(pcap)
            for ts, buf in packets:
                ethPacket = dpkt.ethernet.Ethernet(buf)
                self.report.addPacket(ethPacket, ts)
                self.flowExtractor.addPacket(ethPacket, ts)
                self.dnsExtractor.addPacket(ethPacket, ts)
            self.flowExtractor.done()


def main():
    """
        cctxpa is a command lien tool for CCTX to parse pcap file and compare with CCTX's Observables
        """
    if len(sys.argv) == 1:
        sys.argv.append('--help')
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default="127.0.0.1", help="CCTX pcap analyser server addresss")
    parser.add_argument('--port', type=int, default=-1, help="CCTX pcap analyser server port")
    parser.add_argument('--https', action='store_true', help="Use https or http")
    parser.add_argument('--path', type=str, default="/api", help="CCTX pcap analyser server login path")
    parser.add_argument('-u', '--username', type=str, required=True, help="Username")
    parser.add_argument('-p', '--password', type=str, required=True, help="Password")
    parser.add_argument('-f', '--pcapfile', type=str, required=True, help="Pcap file need to parse!")
    parser.add_argument('-o', '--outputfile', type=str, default="report.txt", help="A file to store output report")
    args = parser.parse_args()

    cctxpa = CCTXPcapAnalyser(args)
    cctxpa.start()
    print(json.dumps(cctxpa.report.toDict(), ensure_ascii=False, cls=MyEncoder))


if __name__ == '__main__':
    main()
