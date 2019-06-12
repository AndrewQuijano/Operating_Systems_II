package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

import nids.kddpreprocessor.enums.conversation_state_t;

import static nids.kddpreprocessor.Net.ip_field_protocol_t.*;

public class Conversation
{

//----------------Conversation.cpp-------------------------------------
	// Array for mapping service_t to string (char *)
	// ! Update with enum service_t (in Conversation.h)
	public static String SERVICE_NAMES [] = {
		// General
		"other",
		"private",

		// ICMP
		"ecr_i",
		"urp_i",
		"urh_i",
		"red_i",
		"eco_i",
		"tim_i",
		"oth_i",

		// UDP
		"domain_u",
		"tftp_u",
		"ntp_u",

		// TCP
		"IRC",
		"X11",
		"Z39_50",
		"aol",
		"auth",
		"bgp",
		"courier",
		"csnet_ns",
		"ctf",
		"daytime",
		"discard",
		"domain",
		"echo",
		"efs",
		"exec",
		"finger",
		"ftp",
		"ftp_data",
		"gopher",
		"harvest",
		"hostnames",
		"http",
		"http_2784",
		"http_443",
		"http_8001",
		"icmp",
		"imap4",
		"iso_tsap",
		"klogin",
		"kshell",
		"ldap",
		"link",
		"login",
		"mtp",
		"name",
		"netbios_dgm",
		"netbios_ns",
		"netbios_ssn",
		"netstat",
		"nnsp",
		"nntp",
		"pm_dump",
		"pop_2",
		"pop_3",
		"printer",
		"remote_job",
		"rje",
		"shell",
		"smtp",
		"sql_net",
		"ssh",
		"sunrpc",
		"supdup",
		"systat",
		"telnet",
		"time",
		"uucp",
		"uucp_path",
		"vmnet",
		"whois"
	};
	public static int NUMBER_OF_SERVICES = SERVICE_NAMES.length;
	private FiveTuple five_tuple;

	private Timestamp last_ts;
	private Timestamp start_ts;
	
	private int src_bytes;
	private int dst_bytes;
	private int packets;
	private int src_packets;
	private int dst_packets;
	private int wrong_fragments;
	private int urgent_packets;
	private conversation_state_t state;
	
	public Conversation(FiveTuple f, Timestamp _start_ts, Timestamp _last_ts)
	{
		five_tuple = f;
		start_ts = _start_ts;
		last_ts = _last_ts;
		state = conversation_state_t.INIT;
		src_bytes = 0;
		dst_bytes = 0;
		packets = 0;
		src_packets = 0;
		dst_packets = 0;
		wrong_fragments = 0;
		urgent_packets = 0;
	}

	public Conversation(Packet packet, Timestamp _start_ts, Timestamp _last_ts)
	{
		five_tuple = packet.get_five_tuple();
		start_ts = _start_ts;
		last_ts = _last_ts;
		state = conversation_state_t.INIT;
		src_bytes = 0;
		dst_bytes = 0;
		packets = 0;
		src_packets = 0;
		dst_packets = 0;
		wrong_fragments = 0;
		urgent_packets = 0;
	}

	public FiveTuple get_five_tuple()
	{
		return five_tuple;
	}

	public conversation_state_t get_internal_state()
	{
		return state;
	}

	public conversation_state_t get_state()
	{
		// Replace internal states
		switch (state) 
		{
			case ESTAB:
				return conversation_state_t.S1;

			case S4:
				return conversation_state_t.OTH;

			case S2F:
				return conversation_state_t.S2;

			case S3F:
				return conversation_state_t.S3;

			default:
				return state;
		}
	}

	boolean is_in_final_state()
	{
		// By default conversation will not end by state transition.
		// TCP subclass will by the special case that will override this.
		return false;
	}

	Timestamp get_start_ts()
	{
		return start_ts;
	}

	Timestamp get_last_ts()
	{
		return last_ts;
	}

	int get_duration_ms()
	{
		return (last_ts - start_ts).get_total_msecs();
	}

	int get_src_bytes()
	{
		return src_bytes;
	}

	int get_dst_bytes()
	{
		return dst_bytes;
	}

	int get_packets()
	{
		return packets;
	}

	int get_src_packets()
	{
		return src_packets;
	}

	int get_dst_packets()
	{
		return dst_packets;
	}

	int get_wrong_fragments()
	{
		return wrong_fragments;
	}

	int get_urgent_packets()
	{
		return urgent_packets;
	}

	String get_service_str()
	{
		// Ensure size of strins matches number of values for enum at compilation time
		/*
#ifdef static_assert
		static_assert(sizeof(Conversation::SERVICE_NAMES) / sizeof(char *) == NUMBER_OF_SERVICES,
			"Mapping of services to strings failed: number of string does not match number of values");
#endif
		*/
		return SERVICE_NAMES[get_service()];
	}

	String get_protocol_type_str()
	{
		switch (five_tuple.get_ip_proto()) 
		{
			case TCP:
				return "tcp";
			case UDP:
				return "udp";
			case ICMP:
				return "icmp";
			default:
				break;
		}
		return "UNKNOWN";
	}

	boolean land()
	{
		return five_tuple.land();
	}

	boolean is_serror()
	{
		switch (get_state())
		{
			case S0:
			case S1:
			case S2:
			case S3:
				return true;
			default:
				break;
		}
		return false;
	}

	boolean is_rerror()
	{
		return (get_state() == conversation_state_t.REJ);
	}

	boolean add_packet(Packet packet)
	{
		// Timestamps
		if (packets == 0)
		{
			start_ts = packet.get_start_ts();
		}
		last_ts = packet.get_end_ts();

		// Add byte counts for correct direction
		if (packet.get_src_ip() == five_tuple.get_src_ip()) 
		{
			src_bytes += packet.get_length();
			src_packets++;
		}
		else 
		{
			dst_bytes += packet.get_length();
			dst_packets++;
		}

		// Packet counts
		// TODO: wrong_fragments
		packets++;
		if (packet.get_tcp_flags().urg())
		{
			urgent_packets++;
		}

		// Make state transitions according to packet
		update_state(packet);

		return is_in_final_state();
	}

	void update_state(Packet packet)
	{
		// By default conversation can only get to state SF (after any packet).
		// TCP subclass will by the special case that will override this.
		state = SF;
	}

	String get_state_str()
	{
		return state_to_str(get_state());
	}

	// TODO: use mapping by array fo String s ?
	String state_to_str(conversation_state_t state)
	{
		switch (state) 
		{
		case INIT: 
			return "INIT"; 
		case S0: 
			return "S0"; 
		case S1: 
			return "S1"; 
		case S2: 
			return "S2"; 
		case S3: 
			return "S3"; 
		case SF: 
			return "SF"; 
		case REJ: 
			return "REJ"; 
		case RSTOS0: 
			return "RSTOS0"; 
		case RSTO: 
			return "RSTO"; 
		case RSTR: 
			return "RSTR"; 
		case SH: 
			return "SH"; 
		case RSTRH: 
			return "RSTRH"; 
		case SHR: 
			return "SHR"; 
		case OTH: 
			return "OTH"; 
		case ESTAB: 
			return "ESTAB"; 
		case S4: 
			return "S4"; 
		case S2F: 
			return "S2F"; 
		case S3F: 
			return "S3F"; 
		default: 
			break;
		}
		return "UNKNOWN";
	}
	
	boolean less(Conversation other)
	{
		return (this.get_last_ts() < other.get_last_ts());
	}
}
