package nids.kddpreprocessor;

public class ConversationFeatures 
{
	private Conversation conv;
	
	private int count;
	private double rerror_rate;
	private int srv_count;
	private double serror_rate;
	private double srv_serror_rate;
	private double srv_rerror_rate;
	private double same_srv_rate;
	private double diff_srv_rate;
	private int same_srv_count;
	private int dst_host_count;
	private int dst_host_srv_count;
	private double dst_host_same_srv_rate;
	private double dst_host_diff_srv_rate;
	private double dst_host_same_src_port_rate;
	private double dst_host_serror_rate;
	private double dst_host_srv_serror_rate;
	private double dst_host_rerror_rate;
	private double dst_host_srv_rerror_rate;
	private int dst_host_same_srv_count;

	public ConversationFeatures(Conversation _conv)
	{
		conv = _conv;
	}

	Conversation get_conversation()
	{
		return conv;
	}

	/**
	 * Getters, setters, inc & dec for derived feature values
	 */
	int get_count()
	{
		return count;
	}
	void set_count(int count) 
	{
		this.count = count;
	}

	int get_srv_count()
	{
		return srv_count;
	}
	
	void set_srv_count(int srv_count) 
	{
		this.srv_count = srv_count;
	}

	double get_serror_rate()
	{
		return serror_rate;
	}
	
	void set_serror_rate(double serror_rate) 
	{
		this.serror_rate = serror_rate;
	}

	double get_srv_serror_rate()
	{
		return srv_serror_rate;
	}
	
	void set_srv_serror_rate(double srv_serror_rate)
	{
		this.srv_serror_rate = srv_serror_rate;
	}

	double get_rerror_rate()
	{
		return rerror_rate;
	}
	
	void set_rerror_rate(double rerror_rate)
	{
		this.rerror_rate = rerror_rate;
	}

	double get_srv_rerror_rate()
	{
		return srv_rerror_rate;
	}
	
	void set_srv_rerror_rate(double srv_rerror_rate)
	{
		this.srv_rerror_rate = srv_rerror_rate;
	}

	double get_same_srv_rate()
	{
		return same_srv_rate;
	}
	
	void set_same_srv_rate(double same_srv_rate) 
	{
		this.same_srv_rate = same_srv_rate;
	}

	double get_diff_srv_rate()
	{
		return diff_srv_rate;
	}
	
	void set_diff_srv_rate(double diff_srv_rate)
	{
		this.diff_srv_rate = diff_srv_rate;
	}

	double get_srv_diff_host_rate()
	{
		return (srv_count == 0) ? 0.0 : ((srv_count - same_srv_count) / (double)srv_count);
	}

	int get_same_srv_count() 
	{
		return same_srv_count;
	}
	
	void set_same_srv_count(int same_srv_count) 
	{
		this.same_srv_count = same_srv_count;
	}

	int get_dst_host_count()
	{
		return dst_host_count;
	}
	void set_dst_host_count(int dst_host_count)
	{
		this.dst_host_count = dst_host_count;
	}

	int get_dst_host_srv_count()
	{
		return dst_host_srv_count;
	}
	
	void set_dst_host_srv_count(int dst_host_srv_count)
	{
		this.dst_host_srv_count = dst_host_srv_count;
	}

	double get_dst_host_same_srv_rate()
	{
		return dst_host_same_srv_rate;
	}
	
	void set_dst_host_same_srv_rate(double dst_host_same_srv_rate)
	{
		this.dst_host_same_srv_rate = dst_host_same_srv_rate;
	}

	double get_dst_host_diff_srv_rate()
	{
		return dst_host_diff_srv_rate;
	}
	
	void set_dst_host_diff_srv_rate(double dst_host_diff_srv_rate) {
		this.dst_host_diff_srv_rate = dst_host_diff_srv_rate;
	}

	double get_dst_host_same_src_port_rate()
	{
		return dst_host_same_src_port_rate;
	}
	
	void set_dst_host_same_src_port_rate(double dst_host_same_src_port_rate) {
		this.dst_host_same_src_port_rate = dst_host_same_src_port_rate;
	}

	double get_dst_host_serror_rate()
	{
		return dst_host_serror_rate;
	}
	
	void set_dst_host_serror_rate(double dst_host_serror_rate)
	{
		this.dst_host_serror_rate = dst_host_serror_rate;
	}

	double get_dst_host_srv_serror_rate()
	{
		return dst_host_srv_serror_rate;
	}
	
	void set_dst_host_srv_serror_rate(double dst_host_srv_serror_rate)
	{
		this.dst_host_srv_serror_rate = dst_host_srv_serror_rate;
	}

	double get_dst_host_rerror_rate()
	{
		return dst_host_rerror_rate;
	}
	
	void set_dst_host_rerror_rate(double dst_host_rerror_rate) 
	{
		this.dst_host_rerror_rate = dst_host_rerror_rate;
	}

	double get_dst_host_srv_rerror_rate()
	{
		return dst_host_srv_rerror_rate;
	}
	
	void set_dst_host_srv_rerror_rate(double dst_host_srv_rerror_rate)
	{
		this.dst_host_srv_rerror_rate = dst_host_srv_rerror_rate;
	}

	double get_dst_host_srv_diff_host_rate()
	{
		return (dst_host_srv_count == 0) ? 0.0 : ((dst_host_srv_count - dst_host_same_srv_count) / (double)dst_host_srv_count);
	}

	int get_dst_host_same_srv_count()
	{
		return dst_host_same_srv_count;
	}
	
	void set_dst_host_same_srv_count(int dst_host_same_srv_count)
	{
		this.dst_host_same_srv_count = dst_host_same_srv_count;
	}
	
	void print(boolean print_extra_features)
	{	
		// Intrinsic features
		//ss << noshowpoint << setprecision(0) << (conv->get_duration_ms() / 1000) << ','; // Cut fractional part
		System.out.print(conv.get_protocol_type_str() + ',');
		System.out.print(conv.get_service_str() + ',');
		System.out.print(conv.get_state_str() + ',');
		System.out.print(conv.get_src_bytes() + ',');
		System.out.print(conv.get_dst_bytes() + ',');
		if (conv.land())
		{
			System.out.print('1' + ',');
		}
		else
		{
			System.out.print('0' + ',');
		}
		System.out.print(conv.get_wrong_fragments() + ',');
		System.out.print(conv.get_urgent_packets() + ',');

		// Derived time windows features, precision of 2
		System.out.print(count + ',');
		System.out.print(srv_count + ',');
		System.out.print(serror_rate + ',');
		System.out.print(srv_serror_rate + ',');
		System.out.print(rerror_rate + ',');
		System.out.print(srv_rerror_rate + ',');
		System.out.print(same_srv_rate + ',');
		System.out.print(diff_srv_rate + ',');
		System.out.print(get_srv_diff_host_rate() + ',');

		// Derived connection count window features
		System.out.print(dst_host_count + ',');
		System.out.print(dst_host_srv_count + ',');
		System.out.print(dst_host_same_srv_rate + ',');
		System.out.print(dst_host_diff_srv_rate + ',');
		System.out.print(dst_host_same_src_port_rate + ',');
		System.out.print(get_dst_host_srv_diff_host_rate() + ',');
		System.out.print(dst_host_serror_rate + ',');
		System.out.print(dst_host_srv_serror_rate + ',');
		System.out.print(dst_host_rerror_rate + ',');
		System.out.print(dst_host_srv_rerror_rate);

		if (print_extra_features) 
		{
			/*
			FiveTuple ft = conv.get_five_tuple();

			// TODO: ugly wtf, but working
			uint32_t src_ip = ft.get_src_ip();
			uint32_t dst_ip = ft.get_dst_ip();
			uint8_t *sip = (uint8_t *)&src_ip;
			uint8_t *dip = (uint8_t *)&dst_ip;
			ss << ',';
			ss << (int)sip[0] << "." << (int)sip[1] << "." << (int)sip[2] << "." << (int)sip[3] << ',';
			ss << ft->get_src_port() << ',';
			ss << (int)dip[0] << "." << (int)dip[1] << "." << (int)dip[2] << "." << (int)dip[3] << ',';
			ss << ft->get_dst_port() << ',';

			// Time (e.g.: 2010-06-14T00:11:23)
			struct tm *ltime;
			//struct tm timeinfo;
			char timestr[20];
			time_t local_tv_sec;
			local_tv_sec = conv->get_last_ts().get_secs();
			ltime = localtime(&local_tv_sec);
			//localtime_s(&timeinfo, &local_tv_sec);
			strftime(timestr, sizeof timestr, "%Y-%m-%dT%H:%M:%S", ltime);
			//strftime(timestr, sizeof timestr, "%Y-%m-%dT%H:%M:%S", &timeinfo);
			ss << timestr;
			*/
		}
		System.out.println("");
	}

}
