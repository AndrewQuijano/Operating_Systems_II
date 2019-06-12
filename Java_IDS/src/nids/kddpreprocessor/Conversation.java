package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

public class Conversation
{
	// From Conversation.h
	/**
	 * Conversatiov states 
	 *	- INIT & SF for all protocols except TCP
	 *	- other states specific to TCP
	 * Description from https://www.bro.org/sphinx/scripts/base/protocols/conn/main.bro.html
	 */
	enum conversation_state_t {
		// General states
		INIT,		// Nothing happened yet.
		SF,			// Normal establishment and termination. Note that this is the same 
					// symbol as for state S1. You can tell the two apart because for S1 there
					// will not be any byte counts in the summary, while for SF there will be.

		// TCP specific
		S0,			// Connection attempt seen, no reply.
		S1,			// Connection established, not terminated.
		S2,			// Connection established and close attempt by originator seen (but no reply from responder).
		S3,			// Connection established and close attempt by responder seen (but no reply from originator).
		REJ,		// Connection attempt rejected.
		RSTOS0,		// Originator sent a SYN followed by a RST, we never saw a SYN-ACK from the responder.
		RSTO,		// Connection established, originator aborted (sent a RST).
		RSTR,		// Established, responder aborted.
		SH,			// Originator sent a SYN followed by a FIN, we never saw a SYN ACK from the responder (hence the connection was “half” open).
		RSTRH,		// Responder sent a SYN ACK followed by a RST, we never saw a SYN from the (purported) originator.
		SHR,		// Responder sent a SYN ACK followed by a FIN, we never saw a SYN from the originator.
		OTH,		// No SYN seen, just midstream traffic (a “partial connection” that was not later closed).

		// Internal states (TCP-specific)
		ESTAB,		// Established - ACK send by originator in S1 state; externally represented as S1
		S4,			// SYN ACK seen - State between INIT and (RSTRH or SHR); externally represented as OTH
		S2F,		// FIN send by responder in state S2 - waiting for final ACK; externally represented as S2
		S3F			// FIN send by originator in state S3 - waiting for final ACK; externally represented as S3
	};
	
	/**
	 * Services
	 * ! order & number of services must be the same in string mapping
	 * see Conversation::SERVICE_NAMES[] in Conversation.cpp
	 */
	enum service_t {
		// General
		SRV_OTHER,
		SRV_PRIVATE,

		// ICMP
		SRV_ECR_I,
		SRV_URP_I,
		SRV_URH_I,
		SRV_RED_I,
		SRV_ECO_I,
		SRV_TIM_I,
		SRV_OTH_I,

		// UDP
		SRV_DOMAIN_U,
		SRV_TFTP_U,
		SRV_NTP_U,

		// TCP
		SRV_IRC,
		SRV_X11,
		SRV_Z39_50,
		SRV_AOL,
		SRV_AUTH,
		SRV_BGP,
		SRV_COURIER,
		SRV_CSNET_NS,
		SRV_CTF,
		SRV_DAYTIME,
		SRV_DISCARD,
		SRV_DOMAIN,
		SRV_ECHO,
		SRV_EFS,
		SRV_EXEC,
		SRV_FINGER,
		SRV_FTP,
		SRV_FTP_DATA,
		SRV_GOPHER,
		SRV_HARVEST,
		SRV_HOSTNAMES,
		SRV_HTTP,
		SRV_HTTP_2784,
		SRV_HTTP_443,
		SRV_HTTP_8001,
		SRV_ICMP,
		SRV_IMAP4,
		SRV_ISO_TSAP,
		SRV_KLOGIN,
		SRV_KSHELL,
		SRV_LDAP,
		SRV_LINK,
		SRV_LOGIN,
		SRV_MTP,
		SRV_NAME,
		SRV_NETBIOS_DGM,
		SRV_NETBIOS_NS,
		SRV_NETBIOS_SSN,
		SRV_NETSTAT,
		SRV_NNSP,
		SRV_NNTP,
		SRV_PM_DUMP,
		SRV_POP_2,
		SRV_POP_3,
		SRV_PRINTER,
		SRV_REMOTE_JOB,
		SRV_RJE,
		SRV_SHELL,
		SRV_SMTP,
		SRV_SQL_NET,
		SRV_SSH,
		SRV_SUNRPC,
		SRV_SUPDUP,
		SRV_SYSTAT,
		SRV_TELNET,
		SRV_TIME,
		SRV_UUCP,
		SRV_UUCP_PATH,
		SRV_VMNET,
		SRV_WHOIS,

		// This must be the last 
		NUMBER_OF_SERVICES
	};
	
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
	
	public Conversation(FiveTuple f, start_ts, last_ts)
	{
		five_tuple = f;
		state = conversation_state_t.valueOf("INIT");
		src_bytes = 0;
		dst_bytes = 0;
		packets = 0;
		src_packets = 0;
		dst_packets = 0;
		wrong_fragments = 0;
		urgent_packets = 0;
	}

	public Conversation(FiveTuple tuple)
		: five_tuple(*tuple), 
		, start_ts(), last_ts()

	{
		state = conversation_state_t.valueOf("INIT");
		src_bytes = 0;
		dst_bytes = 0;
		packets = 0;
		src_packets = 0;
		dst_packets = 0;
		wrong_fragments = 0;
		urgent_packets = 0;
	}

	public Conversation(const Packet *packet)
		: five_tuple(packet->get_five_tuple()),
		, start_ts(), last_ts()
	{
		state = conversation_state_t.valueOf("INIT");
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
				return S1;

			case S4:
				return OTH;

			case S2F:
				return S2;

			case S3F:
				return S3;

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
			break;
		case UDP:
			return "udp";
			break;
		case ICMP:
			return "icmp";
			break;
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
			break;

		default:
			break;
		}

		return false;
	}

	boolean is_rerror()
	{
		return (get_state() == REJ);
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
			urgent_packets++;

		// Make state transitions according to packet
		update_state(packet);

		return is_in_final_state();
	}

	void update_state(Packet * packet)
	{
		// By default conversation can only get to state SF (after any packet).
		// TCP subclass will by the special case that will override this.
		state = SF;
	}

	String get_state_str()
	{
		return state_to_str(get_state());
	}

	// TODO: use mapping by array fo char*s ?
	String state_to_str(conversation_state_t state)
	{
		switch (state) 
		{
		case INIT: 
			return "INIT"; 
			break;
		case S0: 
			return "S0"; 
			break;
		case S1: 
			return "S1"; 
			break;
		case S2: 
			return "S2"; 
			break;
		case S3: 
			return "S3"; 
			break;
		case SF: 
			return "SF"; 
			break;
		case REJ: 
			return "REJ"; 
			break;
		case RSTOS0: 
			return "RSTOS0"; 
			break;
		case RSTO: 
			return "RSTO"; 
			break;
		case RSTR: 
			return "RSTR"; 
			break;
		case SH: 
			return "SH"; 
			break;
		case RSTRH: 
			return "RSTRH"; 
			break;
		case SHR: 
			return "SHR"; 
			break;
		case OTH: 
			return "OTH"; 
			break;
		case ESTAB: 
			return "ESTAB"; 
			break;
		case S4: 
			return "S4"; 
			break;
		case S2F: 
			return "S2F"; 
			break;
		case S3F: 
			return "S3F"; 
			break;
		default: 
			break;
		}
		return "UNKNOWN";
	}
	
	boolean Conversation less(Conversation other)
	{
		return (this.get_last_ts() < other.get_last_ts());
	}
}
