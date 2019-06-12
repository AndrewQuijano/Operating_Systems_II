package nids.kddpreprocessor;

// Net.h
/*
 * Ethernet type/length field
 */
public enum eth_field_type_t  
{
	TYPE_ZERO(0),
	MIN_ETH2(0x600),
	IPV4(0x800);
	private int value;

	private eth_field_type_t(int value) 
	{
		this.value = value;
	}
};

/*
 * ICMP type field
 * Values from linux source code used
 * https://github.com/torvalds/linux/blob/master/include/uapi/linux/icmp.h
 */
public enum icmp_field_type_t
{
	ECHOREPLY(0),
	DEST_UNREACH(3),
	SOURCE_QUENCH(4),
	REDIRECT(5),
	ECHO(8),
	TIME_EXCEEDED(11),
	PARAMETERPROB(12),
	TIMESTAMP(13),
	TIMESTAMPREPLY(14),
	INFO_REQUEST(15),
	INFO_REPLY(16),
	ADDRESS(17),
	ADDRESSREPLY(18);
	private int value;

	private icmp_field_type_t(int value) 
	{
		this.value = value;
	}
};

/*
 * IP protocol field
 */
enum ip_field_protocol_t
{
	PROTO_ZERO(0), ICMP(1), TCP(6), UDP(17);
	private int value;

	private ip_field_protocol_t(int value) 
	{
		this.value = value;
	}
};

public class Net 
{
	/*
	 * Ethernet header
	 */
	public ether_header_t ()
	{
		int dst_addr[] = new int[6];
		int src_addr[] = new int[6];
		eth_field_type_t type_length;

		public final static int ETH2_HEADER_LENGTH = 14;
		
		boolean is_ethernet2()
		{
			return (ntohs(type_length) >= MIN_ETH2);
		}

		boolean is_type_ipv4()
		{
			return (ntohs(type_length) == IPV4);
		}

		int get_eth2_sdu()
		{
			return (((uint8_t *) this) + ETH2_HEADER_LENGTH);
		}
	};

	/*
	 * IP header
	 */
	public class ip_header_t
	{
		public ip_header_t()
		{
			
		}
		int ver_ihl;	// 4 bits version and 4 bits internet header length
		int tos;
		int total_length;
		int id;
		int flags_fo;	// 3 bits flags and 13 bits fragment-offset
		int ttl;
		ip_field_protocol_t protocol;
		int checksum;
		int src_addr;
		int dst_addr;

		static final int IP_MIN_HEADER_LENGTH = 20;

		int ihl()
		{
			return (ver_ihl & 0x0F);
		}

		int header_length()
		{
			return ihl() * sizeof(uint32_t);
		}

		int flags()
		{
			return (ntohs(flags_fo) >> 13) & 0x7;
		}

		// Evil bit (reserved)
		boolean flag_eb()
		{
			return ((flags() & 0x1) != 0);
		}
		
		// Do Not Fragment
		boolean flag_df()
		{
			return ((flags() & 0x2) != 0);
		}
		
		// More Fragments
		boolean flag_mf()
		{
			return ((flags() & 0x4) != 0);
		}

		int frag_offset()
		{
			return (ntohs(flags_fo) & 0x01FFF) << 3; // 1 unit = 8 bytes
		}

		String protocol_str()
		{
			switch (protocol)
			{
				case ICMP:
					return "ICMP";
				case TCP:
					return "TCP";
				case UDP:
					return "UDP";
				default:
					break;
			}
			return "other";
		}

		int get_sdu()
		{
			return (((uint8_t *) this) + header_length());
		}
	};

	/*
	 * UDP header 
	 */
	public class udp_header_t
	{
		public udp_header_t()
		{
			
		}
		int src_port;
		int dst_port;
		int length;
		int checksum;
		
		static final int UDP_MIN_HEADER_LENGTH = 8;
	}

	/*
	* TCP flags field
	*/
	public tcp_field_flags_t() 
	{
		uint8_t flags;

		tcp_field_flags_t();
		tcp_field_flags_t(uint8_t flags);
		boolean fin();	
		boolean syn();
		boolean rst();
		boolean psh();
		boolean ack();
		boolean urg();	// Urgent
		boolean ece();	// ECN Echo
		boolean cwr();	// Congestion Window Reduced
		tcp_field_flags_t::tcp_field_flags_t(uint8_t flags)
		: flags(flags)
	{
		
	}

	tcp_field_flags_t::tcp_field_flags_t()
		: flags(0)
	{
		
	}

	boolean tcp_field_flags_t::fin()
	{
		return ((flags & 0x01) != 0);
	}

	boolean tcp_field_flags_t::syn()
	{
		return ((flags & 0x02) != 0);
	}

	boolean tcp_field_flags_t::rst()
	{
		return ((flags & 0x04) != 0);
	}

	boolean tcp_field_flags_t::psh()
	{
		return ((flags & 0x08) != 0);
	}

	boolean tcp_field_flags_t::ack()
	{
		return ((flags & 0x10) != 0);
	}

	boolean tcp_field_flags_t::urg()
	{
		return ((flags & 0x20) != 0);
	}

	boolean tcp_field_flags_t::ece()
	{
		return ((flags & 0x40) != 0);
	}

	boolean tcp_field_flags_t::cwr()
	{
		return ((flags & 0x80) != 0);
	}
	};

	/*
	 * TCP header
	 */
	public tcp_header_t()
	{
		uint16_t src_port;
		uint16_t dst_port;
		uint32_t seq;
		uint32_t ack;
		uint8_t data_offset;  // 4 bits offset + 4 bits reserved
		tcp_field_flags_t flags;
		uint16_t window_size;
		uint16_t checksum;
		uint16_t urgent_p;
		final static int TCP_MIN_HEADER_LENGTH = 20;
	};

	/*
	 * ICMP header
	 */
	public icmp_header_t()
	{
		icmp_field_type_t type;
		int code;
		int checksum;
		static final int ICMP_MIN_HEADER_LENGTH = 8;
	};

	// Net.cpp
}