/* Convert transliterated Tamil text to codes known to the Tamilmax.tex */
/* set of macros using the wntml fonts */

#include <stdio.h>
#include <ctype.h>


/* globally accessible variables */

int	tamilflag,t_errors,true,false,errorcount,transflag;
char	switcher,tdelim;
char	tspace[2];
void	changestate();
FILE	*input,*output;
char filename[128];



/* functions */

/*  void bracket_err()
{
   printf("\nCharacter '}' read while scanning Tamil; need to edit file.\n");
   printf("Examine end of the output file to find location of problem.");
   fclose(input);
   fclose(output);
   abort();
} */

void haccbox()
{
    puts("Tamilize: Tamil to TeX converter v:0.97 of 4/24/90");
    puts("Humanities And Arts Computing Center, DR-10");
    puts("University of Washington");
    puts("Seattle, Washington, 98195  USA");
    puts("phone (206)-543-4218");
    puts("ridgeway@blake.u.washington.edu");
    puts("Copyright 1990 Humanities and Arts Computing Center");
    puts("You are welcome to use this work-in-progress, but please do not");
    puts("redistribute: rather, refer other interested parties to us.");
    puts("Since this is a work in progress, we do not want uncontrolled");
    puts("proliferation of pre-release versions.");
    return;
}

FILE *getopen(char *access)
{
	int	temp;
	FILE	*handle;
	gets(filename);
	handle=fopen(filename,access);
	if (handle ==  (FILE *) NULL) {
            printf("Can't open file %s",filename);
            errorcount++;
            if (errorcount > 9) {
                 printf("\n\n\n\n\nToo many errors!\n");
                 abort();
                 }
	  }
	return handle;
}
FILE *get_file(char *access,char *prompt)
{
	puts(prompt);
	return getopen(access);
}

int isvowel(char thischar)
{
  switch (thischar) {
     case 'a' :
     case 'e' :
     case 'i' :
     case 'o' :
     case 'u' : return true;
     default  : return false;
     }
}

void stringout(char *string)
{
  fputs(string,output);
}

void charout(char thischar)
{
  putc(thischar,output);
}

void romanout(char thischar)
{
  stringout("{\\roman ");
  charout(thischar);
  charout('}');
}

void transcribe_err(char thischar)
{
  printf("Character %c encountered in Tamil environment.\n",thischar);
  romanout(thischar);
}

void pushback(char thischar)
{
  ungetc(thischar,input);
}

void processtamil()
{
  char ch;
  int  newsyl;
  newsyl=true;
  for (tamilflag=true; tamilflag==true; ) {
    ch = getc(input);
    if (ch == EOF) abort();
    if (ch == switcher) changestate();
    else if (isspace(ch)) {
            stringout(tspace);
            charout(ch);            
            for ( ch=getc(input); isspace(ch); ch=getc(input)) charout(ch);
            pushback(ch);
            newsyl=true;
	    }
    else if (ispunct(ch) ) {
             if (ch == 125) printf("\nCharacter } encountered while scanning tamil -- probable error.\n");
             romanout(ch);
             newsyl=true;
             }
    else {
            switch (ch) {
                case 'a':
                case 'e':
                case 'i':
                case 'o':
                case 'u': if (newsyl==true) {
			      charout(tdelim);
			      newsyl=false;
			      }
                          charout(ch);
                          break;
                case 'c':
                case 't':
                case 'p':
                case 'm':
                case 'y':
                case 'r':
                case 'l':
                case 'v':
                case 's':
                case 'j':
                case 'x':
                case 'h': charout(tdelim);
                          charout(ch);
                          newsyl=false;
                          break;
                case 'k': charout(tdelim);
                          ch=getc(input);
                          if (ch=='4') charout('X');
                          else {
                              charout('k');
                              pushback(ch);
                              }
                          newsyl=false;
                          break;
                case '2': charout(tdelim);
                          charout('N');
                          newsyl=false;
                          break;
                case '3': charout(tdelim);
                          stringout("NN");
                          newsyl=false;
                          break;
                case '4': charout(tdelim);
                          charout('S');
                          newsyl=false;
                          break;
                case '5': charout(tdelim);
                          stringout("NY");
                          newsyl=false;
                          break;
                case '6': charout(tdelim);
                          charout('R');
                          newsyl=false;
                          break;
                case '7': charout(tdelim);
                          charout('Z');
                          newsyl=false;
                          break;
                case '8': charout(tdelim);
                          charout('T');
                          newsyl=false;
                          break;
                case '9': charout(tdelim);
                          charout('L');
                          newsyl=false;
                          break;
                case 'n': charout(tdelim);
                          ch=getc(input);
                          if (ch=='g') stringout("ng");
                          else {
                              charout('n');
                              pushback(ch);
                              }
                          newsyl=false;
                          break;
                default : transcribe_err(ch);
                          newsyl=true;
                } /* endcase */
    }  /* endif */
  }  /* endfor*/
}

void starttamil()
{
  stringout("{\\btam ");  /*   stringout("{\\starttamil\%\n"); */
  processtamil();
}

void endtamil()
{
  stringout("}\\etam{}");  /* stringout("}\\endtamil\%\n");  */
  tamilflag=false;
}

void changestate()
{
  if (tamilflag==true) endtamil();
  else starttamil();
}

main(int argc, char *argv[])
{
  int ch,err,notdone,vowflag,initflag;
  errorcount=0;
  switcher='~';
  true=1;
  false=0;
  tamilflag=false;
  tdelim=1;  /* i.e. control-a ::: if yah don't like it, change it */
  tspace[0]=tdelim;
  tspace[1]=' ';
  haccbox();
  vowflag=0;
  if (argc > 1) input = fopen(argv[1],"rb");
  if (input == (FILE *) NULL) {
	/* prompt for and open input file */
	for ( ; input == (FILE *) NULL ; input=get_file("rb","Enter name of input file: ")) ;
        }
        /* we are making these binary, as we have no guarantee what kind */
        /* of character may be in the transcription: we don't care about */
        /* ends of lines, as we are reading character by character */
   if (argc > 2) output = fopen(argv[2],"wb");
   if (output == (FILE *) NULL) {
	for ( ; output == (FILE *) NULL ; output=get_file("wb","Enter name of output file: ")) ;
	/* prompt for and open output file */
        }
   while ((ch = getc(input)) != EOF) {
	if (ch == switcher) changestate();
	else {
		if (ch == '|') {
                  vowflag=1;
		  notdone=1;
		  initflag=2;
		  while (notdone) {
		  ch=getc(input);
                  if (isalnum(ch)) {
                    initflag--;
                    if (vowflag==0) {
		       if (! isvowel(ch)) stringout("\\-");
                       }
		    if (isvowel(ch)) vowflag=1;
                    else vowflag=0;
                    }
                  else {
                     vowflag=1;
                     initflag=2;
                     }
		  if (ch==EOF) notdone=0;
		  else {
		    switch(ch) {
		      case '2': stringout("\\ndot{}");
		      	break;
		      case '3': stringout("\\nndot{}");
		      	break;
		      case '4': stringout("\\skts{}");
			break;
		      case '5': stringout("\\paln{}");
		      	break;
		      case '6': stringout("\\rdot{}");
		      	break;
		      case '7': stringout("\\rdotdot{}");
			break;
		      case 'T': stringout("\\tdot{}");
			 break;
		      case 'D': stringout("\\dotd{}");
			 break;
		      case '8':
		                 if ( initflag > 0 ) stringout("\\tdot{}");
		                 else {
		                      err=getc(input);
		                      if (err == '8') stringout("\\tdot{}\\tdot{}");
				      else {
					  stringout("\\dotd{}");
					  pushback(err);
					  }
		                      }
		      	break;
		      case '9': stringout("\\dotl{}");
		      	break;
		      case '|': notdone=0;
		        break;
		      default: putc(ch,output);
			} /* endcase */
		  } /* end else */
		} /* endwhile */
		} /* endif */
		else putc(ch,output);
	}  /* endelse */
	} /* endwhile */
   fclose(input);
   fclose(output);
   puts("Tamilize is done.");
}
