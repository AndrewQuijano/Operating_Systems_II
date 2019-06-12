package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

public class IpDatagram 
{
	private Timestamp end_ts;
	private int frame_count = 0;
	
	public IpDatagram(Timestamp ts) 
	{
		end_ts = ts;
	}

	Timestamp get_end_ts()
	{
		return this.end_ts;
	}
	
	void set_end_ts(Timestamp end_ts)
	{
		this.end_ts = end_ts;
	}

	int get_frame_count()
	{
		return frame_count;
	}

	void set_frame_count(int frame_count)
	{
		this.frame_count = frame_count;
	}

	void inc_frame_count()
	{
		this.frame_count++;
	}
}
