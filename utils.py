class Math: 
    @staticmethod 
    def ip_to_number(ip_addy):
            split_numbers = ip_addy.split('.')

            first_octet = int(split_numbers[0]) << 24
            second_octet = int(split_numbers[1]) << 16
            third_octet = int(split_numbers[2]) << 8
            fourth_octet = int(split_numbers[3])

            return first_octet + second_octet + third_octet + fourth_octet

    @staticmethod
    def number_to_ip(ip_number):
        first_octet = (ip_number >> 24) & 0xFF
        second_octet = (ip_number >> 16) & 0xFF
        third_octet = (ip_number >> 8) & 0xFF
        fourth_octet = ip_number & 0xFF

        return "%d.%d.%d.%d" % (first_octet, second_octet, third_octet, fourth_octet)

    @staticmethod
    def prefix_match(target_ip, network_ip, netmask_int):
        network_id = target_ip & netmask_int 
        return network_id == network_ip