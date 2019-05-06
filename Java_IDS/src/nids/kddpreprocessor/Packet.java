package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

public class Packet 
{
	private Timestamp start_ts;
	private boolean eth2 = false;
	private eth_type(TYPE_ZERO);
	private FiveTuple five_tuple;
	private tcp_flags();
	private icmp_type(ECHOREPLY);
	private int icmp_code = 0;
	private int length = 0;
	
	public Packet(Timestamp _start_ts, boolean _eth2, eth_type(TYPE_ZERO), five_tuple, 
			tcp_flags(), icmp_type(ECHOREPLY), _icmp_code, _length)
	{
		start_ts = _start_ts;
		eth2 = _eth2;
		//private eth_type(TYPE_ZERO);
		five_tuple = new FiveTuple();
		//private tcp_flags();
		//private icmp_type(ECHOREPLY);
		icmp_code = _imcp_code;
		length = _length;
	}

	Timestamp get_start_ts()
	{
		return start_ts;
	}

	void set_start_ts(Timestamp start_ts)
	{
		this.start_ts = start_ts;
	}

	Timestamp get_end_ts()
	{
		// Return the start timestamp by default
		return start_ts;
	}

	boolean is_eth2()
	{
		return eth2;
	}

	void set_eth2(bool is_eth2)
	{
		this.eth2 = is_eth2;
	}

	eth_field_type_t get_eth_type()
	{
		return eth_type;
	}

	void Packet::set_eth_type(eth_field_type_t eth_type){
		this.eth_type = eth_type;
	}

	FiveTuple get_five_tuple()
	{
		return five_tuple;
	}
	
	void set_five_tuple(const FiveTuple &five_tuple)
	{
		this->five_tuple = five_tuple;
	}

	ip_field_protocol_t Packet::get_ip_proto()
	{
		return five_tuple.get_ip_proto();
	}

	void Pset_ip_proto(ip_field_protocol_t ip_proto)
	{
		this.five_tuple.set_ip_proto(ip_proto);
	}

	int get_src_ip()
	{
		return five_tuple.get_src_ip();
	}

	void set_src_ip(uint32_t src_ip)
	{
		this.five_tuple.set_src_ip(src_ip);
	}

	uint32_t Packet::get_dst_ip()
	{
		return five_tuple.get_dst_ip();
	}

	void set_dst_ip(uint32_t dst_ip)
	{
		this.five_tuple.set_dst_ip(dst_ip);
	}

	int get_src_port()
	{
		return five_tuple.get_src_port();
	}

	void set_src_port(uint16_t src_port)
	{
		this->five_tuple.set_src_port(src_port);
	}

	int get_dst_port()
	{
		return five_tuple.get_dst_port();
	}

	void set_dst_port(uint16_t dst_port)
	{
		this.five_tuple.set_dst_port(dst_port);
	}

	tcp_field_flags_t Packet::get_tcp_flags()
	{
		return tcp_flags;
	}

	void set_tcp_flags(tcp_field_flags_t tcp_flags)
	{
		this->tcp_flags = tcp_flags;
	}

	icmp_field_type_t get_icmp_type()
	{
		return icmp_type;
	}
	void set_icmp_type(icmp_field_type_t icmp_type)
	{
		this->icmp_type = icmp_type;
	}

	int get_icmp_code()
	{
		return icmp_code;
	}
	void set_icmp_code(uint8_t icmp_code)
	{
		this.icmp_code = icmp_code;
	}

	int get_length()
	{
		return length;
	}

	void set_length(size_t length)
	{
		this.length = length;
	}

	int get_frame_count()
	{
		// By default packet consists of 1 frame
		return 1;
	}

	void print_human()
	{
		// TODO: WTF ugly code, just for debugging, mal si branic..
		stringstream ss;

		struct tm *ltime;
		//struct tm timeinfo;
		char timestr[16];
		time_t local_tv_sec;
		//local_tv_sec = start_ts.get_secs();
		ltime = localtime(&local_tv_sec);
		//localtime_s(&timeinfo, &local_tv_sec);
		strftime(timestr, sizeof timestr, "%H:%M:%S", ltime);
		//strftime(timestr, sizeof timestr, "%H:%M:%S", &timeinfo);
		ss << timestr;

		ss << (is_eth2() ? " ETHERNET II" : " NON-ETHERNET");
		if (!is_eth2()) {
			cout << endl << ss.str() << endl;
			return;
		}
		ss << (eth_type == IPV4 ? " > IP" : " > NON-IP");
		if (eth_type != IPV4) {
			ss << "(0x" << hex << eth_type << dec << ")";
			cout << endl << ss.str() << endl;
			return;
		}

		if (get_ip_proto() == ICMP) {
			ss << " > ICMP " << endl;
		}
		else if (get_ip_proto() == TCP) {
			ss << " > TCP " << endl;
		}
		else if (get_ip_proto() == UDP) {
			ss << " > UDP " << endl;
		}
		else {
			ss << " > Other(0x" << hex << get_ip_proto() << dec << ")" << endl;
		}

		// Cast ips to arrays of octets
		uint32_t src_ip = get_src_ip();
		uint32_t dst_ip = get_dst_ip();
		uint8_t *sip = (uint8_t *)&src_ip;
		uint8_t *dip = (uint8_t *)&dst_ip;

		if (get_ip_proto() != TCP && get_ip_proto() != UDP) {
			ss << "  src=" << (int)sip[0] << "." << (int)sip[1] << "." << (int)sip[2] << "." << (int)sip[3];
			ss << " dst=" << (int)dip[0] << "." << (int)dip[1] << "." << (int)dip[2] << "." << (int)dip[3];
			ss << " length=" << get_length();
			if (get_frame_count() > 1)
				ss << " frames=" << get_frame_count();
			ss << endl;
			if (get_ip_proto() == ICMP) {
				ss << "  icmp_type=" << icmp_type << " icmp_code=" << icmp_code << endl;
			}
		}
		else {
			ss << "  src=" << (int)sip[0] << "." << (int)sip[1] << "." << (int)sip[2] << "." << (int)sip[3] << ":" << get_src_port();
			ss << " dst=" << (int)dip[0] << "." << (int)dip[1] << "." << (int)dip[2] << "." << (int)dip[3] << ":" << get_dst_port();
			ss << " length=" << get_length();
			if (get_frame_count() > 1)
				ss << " frames=" << get_frame_count();
			ss << endl;

			if (get_ip_proto() == TCP) {
				ss << "  Flags(0x" << hex << (int) tcp_flags.flags << dec << "): ";
				ss << (tcp_flags.fin() ? "F" : "");
				ss << (tcp_flags.syn() ? "S" : "");
				ss << (tcp_flags.rst() ? "R" : "");
				ss << (tcp_flags.ack() ? "A" : "");
				ss << (tcp_flags.urg() ? "U" : "");
				ss << endl;
			}
		}

		cout << endl << ss.str();
	}
}
