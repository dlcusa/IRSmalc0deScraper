#!/usr/bin/python2.7
def malc0deCsv():
    """Build current http://malc0de.com/database/ CSV file.
    
    This is the IRS UNIX support position pre-interview
    programming assignment for candidate David L. Craig.

    This is his first ever Python project, although he
    looked at Python 3 on April 4, 2012 to help his
    oldest son debug a problem, and scanned the Linux Mint
    live installer for debugging an install much further
    back in time.  There is surely a more elegant solution
    than this.

    The development included about 12 hours absorbing the
    Python 2.7.3 tutorial, another 11 obtaining and
    learning bs4, and another 2 for using csv; all while
    trying to squeeze in previously planned happy holidays
    with the family.

    Project requirements:
    
    Hints
    ===
    
    import csv, datetime, requests, time
    
    from bs4 import BeautifulSoup
    
    
    Requirements
    ====
    
    * Utilize Python 2.7.3
    
    * Source URL => http://malc0de.com/database/
    
    * Scrape the following values from the page
    
    Date, File Name{If there is a file name in the URL},IP Address, ASN, ASN
    Name,MD5 hash
    
    * Note IP Addresses need to be written in the following format to the CSV
    file ->
    
    10{.}10{.}10{.}10
    
    * Write the product to a CSV file with file format
    
    Discovery Date,File Name,IP Address,ASN,ASN Name,MD5
    
    * CSV file format needs to be as follows
    
    "Malecode-Culled-Product-" + the_current_date_time + '.csv'
    
    * Post your code and output product to www.github.com and email back URL
    links to the code and the CSV output product to this email.
    """
    #-----------------------------------------------------------------------
    import csv, datetime, urllib2, sys, re
    from bs4 import BeautifulSoup
    from datetime import datetime, date, time
    the_current_date_time = datetime.utcnow().strftime("%Y_%m_%d-%H_%M_%S_UT")
    of = "Malecode-Culled-Product-" + the_current_date_time + '.csv'
    print "Creating file", of

    # The current column headers (Domain is assumed to be File Name)
    hl    = ['<th>Date</th>'                           ,
             '<th>Domain</th>'                         ,
             '<th>IP</th>'                             ,
             '<th>CC</th>'                             ,
             '<th>ASN</th>'                            ,
             '<th>Autonomous System Name</th>'         ,
             '<th>Click Md5 for VirusTotal Report</th>']
    ch = ('Discovery Date', # CSV headers tuple
          'File Name',
          'IP Address',
          'ASN',
          'ASN Name',
          'MD5')
    
    nr = 0 # accumulate number of data records processed
    with open(of,'' 'w') as f:
        try:
            csv = csv.writer(f)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            raise
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        csv.writerow(ch)
        for pg in range(1, 99999): # for each page (break on empty table)
            murl = 'http://malc0de.com/database/?&page=' + str(pg)
            try:
                malhtml = BeautifulSoup(urllib2.urlopen(murl), "lxml")
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                raise
            except:
                print "Unexpected error:", sys.exc_info()[0]
                raise
            if pg == 1: # first page only, verify the column headers
                hc = malhtml.table.tr.contents
                if len(hc) != 7:
                    print 'Table does not contain seven columns--aborting'
                    sys.exit()
                for hx in range(6):
                    if str(hc[hx]) != hl[hx]:
                        print 'Column', hx + 1, 'has an unexpected heading',
                        print '(' + str(hc[hx]) + ')--aborting'
                        sys.exit()
            td = malhtml.table.find_all("td") # Extract all td entries in the page
            for dx in range(0, len(td), 7): # For every row of seven td entries:
                # print 'dx:', str(dx)
                rdt = BeautifulSoup(str(td[dx + 0]))
                vdt = rdt.td.string.encode('utf-8')
                # print 'vdt:', str(vdt)
                rfn = BeautifulSoup(str(td[dx + 1]))
                # strip '<td> ' and '</td>' (some rfn.td values don't string (?) )
                # vfn = rfn.td.prettify()[5:-6]
                try:
                    vfn = rfn.td.string.encode('utf-8')
                except:
                    vfn = rfn.td.string
                # print 'vfn:', str(vfn)
                rip = BeautifulSoup(str(td[dx + 2]))
                vip = re.sub('[.]', '{.}', rip.td.a.string, count=3)
                # print 'vip:', str(vip)
                rcc = BeautifulSoup(str(td[dx + 3]))
                vcc = rcc.td.a.string.encode('utf-8')
                # print 'vcc:', str(vcc)
                rnu = BeautifulSoup(str(td[dx + 4]))
                vnu = rnu.td.a.string.encode('utf-8')
                # print 'vnu:', str(vnu)
                rna = BeautifulSoup(str(td[dx + 5]))
                try:
                    vna = rna.td.string.encode('utf-8')
                except:
                    vna = rna.td.string
                # print 'vna:', str(vna)
                rmd = BeautifulSoup(str(td[dx + 6]))
                vmd = rmd.td.a.string.encode('utf-8')
                # print 'vmd:', str(vmd)
                # print '-' * 50
                csv.writerow((vdt, vfn, vip, vcc, vnu, vna, vmd))
            print 'Data rows for page', str(pg) + ':', len(td) / 7
            nr = nr + len(td) / 7
            if len(td) == 0:
                break
    f.closed
    print 'Total data rows:', str(nr)
if __name__ == "__main__":
    import sys
    # print(int(sys.argv[1]))
    malc0deCsv()
