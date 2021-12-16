import binascii
from functools import singledispatchmethod, reduce
from dataclasses import dataclass
from typing import Union
from enum import Enum


class BitView(object):
    def __init__(self, data: bytes):
        self._data = data

    def __getitem__(self, index):
        return self._getitem(index)

    @singledispatchmethod
    def _getitem(self, index: Union[int, slice]):
        raise Exception("Bad argument type")
    
    @_getitem.register
    def _(self, index: int):
        byteIndex = index // 8
        bitIndex = index % 8
        return 1 if self._data[byteIndex] & (1 << (7 - bitIndex)) else 0

    @_getitem.register
    def _(self, index: slice):
        res = 0
        for i in range(index.start or 0, index.stop or len(self), index.step or 1):
            res = (res << 1) | self._getitem(i)
        
        return res

    def __len__(self):
        return len(self._data) * 8


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    LITERAL = 4
    MAX = 3
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL = 7


def parse_literal(view: BitView, idx: int, version: int):
    data = 0
    section = view[idx: idx+5]
    idx += 5
    while section & (1 << 4):
        data = (data << 4) | (section & 0xf)
        section = view[idx: idx + 5]
        idx += 5
    data = (data << 4) | (section & 0xf)

    packet = {
            "type": PacketType.LITERAL,
            "version": version,
            "value": data
        }
    return (packet, idx)


def parse_operator(view: BitView, idx: int, version: int, opType: int):
    subPackets = []
    if view[idx] == 1:
        idx += 1
        noSubPackets = view[idx:idx+11]
        idx += 11

        for i in range(noSubPackets):
            packet, idx = parse_packet(view, idx)
            subPackets.append(packet)

    else:
        idx += 1
        subPacketLength = view[idx:idx + 15]
        idx += 15
        end = idx + subPacketLength
        while idx < end:
            packet, idx = parse_packet(view, idx)
            subPackets.append(packet)
    return {
            "type": PacketType(opType),
            "version": version,
            "packets": subPackets
        }, idx

def parse_packet(view: BitView, startIdx: int):
    idx = startIdx
    version = view[idx:idx+3]
    idx += 3
    packetType = view[idx: idx+3]
    idx += 3

    if packetType == 4:
        return parse_literal(view, idx, version)
    else:
        return parse_operator(view, idx, version, packetType)

def find_version_sum(packet):
    if packet["type"] == PacketType.LITERAL:
        return packet["version"]
    else:
        return packet["version"] + sum(find_version_sum(packet) for packet in packet["packets"])


PACKET_EVAL_FNS = {
    PacketType.LITERAL: lambda packet: packet["value"],
    PacketType.SUM: lambda packet: sum(eval_packet(subPack) for subPack in packet["packets"]),
    PacketType.PRODUCT: lambda packet: reduce(lambda acc, v: acc * v, map(eval_packet, packet["packets"]), 1),
    PacketType.MIN: lambda packet: min(eval_packet(subPack) for subPack in packet["packets"]),
    PacketType.MAX: lambda packet: max(eval_packet(subPack) for subPack in packet["packets"]),
    PacketType.LESS_THAN: lambda packet: 1 if eval_packet(packet["packets"][0]) < eval_packet(packet["packets"][1]) else 0,
    PacketType.GREATER_THAN: lambda packet: 1 if eval_packet(packet["packets"][0]) > eval_packet(packet["packets"][1]) else 0,
    PacketType.EQUAL: lambda packet: 1 if eval_packet(packet["packets"][0]) == eval_packet(packet["packets"][1]) else 0,
}


def eval_packet(packet):
    return PACKET_EVAL_FNS[packet["type"]](packet)


with open("../input", "r") as f:
    data = f.readline().strip()

data = binascii.unhexlify(data)

view = BitView(data)

packet, _ = parse_packet(view, 0)

print(find_version_sum(packet))
print(eval_packet(packet))
