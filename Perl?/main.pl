use Time::HiRes qw(clock_gettime CLOCK_REALTIME);

my $lastGenerated = 1;
my $m = 2 ** 31 - 1;
my $a = 7 ** 5;

# this is SO much easier than rust
sub nextNumber {
    $lastGenerated = $lastGenerated * $a % $m;
    return $lastGenerated;
}

sub swap {
    my (@array, $i, $j) = @_;
    my $temp = @array[$i];
    @array[$i] = @array[$j];
    @array[$j] = $temp;
}

sub fisherYates {
    my @array = @_[0];
    for (my $i = scalar(@array) - 1; $i > 0; $i--) {
        my $j = nextNumber() % ($i + 1);
        swap(@array, $i, $j);
    }
}

for (my $i = 0; $i < 5; $i++) {
    @a = (1, 2, 3, 4, 5)
    print("@a");
}
