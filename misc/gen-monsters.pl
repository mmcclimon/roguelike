#!perl
use v5.24;
use warnings;
use Data::Dumper::Concise;

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
my $pgroup   = qr{\([^)]+\)};
my $sep      = qr{,?\s*};

my %monsters;
for my $line (@monsters) {
  # clean up whitespace and comments
  $line =~ s/$cstart.*?$cend//gs;
  $line =~ s/\s+/ /gs;
  $line =~ s/$sep$//g;

  # expand this macro
  $line =~ s/NO_ATTK/ATTK(0, 0, 0, 0)/g;

  my @parts = $line =~ m{
    ^MON\( \s*                                # start
      "(?<desc>[^"]+)"                  $sep  # C: desc
      (?<symb>$one_flag)                $sep  # C: symbol
      (?<levl>LVL$pgroup)               $sep  # C: level
      (?<genf>$flag_set)                $sep  # C: gen flags
        A\(                                   #    literal A-paren
      (?<attk>                                # C: attack capture start
          (?:ATTK$pgroup$sep){6}              #    6 ATTK macros
      )                              #   $sep  # attack capture end
        \)      $sep                          #    close of A-paren
      (?<size>SIZ$pgroup)               $sep  # C: size
      (?<res1>$flag_set)                $sep  # C: resistance 1
      (?<res2>$flag_set)                $sep  # C: resistance 2
      (?<flg1>$flag_set)                $sep  # C: flags 1
      (?<flg2>$flag_set)                $sep  # C: flags 2
      (?<flg3>$flag_set)                $sep  # C: flags 3
      (?<diff>[0-9]+)                   $sep  # C: difficulty
      (?<colr>$one_flag)                      # C: color
    \)$                                       # phew
  }x;

  die "bad parse: <$line>" unless @parts == 13;

  my %attrs = %+;
  my $key = lc $attrs{desc} =~ s/[-\s]+/_/gr;

  $monsters{$key} = \%attrs;
}

# Munge 'em and print 'em
my @delete_keys = qw( genf flg1 flg2 flg3 res1 res2 size );

for my $k (sort keys %monsters) {
  my $m = $monsters{$k};
  $m->{difficulty} = delete $m->{diff};

  my $color = delete $m->{colr};
  $m->{color} = lc $color =~ s/^CLR_//r;

  $m->{glyph} = NH::symbol( delete $m->{symb} );

  my ($dcount, $dtype) = NH::attack( delete $m->{attk} );
  $m->{atk_dcount} = $dcount;
  $m->{atk_dtype}  = $dtype;

  my ($level, $move, $ac) = NH::stats( delete $m->{levl} );
  $m->{level} = $level;
  $m->{move}  = $move;
  $m->{ac}    = $ac;

  # This isn't really necessary, but might as well so Dumper output is clean.
  delete $m->@{@delete_keys};

  print <<END_MONSTER;
[$k]
description = '$m->{desc}'
glyph       = '$m->{glyph}'
level       = $m->{level}
difficulty  = $m->{difficulty}
move        = $m->{move}
ac          = $m->{ac}
atk_dcount  = $m->{atk_dcount}
atk_dtype   = $m->{atk_dtype}
color       = '$m->{color}'

END_MONSTER
}

package NH;

my %syms;
sub symbol { $syms{ $_[0] } }

# for now, we're just gonna grab the first attack.
sub attack {
  my ($str) = @_;
  my ($attack) = grep {; length } split /(ATTK$pgroup)$sep/, $str;
  my ($dcount, $dtype) = $attack =~ /ATTK\(.*?(\d+),\s*(\d+)\)/;
  return ($dcount, $dtype);
}

sub stats {
  my ($str) = @_;
  my ($level, $move, $ac, @rest) = $str =~ /(\d+)/g;
  return ($level, $move, $ac);
}

BEGIN {
%syms = (
  S_ANT         => 'a',
  S_BLOB        => 'b',
  S_COCKATRICE  => 'c',
  S_DOG         => 'd',
  S_EYE         => 'e',
  S_FELINE      => 'f',
  S_GREMLIN     => 'g',
  S_HUMANOID    => 'h',
  S_IMP         => 'i',
  S_JELLY       => 'j',
  S_KOBOLD      => 'k',
  S_LEPRECHAUN  => 'l',
  S_MIMIC       => 'm',
  S_NYMPH       => 'n',
  S_ORC         => 'o',
  S_PIERCER     => 'p',
  S_QUADRUPED   => 'q',
  S_RODENT      => 'r',
  S_SPIDER      => 's',
  S_TRAPPER     => 't',
  S_UNICORN     => 'u',
  S_VORTEX      => 'v',
  S_WORM        => 'w',
  S_XAN         => 'x',
  S_LIGHT       => 'y',
  S_ZRUTY       => 'z',
  S_ANGEL       => 'A',
  S_BAT         => 'B',
  S_CENTAUR     => 'C',
  S_DRAGON      => 'D',
  S_ELEMENTAL   => 'E',
  S_FUNGUS      => 'F',
  S_GNOME       => 'G',
  S_GIANT       => 'H',
  S_JABBERWOCK  => 'J',
  S_KOP         => 'K',
  S_LICH        => 'L',
  S_MUMMY       => 'M',
  S_NAGA        => 'N',
  S_OGRE        => 'O',
  S_PUDDING     => 'P',
  S_QUANTMECH   => 'Q',
  S_RUSTMONST   => 'R',
  S_SNAKE       => 'S',
  S_TROLL       => 'T',
  S_UMBER       => 'U',
  S_VAMPIRE     => 'V',
  S_WRAITH      => 'W',
  S_XORN        => 'X',
  S_YETI        => 'Y',
  S_ZOMBIE      => 'Z',
  S_HUMAN       => '@',
  S_GHOST       => ' ',
  S_GOLEM       => "'",
  S_DEMON       => '&',
  S_EEL         => ';',
  S_LIZARD      => ':',
  S_INVISIBLE   => 'I',
  S_WORM_TAIL   => '~',
  S_MIMIC_DEF   => ']',
);
}
