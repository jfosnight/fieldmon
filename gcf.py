# -*- coding: utf-8 -*-
#! /bin/python

import math

def gcf(pt1, pt2):
    return gcf_degrees(pt1[0], pt1[1], pt2[0], pt2[1])

def gcf_degrees(lat1, lon1, lat2, lon2):
    # http://williams.best.vwh.net/avform.htm#GCF
    # sqrt(  (sin((lat1-lat2)/2))^2 + cos(lat1)*cos(lat2)*(sin((lon1-lon2)/2 ))^2  )
    #d=2*asin(  )

    R = 6371000 # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lam1 = math.radians(lon1)
    lam2 = math.radians(lon2)

    a = math.sin( (phi1 - phi2)/2 )**2    +    math.cos(phi1)*math.cos(phi2)*(math.sin( (lam1 - lam2) / 2 )**2)
    d = R * 2*math.asin( math.sqrt(a) )
    return d
