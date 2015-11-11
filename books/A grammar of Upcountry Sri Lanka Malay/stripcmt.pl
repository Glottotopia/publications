#!/usr/bin/perl

open (IN,"$ARGV[0]") or die "Can't open IN  : $ARGS[1] $!";
open (OUTTEXT,"> $ARGV[0]+text") or die "Can't open OUTTEXT : $!";
open (OUTCOMMENT,"> $ARGV[0]+cmt") or die "Can't open nOUTCOMMENT  : $!";

$current=0;
while ($current=<IN>){
	if($current=~/section{/){ print OUTCOMMENT $current};
        ($current=~/^%/)?print OUTCOMMENT $current: print OUTTEXT $current;
}

close(IN,OUTTEXT,OUTCOMMENT);