package nids.kddpreprocessor;

import static nids.kddpreprocessor.Net.icmp_field_type_t.*;
import static nids.kddpreprocessor.enums.service_t.*;

import nids.kddpreprocessor.Net.icmp_field_type_t;
import nids.kddpreprocessor.enums.service_t;

public class IcmpConversation extends Conversation
{
	icmp_field_type_t icmp_type;
	int icmp_code = 0;
	

	public IcmpConversation(FiveTuple tuple)
	{
		super(tuple, null, null);
		icmp_type = ECHOREPLY;
	}

	public IcmpConversation(Packet packet)
	{
		super(packet, null, null);
		icmp_type = packet.get_icmp_type();
		icmp_code = packet.get_icmp_code();
	}

	service_t get_service()
	{
		switch (icmp_type)
		{
		case ECHOREPLY:
			return SRV_ECR_I;	// Echo Reply (0)

		case DEST_UNREACH:
			if (icmp_code == 0)			// Destination network unreachable
				return SRV_URP_I;
			else if (icmp_code == 1)	// Destination host unreachable
				return SRV_URH_I;
			else
				return SRV_OTH_I;		// Other ICMP messages;

		case REDIRECT:
			return SRV_RED_I;	// Redirect message (5)

		case ECHO:
			return SRV_ECO_I;	// Echo Request (8)

		case TIME_EXCEEDED:		// Time Exceeded (11)
			return SRV_TIM_I;

		default:
			return SRV_OTH_I;	// Other ICMP messages;

		}
	}
}
