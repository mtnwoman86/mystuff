#!/usr/bin/env python
import csv
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

class Discharge( pd.DataFrame ):
    """
    Discharge class will read WAPDA runoff ASCII files, and return a pandas DataFrame.

    2014-09-24 M. J. Brodzik brodzik@nsidc.org 303-492-8263
    National Snow & Ice Data Center, Boulder CO
    Copyright (C) 2014 Regents of the University of Colorado at Boulder
    
    """
    data = pd.DataFrame()
    
    def read( self, filename, verbose=False ):
        """
        usage: discharge.read( filename, verbose=False )
        
        Reads daily discharge by date from WAPDA filename into a pandas DataFrame.
        
        Assumes file format:
        year month day doy discharge(m^3/s) measured

        Assumes stored discharge units are m^3/s, converts these to km^3/day.

        """

        # Now use the elevation information to set up column headers
        col_names = [ 'yyyy', 'mm', 'dd', 'doy', 'Discharge', 'Measured' ]

        # Now read the data part of the file into a DataFrame
        # Use header=None in order to not use anything in the file for the header, and
        # to pass in col_names list for column headers instead.
        self.data = pd.read_table( filename, sep="\s+", header=None,
                              names=col_names, index_col='doy' )

        # Use the yyyy, mm, dd columns to make a time series index for this DataFrame:
        date_list = []
        for ( yyyy, mm, dd ) in zip( self.data['yyyy'].values,
                                     self.data['mm'].values,
                                     self.data['dd'].values ):
            date_list.append( dt.date( yyyy, mm, dd ) )
        dates = pd.to_datetime( date_list )
        self.data['Date'] = dates
        self.data.set_index( [ 'Date' ], inplace=True )
        self.data.drop( [ 'yyyy', 'mm', 'dd' ], axis=1, inplace=True )

        # Convert stored values of m^3/s to km^3/day
        sec_per_day = 60.0 * 60.0 * 24.0
        m3_per_km3 = 1000.0 * 1000.0 * 1000.0
        self.data['Discharge'] = self.data['Discharge'] * sec_per_day / m3_per_km3

        if verbose:
            print ( __name__ + ": read discharge data from " + filename )
            print ( __name__ + ": " + str( len( self.data.index ) ) + " dates." )
            print ( __name__ + ": " + str( len( self.data.columns ) ) + " columns." )
        
