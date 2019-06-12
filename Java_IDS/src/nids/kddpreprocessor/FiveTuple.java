package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4;

import nids.kddpreprocessor.Net.ip_field_protocol_t;
import static nids.kddpreprocessor.Net.ip_field_protocol_t.*;

public class FiveTuple
{
	public ip_field_protocol_t ip_proto;
	public int src_ip;
	public int dst_ip;
	public int src_port;
	public int dst_port;
	
	public FiveTuple(Ip4 ip)
	{
		ip_proto = PROTO_ZERO;
		src_ip = 0;
		dst_ip = 0;
		src_port = 0;
		dst_port = 0;
	}
	
	public FiveTuple()
	{
		ip_proto = PROTO_ZERO;
		src_ip = 0;
		dst_ip = 0;
		src_port = 0;
		dst_port = 0;
	}
	
	ip_field_protocol_t get_ip_proto()
	{
		return ip_proto;
	}

	void set_ip_proto(ip_field_protocol_t ip_proto)
	{
		this.ip_proto = ip_proto;
	}

	int get_src_ip()
	{
		return src_ip;
	}

	void set_src_ip(int src_ip)
	{
		this.src_ip = src_ip;
	}

	int get_dst_ip()
	{
		return dst_ip;
	}

	void set_dst_ip(int dst_ip)
	{
		this.dst_ip = dst_ip;
	}

	int get_src_port()
	{
		return src_port;
	}

	void set_src_port(int src_port)
	{
		this.src_port = src_port;
	}

	int get_dst_port()
	{
		return dst_port;
	}

	void set_dst_port(int dst_port)
	{
		this.dst_port = dst_port;
	}

	boolean land()
	{
		return (src_ip == dst_ip && src_port == dst_port);
	}

	boolean less(FiveTuple other)
	{
		if (ip_proto < other.ip_proto)
		{
			return true;
		}
		if (ip_proto > other.ip_proto)
		{
			return false;
		}

		// IP protocols are same
		if (src_ip < other.src_ip)
		{
			return true;
		}
		if (src_ip > other.src_ip)
		{
			return false;
		}

		// src IPs are equal
		if (dst_ip < other.dst_ip)
		{
			return true;
		}
		if (dst_ip > other.dst_ip)
		{
			return false;
		}

		// dst IPs are equal
		if (src_port < other.src_port)
		{
			return true;
		}
		if (src_port > other.src_port)
		{
			return false;
		}

		// src ports are equal
		return (dst_port < other.dst_port);
	}

	FiveTuple get_reversed()
	{
		FiveTuple tuple = new FiveTuple();
		tuple.ip_proto = this.ip_proto;
		tuple.src_ip = this.dst_ip;
		tuple.dst_ip = this.src_ip;
		tuple.src_port = this.dst_port;
		tuple.dst_port = this.src_port;
		return tuple;
	}
}
