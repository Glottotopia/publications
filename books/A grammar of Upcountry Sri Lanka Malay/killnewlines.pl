#!/usr/bin/perl -w

# open (INFILE, "$ARGV[0]")||die("failed to open $ARGV[0]");
# $current = 

open (INFILE, "$ARGV[0]")||die("failed to open $ARGV[0]");
$current=1;
while($current=<INFILE>){
	chop $current;
	$current=~s/\s+/ /g;
	$current=~s/(number: [\d\.]*)/$1\n/g;
	$current=~s/(name: .*)/$1\n/g;
	$current=~s/(content: .*)/$1\n/g;
	print $current, " ";
}
close (INFILE);