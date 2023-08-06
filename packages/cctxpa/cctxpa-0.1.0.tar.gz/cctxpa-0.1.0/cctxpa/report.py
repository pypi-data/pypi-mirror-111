import hashlib

from dpkt import ethernet, ip, ip6
from dpkt.utils import inet_to_str
from .pcap_extractor.mail import Mail
from .pcap_extractor.TCPFlow import TCPFlow
from .pcap_extractor.DNSExtractor import DNSItem
from .pcap_extractor.HTTPParser import HttpData
from abc import ABCMeta, abstractmethod


class DictSerializable(object):
    """
    可序列化为字典的类的基类 => 继承本抽象类的类拥有序列化成字典的能力
    """
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    @abstractmethod
    def toDict(self) -> dict:
        pass


class TCPMixin(DictSerializable):
    """
    TCP记录，所有继承本类的记录都拥有记录TCP属性的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.srcPort = 0
        self.dstIP = ""
        self.dstPort = 0

    def setTCP(self, tcpFlow: TCPFlow):
        self.srcIP = tcpFlow.srcIP
        self.srcPort = tcpFlow.srcPort
        self.dstIP = tcpFlow.dstIP
        self.dstPort = tcpFlow.dstPort

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "srcPort": self.srcPort,
            "dstIP": self.dstIP,
            "dstPort": self.dstPort
        }


class IPMixin(DictSerializable):
    """
    IP记录，所有继承本类的记录都拥有记录IP地址的功能
    """

    def __init__(self):
        self.srcIP = ""
        self.dstIP = ""

    def setIP(self, ethPacket: ethernet.Ethernet):
        ipPacket = ethPacket.data
        self.srcIP = inet_to_str(ipPacket.src)
        self.dstIP = inet_to_str(ipPacket.dst)

    def toDict(self) -> dict:
        return {
            "srcIP": self.srcIP,
            "dstIP": self.dstIP
        }


class RecordBase(DictSerializable):
    """
    所有报告记录的基类
    """

    class ObservableItem(DictSerializable):
        def __init__(self, observableId: str, observableType: str):
            self.observableId = observableId
            self.observableType = observableType

        def toDict(self) -> dict:
            return {
                "observableId": self.observableId,
                "observableType": self.observableType
            }

    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    def __init__(self):
        self.observables = []

    def setObservables(self, observables: [ObservableItem]):
        self.observables = observables

    def toDict(self) -> dict:
        res = []
        for observable in self.observables:
            res.append(observable.toDict())
        return {
            "observables": res
        }


class FileHash(DictSerializable):
    """
    表示文件Hash值
    """

    def __init__(self, data: bytes):
        self.md5 = hashlib.md5(data).hexdigest()
        self.sha1 = hashlib.sha1(data).hexdigest()
        self.sha256 = hashlib.sha256(data).hexdigest()

    def toDict(self) -> dict:
        return {
            "md5": self.md5,
            "sha1": self.sha1,
            "sha256": self.sha256
        }


class FileItem(DictSerializable):
    """
    文件条目
    """

    def __init__(self, fileData: bytes, filename: str = "", fileType: str = ""):
        self.filename = filename,
        self.fileType = fileType,
        self.fileHash = FileHash(fileData)

    def toDict(self) -> dict:
        return {
            "filename": self.filename,
            "fileType": self.fileType,
            "fileHash": self.fileHash.toDict()
        }


class EmailRecord(RecordBase, TCPMixin):
    """
    Email记录
    """

    def __init__(self):
        super().__init__()
        self.plain = ""  # 消息内容
        self.html = ""  # html格式的内容
        self.From = ""  # 发件人地址
        self.To = ""  # 收件人地址
        self.Cc = ""  # 抄送地址
        # self.Date = ""  # 日期和时间
        self.Subject = ""  # 主题
        self.MessageID = ""  # 消息ID
        self.files = []

    def initByMailAndObservable(self, mail: Mail):
        self.plain = mail.plain
        if isinstance(self.plain, bytes):
            self.plain = self.plain.decode()
        self.html = mail.html
        self.From = mail.From
        self.To = mail.To
        self.Cc = mail.Cc
        # self.Date = mail.Date
        self.Subject = mail.Subject
        self.MessageID = mail.MessageID
        for mailFile in mail.files:
            self.files.append(FileItem(mailFile.fileData, mailFile.fileName, mailFile.fileType))

    def toDict(self) -> dict:
        filesDict = []
        for file in self.files:
            filesDict.append(file.toDict())
        return {
            "plain": self.plain,
            "html": self.html,
            "from": self.From,
            "to": self.To,
            "cc": self.Cc,
            # "date": self.Date,
            "subject": self.Subject,
            "messageId": self.MessageID,
            "files": filesDict,
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class DNSRecord(RecordBase, IPMixin):
    """
    DNS解析记录
    """

    def __init__(self):
        super().__init__()
        self.domain = ""
        self.domain_type = ""
        self.value = ""
        self.timestamp = 0

    def initByDNSItem(self, item: DNSItem):
        self.domain = item.domain
        self.domain_type = item.domain_type
        self.value = item.value
        self.timestamp = item.timestamp
        self.setIP(item.ethPacket)

    def toDict(self) -> dict:
        return {
            "domain": self.domain,
            "domain_type": self.domain_type,
            "value": self.value,
            "timestamp": self.timestamp,
            **RecordBase.toDict(self),
            **IPMixin.toDict(self)
        }


class HTTPRecord(RecordBase, TCPMixin):
    """
    HTTP记录
    """

    class HttpRequest(DictSerializable):
        """
        HTTP请求记录
        """

        def __init__(self, httpData: HttpData):
            self.uri = httpData.request.uri
            self.method = httpData.request.method
            self.headers = httpData.request.headers
            self.version = httpData.request.version
            self.domain = httpData.getDomain()
            self.url = httpData.getUrl()

        def toDict(self) -> dict:
            return {
                "uri": self.uri,
                "method": self.method,
                "headers": self.headers,
                "version": self.version,
                "domain": self.domain,
                "url": self.url
            }

    class HttpResponse(DictSerializable):
        """
        HTTP响应记录
        """

        def __init__(self, httpData: HttpData):
            self.status = httpData.response.status
            self.reason = httpData.response.reason
            self.body = httpData.response.body
            self.headers = httpData.response.headers
            self.version = httpData.response.version

        def toDict(self) -> dict:
            return {
                "status": self.status,
                "reason": self.reason,
                # "body": self.body,
                "headers": self.headers,
                "version": self.version
            }

    def __init__(self, httpData: HttpData):
        super().__init__()
        self.request = HTTPRecord.HttpRequest(httpData)
        self.response = HTTPRecord.HttpResponse(httpData)

    def toDict(self) -> dict:
        return {
            "request": self.request.toDict(),
            "response": self.response.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class FTPRecord(RecordBase, TCPMixin):
    """
    FTP 记录
    """

    def __init__(self, data: bytes):
        super().__init__()
        self.fileHash = FileHash(data)

    def toDict(self) -> dict:
        return {
            "fileHash": self.fileHash.toDict(),
            **RecordBase.toDict(self),
            **TCPMixin.toDict(self)
        }


class Report(DictSerializable):
    """
    对比报告
    """

    def toDict(self) -> dict:
        emailRecordsDict = []
        ftpRecordsDict = []
        httpRecordsDict = []
        domainRecordsDict = []
        for emailRecord in self.emailRecords:
            emailRecordsDict.append(emailRecord.toDict())
        for ftpRecord in self.ftpRecords:
            ftpRecordsDict.append(ftpRecord.toDict())
        for httpRecord in self.httpRecords:
            httpRecordsDict.append(httpRecord.toDict())
        for domainRecord in self.domainRecords:
            domainRecordsDict.append(domainRecord.toDict())
        return {
            "totalPacket": self.totalPacket,
            "totalIPAddress": self.totalIPAddress,
            "totalIPv6Address": self.totalIPv6Address,
            "totalIPPacket": self.totalIPPacket,
            "totalIPv6Packet": self.totalIPv6Packet,
            "duration": self.duration,
            "totalTCPFlowNum": self.totalTCPFlowNum,
            "totalHTTPNum": self.totalHTTPNum,
            "totalFTPNum": self.totalFTPNum,
            "totalEmailNum": self.totalEmailNum,
            "totalFileNum": self.totalFileNum,
            "totalDomainNum": self.totalDomainNum,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "emailRecords": emailRecordsDict,
            "ftpRecords": ftpRecordsDict,
            "httpRecords": httpRecordsDict,
            "domainRecords": domainRecordsDict
        }

    def __init__(self):
        self.totalPacket = 0  # Total packet num in pcap file
        self.totalIPAddress = 0  # Total ipv4 address num in pcap file
        self.totalIPv6Address = 0  # Total ipv6 address num in pcap file
        self.totalIPPacket = 0  # Total ipv4 packet num in pcap file
        self.totalIPv6Packet = 0  # Total ipv6 pcaket num in pcap file
        self.duration = 0  # The duration between the begin of pcap file and end of pcap file
        self.totalTCPFlowNum = 0  # Total TCP flow num in pcap file
        self.totalHTTPNum = 0  # Total HTTP session num in pcap file
        self.totalFTPNum = 0  # Total FTP session num in pcap file
        self.totalEmailNum = 0  # Total email num in pcap file，contain SMTP、POP3 and IMAP protocol
        self.totalFileNum = 0  # Total file num extract from pcap file, from FTP、SMTP、POP3 、IMAP and HTTP
        self.totalDomainNum = 0  # Total domain num extract from DNS query and DNS response）

        self.emailRecords = []  # contain all email which some observable match it
        self.ftpRecords = []  # contain all FTP session which some observable match it
        self.httpRecords = []  # contain all HTTP session which some observable match it
        self.domainRecords = []  # contain all Domain query record which some observable match it

        self.isFirst = True
        self.ipv4AddressSet = set()
        self.ipv6AddressSet = set()
        self.startTime = 0
        self.endTime = 0

    def addPacket(self, ethPacket: ethernet.Ethernet, timestamp: float):
        """
        每解析到一个以太网包，
        :return:
        """
        if self.isFirst:
            self.startTime = timestamp
            self.isFirst = False
        self.endTime = timestamp
        self.duration = self.endTime - self.startTime

        self.totalPacket += 1
        ipPacket = ethPacket.data
        if isinstance(ethPacket.data, ip.IP):
            # 如果是 IPv4 包
            self.totalIPPacket += 1
            self.ipv4AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv4AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPAddress = len(self.ipv4AddressSet)
        elif isinstance(ethPacket.data, ip6.IP6):
            self.totalIPv6Packet += 1
            self.ipv6AddressSet.add(inet_to_str(ipPacket.src))
            self.ipv6AddressSet.add(inet_to_str(ipPacket.dst))
            self.totalIPv6Address = len(self.ipv6AddressSet)
        else:
            return False

    def addTCPFlow(self, tcpFlow: TCPFlow):
        """
        每解析到一个 TCP 流就调用本回调
        :param tcpFlow:
        :return:
        """
        self.totalTCPFlowNum += 1

    def addEmail(self, mail: Mail, tcpFlow: TCPFlow, observables: [RecordBase.ObservableItem]):
        """
        每解析到一个 Email，就调用本方法
        :param observables:
        :param mail:
        :param tcpFlow:
        :return:
        """
        self.totalEmailNum += 1
        self.totalFileNum += len(mail.files)
        emailRecord = EmailRecord()
        emailRecord.initByMailAndObservable(mail)
        emailRecord.setTCP(tcpFlow)
        emailRecord.setObservables(observables)
        self.emailRecords.append(emailRecord)

    def addDNSRecord(self, item: DNSItem, observables: [RecordBase.ObservableItem]):
        """
        每解析到一个 DNSRecord，就调动本方法
        :param observables:
        :param item:
        :return:
        """
        self.totalDomainNum += 1
        dnsRecord = DNSRecord()
        dnsRecord.initByDNSItem(item)
        dnsRecord.setObservables(observables)
        self.domainRecords.append(dnsRecord)

    def addHttp(self, httpData: HttpData, tcpFlow: TCPFlow, observables: [RecordBase.ObservableItem]):
        """
        每解析到一个 HttpData，就调用本方法
        :param observables:
        :param httpData:
        :param tcpFlow:
        :return:
        """
        self.totalHTTPNum += 1
        httpRecord = HTTPRecord(httpData)
        httpRecord.setTCP(tcpFlow)
        httpRecord.setObservables(observables)
        self.httpRecords.append(httpRecord)

    def addFTP(self, data: bytes, tcpFlow: TCPFlow, observables: [RecordBase.ObservableItem]):
        """
        每解析到一个 FTP 文件，就调用本方法
        :param observables:
        :param data:
        :param tcpFlow:
        :return:
        """
        self.totalFTPNum += 1
        ftpRecord = FTPRecord(data)
        ftpRecord.setTCP(tcpFlow)
        ftpRecord.setObservables(observables)
        self.ftpRecords.append(ftpRecord)
