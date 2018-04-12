/* Simple Raw Sniffer                                                    */ 
/* Author: Luis Martin Garcia. luis.martingarcia [.at.] gmail [d0t] com  */
/* To compile: gcc simplesniffer.c -o simplesniffer -lpcap               */ 
/* Run as root!                                                          */ 
/*                                                                       */
/* This code is distributed under the GPL License. For more info check:  */
/* http://www.gnu.org/copyleft/gpl.html                                  */

#include <pcap.h> 
#include <stdio.h>
#include <stdlib.h> 
#include <signal.h>
#include <sched.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <errno.h>
#include <sys/poll.h>
#include <netinet/in_systm.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip6.h>
#include <net/ethernet.h>     /* the L2 protocols */
#include <sys/time.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <monetary.h>
#include <locale.h>

#define NUM_MAX_PACKETS 2000
#define MAXBYTES2CAPTURE 2048 
FILE *f1;

struct Vector{
	struct in_addr dst;
	long int sec;
	long int msec;	
};


struct Vector hash[NUM_MAX_PACKETS];
unsigned int globaldst;
long int sec;
long int msec;
int c;
int num_pkt = 0;
char *measure_rules=NULL;


//void dump_stats(struct in_addr dst);
/* processPacket(): Callback function called by pcap_loop() everytime a packet */
/* arrives to the network card. This function prints the captured raw data in  */
/* hexadecimal.                                                                */
void processPacket(u_char *arg, const struct pcap_pkthdr* pkthdr, const u_char * packet){ 
	int * counter = (int*) arg;

	unsigned int sip,dip,temp;
	struct in_addr srcip,dstip;
	memcpy((unsigned char*)&dip,packet+30,4);
	dstip.s_addr = dip;
	temp = ntohl(dip) >> 24;
	globaldst = dip;
	hash[num_pkt].sec = pkthdr->ts.tv_sec; //cur_time.tv_sec;//s;
	hash[num_pkt].msec = pkthdr->ts.tv_usec;//cur_time.tv_usec; //usec;
	c++;
	struct in_addr dst = {0};
	hash[num_pkt].dst.s_addr = dip;
	num_pkt++;
	return; 
} 

/* ******************************** */

void dump_stats()
{
	char fname[200];
	char num[10];
	int cont = 0;
	FILE *f;
	
	
	do{
		cont++;
		sprintf(num, "%d",cont);
		strcpy(fname,"");
		strcat(fname,"timestamp");
		strcat(fname,measure_rules);
		strcat(fname,"-");
		strcat(fname,num);
		strcat(fname,".txt");
	}
	while(access(fname, F_OK) != -1);

	f = fopen(fname,"a");
	int i;
	printf("\nGenerating capture time log");
	for(i=0;i < atoi(measure_rules);i++)
			fprintf(f, "dst: %s sec %ld usec %ld\n", inet_ntoa(hash[i].dst), hash[i].sec, hash[i].msec);

	printf("\nFinished capture time log!\n");
	  fclose(f);
}


/* main(): Main function. Opens network interface and calls pcap_loop() */
int main(int argc, char *argv[] ){

	 int i=0, count=0; 
	 pcap_t *descr = NULL; 
	 char errbuf[PCAP_ERRBUF_SIZE], *device=NULL; 
	 memset(errbuf,0,PCAP_ERRBUF_SIZE); 


	 struct bpf_program fp; //the complied filter
	 char filter_exp[] = "ip or arp or icmp";//filter expression
	 bpf_u_int32 mask; //Our net mask
	 bpf_u_int32 net; //our IP

	 if( argc > 1){  /* If user supplied interface name, use it. */
		device = argv[1];
		measure_rules = argv[2];
		count = atoi(argv[3]);
	 }
	 else{  /* Get the name of the first device suitable for capture */ 
	  	if(pcap_lookupnet(device, &net, &mask, errbuf) == -1) {
			fprintf(stderr, "Can't get netmask for device %s\n", device);
			net = 0;
			mask = 0;
		}

	    	if((device = pcap_lookupdev(errbuf)) == NULL){
			fprintf(stderr, "ERROR1: %s\n", errbuf);
			exit(1);
	    	}
	 }
	

	 printf("Opening device %s\n", device); 
	 //f1  = fopen("packet_timestamp.txt","w");

	 /* Open device in promiscuous mode */ 
	 if ( (descr = pcap_open_live(device, MAXBYTES2CAPTURE, 1,  512, errbuf)) == NULL){
		fprintf(stderr, "ERROR2: %s\n", errbuf);
		exit(1);
	 }
	 
	 /* Compile and apply the filter */
	if (pcap_compile(descr, &fp, filter_exp, 0, net) == -1) {
			fprintf(stderr, "Couldn't parse filter %s: %s\n", filter_exp, pcap_geterr(descr));
			return(1);
	}
	if (pcap_setfilter(descr, &fp) == -1) {
			fprintf(stderr, "Couldn't install filter %s: %s\n", filter_exp, pcap_geterr(descr));
			return(1);
	}
	 
	 /* Loop forever & call processPacket() for every received packet*/ 
	 if ( pcap_loop(descr, atoi(measure_rules), processPacket, (u_char *)&count) == -1){
		fprintf(stderr, "ERROR3: %s\n", pcap_geterr(descr) );
		exit(1);
	 }
	dump_stats();
	return 0; 

} 

/* EOF*/
