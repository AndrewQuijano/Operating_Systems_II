package start;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Scanner;

import org.jnetpcap.Pcap;
import org.jnetpcap.PcapDumper;
import org.jnetpcap.PcapIf;
import org.jnetpcap.packet.PcapPacket;
import org.jnetpcap.packet.PcapPacketHandler;
import org.jnetpcap.protocol.network.Arp;
import org.jnetpcap.protocol.tcpip.Tcp;

import nids.Sniffer;
import nids.kdd;

public class Start 
{
	public static final String DATE_FORMAT_NOW = "yyyyMMddHHmmss";
	private static Scanner on;
	
	public static String now()
	{    
		Calendar cal = Calendar.getInstance();    
		SimpleDateFormat df = new SimpleDateFormat(DATE_FORMAT_NOW);    
		return df.format(cal.getTime());    
	} 

	public static void main(String[] args) throws Exception 
	{
		/*
		if(!Sniffer.start())
		{
			System.out.println("Error!");
		}
		*/
		
		kdd test = new kdd();
		List<PcapPacket> l = test.getPacketList("C:\\Users\\Andrew\\Desktop\\lol.pcap");
		Tcp t = new Tcp();
		
		for (int i = 0; i < l.size(); i++)
		{
			PcapPacket p = l.get(i);
			//t = p.getHeader(t);
			//System.out.println(t.toString());
		}
		/*

		List<PcapIf> alldevs = new ArrayList<PcapIf>();
		int i = 0;
		final StringBuilder errbuf = new StringBuilder();
		while(i < alldevs.size())
		{
			System.out.println(i+" : "+alldevs.get(i++).getName());
		}

		System.out.println("Enter which device do you want to use to listen:");
		int choice = new Scanner(System.in).nextInt();
		//System.out.println(System.getProperty("java.library.path"));
		PcapIf device = alldevs.get(choice);
		System.out.println("how long would you like to scan for");
		int n = new Scanner(System.in).nextInt();
		int snaplen = 64 * 1024;			// Capture all packets, no trucation
		int flags = Pcap.MODE_PROMISCUOUS;	// capture all packets
		int timeout = n * 1000;				// 10 seconds in millis

		Pcap pcap = Pcap.openLive(device.getName(), snaplen, flags, timeout, errbuf);   
		if (pcap == null)
		{    
			System.err.printf("Error while opening device for capture: %s\n", errbuf.toString());    
			return;
		}
		String ofile = "Packet "+ now().toString() + ".pcap";    
		PcapDumper dumper = pcap.dumpOpen(ofile);	// output file 

        //Create packet handler which will receive packets
        PcapPacketHandler<PcapDumper> jpacketHandler = new PcapPacketHandler<PcapDumper>() 
        {
            Arp arp = new Arp();

            public void nextPacket(PcapPacket packet, PcapDumper user) 
            {
                //Here i am capturing the ARP packets only,you can capture any packet that you want by just changing the below if condition
                if (packet.hasHeader(arp)) 
                {
                    System.out.println("Hardware type" + arp.hardwareType());
                    System.out.println("Protocol type" + arp.protocolType());
                    System.out.println("Packet:" + arp.getPacket());
                    System.out.println();
                }
            }
        };
        
		on = new Scanner(System.in);
		
		System.out.println("write true for program to start false for program to stop");
		pcap.setTimeout(2);
		while(on.nextBoolean())
		{
			if(on.hasNextBoolean())
			{
				System.out.println("Are you sure?");
				if(pcap.activate() > 0)
				{
					pcap.close();
					System.out.println("Scanner off");
				}
				on = new Scanner(System.in);
			}
			System.err.println("scanning");
			pcap.loop(Pcap.LOOP_INFINITE, jpacketHandler, dumper);  
			if(!on.nextBoolean())
			{
				pcap.breakloop();
			}
			System.err.println("scanning completed do you want to scan more");
		}
		*/
	}
}