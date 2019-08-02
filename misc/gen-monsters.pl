#!perl
use v5.24;
use warnings;

open my $fh, '<', 'misc/monsters.c' or die "couldn't open file: $!";

my $slurped;
{
  local $/ = undef;
  $slurped = <$fh>;
}

# it's time for...shitty parsing!
my @bits = split /(MON\()/, $slurped;
shift @bits;  # first is empty string.

# join in pairs
my @monsters;
while (@bits) {
  my @this_mon = (splice @bits, 0, 2);
  s/(^\s*|\s*$)//gsn for @this_mon;
  push @monsters, (join '', @this_mon);
}

# My life has led me to this point, implementing a shitty C preprocessor in
# perl.  Each hunk in @monsters has a single monster, a bunch of garbage
# whitespace, and possibly trailing comments.  LUCKILY, we can be reasonably
# sure that because this used to like, actually compile, we have a reasonably
# parseable format.
my $cstart   = qr{\Q/*\E};
my $cend     = qr{\Q*/\E};
my $one_flag = qr{[A-Z_]+};
my $flag_set = qr{[^,]+};
my $sep      = qr{,\s*};

my $sed_yes = 'A(ATTK(AT_BITE, AD_SSEX, 0, 0), ATTK(AT_CLAW, AD_PHYS, 1, 3),'
            . ' ATTK(AT_CLAW, AD_PHYS, 1, 3), NO_ATTK, NO_ATTK, NO_ATTK)';
my $sed_no  = 'A(ATTK(AT_CLAW, AD_PHYS, 1, 3), ATTK(AT_CLAW, AD_PHYS, 1, 3),'
            . ' ATTK(AT_BITE, AD_DRLI, 2, 6), NO_ATTK, NO_ATTK, NO_ATTK)';

for my $line (@monsters) {
  # clean up whitespace and comments
  $line =~ s/$cstart.*?$cend//gs;
  $line =~ s/\s+/ /gs;
  $line =~ s/,?\s*$//g;

  # omg, expand some macros
  $line =~ s/SEDUCTION_ATTACKS_YES/$sed_yes/;
  $line =~ s/SEDUCTION_ATTACKS_NO/$sed_no/;
  $line =~ s/NO_ATTK/ATTK(0, 0, 0, 0)/g;

  my @parts = $line =~ m{
    ^MON\( \s*                   # start
      "(?<desc>.*?)"       $sep  # C: desc
      (?<symb>$one_flag)   $sep  # C: sym
      (?<levl>LVL\(.*?\))  $sep  # C: level
      (?<genf>$flag_set)   $sep  # C: gen flags
      (?<attk>                   # C: attack capture start
        A\(                         # literal A(   #)
          (?:                       # non-capture group
            ATTK\(.*?\)             # ATTK macro
              ,?\s*                 # maybe-sep
          ){6}                      # six of these
        \)                          # close of A(  #)
      )                    $sep  # attack capture end
      (?<size>SIZ\(.*?\))  $sep  # C: size
      (?<res1>$flag_set)   $sep  # C: resistance 1
      (?<res2>$flag_set)   $sep  # C: resistance 2
      (?<flg1>$flag_set)   $sep  # C: flags 1
      (?<flg2>$flag_set)   $sep  # C: flags 2
      (?<flg3>$flag_set)   $sep  # C: flags 3
      (?<diff>[0-9]+)      $sep  # C: difficulty
      (?<colr>$one_flag)         # C: color
    \)$                          # phew
  }x;

  die "bad parse: <$line>" unless @parts == 13;

  use Data::Dumper::Concise;
  print Dumper \%+;


}
