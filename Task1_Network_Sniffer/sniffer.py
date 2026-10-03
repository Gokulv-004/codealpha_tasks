#!/usr/bin/env python3
from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw

def process_packet(packet):
    print("\n" + "=" * 60)

    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        proto_num = packet[IP].proto

        # Identify protocol
        if proto_num == 6:
            proto = "TCP"
        elif proto_num == 17:
            proto = "UDP"
        elif proto_num == 1:
            proto = "ICMP"
        else:
            proto = f"Other ({proto_num})"

        print(f"Source IP      : {src}")
        print(f"Destination IP : {dst}")
        print(f"Protocol       : {proto}")

        # Show ports for TCP/UDP
        if TCP in packet:
            print(f"Source Port    : {packet[TCP].sport}")
            print(f"Dest Port      : {packet[TCP].dport}")
        elif UDP in packet:
            print(f"Source Port    : {packet[UDP].sport}")
            print(f"Dest Port      : {packet[UDP].dport}")

        # Show payload if present
        if Raw in packet:
            payload = packet[Raw].load
            try:
                print(f"Payload        : {payload.decode('utf-8', errors='ignore')[:100]}")
            except Exception:
                print(f"Payload (raw)  : {payload[:50]}")

def main():
    print("Starting Network Sniffer on wlan0... Press Ctrl+C to stop.\n")
    sniff(iface="wlan0", prn=process_packet, store=False)

if __name__ == "__main__":
    main()
