package nids.kddpreprocessor.enums;

/*
 * ICMP type field
 * Values from linux source code used
 * https://github.com/torvalds/linux/blob/master/include/uapi/linux/icmp.h
 */
enum icmp_field_type_t
{
	ECHOREPLY(0),
	DEST_UNREACH(3),
	SOURCE_QUENCH(4),
	REDIRECT(5),
	ECHO(8),
	TIME_EXCEEDED(11),
	PARAMETERPROB(12),
	TIMESTAMP(13),
	TIMESTAMPREPLY(14),
	INFO_REQUEST(15),
	INFO_REPLY(16),
	ADDRESS(17),
	ADDRESSREPLY(18);
	private int value;

	private icmp_field_type_t(int value) 
	{
		this.setValue(value);
	}

	public int getValue() 
	{
		return value;
	}

	public void setValue(int value) 
	{
		this.value = value;
	}
};
