package nids.kddpreprocessor;

public class Config {
	
	/**
	 * Constructor for default timeout values:
	 * - IP Fragmentation timeout 30s (Linux default)
	 *		http://www.linuxinsight.com/proc_sys_net_ipv4_ipfrag_time.html
	 * - Other values derived from iptables doc
	 *		http://www.iptables.info/en/connection-state.html
	 */
	
	private int files_c;
	private String [] files_v;
	private int get_interface_num;
	private int interface_num;
	private int pcap_read_timeout;
	private int additional_frame_len;
	private int ipfrag_timeout;
	private int ipfrag_check_interval_ms;
	private int tcp_syn_timeout;
	private int tcp_estab_timeout;
	private int tcp_rst_timeout;
	private int tcp_fin_timeout;
	private int tcp_last_ack_timeout;
	private int udp_timeout;
	private int icmp_timeout;
	private int conversation_check_interval_ms;
	private int time_window_size_ms;
	private int count_window_size;
	private boolean print_extra_features;
	private boolean print_filename;
	
	public Config()
	{
		files_c = 0;
		files_v = null;
		interface_num = 1;
		pcap_read_timeout = 1000;
		additional_frame_len = 0;
		ipfrag_timeout = 30;
		ipfrag_check_interval_ms = 1000;
		tcp_syn_timeout = 120;
		tcp_estab_timeout = 5 * 24 * 3600; // 5 days
		tcp_rst_timeout = 10;
		tcp_fin_timeout = 120;
		tcp_last_ack_timeout = 30;
		udp_timeout = 180;
		icmp_timeout = 30;
		conversation_check_interval_ms = 1000;
		time_window_size_ms = 2000;
		count_window_size = 100;
		print_extra_features = false;
		print_filename = false;
	}

	int get_files_count()
	{
		return files_c;
	}
	
	void set_files_count(int files_c)
	{
		this.files_c = files_c;
	}

	String [] get_files_values()
	{
		return files_v;
	}
	void set_files_values(String [] files_v)
	{
		this.files_v = files_v;
	}

	int get_interface_num()
	{
		return interface_num;
	}
	void set_interface_num(int interface_num)
	{
		this.interface_num = interface_num;
	}

	int get_pcap_read_timeout()
	{
		return pcap_read_timeout;
	}
	void set_pcap_read_timeout(int pcap_read_timeout)
	{
		this.pcap_read_timeout = pcap_read_timeout;
	}

	int get_additional_frame_len()
	{
		return additional_frame_len;
	}
	void set_additional_frame_len(int additional_frame_len)
	{
		this.additional_frame_len = additional_frame_len;
	}

	int get_ipfrag_timeout()
	{
		return ipfrag_timeout;
	}
	void set_ipfrag_timeout(int ipfrag_timeout)
	{
		this.ipfrag_timeout = ipfrag_timeout;
	}

	int get_ipfrag_check_interval_ms()
	{
		return ipfrag_check_interval_ms;
	}
	void set_ipfrag_check_interval_ms(int ipfrag_check_interval_ms)
	{
		this.ipfrag_check_interval_ms = ipfrag_check_interval_ms;
	}

	int get_tcp_syn_timeout()
	{
		return tcp_syn_timeout;
	}
	
	void set_tcp_syn_timeout(int tcp_syn_timeout)
	{
		this.tcp_syn_timeout = tcp_syn_timeout;
	}

	int get_tcp_estab_timeout()
	{
		return tcp_estab_timeout;
	}
	void set_tcp_estab_timeout(int tcp_estab_timeout)
	{
		this.tcp_estab_timeout = tcp_estab_timeout;
	}

	int get_tcp_rst_timeout()
	{
		return tcp_rst_timeout;
	}
	void set_tcp_rst_timeout(int tcp_rst_timeout)
	{
		this.tcp_rst_timeout = tcp_rst_timeout;
	}

	int get_tcp_fin_timeout()
	{
		return tcp_fin_timeout;
	}
	void set_tcp_fin_timeout(int tcp_fin_timeout)
	{
		this.tcp_fin_timeout = tcp_fin_timeout;
	}

	int get_tcp_last_ack_timeout()
	{
		return tcp_last_ack_timeout;
	}
	void set_tcp_last_ack_timeout(int tcp_last_ack_timeout)
	{
		this.tcp_last_ack_timeout = tcp_last_ack_timeout;
	}

	int get_udp_timeout()
	{
		return udp_timeout;
	}
	void set_udp_timeout(int udp_timeout)
	{
		this.udp_timeout = udp_timeout;
	}

	int get_icmp_timeout()
	{
		return icmp_timeout;
	}
	void set_icmp_timeout(int icmp_timeout)
	{
		this.icmp_timeout = icmp_timeout;
	}

	int get_conversation_check_interval_ms()
	{
		return conversation_check_interval_ms;
	}
	void set_conversation_check_interval_ms(int conversation_check_interval_ms)
	{
		this.conversation_check_interval_ms = conversation_check_interval_ms;
	}

	int get_time_window_size_ms()
	{
		return time_window_size_ms;
	}
	
	void set_time_window_size_ms(int time_window_size_ms)
	{
		this.time_window_size_ms = time_window_size_ms;
	}

	int get_count_window_size()
	{
		return count_window_size;
	}
	void set_count_window_size(int count_window_size)
	{
		this.count_window_size = count_window_size;
	}

	boolean should_print_extra_features()
	{
		return print_extra_features;
	}
	void set_print_extra_features(boolean print_extra_features)
	{
		this.print_extra_features = print_extra_features;
	}

	boolean should_print_filename()
	{
		return print_filename;
	}
	void set_print_filename(boolean print_filename)
	{
		this.print_filename = print_filename;
	}
}
