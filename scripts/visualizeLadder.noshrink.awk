#!/usr/bin/awk -f

BEGIN {
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
    
    n=40;
    
    nx = n;
    ny = ymax/xmax*n;
    
    r = "";
    for ( i=0; i<nx; ++i )
    {
	r = r "." ;
    }

    for ( i=0; i<ny; ++i )
    {
	t[i] = r ;
    }

    for ( j=0; j<p; ++j )
    {
	rx = int(x[j]/xmax*n-0.1);
	ry = int(y[j]/xmax*n-0.1);
	
	s=t[ry];
	left = substr(s,1,rx);
	right = substr(s,rx+2);
	
	t[ry]= left "X" right;
    }

    for ( i=0; i<ny; ++i )
    {
	print t[i] ;
    }
}
