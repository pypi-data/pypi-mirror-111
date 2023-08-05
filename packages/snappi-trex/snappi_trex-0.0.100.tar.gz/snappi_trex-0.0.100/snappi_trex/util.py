class Util:
    """
    This class contains miscellaneous utility functions
    """
    def get_mask(bits):
        """
        returns a mask of 1's of size bits
        """
        result = (1 << bits) - 1
        return result

    
    def uint_to_int(uint, size):
        """
        converts an unsigned int of size n to a signed int of size n
        """
        result = uint & Util.get_mask(size)
        if result >= (1 << (size-1)):
            result -= (1 << size)
        return result


    def convert_to_long(value, layer_type):
        """
        Parses address values into a long int
        args:
            - value: A string or long representing the address
            - layer_type: A string representing the layer type
        """
        if isinstance(value, int): 
            return value

        if layer_type == 'IP':
            elements = value.split('.')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e)
            return result

        if layer_type == 'Ethernet':
            elements = value.split(':')
            result = 0
            for e in elements:
                result = result << 8
                if len(e) == 0:
                    continue
                result += int(e, 16)
            return result

        if layer_type == 'ARP':
            if len(value.split('.')) == 4:
                return Util.convert_to_long(value, 'IP')
            elif len(value.split(':')) == 6:
                return Util.convert_to_long(value, 'Ethernet')
            else:
                raise SyntaxError()
        
        return value

    def get_header_info():
        return {
            "ethernet": {
                "scapy_name": "Ethernet",
                "src": {"field_str": "src", "length": 48, "bit_fixup": 0},
                "dst": {"field_str": "dst", "length": 48, "bit_fixup": 0}
            },
            "ipv4": {
                "scapy_name": "IP",
                "src": {"field_str": "src", "length": 32, "bit_fixup": 0},
                "dst": {"field_str": "dst", "length": 32, "bit_fixup": 0},
                "version": {"field_str": "version", "length": 4, "bit_fixup": 0},
                "header_length": {"field_str": "ihl", "length": 4, "bit_fixup": 0},
                "priority": {"field_str": "tos", "length": 8, "bit_fixup": 0},
                "total_length": {"field_str": "len", "length": 16, "bit_fixup": 0},
                "identification": {"field_str": "id", "length": 16, "bit_fixup": 0},
                "reserved": {"field_str": "flags", "length": 1, "bit_fixup": 0},
                "dont_fragment": {"field_str": "flags", "length": 1, "bit_fixup": 1},
                "more_fragments": {"field_str": "flags", "length": 1, "bit_fixup": 2},
                "fragment_offset": {"field_str": "frag", "length": 13, "bit_fixup": 3},
                "time_to_live": {"field_str": "ttl", "length": 8, "bit_fixup": 0},
                "protocol": {"field_str": "proto", "length": 8, "bit_fixup": 0}
            },
            "udp": {
                "scapy_name": "UDP",
                "src_port": {"field_str": "sport", "length": 16, "bit_fixup": 0},
                "dst_port": {"field_str": "dport", "length": 16, "bit_fixup": 0},
                "length": {"field_str": "len", "length": 16, "bit_fixup": 0}
            },
            "tcp": {
                "scapy_name": "TCP",
                "src_port": {"field_str": "sport", "length": 16, "bit_fixup": 0},
                "dst_port": {"field_str": "dport", "length": 16, "bit_fixup": 0},
                "seq_num": {"field_str": "seq", "length": 32, "bit_fixup": 0},
                "ack_num": {"field_str": "ack", "length": 32, "bit_fixup": 0},
                "data_offset": {"field_str": "dataofs", "length": 4, "bit_fixup": 0},
                "ecn_ns": {"field_str": "flags", "length": 1, "bit_fixup": 7},
                "ecn_cwr": {"field_str": "flags", "length": 1, "bit_fixup": 8},
                "ecn_echo": {"field_str": "flags", "length": 1, "bit_fixup": 9},
                "ctl_urg": {"field_str": "flags", "length": 1, "bit_fixup": 10},
                "ctl_ack": {"field_str": "flags", "length": 1, "bit_fixup": 11},
                "ctl_psh": {"field_str": "flags", "length": 1, "bit_fixup": 12},
                "ctl_rst": {"field_str": "flags", "length": 1, "bit_fixup": 13},
                "ctl_syn": {"field_str": "flags", "length": 1, "bit_fixup": 14},
                "ctl_fin": {"field_str": "flags", "length": 1, "bit_fixup": 15},
                "window": {"field_str": "window", "length": 16, "bit_fixup": 0}
            },
            "arp": {
                "scapy_name": "ARP",
                "hardware_type": {"field_str": "hwtype", "length": 16, "bit_fixup": 0},
                "protocol_type": {"field_str": "ptype", "length": 16, "bit_fixup": 0},
                "hardware_length": {"field_str": "hwlen", "length": 8, "bit_fixup": 0},
                "protocol_length": {"field_str": "plen", "length": 8, "bit_fixup": 0},
                "operation": {"field_str": "op", "length": 16, "bit_fixup": 0},
                "sender_hardware_addr": {"field_str": "hwsrc", "length": 48, "bit_fixup": 0},
                "sender_protocol_addr": {"field_str": "psrc", "length": 32, "bit_fixup": 0},
                "target_hardware_addr": {"field_str": "hwdst", "length": 48, "bit_fixup": 0},
                "target_protocol_addr": {"field_str": "pdst", "length": 32, "bit_fixup": 0}
            },
            "vlan": {
                "scapy_name": "Dot1Q",
                "priority": {"field_str": "prio", "length": 3, "bit_fixup": 0},
                "cfi": {"field_str": "id", "length": 1, "bit_fixup": 3},
                "id": {"field_str": "vlan", "length": 12, "bit_fixup": 4},
                "tpid": {"field_str": "type", "length": 16, "bit_fixup": 0}
            }
        }

    def get_metrics_columns():
        return {
            "frames_tx": "opackets",
            "frames_rx": "ipackets",
            "bytes_tx": "obytes",
            "bytes_rx": "ibytes",
            "frames_tx_rate": "tx_pps",
            "frames_rx_rate": "rx_pps",
            "bytes_tx_rate": "tx_bps",
            "bytes_rx_rate": "rx_bps"
        }