package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

public class IpFragment 
{
	int ip_id;
	boolean ip_flag_mf = false;
	int ip_frag_offset = 0;
	int ip_payload_length = 0;
	
	public IpFragment(Packet packet)
	{
		
	}

	int get_ip_id()
	{
		return ip_id;
	}

	void set_ip_id(int ip_id)
	{
		this.ip_id = ip_id;
	}

	boolean get_ip_flag_mf()
	{
		return ip_flag_mf;
	}

	void set_ip_flag_mf(boolean ip_flag_mf)
	{
		this.ip_flag_mf = ip_flag_mf;
	}

	int get_ip_frag_offset()
	{
		return ip_frag_offset;
	}

	void set_ip_frag_offset(int ip_frag_offset)
	{
		this.ip_frag_offset = ip_frag_offset;
	}

	int get_ip_payload_length()
	{
		return ip_payload_length;
	}

	void set_ip_payload_length(int ip_payload_length)
	{
		this.ip_payload_length = ip_payload_length;
	}

	public Timestamp get_end_ts() 
	{
		return null;
	}
}
