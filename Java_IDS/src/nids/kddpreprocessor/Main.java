package nids.kddpreprocessor;

import java.util.ArrayList;
import java.util.List;

import org.jnetpcap.Pcap;
import org.jnetpcap.PcapIf;
import org.jnetpcap.protocol.lan.Ethernet;
import org.jnetpcap.protocol.network.Ip4;
import org.jnetpcap.protocol.network.Ip4.Timestamp;

import nids.kddpreprocessor.enums.eth_field_type_t;
import nids.kddpreprocessor.Net.ip_field_protocol_t;

import static nids.kddpreprocessor.Net.ip_field_protocol_t.*;
import static nids.kddpreprocessor.enums.eth_field_type_t.*;

public class Main 
{
	static boolean temination_requested = false;
	
	public static void main(String [] args)
	{
		Runtime.getRuntime().addShutdownHook(new Thread() 
		{
			public void run() 
			{
				System.out.println("Terminating extractor (signal received)");
				temination_requested = true;
			}
		});
		
		Config config = new Config();
		parse_args(args.length, args, config);

		if (config.get_files_count() == 0) 
		{
			// Input from interface
			int inum = config.get_interface_num();
			if (config.should_print_filename())
			{
				System.out.println("INTERFACE " + inum);
			}
			Sniffer sniffer = new Sniffer(inum, config);
			extract(sniffer, config, true);
		}
		else 
		{
			// Input from files
			int count = config.get_files_count();
			String [] files = config.get_files_values();
			for (int i = 0; i < count; i++) 
			{
				if (config.should_print_filename())
				{
					System.out.println("FILE '" + files[i] + "'");
				}
				Sniffer sniffer = new Sniffer(files[i], config);
				extract(sniffer, config, false);
			}
		}
	}

	static void extract(Sniffer sniffer, Config config, boolean is_running_live)
	{
		IpReassembler reasm;
		ConversationReconstructor conv_reconstructor = new ConversationReconstructor(config);
		StatsEngine stats_engine = new StatsEngine(config);

		boolean has_more_traffic = true;
		while (!temination_requested && (has_more_traffic || is_running_live)) 
		{
			// Get frame from sniffer
			IpFragment frag = sniffer.next_frame();
			has_more_traffic = (frag != null);

			Packet datagr = null;
			if (has_more_traffic) 
			{
				// Do some assertion about the type of packet just to be sure
				// If sniffer's filter fails to fulfill this assertion, "continue" can be used here
				eth_field_type_t eth_type = frag.get_eth_type();
				ip_field_protocol_t ip_proto = frag.get_ip_proto();
				assert(eth_type == IPV4 && (ip_proto == TCP || ip_proto == UDP || ip_proto == ICMP));

				Timestamp now = frag.get_end_ts();

				// IP Reassemble, frag must not be used after this
				datagr = reasm.reassemble(frag);

				// Conversation reconstruction
				if (datagr == null) 
				{
					conv_reconstructor.add_packet(datagr);
				}
				else 
				{
					// Tell conversation reconstruction just how the time goes on
					conv_reconstructor.report_time(now);
				}
			}

			// Output timed out conversations 
			Conversation conv;
			while ((conv = conv_reconstructor.get_next_conversation()) != null) 
			{
				ConversationFeatures cf = stats_engine.calculate_features(conv);
				conv = null;		// Should not be used anymore, object will commit suicide
				cf.print(config.should_print_extra_features());
			}
		}
		// START HERE IF NOT ACTIVELY SNIFFING.

		// If no more traffic, finish everything
		conv_reconstructor.finish_all_conversations();

		// Output leftover conversations
		Conversation conv;
		while ((conv = conv_reconstructor.get_next_conversation()) != null)
		{
			ConversationFeatures cf = stats_engine.calculate_features(conv);
			conv = null;
			cf.print(config.should_print_extra_features());
		}
	}

	static void usage(String name)
	{
		// Option '-' originally meant to use big read timeouts and exit on first timeout. Other approach used
		// because original approach did not work (does this option make sense now?).
		System.out.println("KDD'99-like feature extractor");
		System.out.println("Usage: " + name + " [OPTION]... [FILE]");
		System.out.println(" -h, --help    Display this usage  ");
		System.out.println(" -l, --list    List interfaces  ");
		System.out.println(" -i   NUMBER   Capture from interface with given number (default 1)");
		System.out.println(" -p   MS       libpcap network read timeout in ms (default 1000)");
		System.out.println(" -e            Print extra features(IPs, ports, end timestamp)");
		System.out.println(" -v            Print filename/interface number before parsing each file");
		System.out.println(" -o   FILE     Write all output to FILE instead of standard output");
		System.out.println(" -a   BYTES    Additional frame length to be add to each frame in bytes");
		System.out.println("                 (e.g. 4B Ethernet CRC) (default 0)");
		System.out.println(" -ft  SECONDS  IP reassembly timeout (default 30)");
		System.out.println(" -fi  MS       Max time between timed out IP fragments lookups in ms (default 1000)");
		System.out.println(" -tst SECONDS  TCP SYN timeout for states S0, S1 (default 120)");
		System.out.println(" -tet SECONDS  TCP timeout for established connections (default 5days)  ");
		System.out.println(" -trt SECONDS  TCP RST timeout for states REJ, RSTO, RSTR, RSTOS0 (default 10)");
		System.out.println(" -tft SECONDS  TCP FIN timeout for states S2, S3 (default 120)");
		System.out.println(" -tlt SECONDS  TCP last ACK timeout (default 30)");
		System.out.println(" -ut  SECONDS  UDP timeout  (default 180)");
		System.out.println(" -it  SECONDS  ICMP timeout  (default 30)");
		System.out.println(" -ci  MS       Max time between timed out connection lookups in ms (default 1000)");
		System.out.println(" -t   MS       Time window size in ms (default 2000)");
		System.out.println(" -c   NUMBER   Count window size (default 100)");
		System.out.println(" ");
	}

	static void list_interfaces()
	{
		final StringBuilder errbuf = new StringBuilder();
		List<PcapIf> alldevs = new ArrayList<PcapIf>();
		int r = Pcap.findAllDevs(alldevs, errbuf);  
		if (r != Pcap.OK || alldevs.isEmpty()) 
		{  
			System.err.printf("Can't read list of devices, error is %s", errbuf.toString());  
			return;  
		}
		
		// In my case use device 2
		for (int i = 0; i < alldevs.size(); i++)
		{
			PcapIf iface = alldevs.get(i);
			System.out.println(i +" : " + iface.getName());
			System.out.println(iface.getDescription());
		}
	}

	// TODO: code snippets in usage() can be reused function/macro
	static void parse_args(int argc, String [] argv, Config config)
	{
		int i;

		// Options
		for (i = 1; i < argc && argv[i].charAt(0) == '-'; i++) 
		{
			int len = argv[i].length();
			if (len < 2)
			{
				invalid_option(argv[i], argv[0]);
			}
			// Second character
			int num;
			switch (argv[i].charAt(1)) 
			{
			case '-': // Long option
				if (argv[i].compareTo("--help") == 0) 
				{
					usage(argv[0]);
					System.exit(0);
				}
				if (argv[i].compareTo("--list") == 0) 
				{
					list_interfaces();
					System.exit(0);
				}

				invalid_option(argv[i], argv[0]);
				break;

			case 'h':
				usage(argv[0]);
				System.exit(0);
				break;

			case 'l':
				list_interfaces();
				System.exit(0);
				break;

			case 'i':
				if (len == 2) 
				{
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}
					num = Integer.parseInt(argv[i], 10);
					config.set_interface_num(num);
				}
				else if (len == 3 && argv[i].charAt(2) == 't')
				{	
					// Option -it
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}
					num = Integer.parseInt(argv[i], 10);
					config.set_icmp_timeout(num);
				}
				else 
				{
					invalid_option(argv[i], argv[0]);
				}
				break;

			case 'e':
				if (len != 2)
				{
					invalid_option(argv[i], argv[0]);
				}
				config.set_print_extra_features(true);
				break;

			case 'v':
				if (len != 2)
				{
					invalid_option(argv[i], argv[0]);
				}

				config.set_print_filename(true);
				break;

			case 'o':
				if (len != 2)
				{
					invalid_option(argv[i], argv[0]);
				}

				if (argc <= ++i)
				{
					invalid_option_value(argv[i - 1], "", argv[0]);
				}
				
				// System.out.println(" -o   FILE     Write all output to FILE instead of standard output");
				/*
				out_stream.open(argv[i]);
				streambuf * coutbuf = std::cout.rdbuf(); //save old buf
				cout.rdbuf(out_stream.rdbuf());		//redirect std::cout
				*/
				break;

			case 'p':
				if (len != 2)
				{
					invalid_option(argv[i], argv[0]);
				}

				if (argc <= ++i)
				{
					invalid_option_value(argv[i - 1], "", argv[0]);
				}
				num = Integer.parseInt(argv[i], 10);

				config.set_pcap_read_timeout(num);
				break;

			case 'a':
				if (len != 2)
				{
					invalid_option(argv[i], argv[0]);
				}

				if (argc <= ++i)
				{
					invalid_option_value(argv[i - 1], "", argv[0]);
				}

				num = Integer.parseInt(argv[i], 10);
				config.set_additional_frame_len(num);
				break;

			case 'c':
				if (len == 2) 
				{
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}
					num = Integer.parseInt(argv[i], 10);
					config.set_count_window_size(num);
				}
				// Option -ci
				else if (len == 3 && argv[i].charAt(2) == 'i')
				{
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}

					num = Integer.parseInt(argv[i], 10);
					config.set_conversation_check_interval_ms(num);
				}
				else 
				{
					invalid_option(argv[i], argv[0]);
				}
				break;

			case 'u':
				// Limit to '-ut'
				if (len != 3 || argv[i].charAt(2) != 't')
				{
					invalid_option(argv[i], argv[0]);
				}

				if (argc <= ++i)
				{
					invalid_option_value(argv[i - 1], "", argv[0]);
				}

				num = Integer.parseInt(argv[i], 10);
				config.set_udp_timeout(num);
				break;

			case 'f':
				if (len != 3)
				{
					invalid_option(argv[i], argv[0]);
				}

				// Third character
				switch (argv[i].charAt(2)) 
				{
				case 't':
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}

					num = Integer.parseInt(argv[i], 10);
					config.set_ipfrag_timeout(num);
					break;

				case 'i':
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}

					num = Integer.parseInt(argv[i], 10);
					config.set_ipfrag_check_interval_ms(num);
					break;

				default:
					invalid_option(argv[i], argv[0]);
					break;
				}
				break;

			case 't':
				if (len == 2) 
				{
					if (argc <= ++i)
					{
						invalid_option_value(argv[i - 1], "", argv[0]);
					}

					num = Integer.parseInt(argv[i], 10);
					config.set_time_window_size_ms(num);
				}
				// Limit to '-t?t'
				else if (len == 4 && argv[i].charAt(3) == 't') 
				{
					// Third character
					switch (argv[i].charAt(2)) 
					{
					case 's':
						if (argc <= ++i)
						{
							invalid_option_value(argv[i - 1], "", argv[0]);
						}

						num = Integer.parseInt(argv[i], 10);
						config.set_tcp_syn_timeout(num);
						break;

					case 'e':
						if (argc <= ++i)
						{
							invalid_option_value(argv[i - 1], "", argv[0]);
						}

						num = Integer.parseInt(argv[i], 10);
						config.set_tcp_estab_timeout(num);
						break;

					case 'r':
						if (argc <= ++i)
						{
							invalid_option_value(argv[i - 1], "", argv[0]);
						}

						num = Integer.parseInt(argv[i], 10);
						config.set_tcp_rst_timeout(num);
						break;

					case 'f':
						if (argc <= ++i)
						{
							invalid_option_value(argv[i - 1], "", argv[0]);
						}

						num = Integer.parseInt(argv[i], 10);
						config.set_tcp_fin_timeout(num);
						break;

					case 'l':
						if (argc <= ++i)
						{
							invalid_option_value(argv[i - 1], "", argv[0]);
						}
						num = Integer.parseInt(argv[i], 10);
						config.set_tcp_last_ack_timeout(num);
						break;

					default:
						invalid_option(argv[i], argv[0]);
						break;
					}
				}
				else 
				{
					invalid_option(argv[i], argv[0]);
				}
				break;

			default:
				invalid_option(argv[i], argv[0]);
				break;
			}
		}

		// File list
		int file_cnt = argc - i;
		config.set_files_count(file_cnt);
		if (file_cnt != 0) 
		{
			config.set_files_values(argv);
		}
	}
	

	static void invalid_option(String opt, String progname)
	{
		System.err.println("Invalid option '" + opt + "'");
		usage(progname);
		System.exit(1);
	}

	static void invalid_option_value(String opt, String val, String progname)
	{
		System.err.println("Invalid value '" + val + "' for option '" + opt + "'");
		usage(progname);
		System.exit(1);
	}
}
