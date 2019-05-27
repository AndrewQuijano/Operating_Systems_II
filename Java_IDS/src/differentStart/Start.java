package differentStart;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import org.jnetpcap.Pcap;
import org.jnetpcap.PcapIf;
import org.jnetpcap.nio.JMemory;
import org.jnetpcap.packet.JFlow;
import org.jnetpcap.packet.JFlowKey;
import org.jnetpcap.packet.JFlowMap;
import org.jnetpcap.packet.JPacket;
import org.jnetpcap.packet.JPacketHandler;
import org.jnetpcap.packet.JScanner;
import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.protocol.tcpip.Http;
import org.jnetpcap.protocol.tcpip.Tcp;

public class Start 
{
	public static void main(String[] args) 
	{

		final StringBuilder errbuf = new StringBuilder();

		List<PcapIf> alldevs = new ArrayList<PcapIf>();
		int r = Pcap.findAllDevs(alldevs, errbuf);  
		if (r != Pcap.OK || alldevs.isEmpty()) 
		{  
			System.err.printf("Can't read list of devices, error is %s", errbuf.toString());  
			return;  
		}
		int i = 0;
		while(i < alldevs.size())
		{
			PcapIf iface = alldevs.get(i);
			System.out.println(i +" : " + iface.getName());
			System.out.println(iface.getDescription());
			++i;
		}
		System.out.println("Enter which device do you want to use to listen :");
		int choice = new Scanner(System.in).nextInt();
		//System.out.println(System.getProperty("java.library.path"));
		PcapIf device = alldevs.get(choice);
		System.out.println("how long would you like to scan for");
		int n = new Scanner(System.in).nextInt();
		int snaplen = 64 * 1024;           // Capture all packets, no trucation
		int flags = Pcap.MODE_PROMISCUOUS; // capture all packets
		int timeout = n * 1000;           // 10 seconds in millis


		Pcap pcap = Pcap.openLive(device.getName(), snaplen, flags, timeout, errbuf);   
		if (pcap == null) 
		{    
			System.err.printf("Error while opening device for capture: %s\n", errbuf.toString());    
			return;    
		}

		pcap.loop(10, new JPacketHandler<StringBuilder>() 
		{
			/**
			 * We purposely define and allocate our working tcp header (accessor)
			 * outside the dispatch function and thus the libpcap loop, as this type
			 * of object is reusable and it would be a very big waist of time and
			 * resources to allocate it per every dispatch of a packet. We mark it
			 * final since we do not plan on allocating any other instances of Tcp.
			 */
			final Tcp tcp = new Tcp();
			final Http http = new Http();

			/**
			 * Our custom handler that will receive all the packets libpcap will
			 * dispatch to us. This handler is inside a libpcap loop and will receive
			 * exactly 10 packets as we specified on the Pcap.loop(10, ...) line
			 * above.
			 * 
			 * @param packet
			 *          a packet from our capture file
			 * @param errbuf
			 *          our custom user parameter which we chose to be a StringBuilder
			 *          object, but could have chosen anything else we wanted passed
			 *          into our handler by libpcap
			 */
			public void nextPacket(JPacket packet, StringBuilder errbuf) 
			{

				if (packet.hasHeader(Tcp.ID)) 
				{
					packet.getHeader(tcp);
					System.out.printf("tcp.dst_port=%d%n", tcp.destination());
					System.out.printf("tcp.src_port=%d%n", tcp.source());
					System.out.printf("tcp.ack=%x%n", tcp.ack());
				}


				if (packet.hasHeader(tcp)) 
				{			
					System.out.printf("tcp header::%s%n", tcp.toString());
				}

				if (packet.hasHeader(tcp) && packet.hasHeader(http)) 
				{
					System.out.printf("http header::%s%n", http);
				}

				System.out.printf("frame #%d%n", packet.getFrameNumber());
			}

		}, errbuf);

		JScanner.getThreadLocal().setFrameNumber(0);

		final PcapPacket packet = new PcapPacket(JMemory.POINTER);
		final Tcp tcp = new Tcp();

		for (int i1 = 0; i1 < 5; i1++) 
		{
			pcap.nextEx(packet);
			if (packet.hasHeader(tcp)) 
			{
				System.out.printf("#%d seq=%08X%n", packet.getFrameNumber(), tcp.seq());
			}
		}
		final Map<JFlowKey, JFlow> flows = new HashMap<JFlowKey, JFlow>();

		for (int i1 = 0; i1 < 50; i1++) 
		{
			pcap.nextEx(packet);
			final JFlowKey key = packet.getState().getFlowKey();

			JFlow flow = flows.get(key);
			if (flow == null) 
			{
				flows.put(key, flow = new JFlow(key));
			}
			flow.add(new PcapPacket(packet));
		}


		for (JFlow flow : flows.values()) 
		{
			if (flow.isReversable()) 
			{
				List<JPacket> forward = flow.getForward();
				for (JPacket p : forward) 
				{
					System.out.printf("%d, ", p.getFrameNumber());
				}
				System.out.println();

				List<JPacket> reverse = flow.getReverse();
				for (JPacket p : reverse) 
				{
					System.out.printf("%d, ", p.getFrameNumber());
				}
			}
			else 
			{
				for (JPacket p : flow.getAll()) 
				{
					System.out.printf("%d, ", p.getFrameNumber());
				}
			}
			System.out.println();
		}

		JFlowMap superFlowMap = new JFlowMap();
		pcap.loop(Pcap.LOOP_INFINITE, superFlowMap, null);

		System.out.printf("superFlowMap::%s%n", superFlowMap);

		/*
		 * Now we have read the remaining packets and we no longer need to keep the
		 * pcap file open.
		 */
		pcap.close();
	}
}

