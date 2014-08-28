#!/usr/bin/awk -f

BEGIN {
    n = 50 ;
    r = "";
    for ( i=0; i<n; ++i )
    {
	r = r "." ;
    }

    for ( i=0; i<n; ++i )
    {
	t[i] = r ;
    }
    
    p=0;
}

{
    xmax=$1;
    ymax=$2;
    x[p]=$1;
    y[p]=$2;
    p++;
}

END {
    print xmax, ymax;

    for ( j=0; j<p; ++j )
    {
	rx = int(x[j]/xmax*n);
	ry = int(y[j]/ymax*n);
	
	s=t[ry];
	left = substr(s,1,rx);
	right = substr(s,rx+2);
	
	t[ry]= left "X" right;
    }

    for ( i=0; i<n; ++i )
    {
	print t[i] ;
    }

}
