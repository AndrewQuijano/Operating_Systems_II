package nids.kddpreprocessor;

import org.jnetpcap.protocol.network.Ip4.Timestamp;

public class IntervalKeeper 
{
	private int interval;		// in usec
	private Timestamp last_ts;
	
	public IntervalKeeper(Timestamp _last_ts)
	{
		last_ts = _last_ts;
		interval = 0;
	}

	public IntervalKeeper(int interval_ms, Timestamp _last_ts)
	{
		interval = interval_ms * 1000;
		last_ts = _last_ts;
	}

	int get_interval()
	{
		return interval / 1000;
	}

	void set_interval(int interval_ms)
	{
		this.interval = interval_ms * 1000;
	}

	void update_time(Timestamp ts)
	{
		last_ts = ts;
	}

	boolean is_timedout(Timestamp now)
	{
		return (now >= last_ts + interval);
	}
}
