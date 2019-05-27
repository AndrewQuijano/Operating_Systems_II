package nids.kddpreprocessor;

import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.protocol.lan.Ethernet;
import org.jnetpcap.protocol.network.Icmp;
import org.jnetpcap.protocol.network.Ip4;
import org.jnetpcap.protocol.network.Ip4.Timestamp;
import org.jnetpcap.protocol.tcpip.Tcp;
import org.jnetpcap.protocol.tcpip.Udp;

public class Packet 
{
	private Timestamp start_ts;
	private boolean eth2 = false;
	private FiveTuple five_tuple;
	private int icmp_code = 0;
	private int length = 0;
	private Ethernet eth_type = null;
	private Tcp tcp_flags = null;
	private Udp udp = null;
    private Icmp icmp_type = null;
    
    // hold source and destination port
    private int src_port = 0;
    private int dest_port = 0;
    
    public Packet(PcapPacket p)
    {
    	/*
    	start_ts = ;
    	eth2 = false;
    	five_tuple;
    	*/
    	length = p.getTotalSize();
    	eth_type = p.getHeader(new Ethernet());
    	tcp_flags = p.getHeader(new Tcp());
    	udp = p.getHeader(new Udp());
    	icmp_type = p.getHeader(new Icmp());
    	if(icmp_type != null)
    	{
    		icmp_code = icmp_type.code();
    	}
    	else
    	{
    		icmp_code = 0;
    	}
    	if(eth_type != null)
    	{
    		//eth_type.
    	}
    	
    	Ip4 ip = p.getHeader(new Ip4());
    	src_port = tcp_flags.source();
    	dest_port = tcp_flags.destination();
    	five_tuple = new FiveTuple();
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

	void set_eth2(boolean is_eth2)
	{
		this.eth2 = is_eth2;
	}

	Ethernet get_eth_type()
	{
		return eth_type;
	}

	void Pset_eth_type(Ethernet eth_type)
	{
		this.eth_type = eth_type;
	}

	FiveTuple get_five_tuple()
	{
		return five_tuple;
	}
	
	void set_five_tuple(FiveTuple five_tuple)
	{
		this.five_tuple = five_tuple;
	}

	int get_ip_proto()
	{
		return five_tuple.get_ip_proto();
	}

	void Pset_ip_proto(int ip_proto)
	{
		this.five_tuple.set_ip_proto(ip_proto);
	}

	int get_src_ip()
	{
		return five_tuple.get_src_ip();
	}

	void set_src_ip(int src_ip)
	{
		this.five_tuple.set_src_ip(src_ip);
	}

	int get_dst_ip()
	{
		return five_tuple.get_dst_ip();
	}

	void set_dst_ip(int dst_ip)
	{
		this.five_tuple.set_dst_ip(dst_ip);
	}

	int get_src_port()
	{
		return five_tuple.get_src_port();
	}

	void set_src_port(int src_port)
	{
		this.five_tuple.set_src_port(src_port);
	}

	int get_dst_port()
	{
		return five_tuple.get_dst_port();
	}

	void set_dst_port(int dst_port)
	{
		this.five_tuple.set_dst_port(dst_port);
	}

	Tcp get_tcp_flags()
	{
		return tcp_flags;
	}

	void set_tcp_flags(Tcp tcp_flags)
	{
		this.tcp_flags = tcp_flags;
	}

	Icmp get_icmp_type()
	{
		return icmp_type;
	}
	void set_icmp_type(Icmp icmp_type)
	{
		this.icmp_type = icmp_type;
	}

	int get_icmp_code()
	{
		return icmp_code;
	}
	void set_icmp_code(int icmp_code)
	{
		this.icmp_code = icmp_code;
	}

	int get_length()
	{
		return length;
	}

	void set_length(int length)
	{
		this.length = length;
	}

	int get_frame_count()
	{
		// By default packet consists of 1 frame
		return 1;
	}
}
